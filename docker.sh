#!/bin/bash

# MCP Hub Docker Management Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Functions
check_requirements() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
}

setup_env() {
    if [ ! -f .env ]; then
        print_info "Creating .env file from template..."
        cp .env.example .env
        print_warning "Please edit .env file with your configurations before running MCP Hub"
    fi
}

dev() {
    print_info "Starting MCP Hub in development mode..."
    setup_env
    docker-compose up --build
}

prod() {
    print_info "Starting MCP Hub in production mode..."
    setup_env
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
    print_success "MCP Hub started in production mode"
    print_info "Check logs with: ./docker.sh logs"
}

stop() {
    print_info "Stopping MCP Hub..."
    docker-compose down
    print_success "MCP Hub stopped"
}

restart() {
    print_info "Restarting MCP Hub..."
    docker-compose restart
    print_success "MCP Hub restarted"
}

logs() {
    docker-compose logs -f mcp-hub
}

status() {
    docker-compose ps
}

clean() {
    print_warning "This will remove all containers, networks, and volumes"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down -v --remove-orphans
        docker system prune -f
        print_success "Cleanup completed"
    else
        print_info "Cleanup cancelled"
    fi
}

shell() {
    docker-compose exec mcp-hub /bin/bash
}

help() {
    echo "MCP Hub Docker Management Script"
    echo
    echo "Usage: $0 <command>"
    echo
    echo "Commands:"
    echo "  dev      - Start in development mode (with hot reload)"
    echo "  prod     - Start in production mode (detached)"
    echo "  stop     - Stop all services"
    echo "  restart  - Restart services"
    echo "  logs     - View logs in real-time"
    echo "  status   - Show service status"
    echo "  shell    - Access container shell"
    echo "  clean    - Clean up containers and volumes"
    echo "  help     - Show this help message"
    echo
    echo "Examples:"
    echo "  $0 dev              # Start development environment"
    echo "  $0 prod             # Start production environment"
    echo "  $0 logs             # View logs"
}

# Main script
case ${1:-help} in
    dev)
        check_requirements
        dev
        ;;
    prod)
        check_requirements
        prod
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    status)
        status
        ;;
    shell)
        shell
        ;;
    clean)
        clean
        ;;
    help|*)
        help
        ;;
esac
