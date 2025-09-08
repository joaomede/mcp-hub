# MCP Hub Docker Setup

Este diretório contém a configuração Docker para o MCP Hub, permitindo execução tanto em desenvolvimento quanto em produção.

## 🚀 Início Rápido

### Script de Gerenciamento (Recomendado)

Use o script `docker.sh` para gerenciar facilmente o MCP Hub:

```bash
# Tornar o script executável (primeira vez)
chmod +x docker.sh

# Desenvolvimento
./docker.sh dev

# Produção
./docker.sh prod

# Ver logs
./docker.sh logs

# Parar serviços
./docker.sh stop

# Ver ajuda
./docker.sh help
```

### Desenvolvimento

1. **Configure as variáveis de ambiente:**
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

2. **Configure os servidores MCP:**
   ```bash
   # Edite config/config.json com seus servidores MCP
   ```

3. **Execute em modo desenvolvimento:**
   ```bash
   docker-compose up --build
   ```

### Produção

1. **Configure as variáveis de ambiente para produção:**
   ```bash
   # Configure MCP_HUB_API_KEY com uma chave segura
   export MCP_HUB_API_KEY="your-production-api-key"
   ```

2. **Execute em modo produção:**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
   ```

## 📁 Estrutura de Arquivos

```
├── docker-compose.yml           # Configuração base (desenvolvimento)
├── docker-compose.prod.yml      # Override para produção
├── Dockerfile                   # Imagem Docker do MCP Hub
├── config/
│   └── config.json             # Configuração dos servidores MCP
├── logs/                       # Logs do MCP Hub (criado automaticamente)
└── .env.example                # Template de variáveis de ambiente
```

## 🔧 Configuração

### Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `MCP_HUB_PORT` | `8000` | Porta do MCP Hub |
| `MCP_HUB_API_KEY` | `default-api-key` | Chave de API para autenticação |
| `MCP_HUB_LOG_LEVEL` | `info` | Nível de log (debug, info, warning, error) |

### Configuração de Servidores MCP

Edite `config/config.json` para definir seus servidores MCP:

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
    }
  }
}
```

## 🏗️ Modos de Execução

### Modo Desenvolvimento

- **Hot Reload**: Mudanças no código são refletidas automaticamente
- **Logs Detalhados**: Nível de log `info` por padrão
- **Volume Binding**: Código fonte montado para desenvolvimento
- **Configuração Flexível**: Arquivo de configuração com hot-reload

```bash
docker-compose up --build
```

### Modo Produção

- **Otimizado**: Sem volume binding de código fonte
- **Logs Otimizados**: Nível de log `warning` por padrão
- **Resource Limits**: Limites de CPU e memória definidos
- **Health Checks**: Verificação de saúde mais frequente
- **Log Rotation**: Configuração de rotação de logs

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

## 🔍 Monitoramento

### Health Check

O MCP Hub inclui um health check que verifica a saúde do serviço:

```bash
# Verificar status
docker-compose ps

# Ver logs de health check
docker-compose logs mcp-hub
```

### Logs

```bash
# Ver logs em tempo real
docker-compose logs -f mcp-hub

# Ver logs de um período específico
docker-compose logs --since="1h" mcp-hub
```

## 🛠️ Comandos Úteis

```bash
# Buildar apenas a imagem
docker-compose build

# Reiniciar serviços
docker-compose restart

# Parar serviços
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Ver status dos serviços
docker-compose ps

# Executar comando no container
docker-compose exec mcp-hub /bin/bash
```

## 🚨 Modo Servidor Único

Para executar um único servidor MCP em vez de usar arquivo de configuração, edite o `command` no `docker-compose.yml`:

```yaml
command: [
  "--port", "8000",
  "--api-key", "${MCP_HUB_API_KEY:-default-api-key}",
  "--",
  "uvx", "mcp-server-time", "--local-timezone=America/New_York"
]
```

## 🔐 Segurança

### Produção

- ✅ Sempre use uma API key forte em produção
- ✅ Configure HTTPS/TLS se exposto publicamente
- ✅ Use secrets management para variáveis sensíveis
- ✅ Configure limites de recursos apropriados
- ✅ Monitore logs para atividade suspeita

### Desenvolvimento

- ⚠️ Nunca commite chaves de API reais
- ⚠️ Use `.env` para variáveis locais (já está no .gitignore)

## 🐛 Troubleshooting

### Container não inicia

```bash
# Verificar logs
docker-compose logs mcp-hub

# Verificar configuração
docker-compose config
```

### Health check falhando

```bash
# Testar health check manualmente
docker-compose exec mcp-hub curl -f http://localhost:8000/health
```

### Problemas de permissão

```bash
# Verificar proprietário dos volumes
ls -la logs/ config/

# Ajustar permissões se necessário
sudo chown -R $USER:$USER logs/ config/
```
