# 🦕 Dino Reserve - Complete Project Structure

## 📁 Full Directory Layout

```
dino-reserve/
├── 📄 README.md                          # Main documentation
├── 📄 QUICKSTART.md                      # Quick setup guide
├── 📄 docker-compose.yml                 # Docker orchestration
├── 📄 Makefile                           # Build automation
├── 📄 .gitignore                         # Git ignore rules
│
├── 📂 backend/                           # FastAPI Backend
│   ├── 📄 main.py                        # Main FastAPI application
│   ├── 📄 config.py                      # Configuration management
│   ├── 📄 logger.py                      # Logging setup
│   ├── 📄 middleware.py                  # Custom middleware
│   ├── 📄 rate_limit.py                  # Rate limiting
│   ├── 📄 monitoring.py                  # Health checks & metrics
│   ├── 📄 requirements.txt               # Python dependencies
│   ├── 📄 seed_data.py                   # Database seeding
│   ├── 📄 manage.py                      # Database management CLI
│   ├── 📄 test_main.py                   # Unit tests
│   ├── 📄 test_api.py                    # API integration tests
│   ├── 📄 Dockerfile                     # Backend Docker image
│   ├── 📄 .env.example                   # Environment variables template
│   ├── 📄 .env                           # Environment variables (gitignored)
│   │
│   ├── 📂 models/                        # Database models
│   │   ├── __init__.py
│   │   ├── restaurant.py
│   │   ├── table.py
│   │   └── reservation.py
│   │
│   ├── 📂 routes/                        # API routes
│   │   ├── __init__.py
│   │   ├── restaurants.py
│   │   ├── tables.py
│   │   └── reservations.py
│   │
│   ├── 📂 schemas/                       # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── restaurant.py
│   │   ├── table.py
│   │   └── reservation.py
│   │
│   ├── 📂 services/                      # Business logic
│   │   ├── __init__.py
│   │   ├── reservation_service.py
│   │   └── notification_service.py
│   │
│   ├── 📂 migrations/                    # Database migrations (Alembic)
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │
│   └── 📂 logs/                          # Application logs
│       └── dinoreserve.log
│
├── 📂 frontend/                          # React Frontend
│   ├── 📄 package.json                   # NPM dependencies
│   ├── 📄 package-lock.json              # Locked dependencies
│   ├── 📄 vite.config.ts                 # Vite configuration
│   ├── 📄 tsconfig.json                  # TypeScript config
│   ├── 📄 tailwind.config.js             # Tailwind CSS config
│   ├── 📄 index.html                     # HTML entry point
│   ├── 📄 Dockerfile                     # Frontend Docker image
│   ├── 📄 nginx.conf                     # Nginx configuration
│   ├── 📄 .env.example                   # Environment variables template
│   ├── 📄 .env                           # Environment variables (gitignored)
│   │
│   ├── 📂 public/                        # Static assets
│   │   ├── favicon.ico
│   │   └── dino-logo.svg
│   │
│   └── 📂 src/                           # Source code
│       ├── 📄 main.tsx                   # Entry point
│       ├── 📄 App.tsx                    # Main app component
│       ├── 📄 index.css                  # Global styles (Tailwind)
│       ├── 📄 globals.css                # Custom global styles
│       │
│       ├── 📂 components/                # React components
│       │   ├── LoginPage.tsx
│       │   ├── RestaurantSelection.tsx
│       │   ├── TableLayout.tsx
│       │   ├── Toast.tsx
│       │   ├── ToastContainer.tsx
│       │   ├── ErrorBoundary.tsx
│       │   ├── LoadingSpinner.tsx
│       │   ├── EmptyState.tsx
│       │   ├── SyncIndicator.tsx
│       │   ├── ConfirmDialog.tsx
│       │   │
│       │   └── 📂 ui/                    # Shadcn UI components
│       │       ├── button.tsx
│       │       ├── card.tsx
│       │       ├── dialog.tsx
│       │       ├── input.tsx
│       │       ├── label.tsx
│       │       └── alert-dialog.tsx
│       │
│       ├── 📂 hooks/                     # Custom React hooks
│       │   ├── index.ts
│       │   ├── useRestaurants.ts
│       │   ├── useTables.ts
│       │   ├── useReservation.ts
│       │   ├── useInterval.ts
│       │   ├── useAutoRefresh.ts
│       │   ├── useLocalStorage.ts
│       │   ├── useDebounce.ts
│       │   └── useToast.ts
│       │
│       ├── 📂 services/                  # API service layer
│       │   └── api.ts
│       │
│       ├── 📂 types/                     # TypeScript types
│       │   ├── index.ts
│       │   ├── restaurant.ts
│       │   ├── table.ts
│       │   └── reservation.ts
│       │
│       ├── 📂 utils/                     # Utility functions
│       │   ├── date.ts
│       │   ├── format.ts
│       │   └── constants.ts
│       │
│       └── 📂 assets/                    # Images, icons, etc.
│           └── dino-icons/
│
├── 📂 .github/                           # GitHub configuration
│   └── 📂 workflows/                     # CI/CD pipelines
│       ├── ci.yml                        # Main CI/CD workflow
│       └── deploy.yml                    # Manual deployment
│
├── 📂 scripts/                           # Utility scripts
│   ├── deploy.sh                         # Deployment script
│   ├── backup.sh                         # Database backup
│   ├── restore.sh                        # Database restore
│   └── setup.sh                          # Initial setup
│
├── 📂 docs/                              # Additional documentation
│   ├── API.md                            # API documentation
│   ├── DATABASE.md                       # Database schema
│   ├── DEPLOYMENT.md                     # Deployment guide
│   └── TROUBLESHOOTING.md                # Common issues
│
└── 📂 backups/                           # Database backups
    └── dinoreserve_YYYYMMDD_HHMMSS.sql
```

