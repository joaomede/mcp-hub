# ⚡️ MCP Hub

**Pure stdio MCP Gateway for aggregating multiple Model Context Protocol servers.**

MCP Hub is a simplified, pure stdio aggregator that runs multiple MCP servers through a single HTTP gateway. Unlike complex solutions, MCP Hub executes and manages all your MCP servers internally through stdio only, exposing them through clean HTTP endpoints.

Pure stdio MCP-to-MCP aggregation. No external servers. No complexity.

> **Note**: This project is adapted from [mcpo](https://github.com/open-webui/mcpo) with a focus on **pure stdio MCP aggregation** rather than mixed transport support, providing a clean gateway solution for stdio MCP server management only.

## 🤔 Why Use MCP Hub?

Managing multiple MCP servers individually is complex:

- 🔓 Each server requires separate management and ports
- ❌ Multiple command-line processes to handle
- 🧩 No unified discovery or routing
- 📊 Scattered monitoring and logging

MCP Hub solves all of that:

- ✅ **Single Entry Point**: One gateway for all your stdio MCP servers
- 🛡 **Unified Management**: Centralized server lifecycle and configuration  
- 🔄 **Hot Reload**: Add/remove servers without restart
- 📍 **Clean Routing**: Path-based routing (`/{server-name}/mcp`)
- 🏗️ **Pure stdio**: Executes MCP servers directly, no external dependencies

What feels like "one more layer" is actually **simplification at scale**.

MCP Hub makes your MCP infrastructure manageable and scalable—right now, with zero complexity.

## 🚀 Quick Usage

We recommend using uv for lightning-fast startup and zero config.

```bash
uvx mcp-hub --port 8000 --api-key "top-secret" -- your_mcp_server_command
```

Or, if you're using Python:

```bash
pip install mcp-hub
mcp-hub --port 8000 --api-key "top-secret" -- your_mcp_server_command
```

**Single MCP Server Examples:**

```bash
# Proxy a single MCP server (available at /mcp)
mcp-hub --port 8000 --api-key "secret" -- uvx mcp-server-time --local-timezone=America/New_York
```

**Multiple MCP Servers (Recommended):**

```bash
# Use config file for multiple servers
mcp-hub --config config.json --hot-reload --port 8000 --api-key "secret"
```

**Multiple stdio MCP Servers (via config file):**

```bash
# Use config file for multiple stdio MCP servers
mcp-hub --config config.json --port 8000 --api-key "secret"
```

You can also run MCP Hub via Docker with no installation:

```bash
docker run -p 8000:8000 ghcr.io/joaomede/mcp-hub:main --api-key "secret" -- your_mcp_server_command
```

**Docker Compose (Recommended for Development & Production):**

For a complete development and production setup, use Docker Compose:

```bash
# Quick start with management script
./docker.sh dev      # Development mode
./docker.sh prod     # Production mode
./docker.sh logs     # View logs
./docker.sh stop     # Stop services

# Or use docker-compose directly
docker-compose up --build                                                    # Development
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build # Production
```

See [DOCKER.md](DOCKER.md) for detailed Docker setup instructions.

**Example - Single Server:**

```bash
uvx mcp-hub --port 8000 --api-key "secret" -- uvx mcp-server-time --local-timezone=America/New_York
```

Your MCP server is now accessible at:
- **MCP Endpoint**: `http://localhost:8000/mcp` 
- **Connect via MCP client**: `mcp-client --url ws://localhost:8000/mcp`

### 🔄 Using a Config File (Recommended)

You can serve **multiple MCP servers** via a single config file that follows the [Claude Desktop](https://modelcontextprotocol.io/quickstart/user) format.

Enable hot-reload mode with `--hot-reload` to automatically watch your config file for changes and reload servers without downtime:

**Start via:**

```bash
mcp-hub --config /path/to/config.json
```

**Or with hot-reload enabled:**

```bash
mcp-hub --config /path/to/config.json --hot-reload
```

**Example config.json (stdio MCP servers only):**

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "time": {
      "command": "uvx",
      "args": ["mcp-server-time", "--local-timezone=America/New_York"]
    },
    "filesystem": {
      "command": "uvx",
      "args": ["mcp-server-filesystem", "--allowed-dir", "/tmp"]
    }
  }
}
```

Each stdio MCP server will be accessible under its own unique route:
- **Memory tools**: `http://localhost:8000/memory/mcp`
- **Time tools**: `http://localhost:8000/time/mcp`
- **Filesystem tools**: `http://localhost:8000/filesystem/mcp`

Connect your MCP client to any of these endpoints to access the tools from that specific server.

📖 **For detailed usage instructions, examples, and best practices, see [USAGE.md](USAGE.md)**

## 🔧 Requirements

- Python 3.11+
- uv (optional, but highly recommended for performance + packaging)

## 🛠️ Development & Testing

To contribute or run tests locally:

1.  **Set up the environment:**
    ```bash
    # Clone the repository
    git clone https://github.com/joaomede/mcp-hub.git
    cd mcp-hub

    # Install dependencies (including dev dependencies)
    uv sync --dev
    ```

2.  **Run unit tests:**
    ```bash
    uv run pytest
    ```

3.  **Run integration tests:**
    ```bash
    # Build Docker image first
    docker build -t mcp-hub:latest .
    
    # Run comprehensive integration test
    python test_mcp_integration.py
    ```
    
    The integration test validates:
    - ✅ Container startup and health checks
    - ✅ Multiple MCP server aggregation
    - ✅ Tool discovery and availability
    - ✅ HTTP endpoint routing (`/{server-name}/mcp/`)
    - ✅ MCP protocol compliance

4.  **Running Locally with Active Changes:**

    To run `mcp-hub` with your local modifications from a specific branch (e.g., `my-feature-branch`):

    ```bash
    # Ensure you are on your development branch
    git checkout my-feature-branch

    # Make your code changes in the src/mcp_hub directory or elsewhere

    # Run mcp-hub using uv, which will use your local, modified code
    # This command starts mcp-hub on port 8000 and proxies your_mcp_server_command
    uv run mcp-hub --port 8000 -- your_mcp_server_command

    # Example with a test MCP server (like mcp-server-time):
    # uv run mcp-hub --port 8000 -- uvx mcp-server-time --local-timezone=America/New_York
    ```
    This allows you to test your changes interactively before committing or creating a pull request. Access your locally running `mcp-hub` instance at `http://localhost:8000` and connect MCP clients to the `/mcp` endpoints.

## 🪪 License

MIT

## 🤝 Contributing

We welcome and strongly encourage contributions from the community!

Whether you're fixing a bug, adding features, improving documentation, or just sharing ideas—your input is incredibly valuable and helps make MCP Hub better for everyone.

Getting started is easy:

- Fork the repo
- Create a new branch
- Make your changes
- Open a pull request

Not sure where to start? Feel free to open an issue or ask a question—we're happy to help you find a good first task.

## 🙏 Acknowledgments

- **[mcpo](https://github.com/open-webui/mcpo)** by Timothy Jaeryang Baek - The original inspiration and foundation for this project
- **[Model Context Protocol](https://modelcontextprotocol.io/)** - The amazing protocol that makes this all possible
- **Open source community** - For the incredible tools and libraries that power this project

## 👨‍💻 Author

**João Medeiros** ([@joaomede](https://github.com/joaomede))
- 🌐 Website: [joaomede.github.io](https://joaomede.github.io)
- 📍 Location: São Paulo, Brazil
- 💼 Analysis and Systems Development | Data Science

---

✨ Let's build the future of interoperable AI tooling together!
