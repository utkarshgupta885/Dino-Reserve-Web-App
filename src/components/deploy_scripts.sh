#!/bin/bash
# deploy.sh - Automated deployment script for Dino Reserve

set -e  # Exit on error

echo "🦕 Starting Dino Reserve Deployment 🦖"
echo "========================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-production}
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo -e "${BLUE}Environment: ${ENVIRONMENT}${NC}"

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if running as root (for production)
check_permissions() {
    if [ "$ENVIRONMENT" = "production" ] && [ "$EUID" -ne 0 ]; then 
        print_error "Please run as root for production deployment"
        exit 1
    fi
}

# Backup database
backup_database() {
    echo ""
    echo "📦 Creating database backup..."
    
    mkdir -p $BACKUP_DIR
    
    if [ "$ENVIRONMENT" = "production" ]; then
        pg_dump dinoreserve > "$BACKUP_DIR/dinoreserve_$TIMESTAMP.sql"
        print_status "Database backed up to $BACKUP_DIR/dinoreserve_$TIMESTAMP.sql"
    else
        print_status "Skipping backup for $ENVIRONMENT environment"
    fi
}

# Pull latest code
update_code() {
    echo ""
    echo "📥 Updating code from repository..."
    
    git fetch --all
    git pull origin main
    
    print_status "Code updated"
}

# Backend deployment
deploy_backend() {
    echo ""
    echo "🐍 Deploying backend..."
    
    cd backend
    
    # Activate virtual environment
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt --quiet
    print_status "Backend dependencies installed"
    
    # Run migrations (if you have them)
    # alembic upgrade head
    
    # Restart backend service
    if [ "$ENVIRONMENT" = "production" ]; then
        sudo systemctl restart dinoreserve-backend
        print_status "Backend service restarted"
    else
        print_status "Backend ready (development mode)"
    fi
    
    cd ..
}

