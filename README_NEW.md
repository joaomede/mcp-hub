# ⚡️ mcpo

**MCP Gateway** - A powerful proxy and aggregator for Model Context Protocol (MCP) servers.

mcpo is a simple yet robust gateway that aggregates multiple MCP servers into a single endpoint, providing unified access, authentication, and management for your MCP tools without any protocol conversion.

Pure MCP-to-MCP. No conversions. No hassle.

## 🤔 Why Use MCP Gateway?

Managing multiple MCP servers individually is complex:

- 🔓 Each server requires separate security configuration
- ❌ Multiple ports and endpoints to manage
- 🧩 No unified discovery or routing
- 📊 Scattered monitoring and logging

MCP Gateway solves all of that:

- ✅ **Single Entry Point**: One gateway for all your MCP servers
- 🛡 **Unified Security**: Centralized authentication and authorization  
- 🔄 **Hot Reload**: Add/remove servers without restart
- 📍 **Smart Routing**: Clean path-based routing (`/server/mcp`)
- 🏗️ **Pure MCP**: No protocol conversion, maintains MCP semantics

What feels like "one more layer" is actually **simplification at scale**.

MCP Gateway makes your MCP infrastructure manageable, secure, and scalable—right now, with zero complexity.

## 🚀 Quick Usage

We recommend using uv for lightning-fast startup and zero config.

```bash
uvx mcpo --port 8000 --api-key "top-secret" -- your_mcp_server_command
```

Or, if you're using Python:

```bash
pip install mcpo
mcpo --port 8000 --api-key "top-secret" -- your_mcp_server_command
```

**Single MCP Server Examples:**

```bash
# Proxy a single MCP server (available at /mcp)
mcpo --port 8000 --api-key "secret" -- uvx mcp-server-time --local-timezone=America/New_York
```

**Multiple MCP Servers (Recommended):**

```bash
# Use config file for multiple servers
mcpo --config config.json --hot-reload --port 8000 --api-key "secret"
```

**SSE and HTTP MCP Servers:**

```bash
# SSE MCP server
mcpo --port 8000 --api-key "secret" --server-type "sse" -- http://127.0.0.1:8001/sse

# With custom headers
mcpo --port 8000 --api-key "secret" --server-type "sse" --header '{"Authorization": "Bearer token"}' -- http://127.0.0.1:8001/sse

# Streamable HTTP MCP server  
mcpo --port 8000 --api-key "secret" --server-type "streamable-http" -- http://127.0.0.1:8002/mcp
```

You can also run mcpo via Docker with no installation:

```bash
docker run -p 8000:8000 ghcr.io/open-webui/mcpo:main --api-key "secret" -- your_mcp_server_command
```

**Example - Single Server:**

```bash
uvx mcpo --port 8000 --api-key "secret" -- uvx mcp-server-time --local-timezone=America/New_York
```

Your MCP server is now accessible at:
- **MCP Endpoint**: `http://localhost:8000/mcp` 
- **Connect via MCP client**: `mcp-client --url ws://localhost:8000/mcp`

### 🔄 Using a Config File (Recommended)

You can serve **multiple MCP servers** via a single config file that follows the [Claude Desktop](https://modelcontextprotocol.io/quickstart/user) format.

Enable hot-reload mode with `--hot-reload` to automatically watch your config file for changes and reload servers without downtime:

**Start via:**

```bash
mcpo --config /path/to/config.json
```

**Or with hot-reload enabled:**

```bash
mcpo --config /path/to/config.json --hot-reload
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

- Python 3.8+
- uv (optional, but highly recommended for performance + packaging)

## 🛠️ Development & Testing

To contribute or run tests locally:

1.  **Set up the environment:**
    ```bash
    # Clone the repository
    git clone https://github.com/open-webui/mcpo.git
    cd mcpo

    # Install dependencies (including dev dependencies)
    uv sync --dev
    ```

2.  **Run tests:**
    ```bash
    uv run pytest
    ```

3.  **Running Locally with Active Changes:**

    To run `mcpo` with your local modifications from a specific branch (e.g., `my-feature-branch`):

    ```bash
    # Ensure you are on your development branch
    git checkout my-feature-branch

    # Make your code changes in the src/mcpo directory or elsewhere

    # Run mcpo using uv, which will use your local, modified code
    # This command starts mcpo on port 8000 and proxies your_mcp_server_command
    uv run mcpo --port 8000 -- your_mcp_server_command

    # Example with a test MCP server (like mcp-server-time):
    # uv run mcpo --port 8000 -- uvx mcp-server-time --local-timezone=America/New_York
    ```
    This allows you to test your changes interactively before committing or creating a pull request. Access your locally running `mcpo` instance at `http://localhost:8000` and connect MCP clients to the `/mcp` endpoints.

## 🪪 License

MIT

## 🤝 Contributing

We welcome and strongly encourage contributions from the community!

Whether you're fixing a bug, adding features, improving documentation, or just sharing ideas—your input is incredibly valuable and helps make mcpo better for everyone.

Getting started is easy:

- Fork the repo
- Create a new branch
- Make your changes
- Open a pull request

Not sure where to start? Feel free to open an issue or ask a question—we're happy to help you find a good first task.

## ✨ Star History

<a href="https://star-history.com/#open-webui/mcpo&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=open-webui/mcpo&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=open-webui/mcpo&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=open-webui/mcpo&type=Date" />
  </picture>
</a>

---

✨ Let's build the future of interoperable AI tooling together!
