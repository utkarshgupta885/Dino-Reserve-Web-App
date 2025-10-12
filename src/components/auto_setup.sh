#!/bin/bash
# Automated Setup Script for Dino Reserve
# This script sets up the entire application from scratch

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
DB_NAME="dinoreserve"
DB_USER="dinouser"
DB_PASS="dinopass123"
PYTHON_VERSION="3.9"
NODE_VERSION="18"

echo -e "${BLUE}"
cat << "EOF"
    ____  _                 ____                             
   / __ \(_)___  ____      / __ \___  ________  ______   _____ 
  / / / / / __ \/ __ \    / /_/ / _ \/ ___/ _ \/ ___/ | / / _ \
 / /_/ / / / / / /_/ /   / _, _/  __(__  )  __/ /   | |/ /  __/
/_____/_/_/ /_/\____/   /_/ |_|\___/____/\___/_/    |___/\___/ 
                                                                
EOF
echo -e "${NC}"
echo "🦕 Automated Setup Script 🦖"
echo "======================================"
echo ""

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "${BLUE}→${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check system requirements
check_requirements() {
    print_info "Checking system requirements..."
    
    local missing_requirements=0
    
    # Check Python
    if command_exists python3; then
        PYTHON_CMD=python3
        print_status "Python found: $(python3 --version)"
    else
        print_error "Python 3 is not installed"
        missing_requirements=1
    fi
    
    # Check Node.js
    if command_exists node; then
        print_status "Node.js found: $(node --version)"
    else
        print_error "Node.js is not installed"
        missing_requirements=1
    fi
    
    # Check npm
    if command_exists npm; then
        print_status "npm found: $(npm --version)"
    else
        print_error "npm is not installed"
        missing_requirements=1
    fi
    
    # Check PostgreSQL
    if command_exists psql; then
        print_status "PostgreSQL found: $(psql --version)"
    else
        print_warning "PostgreSQL is not installed (you can use SQLite instead)"
    fi
    
    # Check git
    if command_exists git; then
        print_status "Git found: $(git --version)"
    else
        print_error "Git is not installed"
        missing_requirements=1
    fi
    
    if [ $missing_requirements -eq 1 ]; then
        echo ""
        print_error "Some requirements are missing. Please install them first."
        echo ""
        echo "Installation commands:"
        echo "  macOS:   brew install python node postgresql"
        echo "  Ubuntu:  sudo apt install python3 python3-pip nodejs npm postgresql"
        echo "  CentOS:  sudo yum install python3 nodejs postgresql-server"
        exit 1
    fi
    
    print_status "All requirements met!"
    echo ""
}

# Setup PostgreSQL database
setup_database() {
    print_info "Setting up PostgreSQL database..."
    
    if ! command_exists psql; then
        print_warning "PostgreSQL not found. Skipping database setup."
        print_info "The application will use SQLite instead."
        return 0
    fi
    
    # Check if database exists
    if psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
        print_warning "Database '$DB_NAME' already exists"
        read -p "Do you want to recreate it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            dropdb $DB_NAME 2>/dev/null || true
            print_status "Dropped existing database"
        else
            print_info "Using existing database"
            return 0
        fi
    fi
    
    # Create database
    createdb $DB_NAME
    print_status "Created database: $DB_NAME"
    
    # Create user
    psql -d $DB_NAME -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';" 2>/dev/null || true
    psql -d $DB_NAME -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
    psql -d $DB_NAME -c "GRANT ALL ON SCHEMA public TO $DB_USER;"
    print_status "Created database user: $DB_USER"
    
    # Test connection
    if psql -U $DB_USER -d $DB_NAME -c "SELECT 'Database ready! 🦕';" >/dev/null 2>&1; then
        print_status "Database connection successful"
    else
        print_warning "Could not connect to database. You may need to configure pg_hba.conf"
    fi
    
    echo ""
}

# Setup backend
setup_backend() {
    print_info "Setting up backend..."
    
    cd backend
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        $PYTHON_CMD -m venv venv
        print_status "Created virtual environment"
    else
        print_info "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip --quiet
    print_status "Upgraded pip"
    
    # Install dependencies
    print_info "Installing backend dependencies..."
    pip install -r requirements.txt --quiet
    print_status "Backend dependencies installed"
    
    # Create .env file
    if [ ! -f ".env" ]; then
        cat > .env << EOF
DATABASE_URL=postgresql://$DB_USER:$DB_PASS@localhost:5432/$DB_NAME
SECRET_KEY=$(openssl rand -hex 32)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
ENVIRONMENT=development
DEBUG=True
EOF
        print_status "Created backend .env file"
    else
        print_info "Backend .env file already exists"
    fi
    
    # Seed database
    print_info "Seeding database with sample data..."
    python seed_data.py
    print_status "Database seeded"
    
    cd ..
    echo ""
}

