# MCP Hub Docker Setup

Docker setup to run MCP Hub in production or local development.

## 🚀 Quick Start

### Management Script (Recommended)

Use the `docker.sh` script to easily manage MCP Hub:

```bash
# Make the script executable (first time)
chmod +x docker.sh

# Development
./docker.sh dev

# Production
./docker.sh prod

# View logs
./docker.sh logs

# Stop services
./docker.sh stop

# View help
./docker.sh help
```

### Development

1. **Set environment variables:**
  ```bash
  cp .env.example .env
  # Edit the .env file with your settings
  ```

2. **Configure MCP servers:**
  ```bash
  # Copy the example file and edit it with your MCP servers
  cp config/config.example.json config/config.json
  ```

3. **Run in development mode:**
  ```bash
  docker compose up --build
  ```

### Production

1. **Set environment variables for production:**
  ```bash
  # Set MCP_HUB_API_KEY to a secure key (or leave empty to disable auth)
  export MCP_HUB_API_KEY="your-production-api-key"
  ```

2. **Run in production mode (single compose):**
  ```bash
  docker compose up -d --build
  ```

## 📁 File Structure

```
├── docker-compose.yml           # Single compose for production
├── Dockerfile                   # Imagem Docker do MCP Hub
├── config/
│   └── config.json             # MCP servers configuration
├── logs/                       # Logs do MCP Hub (criado automaticamente)
└── .env.example                # Template de variáveis de ambiente
```

## 🔧 Configuration

### Variáveis de Ambiente

| Variable | Default | Description |
|----------|--------|-----------|
| `MCP_HUB_PORT` | `8000` | MCP Hub port |
| `MCP_HUB_API_KEY` | `default-api-key` (empty disables auth) | API key for authentication |
| `MCP_HUB_LOG_LEVEL` | `info` | Log level (debug, info, warning, error) |

### MCP Servers Configuration

Edit `config/config.json` to define your MCP servers:

```json
{
  "mcpServers": {
  "memory": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-memory"] },
  "filesystem": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"] },
  "time": { "command": "uvx", "args": ["mcp-server-time", "--local-timezone", "America/New_York"] },
  "git": { "command": "uvx", "args": ["mcp-server-git", "--repository", "/repo"] }
  }
}
```

## 🏗️ Run Modes

### Development Mode

- **Hot Reload**: Code changes are reflected automatically
- **Detailed Logs**: `info` log level by default
- **Volume Binding**: Source code mounted for development
- **Flexible Configuration**: Config file with hot-reload

```bash
docker compose up --build
```

### Production Mode

- **Optimized**: No source volume binding
- **Optimized Logs**: `warning` log level by default
- **Resource Limits**: CPU and memory limits set
- **Health Checks**: More frequent health checks
- **Log Rotation**: Log rotation configured

```bash
docker compose up -d --build
```

## 🔍 Monitoring

### Health Check

MCP Hub includes a health check:

```bash
# Check status
docker compose ps

# Check health check logs
docker compose logs mcp-hub
```

### Logs

```bash
# View logs in real time
docker compose logs -f mcp-hub

# View logs for a specific period
docker compose logs --since="1h" mcp-hub
```

## 🛠️ Useful Commands

```bash
# Build the image only
docker compose build

# Restart services
docker compose restart

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# View services status
docker compose ps

# Run a command in the container
docker compose exec mcp-hub /bin/bash
```

## 🚨 Single Server Mode

To run a single MCP server instead of using a config file, edit the `command` in `docker-compose.yml`:

```yaml
command: [
  "--port", "8000",
  "--api-key", "${MCP_HUB_API_KEY:-default-api-key}",
  "--",
  "uvx", "mcp-server-time", "--local-timezone=America/New_York"
]
```

## 🔐 Security

### Production

- ✅ Always use a strong API key in production
- ✅ Configure HTTPS/TLS if exposed publicly
- ✅ Use secrets management for sensitive variables
- ✅ Configure appropriate resource limits
- ✅ Monitor logs for suspicious activity

### Development

- ⚠️ Never commit real API keys
- ⚠️ Use `.env` for local variables (already in .gitignore)

## 🐛 Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs mcp-hub

# Check configuration
docker-compose config
```

### Health check failing

```bash
# Test the health check manually
docker-compose exec mcp-hub curl -f http://localhost:8000/health
```

### Permission issues

```bash
# Check volume ownership
ls -la logs/ config/

# Adjust permissions if necessary
sudo chown -R $USER:$USER logs/ config/
```

## 🔓 Run without key (Keyless)

- CLI/local: omit `--api-key` or pass an empty value `--api-key ""`.
- Docker Compose: set `MCP_HUB_API_KEY` empty in `.env`.

When the API key is empty, authentication is disabled. Not recommended for public exposure.

## 📎 Tips

- Git server: mount a valid repository as read-only in `/repo` and point `mcp-server-git` to `--repository /repo`.
