# 🦕 Dino Reserve - Quick Start Guide

Get your Dino Reserve application up and running in minutes!

## 📋 Prerequisites Checklist

- [ ] Node.js 18+ installed (`node --version`)
- [ ] Python 3.9+ installed (`python --version`)
- [ ] PostgreSQL 14+ installed (`psql --version`)
- [ ] Git installed (`git --version`)

## 🚀 Quick Start (5 Minutes)

### Step 1: Database Setup (2 minutes)

```bash
# Start PostgreSQL
# macOS: brew services start postgresql@14
# Linux: sudo systemctl start postgresql
# Windows: Start PostgreSQL service from Services

# Create database and user
createdb dinoreserve
psql -d dinoreserve -c "CREATE USER dinouser WITH PASSWORD 'dinopass123';"
psql -d dinoreserve -c "GRANT ALL PRIVILEGES ON DATABASE dinoreserve TO dinouser;"
psql -d dinoreserve -c "GRANT ALL ON SCHEMA public TO dinouser;"

# Verify connection
psql -U dinouser -d dinoreserve -c "SELECT 'Database ready! 🦕';"
```

### Step 2: Backend Setup (2 minutes)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start the server (automatically seeds data)
python main.py

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# API docs available at: http://localhost:8000/docs
```

Keep this terminal open! ✅

### Step 3: Frontend Setup (1 minute)

Open a NEW terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# You should see:
# VITE ready in XXX ms
# Local: http://localhost:5173/
```

### Step 4: Open Application! 🎉

Visit: **http://localhost:5173**

**Default Login (for demo):**
- Username: `manager`
- Password: `dino123`

---

## 📦 Alternative Setup with Docker

If you have Docker installed:

```bash
# From project root
docker-compose up -d

# Wait 30 seconds for services to start

# Access application at:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## 🧪 Testing the Installation

### Test Backend API:

```bash
# In a new terminal
cd backend
python test_api.py

# Should see: ✅ ALL TESTS PASSED!
```

### Test Frontend:

1. Visit http://localhost:5173
2. Login with any username/password
3. Click on "T-Rex Tavern"
4. See 25 tables with dino emojis! 🦕

---

## 🛠️ Troubleshooting

### Problem: "Database connection failed"

```bash
# Check if PostgreSQL is running
pg_isready

# If not running, start it:
# macOS: brew services start postgresql@14
# Linux: sudo systemctl start postgresql
# Windows: Start from Services panel

# Verify database exists
psql -l | grep dinoreserve
```

### Problem: "Module not found" errors in backend

```bash
# Make sure virtual environment is activated
which python  # Should show path in venv folder

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Problem: "Cannot connect to backend" in frontend

```bash
# Check backend is running
curl http://localhost:8000

# Should return: {"message":"🦕 Welcome to Dino Reserve API! 🦖"}

# If not, check backend terminal for errors
# Common issue: Port 8000 already in use
# Solution: Kill process on port 8000
# macOS/Linux: lsof -ti:8000 | xargs kill -9
# Windows: netstat -ano | findstr :8000, then taskkill /PID <PID> /F
```

### Problem: Frontend shows blank page

```bash
# Check browser console (F12)
# Common fixes:

# 1. Clear cache and hard reload (Ctrl+Shift+R)

# 2. Check for missing dependencies
cd frontend
npm install

# 3. Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Problem: Tables not showing reservations

```bash
# Re-seed the database with sample data
cd backend
python seed_data.py

# Refresh frontend browser page
```

---

## 📊 Seeding Sample Data

To populate with realistic reservations:

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run seed script
python seed_data.py

# This adds:
# - 5 restaurants with 25 tables each
# - Sample reservations for next 3 days
# - Historical reservations (past 7 days)
```

---

## 🔧 Development Tips

### Backend Development:

```bash
# Auto-reload on code changes (already enabled)
uvicorn main:app --reload

# View API documentation
# Visit: http://localhost:8000/docs
# Interactive Swagger UI with all endpoints!

# Database shell access
psql -U dinouser -d dinoreserve

# View all reservations
psql -U dinouser -d dinoreserve -c "SELECT * FROM reservations LIMIT 5;"
```

### Frontend Development:

```bash
# Use the API service for all backend calls
# Located at: src/services/api.ts

import { api } from '@/services/api';

// Example usage:
const restaurants = await api.restaurants.getAll();
const tables = await api.restaurants.getTables(restaurantId);
```

### Hot Module Replacement:

Both frontend and backend support hot reloading!
- **Frontend**: Edit files in `src/`, changes appear instantly
- **Backend**: Edit `main.py`, server restarts automatically

---

## 📱 Production Deployment

### Backend:

```bash
# Build production server
pip install gunicorn

# Run with multiple workers
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Frontend:

```bash
# Build for production
npm run build

# Output in dist/ folder
# Deploy to:
# - Vercel: vercel deploy
# - Netlify: netlify deploy --prod
# - Any static host
```

### Environment Variables:

Create `.env` files:

**Backend `.env`:**
```
DATABASE_URL=postgresql://user:pass@host:5432/dinoreserve
SECRET_KEY=your-production-secret-key
CORS_ORIGINS=https://yourdomain.com
```

**Frontend `.env`:**
```
VITE_API_URL=https://api.yourdomain.com
```

---

## 📚 Next Steps

1. ✅ **Customize Restaurants**: Edit `main.py` seed data
2. ✅ **Add Authentication**: Implement JWT tokens
3. ✅ **Add Email Notifications**: Send confirmation emails
4. ✅ **Add Analytics Dashboard**: Track popular times
5. ✅ **Mobile App**: Use same API with React Native

---

## 🆘 Still Having Issues?

**Common Port Conflicts:**
```bash
# Backend (8000)
lsof -ti:8000 | xargs kill -9    # macOS/Linux
netstat -ano | findstr :8000     # Windows

# Frontend (5173)
lsof -ti:5173 | xargs kill -9    # macOS/Linux
netstat -ano | findstr :5173     # Windows

# Database (5432)
lsof -ti:5432 | xargs kill -9    # macOS/Linux
```

**Reset Everything:**
```bash
# Backend
cd backend
rm -rf venv __pycache__
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules dist .vite
npm install

# Database
dropdb dinoreserve
createdb dinoreserve
# Then run seed_data.py
```

---

## ✨ Success Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] Can login to application
- [ ] Can see 5 restaurants
- [ ] Can view tables (25 per restaurant)
- [ ] Can create/update/cancel reservations
- [ ] Dinos are happy! 🦕🦖

---

**🎉 Congratulations! Your Dino Reserve is ready to feed hungry dinos! 🦖🍴**

Need help? Check the main README.md or run the test scripts!
