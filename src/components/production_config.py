# config.py - Backend Configuration Management
"""
Configuration management for Dino Reserve API
Supports multiple environments: development, staging, production
"""

import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Dino Reserve"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://dinouser:dinopass123@localhost:5432/dinoreserve"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    JWT_SECRET_KEY: str = "jwt-secret-key-change-this"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/dinoreserve.log"
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = False
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Email (for notifications)
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "noreply@dinoreserve.com"
    
    # Redis (for caching)
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_ENABLED: bool = False
    
    # Monitoring
    SENTRY_DSN: str = ""
    SENTRY_ENABLED: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# ============================================
# logger.py - Logging Configuration

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "dinoreserve", log_file: str = "logs/dinoreserve.log"):
    """
    Set up logger with both file and console handlers
    """
    # Create logs directory if it doesn't exist
    log_path = Path(log_file).parent
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Initialize logger
logger = setup_logger()

# ============================================
# middleware.py - Custom Middleware

from fastapi import Request, status
from fastapi.responses import JSONResponse
from time import time
import uuid

class RequestLoggingMiddleware:
    """Log all requests with timing"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time()
        
        # Log request
        logger.info(f"[{request_id}] {request.method} {request.url.path}")
        
        try:
            response = await call_next(request)
            
            # Log response
            duration = time() - start_time
            logger.info(
                f"[{request_id}] Completed {response.status_code} in {duration:.3f}s"
            )
            
            # Add custom headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{duration:.3f}s"
            
            return response
        
        except Exception as e:
            duration = time() - start_time
            logger.error(f"[{request_id}] Error: {str(e)} after {duration:.3f}s")
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error", "request_id": request_id}
            )

# ============================================
# rate_limit.py - Rate Limiting

from fastapi import HTTPException, Request
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed"""
        now = datetime.now()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        # Clean old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > window_start
        ]
        
        # Check limit
        if len(self.requests[identifier]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[identifier].append(now)
        return True
    
    async def __call__(self, request: Request):
        """Middleware to check rate limit"""
        # Use IP address as identifier
        identifier = request.client.host
        
        if not self.is_allowed(identifier):
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )

# ============================================
# systemd service file
# Save as: /etc/systemd/system/dinoreserve-backend.service

# [Unit]
# Description=Dino Reserve FastAPI Backend
# After=network.target postgresql.service
# 
# [Service]
# Type=simple
# User=www-data
# Group=www-data
# WorkingDirectory=/var/www/dinoreserve/backend
# Environment="PATH=/var/www/dinoreserve/backend/venv/bin"
# ExecStart=/var/www/dinoreserve/backend/venv/bin/gunicorn main:app \
#     --workers 4 \
#     --worker-class uvicorn.workers.UvicornWorker \
#     --bind 0.0.0.0:8000 \
#     --access-logfile /var/log/dinoreserve/access.log \
#     --error-logfile /var/log/dinoreserve/error.log \
#     --log-level info
# Restart=always
# RestartSec=10
# 
# [Install]
# WantedBy=multi-user.target

# ============================================
# nginx configuration
# Save as: /etc/nginx/sites-available/dinoreserve

# upstream backend {
#     server 127.0.0.1:8000;
# }
# 
# server {
#     listen 80;
#     server_name dinoreserve.com www.dinoreserve.com;
#     
#     # Redirect to HTTPS
#     return 301 https://$server_name$request_uri;
# }
# 
# server {
#     listen 443 ssl http2;
#     server_name dinoreserve.com www.dinoreserve.com;
#     
#     # SSL Configuration
#     ssl_certificate /etc/letsencrypt/live/dinoreserve.com/fullchain.pem;
#     ssl_certificate_key /etc/letsencrypt/live/dinoreserve.com/privkey.pem;
#     ssl_protocols TLSv1.2 TLSv1.3;
#     ssl_ciphers HIGH:!aNULL:!MD5;
#     
#     # Frontend (React build)
#     root /var/www/dinoreserve/frontend/dist;
#     index index.html;
#     
#     # Gzip compression
#     gzip on;
#     gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
#     
#     # Frontend routes
#     location / {
#         try_files $uri $uri/ /index.html;
#     }
#     
#     # Backend API
#     location /api/ {
#         proxy_pass http://backend/;
#         proxy_http_version 1.1;
#         proxy_set_header Upgrade $http_upgrade;
#         proxy_set_header Connection 'upgrade';
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#         proxy_cache_bypass $http_upgrade;
#         proxy_connect_timeout 60s;
#         proxy_send_timeout 60s;
#         proxy_read_timeout 60s;
#     }
#     
#     # Static files caching
#     location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
#         expires 1y;
#         add_header Cache-Control "public, immutable";
#     }
#     
#     # Security headers
#     add_header X-Frame-Options "SAMEORIGIN" always;
#     add_header X-Content-Type-Options "nosniff" always;
#     add_header X-XSS-Protection "1; mode=block" always;
#     add_header Referrer-Policy "no-referrer-when-downgrade" always;
# }

# ============================================
# monitoring.py - Health Check & Metrics

from fastapi import APIRouter
from datetime import datetime
from sqlalchemy import text
import psutil
import os

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "dinoreserve-api",
        "version": "1.0.0"
    }

@router.get("/health/db")
async def database_health(db = Depends(get_db)):
    """Check database connectivity"""
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

@router.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    process = psutil.Process(os.getpid())
    
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "memory_used_mb": process.memory_info().rss / 1024 / 1024,
        "disk_usage_percent": psutil.disk_usage('/').percent,
        "uptime_seconds": time.time() - process.create_time()
    }
