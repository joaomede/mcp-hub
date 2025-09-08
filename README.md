# ⚡️ MCP Hub

**A powerful MCP Gateway for aggregating multiple Model Context Protocol servers.**

MCP Hub is a simple yet robust gateway that aggregates multiple MCP servers into a single endpoint, providing unified access, authentication, and management for your MCP tools without any protocol conversion.

Pure MCP-to-MCP. No conversions. No hassle.

> **Note**: This project is inspired by and evolved from [mcpo](https://github.com/open-webui/mcpo) by Timothy Jaeryang Baek. MCP Hub focuses on pure MCP protocol forwarding without OpenAPI conversion, providing a clean gateway solution for MCP server aggregation.

## 🤔 Why Use MCP Hub?

Managing multiple MCP servers individually is complex:

- 🔓 Each server requires separate security configuration
- ❌ Multiple ports and endpoints to manage
- 🧩 No unified discovery or routing
- 📊 Scattered monitoring and logging

MCP Hub solves all of that:

- ✅ **Single Entry Point**: One gateway for all your MCP servers
- 🛡 **Unified Security**: Centralized authentication and authorization  
- 🔄 **Hot Reload**: Add/remove servers without restart
- 📍 **Smart Routing**: Clean path-based routing (`/server/mcp`)
- 🏗️ **Pure MCP**: No protocol conversion, maintains MCP semantics

What feels like "one more layer" is actually **simplification at scale**.

MCP Hub makes your MCP infrastructure manageable, secure, and scalable—right now, with zero complexity.

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

**SSE and HTTP MCP Servers:**

```bash
# SSE MCP server
mcp-hub --port 8000 --api-key "secret" --server-type "sse" -- http://127.0.0.1:8001/sse

# With custom headers
mcp-hub --port 8000 --api-key "secret" --server-type "sse" --header '{"Authorization": "Bearer token"}' -- http://127.0.0.1:8001/sse

# Streamable HTTP MCP server  
mcp-hub --port 8000 --api-key "secret" --server-type "streamable-http" -- http://127.0.0.1:8002/mcp
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

**Example config.json:**

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
    "mcp_sse": {
      "type": "sse",
      "url": "http://127.0.0.1:8001/sse",
      "headers": {
        "Authorization": "Bearer token",
        "X-Custom-Header": "value"
      }
    },
    "mcp_streamable_http": {
      "type": "streamable-http",
      "url": "http://127.0.0.1:8002/mcp"
    }
  }
}
```

Each MCP server will be accessible under its own unique route:
- **Memory tools**: `http://localhost:8000/memory/mcp`
- **Time tools**: `http://localhost:8000/time/mcp`
- **SSE server**: `http://localhost:8000/mcp_sse/mcp`
- **HTTP server**: `http://localhost:8000/mcp_streamable_http/mcp`

Connect your MCP client to any of these endpoints to access the tools from that specific server.

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

2.  **Run tests:**
    ```bash
    uv run pytest
    ```

3.  **Running Locally with Active Changes:**

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
