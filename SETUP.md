# Kuberns CRM - Setup Guide

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 12+
- Redis (for Celery tasks)

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Create and activate virtual environment**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
Create a `.env` file in the `backend` directory:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=kuberns_crm
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

5. **Create database**:
```sql
CREATE DATABASE kuberns_crm;
```

6. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create superuser**:
```bash
python manage.py createsuperuser
```

8. **Start development server**:
```bash
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Start development server**:
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Creating Initial Users

After creating a superuser, you can create users through the Django admin at `http://localhost:8000/admin` or via the API.

### User Roles:
- **sales_executive**: Can view and manage only assigned leads
- **sales_manager**: Can view all leads, assign leads, review activities
- **admin**: Full access including user management

## Testing the System

1. **Login**: Use the superuser credentials or create a test user
2. **Create a Lead**: Navigate to Leads → New Lead
3. **Log a Visit**: Navigate to Tasks → Log Visit
4. **View Dashboard**: Check the dashboard for statistics

## Common Issues

### Database Connection Error
- Ensure PostgreSQL is running
- Check database credentials in `.env` file
- Verify database exists: `CREATE DATABASE kuberns_crm;`

### CORS Errors
- Ensure backend CORS settings include `http://localhost:3000`
- Check that frontend proxy is configured in `vite.config.js`

### Authentication Issues
- Clear browser localStorage
- Check that token is being saved after login
- Verify API endpoints are correct

## Next Steps

1. Configure email settings for notifications
2. Set up Celery workers for background tasks
3. Configure production settings
4. Set up SSL certificates for production
5. Configure backup strategy
