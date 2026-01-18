# Installation Guide - Prerequisites Required

## Current Status
❌ Python is not installed  
❌ Node.js is not installed

## Required Prerequisites

### 1. Python 3.9 or Higher
**Download and Install:**
- Visit: https://www.python.org/downloads/
- Download Python 3.11 or 3.12 (recommended)
- **Important**: During installation, check "Add Python to PATH"
- Verify installation: Open a new terminal and run `python --version`

### 2. Node.js 18 or Higher
**Download and Install:**
- Visit: https://nodejs.org/
- Download the LTS version (recommended)
- Install with default settings
- Verify installation: Open a new terminal and run `node --version` and `npm --version`

### 3. PostgreSQL 12 or Higher
**Download and Install:**
- Visit: https://www.postgresql.org/download/windows/
- Download and install PostgreSQL
- Remember the password you set for the `postgres` user
- Verify installation: PostgreSQL should start automatically as a service

### 4. Redis (Optional - for Celery tasks)
**Download and Install:**
- Visit: https://github.com/microsoftarchive/redis/releases (Windows)
- Or use WSL2 with Redis
- Or use Docker: `docker run -d -p 6379:6379 redis`

## After Installing Prerequisites

Once Python and Node.js are installed, **close and reopen your terminal**, then run:

### Backend Setup
```powershell
# Navigate to backend
cd C:\Users\Admin\Desktop\CRM\kuberns-crm\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example if exists, or create new)
# Set up your database credentials

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### Frontend Setup
```powershell
# Open a NEW terminal window
# Navigate to frontend
cd C:\Users\Admin\Desktop\CRM\kuberns-crm\frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Quick Installation Scripts

After installing prerequisites, you can use these commands:

### Backend (in backend directory):
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend (in frontend directory):
```powershell
npm install
npm run dev
```

## Troubleshooting

### Python not found after installation
- Restart your terminal/IDE
- Check if Python is in PATH: `$env:PATH -split ';' | Select-String python`
- Reinstall Python and ensure "Add to PATH" is checked

### Node.js not found after installation
- Restart your terminal/IDE
- Verify installation: `where.exe node`

### Database connection errors
- Ensure PostgreSQL service is running
- Check database credentials in `.env` file
- Create database: `CREATE DATABASE kuberns_crm;`

### Port already in use
- Backend (8000): Change port: `python manage.py runserver 8001`
- Frontend (3000): Vite will automatically use next available port

## Next Steps After Installation

1. ✅ Install Python 3.9+
2. ✅ Install Node.js 18+
3. ✅ Install PostgreSQL
4. ✅ Set up backend (see commands above)
5. ✅ Set up frontend (see commands above)
6. ✅ Create superuser account
7. ✅ Access application at http://localhost:3000