## 🔗 How Everything Connects

### 1. **User Flow**

```
User Browser
    ↓
Frontend (React on port 5173/3000)
    ↓ HTTP Requests
API Service Layer (services/api.ts)
    ↓ REST API calls
Backend (FastAPI on port 8000)
    ↓ SQL Queries
Database (PostgreSQL on port 5432)
```

### 2. **Frontend Architecture**

```
App.tsx (Router)
    ├── LoginPage
    ├── RestaurantSelection
    │       ↓ (uses useRestaurants hook)
    │       ↓ (calls api.restaurants.getAll())
    └── TableLayout
            ↓ (uses useTables, useReservation hooks)
            ↓ (calls api.restaurants.getTables())
            ↓ (calls api.reservations.create/update/cancel())
```

### 3. **Backend Architecture**

```
main.py (FastAPI App)
    ├── CORS Middleware
    ├── Logging Middleware
    ├── Rate Limiting
    │
    ├── Routes
    │   ├── GET  /restaurants
    │   ├── GET  /restaurants/{id}
    │   ├── GET  /restaurants/{id}/tables
    │   ├── POST /reservations
    │   ├── PUT  /reservations/{id}
    │   └── DELETE /reservations/{id}
    │
    ├── Database Models (SQLAlchemy)
    │   ├── Restaurant
    │   ├── Table
    │   └── Reservation
    │
    └── Database Session (PostgreSQL)
```

### 4. **Data Flow Example: Creating a Reservation**

```
1. User clicks table in TableLayout
   ↓
2. Opens reservation form (Dialog)
   ↓
3. User fills form and clicks "Feed Dino"
   ↓
4. useReservation.createReservation() called
   ↓
5. api.reservations.create() sends POST request
   ↓
6. FastAPI receives request at POST /reservations
   ↓
7. Validates data (Pydantic)
   ↓
8. Checks table availability (SQLAlchemy)
   ↓
9. Creates reservation in database
   ↓
10. Returns reservation data
    ↓
11. Frontend updates table status
    ↓
12. Shows success toast notification
```

## 🚀 Quick Commands Reference

### Development

