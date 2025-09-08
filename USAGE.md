# 📖 MCP Hub Usage Guide

## 🎯 Quick Start

### Single MCP Server

```bash
# Run a single MCP server (available at /mcp endpoint)
mcp-hub --port 8000 --api-key "your-secret-key" -- uvx mcp-server-time
```

### Multiple MCP Servers (Recommended)

```bash
# Create config.json with your servers
mcp-hub --config config.json --port 8000 --api-key "your-secret-key"
```

## 🔧 Configuration

### Config File Format

MCP Hub uses the same configuration format as Claude Desktop:

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

### Server Endpoints

Each configured server gets its own endpoint:

- **Memory Server**: `http://localhost:8000/memory/mcp`
- **Time Server**: `http://localhost:8000/time/mcp`
- **Filesystem Server**: `http://localhost:8000/filesystem/mcp`

### Hot Reload

Enable automatic configuration reloading:

```bash
mcp-hub --config config.json --hot-reload
```

Changes to `config.json` will be automatically applied without restart.

## 🔐 Authentication

### API Key Authentication

Protect your MCP Hub with an API key:

```bash
mcp-hub --api-key "your-secret-key" --config config.json
```

All requests must include the API key:

```bash
curl -H "Authorization: Bearer your-secret-key" \
     http://localhost:8000/memory/mcp
```

## 🐳 Docker Usage

### Quick Start

```bash
# Build the image
docker build -t mcp-hub:latest .

# Run with config file
docker run -p 8000:8000 \
  -v $(pwd)/config.json:/app/config.json \
  -e MCP_HUB_API_KEY="your-secret-key" \
  mcp-hub:latest --config /app/config.json --host 0.0.0.0
```

### Docker Compose (Recommended)

```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

See [DOCKER.md](DOCKER.md) for detailed Docker configuration.

## 🛠️ Development & Testing

### Local Development

```bash
# Install dependencies
uv sync --dev

# Run locally with live reload
uv run mcp-hub --config config.json --port 8000
```

### Testing

```bash
# Unit tests
uv run pytest

# Integration tests (requires Docker)
docker build -t mcp-hub:latest .
python test_mcp_integration.py
```

## 🔍 Monitoring & Health Checks

### Health Endpoint

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "servers": {
    "memory": "running",
    "time": "running"
  }
}
```

### Logs

```bash
# Docker logs
docker logs mcp-hub-container

# Local development
# Logs are printed to stdout
```

## 🚨 Troubleshooting

### Common Issues

1. **Server Not Starting**
   ```bash
   # Check config syntax
   python -m json.tool config.json
   
   # Verify MCP server commands work independently
   uvx mcp-server-time --help
   ```

2. **Connection Refused**
   ```bash
   # Check if port is available
   lsof -i :8000
   
   # Test health endpoint
   curl http://localhost:8000/health
   ```

3. **Authentication Errors**
   ```bash
   # Verify API key format
   curl -H "Authorization: Bearer your-api-key" \
        http://localhost:8000/health
   ```

### Debug Mode

Enable detailed logging:

```bash
mcp-hub --config config.json --log-level debug
```

## 📋 Best Practices

### Configuration

- ✅ Use descriptive server names in config
- ✅ Set appropriate timeouts for your use case
- ✅ Use absolute paths for file-based servers
- ✅ Test individual MCP servers before aggregating

### Security

- ✅ Always use strong API keys in production
- ✅ Restrict network access to trusted clients
- ✅ Use HTTPS/TLS for public deployments
- ✅ Rotate API keys regularly

### Performance

- ✅ Use hot-reload only in development
- ✅ Configure appropriate resource limits in Docker
- ✅ Monitor server health and restart failed servers
- ✅ Use connection pooling for high-traffic scenarios

## 🔗 Integration Examples

### Claude Desktop

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "mcp-hub": {
      "command": "curl",
      "args": [
        "-H", "Authorization: Bearer your-api-key",
        "http://localhost:8000/memory/mcp"
      ]
    }
  }
}
```

### Python Client

```python
import requests

# Connect to aggregated server
response = requests.post(
    "http://localhost:8000/memory/mcp",
    headers={"Authorization": "Bearer your-api-key"},
    json={"method": "tools/list"}
)

tools = response.json()
print(f"Available tools: {len(tools['result']['tools'])}")
```

### HTTP API

```bash
# List available tools
curl -X POST \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}' \
  http://localhost:8000/memory/mcp

# Call a specific tool
curl -X POST \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/call", "params": {"name": "create_entity", "arguments": {"name": "test"}}}' \
  http://localhost:8000/memory/mcp
```

## 📚 Additional Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Available MCP Servers](https://github.com/modelcontextprotocol/servers)
- [Claude Desktop Configuration](https://modelcontextprotocol.io/quickstart/user)
- [Docker Documentation](DOCKER.md)
