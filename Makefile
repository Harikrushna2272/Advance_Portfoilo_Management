# Makefile for StockAI Trading System

.PHONY: help install dev test build run stop clean logs

# Default target
help:
	@echo "StockAI Trading System - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  install     - Install dependencies"
	@echo "  dev         - Run in development mode"
	@echo "  test        - Run tests"
	@echo ""
	@echo "Docker:"
	@echo "  build       - Build Docker images"
	@echo "  run         - Run with Docker Compose"
	@echo "  stop        - Stop Docker containers"
	@echo "  logs        - View logs"
	@echo "  clean       - Clean up Docker resources"
	@echo ""
	@echo "Utilities:"
	@echo "  format      - Format code with black"
	@echo "  lint        - Run linting"
	@echo "  setup       - Initial setup"

# Development commands
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Installing spaCy language model..."
	python -m spacy download en_core_web_sm

dev:
	@echo "Running in development mode..."
	python src/main.py

ui:
	@echo "Starting Streamlit UI..."
	streamlit run src/ui/streamlit_app.py --server.port=8501

test:
	@echo "Running tests..."
	python -m pytest tests/ -v

# Docker commands
build:
	@echo "Building Docker images..."
	docker-compose build

run:
	@echo "Starting StockAI with Docker Compose..."
	docker-compose up -d

stop:
	@echo "Stopping Docker containers..."
	docker-compose down

logs:
	@echo "Viewing logs..."
	docker-compose logs -f stockai

clean:
	@echo "Cleaning up Docker resources..."
	docker-compose down -v --remove-orphans
	docker system prune -f

# Code quality
format:
	@echo "Formatting code..."
	black src/ tests/
	isort src/ tests/

lint:
	@echo "Running linting..."
	flake8 src/ tests/
	mypy src/

# Setup
setup:
	@echo "Setting up StockAI..."
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		cp env.example .env; \
		echo "Please update .env with your API keys and configuration"; \
	fi
	@echo "Creating necessary directories..."
	mkdir -p logs models data
	@echo "Setup complete!"

# Database commands
db-migrate:
	@echo "Running database migrations..."
	# Add migration commands here

db-reset:
	@echo "Resetting database..."
	docker-compose down -v
	docker-compose up -d postgres
	sleep 10
	docker-compose up -d

# Monitoring
monitor:
	@echo "Opening monitoring dashboards..."
	@echo "Streamlit UI: http://localhost:8501"
	@echo "Grafana: http://localhost:3000 (admin/admin)"
	@echo "Prometheus: http://localhost:9090"

# Production deployment
deploy:
	@echo "Deploying to production..."
	# Add production deployment commands here

# Backup
backup:
	@echo "Creating backup..."
	docker-compose exec postgres pg_dump -U stockai stockai > backup_$(shell date +%Y%m%d_%H%M%S).sql

# Restore
restore:
	@echo "Restoring from backup..."
	@read -p "Enter backup file name: " file; \
	docker-compose exec -T postgres psql -U stockai stockai < $$file