# Setup frontend
setup_frontend() {
    print_info "Setting up frontend..."
    
    cd frontend
    
    # Install dependencies
    print_info "Installing frontend dependencies (this may take a few minutes)..."
    npm install
    print_status "Frontend dependencies installed"
    
    # Create .env file
    if [ ! -f ".env" ]; then
        cat > .env << EOF
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Dino Reserve
EOF
        print_status "Created frontend .env file"
    else
        print_info "Frontend .env file already exists"
    fi
    
    cd ..
    echo ""
}

# Create utility scripts
create_scripts() {
    print_info "Creating utility scripts..."
    
    # Start script
    cat > start.sh << 'EOF'
#!/bin/bash
echo "🦕 Starting Dino Reserve..."

# Start backend
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Start frontend
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ Services started!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "📍 URLs:"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
EOF
    chmod +x start.sh
    print_status "Created start.sh"
    
    # Stop script
    cat > stop.sh << 'EOF'
#!/bin/bash
echo "🛑 Stopping Dino Reserve..."

# Kill processes
pkill -f "python main.py"
pkill -f "vite"

echo "✅ Services stopped"
EOF
    chmod +x stop.sh
    print_status "Created stop.sh"
    
    echo ""
}

# Test installation
test_installation() {
    print_info "Testing installation..."
    
    # Test backend
    cd backend
    source venv/bin/activate
    
    print_info "Starting backend temporarily..."
    python main.py > /dev/null 2>&1 &
    BACKEND_PID=$!
    
    # Wait for backend to start
    sleep 5
    
    if curl -f http://localhost:8000/ > /dev/null 2>&1; then
        print_status "Backend is responding"
    else
        print_error "Backend is not responding"
    fi
    
    # Stop backend
    kill $BACKEND_PID 2>/dev/null || true
    
    cd ..
    
    echo ""
}

# Print success message
print_success() {
    echo ""
    echo -e "${GREEN}"
    cat << "EOF"
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║   🎉  Installation Complete! 🎉                      ║
    ║                                                       ║
    ║   Your Dino Reserve is ready to serve hungry dinos!  ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    echo ""
    echo "📚 Next Steps:"
    echo ""
    echo "  1. Start the application:"
    echo -e "     ${BLUE}./start.sh${NC}"
    echo ""
    echo "  2. Open your browser:"
    echo -e "     ${BLUE}http://localhost:5173${NC}"
    echo ""
    echo "  3. Login with any credentials (demo mode)"
    echo ""
    echo "  4. Explore the API documentation:"
    echo -e "     ${BLUE}http://localhost:8000/docs${NC}"
    echo ""
    echo "📖 Useful Commands:"
    echo ""
    echo "  Stop services:      ./stop.sh"
    echo "  View database:      cd backend && python manage.py stats"
    echo "  Run tests:          cd backend && pytest test_main.py"
    echo "  View logs:          cd backend/logs && tail -f dinoreserve.log"
    echo ""
    echo "📄 Documentation:"
    echo "  - README.md          - Main documentation"
    echo "  - QUICKSTART.md      - Quick start guide"
    echo "  - COMPLETE_PROJECT_STRUCTURE.md - Full project overview"
    echo ""
    echo "🦕 Happy Dino Management! 🦖"
    echo ""
}

# Main installation flow
main() {
    clear
    
    echo "This script will install and configure Dino Reserve."
    echo "The installation process will:"
    echo "  • Check system requirements"
    echo "  • Setup PostgreSQL database"
    echo "  • Install backend dependencies"
    echo "  • Install frontend dependencies"
    echo "  • Create configuration files"
    echo "  • Seed sample data"
    echo ""
    read -p "Do you want to continue? (Y/n): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]] && [[ ! -z $REPLY ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    
    echo ""
    echo "🚀 Starting installation..."
    echo ""
    
    check_requirements
    setup_database
    setup_backend
    setup_frontend
    create_scripts
    test_installation
    
    print_success
}

# Run main function
main
