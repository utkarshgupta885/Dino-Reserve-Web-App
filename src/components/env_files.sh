# Backend .env.example
# Copy this to .env and update with your actual values

# Database Configuration
DATABASE_URL=postgresql://dinouser:dinopass123@localhost:5432/dinoreserve
# For SQLite (development): DATABASE_URL=sqlite:///./dinoreserve.db

# API Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
API_HOST=0.0.0.0
API_PORT=8000

# CORS Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# JWT Configuration (for future auth implementation)
JWT_SECRET_KEY=another-secret-key-for-jwt-tokens
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development

# ============================================

# Frontend .env.example
# Copy this to .env in the frontend directory

# API Base URL
VITE_API_URL=http://localhost:8000

# App Configuration
VITE_APP_NAME=Dino Reserve
VITE_APP_VERSION=1.0.0

# Feature Flags
VITE_ENABLE_DEBUG=true
