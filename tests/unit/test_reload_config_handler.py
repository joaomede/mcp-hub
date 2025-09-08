import pytest
from fastapi import FastAPI
from mcp_hub.main import reload_config_handler, create_sub_app, unmount_servers

@pytest.mark.asyncio
async def test_reload_config_handler_add_server():
    main_app = FastAPI()
    old_config = {"mcpServers": {}}
    new_config = {
        "mcpServers": {
            "server1": {
                "command": "echo",
                "args": ["hello"]
            }
        }
    }
    main_app.state.config_data = old_config
    main_app.state.path_prefix = "/"

    await reload_config_handler(main_app, new_config)

    assert any(route.path == "/server1/mcp" for route in main_app.router.routes)

@pytest.mark.asyncio
async def test_reload_config_handler_remove_server():
    main_app = FastAPI()
    old_config = {
        "mcpServers": {
            "server1": {
                "command": "echo",
                "args": ["hello"]
            }
        }
    }
    new_config = {"mcpServers": {}}
    main_app.state.config_data = old_config
    main_app.state.path_prefix = "/"

    # Add a route to simulate an existing server
    sub_app = create_sub_app("server1", old_config["mcpServers"]["server1"], None, None, False, None, 10, None)
    main_app.mount("/server1/mcp", sub_app)

    await reload_config_handler(main_app, new_config)

    assert not any(route.path == "/server1/mcp" for route in main_app.router.routes)

@pytest.mark.asyncio
async def test_reload_config_handler_update_server():
    main_app = FastAPI()
    old_config = {
        "mcpServers": {
            "server1": {
                "command": "echo",
                "args": ["hello"]
            }
        }
    }
    new_config = {
        "mcpServers": {
            "server1": {
                "command": "echo",
                "args": ["world"]
            }
        }
    }
    main_app.state.config_data = old_config
    main_app.state.path_prefix = "/"

    # Add a route to simulate an existing server
    sub_app = create_sub_app("server1", old_config["mcpServers"]["server1"], None, None, False, None, 10, None)
    main_app.mount("/server1/mcp", sub_app)

    await reload_config_handler(main_app, new_config)

    # Check if the server was updated
    updated_route = next((route for route in main_app.router.routes if route.path == "/server1/mcp"), None)
    assert updated_route is not None
    assert updated_route.app.state.args == ["world"]
