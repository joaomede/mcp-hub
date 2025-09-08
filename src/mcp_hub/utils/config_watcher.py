import asyncio
import json
import logging
import time
from pathlib import Path
from typing import Callable, Optional, Dict, Any, Awaitable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileMovedEvent, FileCreatedEvent
import threading


logger = logging.getLogger(__name__)


class ConfigChangeHandler(FileSystemEventHandler):
    """Handler for config file changes."""

    def __init__(self, config_path: Path, reload_callback: Callable[[Dict[str, Any]], Awaitable[None]], loop: asyncio.AbstractEventLoop):
        self.config_path = config_path.resolve()  # Resolve to absolute path
        self.reload_callback = reload_callback
        self.loop = loop  # Store reference to the main event loop
        self._last_modification = 0
        self._debounce_delay = 0.5  # 500ms debounce

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        # Check if the modified file is our config file
        event_path = Path(event.src_path).resolve()
        logger.debug(f"File modified: {event_path}, watching: {self.config_path}")

        # Also check for file name match in case of temporary files or atomic writes
        if (event_path == self.config_path or
            event_path.name == self.config_path.name and event_path.parent == self.config_path.parent):

            logger.info(f"Config file modified: {self.config_path}")
            self._trigger_reload()
        else:
            logger.debug(f"File {event_path} modified but not our config file {self.config_path}")

    def on_moved(self, event):
        """Handle file move events (atomic writes)."""
        if event.is_directory:
            return

        # Check if the destination is our config file (atomic write pattern)
        dest_path = Path(event.dest_path).resolve()
        logger.debug(f"File moved: {event.src_path} -> {dest_path}, watching: {self.config_path}")

        if (dest_path == self.config_path or
            dest_path.name == self.config_path.name and dest_path.parent == self.config_path.parent):

            logger.info(f"Config file replaced via move: {self.config_path}")
            self._trigger_reload()

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        # Check if the created file is our config file
        event_path = Path(event.src_path).resolve()
        logger.debug(f"File created: {event_path}, watching: {self.config_path}")

        if (event_path == self.config_path or
            event_path.name == self.config_path.name and event_path.parent == self.config_path.parent):

            logger.info(f"Config file created: {self.config_path}")
            self._trigger_reload()

    def _trigger_reload(self):
        """Common method to trigger a reload."""
        current_time = time.time()

        # Debounce rapid file changes
        if current_time - self._last_modification < self._debounce_delay:
            logger.debug(f"Debouncing file change (too soon): {current_time - self._last_modification:.2f}s")
            return

        self._last_modification = current_time
        logger.info(f"Config file change detected: {self.config_path}")

        # Schedule the reload callback using the stored loop reference
        try:
            # Use call_soon_threadsafe to schedule the coroutine from a different thread
            future = asyncio.run_coroutine_threadsafe(self._handle_config_change(), self.loop)
            logger.debug(f"Scheduled config reload task from thread: {future}")
        except Exception as e:
            logger.error(f"Failed to schedule config reload: {e}")

    async def _handle_config_change(self):
        """Handle config change with proper error handling."""
        try:
            await asyncio.sleep(self._debounce_delay)  # Additional debounce

            logger.debug(f"Processing config file change: {self.config_path}")

            # Read and validate the new config
            with open(self.config_path, 'r') as f:
                new_config = json.load(f)

            # Call the reload callback
            await self.reload_callback(new_config)

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_path}")
        except Exception as e:
            logger.error(f"Error reloading config: {e}")


class ConfigWatcher:
    """Watches a config file for changes and triggers reloads."""

    def __init__(self, config_path: str, reload_callback: Callable[[Dict[str, Any]], Awaitable[None]]):
        self.config_path = Path(config_path).resolve()
        self.reload_callback = reload_callback
        self.observer: Optional[Observer] = None
        self.handler: Optional[ConfigChangeHandler] = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        # If we create our own loop we store the thread here so we can stop it
        self._loop_thread: Optional[threading.Thread] = None
        self._created_own_loop = False

    def start(self):
        """Start watching the config file."""
        if not self.config_path.exists():
            logger.error(f"Config file does not exist: {self.config_path}")
            return

        # Get the current event loop
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            # No running loop in this thread; create a background loop in a dedicated thread
            logger.info("No running event loop found, creating a background event loop for ConfigWatcher")
            self.loop = asyncio.new_event_loop()
            def _run_loop(loop: asyncio.AbstractEventLoop):
                asyncio.set_event_loop(loop)
                loop.run_forever()

            self._loop_thread = threading.Thread(target=_run_loop, args=(self.loop,), daemon=True)
            self._loop_thread.start()
            self._created_own_loop = True

        self.handler = ConfigChangeHandler(self.config_path, self.reload_callback, self.loop)
        self.observer = Observer()

        # Watch the directory containing the config file
        watch_dir = self.config_path.parent
        logger.debug(f"Watching directory: {watch_dir} for file: {self.config_path}")
        self.observer.schedule(self.handler, str(watch_dir), recursive=False)

        self.observer.start()
        logger.info(f"Started watching config file: {self.config_path}")
        logger.debug(f"File watcher is alive: {self.observer.is_alive()}")

    def stop(self):
        """Stop watching the config file."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info(f"Stopped watching config file: {self.config_path}")

        # If we created our own loop, stop it cleanly
        if getattr(self, '_created_own_loop', False) and self.loop:
            try:
                self.loop.call_soon_threadsafe(self.loop.stop)
            except Exception:
                pass
            if self._loop_thread:
                self._loop_thread.join(timeout=2)
            self._created_own_loop = False
            self.loop = None
            self._loop_thread = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()