# Frontend deployment
deploy_frontend() {
    echo ""
    echo "⚛️  Deploying frontend..."
    
    cd frontend
    
    # Install dependencies
    npm ci --silent
    print_status "Frontend dependencies installed"
    
    # Build for production
    npm run build
    print_status "Frontend built successfully"
    
    # Deploy build files
    if [ "$ENVIRONMENT" = "production" ]; then
        sudo rm -rf /var/www/dinoreserve/*
        sudo cp -r dist/* /var/www/dinoreserve/
        sudo chown -R www-data:www-data /var/www/dinoreserve
        print_status "Frontend files deployed to /var/www/dinoreserve"
    else
        print_status "Frontend build complete (development mode)"
    fi
    
    cd ..
}

# Docker deployment
deploy_docker() {
    echo ""
    echo "🐳 Deploying with Docker..."
    
    # Pull latest images
    docker-compose pull
    print_status "Docker images pulled"
    
    # Rebuild and restart
    docker-compose down
    docker-compose up -d --build
    print_status "Docker containers running"
    
    # Wait for services to start
    echo "⏳ Waiting for services to be ready..."
    sleep 10
    
    # Check health
    if docker-compose ps | grep -q "Up"; then
        print_status "All services are running"
    else
        print_error "Some services failed to start"
        docker-compose logs
        exit 1
    fi
}

# Health check
health_check() {
    echo ""
    echo "🏥 Running health checks..."
    
    # Check backend
    if curl -f http://localhost:8000/ > /dev/null 2>&1; then
        print_status "Backend API is healthy"
    else
        print_error "Backend API health check failed"
        exit 1
    fi
    
    # Check frontend (if deployed)
    if [ "$ENVIRONMENT" = "production" ]; then
        if curl -f http://localhost/ > /dev/null 2>&1; then
            print_status "Frontend is healthy"
        else
            print_error "Frontend health check failed"
            exit 1
        fi
    fi
}

# Main deployment flow
main() {
    echo ""
    echo "🚀 Starting deployment process..."
    
    check_permissions
    backup_database
    
    if [ "$ENVIRONMENT" = "docker" ]; then
        deploy_docker
    else
        update_code
        deploy_backend
        deploy_frontend
    fi
    
    health_check
    
    echo ""
    echo "========================================"
    echo -e "${GREEN}🎉 Deployment completed successfully! 🎉${NC}"
    echo "========================================"
    echo ""
    echo "📊 Deployment Summary:"
    echo "  - Environment: $ENVIRONMENT"
    echo "  - Timestamp: $TIMESTAMP"
    echo "  - Backend: Running on port 8000"
    echo "  - Frontend: Running on port 3000 (or 80)"
    echo ""
    echo "🦕 Your dinos are ready to welcome guests! 🦖"
}

# Rollback function
rollback() {
    echo ""
    echo "⏮️  Rolling back deployment..."
    
    # Restore database backup
    if [ -f "$BACKUP_DIR/dinoreserve_$TIMESTAMP.sql" ]; then
        psql dinoreserve < "$BACKUP_DIR/dinoreserve_$TIMESTAMP.sql"
        print_status "Database restored"
    fi
    
    # Git reset
    git reset --hard HEAD^
    print_status "Code reverted"
    
    # Restart services
    if [ "$ENVIRONMENT" = "docker" ]; then
        docker-compose restart
    else
        sudo systemctl restart dinoreserve-backend
    fi
    
    print_status "Rollback complete"
}

# Handle errors
trap 'echo -e "${RED}Deployment failed!${NC}"; rollback' ERR

# Run main deployment
main

# ============================================
# Makefile
# Save as: Makefile

# .PHONY: help install dev test clean build deploy docker-up docker-down
# 
# help:
# 	@echo "🦕 Dino Reserve - Available Commands 🦖"
# 	@echo ""
# 	@echo "Development:"
# 	@echo "  make install       - Install all dependencies"
# 	@echo "  make dev           - Start development servers"
# 	@echo "  make test          - Run all tests"
# 	@echo "  make lint          - Run linters"
# 	@echo ""
# 	@echo "Database:"
# 	@echo "  make db-create     - Create database"
# 	@echo "  make db-seed       - Seed database with sample data"
# 	@echo "  make db-reset      - Reset database (WARNING: deletes all data)"
# 	@echo ""
# 	@echo "Docker:"
# 	@echo "  make docker-up     - Start Docker containers"
# 	@echo "  make docker-down   - Stop Docker containers"
# 	@echo "  make docker-logs   - View Docker logs"
# 	@echo ""
# 	@echo "Deployment:"
# 	@echo "  make build         - Build frontend and backend"
# 	@echo "  make deploy-staging    - Deploy to staging"
# 	@echo "  make deploy-production - Deploy to production"
# 
# install:
# 	@echo "📦 Installing dependencies..."
# 	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
# 	cd frontend && npm install
# 	@echo "✅ Installation complete!"
# 
# dev:
# 	@echo "🚀 Starting development servers..."
# 	@make -j2 dev-backend dev-frontend
# 
# dev-backend:
# 	cd backend && source venv/bin/activate && python main.py
# 
# dev-frontend:
# 	cd frontend && npm run dev
# 
# test:
# 	@echo "🧪 Running tests..."
# 	cd backend && source venv/bin/activate && pytest test_main.py -v
# 	@echo "✅ All tests passed!"
# 
# lint:
# 	@echo "🔍 Running linters..."
# 	cd backend && source venv/bin/activate && flake8 . && black --check .
# 	cd frontend && npm run lint
# 
# db-create:
# 	createdb dinoreserve
# 	psql -d dinoreserve -c "CREATE USER dinouser WITH PASSWORD 'dinopass123';"
# 	psql -d dinoreserve -c "GRANT ALL PRIVILEGES ON DATABASE dinoreserve TO dinouser;"
# 
# db-seed:
# 	cd backend && source venv/bin/activate && python seed_data.py
# 
# db-reset:
# 	@echo "⚠️  WARNING: This will delete all data!"
# 	@read -p "Are you sure? [y/N] " confirm; \
# 	if [ "$$confirm" = "y" ]; then \
# 		dropdb dinoreserve; \
# 		make db-create; \
# 		make db-seed; \
# 	fi
# 
# docker-up:
# 	docker-compose up -d
# 	@echo "✅ Docker containers started!"
# 	@make docker-logs
# 
# docker-down:
# 	docker-compose down
# 
# docker-logs:
# 	docker-compose logs -f
# 
# build:
# 	@echo "🏗️  Building application..."
# 	cd frontend && npm run build
# 	@echo "✅ Build complete!"
# 
# deploy-staging:
# 	./deploy.sh staging
# 
# deploy-production:
# 	@echo "⚠️  Deploying to PRODUCTION"
# 	@read -p "Are you sure? [y/N] " confirm; \
# 	if [ "$$confirm" = "y" ]; then \
# 		./deploy.sh production; \
# 	fi
# 
# clean:
# 	@echo "🧹 Cleaning up..."
# 	cd backend && rm -rf __pycache__ .pytest_cache venv
# 	cd frontend && rm -rf node_modules dist .vite
# 	@echo "✅ Cleanup complete!"