```bash
# Start everything
make dev                    # Both frontend & backend

# Individual services
make dev-backend           # Backend only (port 8000)
make dev-frontend          # Frontend only (port 5173)

# With Docker
make docker-up             # All services with Docker
make docker-logs           # View logs
```

### Database

```bash
# Setup
make db-create             # Create database
make db-seed               # Add sample data

# Management
python manage.py stats     # Show statistics
python manage.py restaurants    # List restaurants
python manage.py tables 1       # Show tables for restaurant 1
python manage.py upcoming       # Show upcoming reservations
```

### Testing

```bash
# Backend tests
cd backend
pytest test_main.py -v
python test_api.py

# Frontend
cd frontend
npm test
npm run lint
```

### Deployment

```bash
# Build
make build                 # Build frontend

# Deploy
./deploy.sh staging        # Deploy to staging
./deploy.sh production     # Deploy to production
make deploy-production     # With confirmation
```

## 🔧 Configuration Files

### Environment Variables

**Backend (.env):**
```env
DATABASE_URL=postgresql://user:pass@localhost/dinoreserve
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:5173
```

**Frontend (.env):**
```env
VITE_API_URL=http://localhost:8000
```

### Key Configuration Points

1. **Database Connection**: `backend/main.py` line 10
2. **CORS Settings**: `backend/main.py` line 45
3. **API Base URL**: `frontend/src/services/api.ts` line 3
4. **Port Configuration**: 
   - Backend: `backend/main.py` line 450
   - Frontend: `frontend/vite.config.ts` line 9

## 📊 Database Schema Summary

```sql
-- restaurants table
id, name, location, dino_type

-- tables table
id, restaurant_id (FK), table_number, capacity

-- reservations table
id, table_id (FK), customer_name, phone, 
party_size, reservation_time, status, created_at
```

## 🎨 Frontend Component Hierarchy

```
App
├── ErrorBoundary
    ├── ToastContainer
    └── Current Page
        ├── LoginPage
        │   ├── Card
        │   ├── Input (username, password)
        │   └── Button (submit)
        │
        ├── RestaurantSelection
        │   ├── Card (for each restaurant)
        │   │   ├── Dino Icon (emoji)
        │   │   ├── Restaurant Name
        │   │   └── Button (Manage Tables)
        │   └── SyncIndicator
        │
        └── TableLayout
            ├── Button (Back)
            ├── Card (Restaurant Info)
            ├── Grid of Table Cards
            │   └── Card (for each table)
            │       ├── Dino Status Icon
            │       ├── Table Number
            │       └── Capacity
            ├── Dialog (Reservation Form)
            │   ├── Input (customer details)
            │   └── Buttons (Save/Cancel)
            └── SyncIndicator
```

## 🔌 API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/restaurants` | List all restaurants |
| GET | `/restaurants/{id}` | Get restaurant details |
| GET | `/restaurants/{id}/tables` | Get tables with status |
| POST | `/reservations` | Create reservation |
| PUT | `/reservations/{id}` | Update reservation |
| DELETE | `/reservations/{id}` | Cancel reservation |
| GET | `/reservations` | List all reservations |
| GET | `/health` | System health check |
| GET | `/metrics` | System metrics |

## 🎯 Key Features Implementation

### 1. Real-time Table Status
- Tables automatically show reserved/available based on active reservations
- Checks reservation_time >= current time
- Updates on every page load

### 2. Auto-refresh
- Uses `useAutoRefresh` hook
- Refreshes table data every 30 seconds
- Can be disabled/enabled via prop

### 3. Error Handling
- ErrorBoundary catches React errors
- Toast notifications for user feedback
- API errors shown with retry option

### 4. State Management
- React useState for component state
- Custom hooks for data fetching
- No external state library needed

## 📦 Dependency Summary

### Backend
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM
- **Pydantic**: Data validation
- **PostgreSQL**: Database
- **Uvicorn**: ASGI server

### Frontend
- **React**: UI library
- **TypeScript**: Type safety
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Radix UI**: Accessible components

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**This completes the full project structure! Each file connects to build a complete, production-ready restaurant reservation system.** 🦕🦖
