# Kuberns CRM - On-Field Sales Management System

A custom CRM built specifically for Kuberns' on-field sales team, designed for IT agencies, partnerships, and long sales cycles.

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Frontend**: React 18 + Vite + Tailwind CSS
- **Database**: PostgreSQL
- **Task Queue**: Celery + Redis (for reminders)

## Project Structure

```
kuberns-crm/
├── backend/          # Django backend
│   ├── config/       # Django settings
│   ├── users/        # User management app
│   ├── leads/        # Lead management app
│   ├── tasks/        # Task & activity management app
│   └── core/         # Core utilities (audit logs, activity tracking)
└── frontend/         # React frontend
    └── src/
        ├── components/
        ├── pages/
        ├── contexts/
        └── services/
```

## Setup Instructions

### Backend Setup

1. **Create virtual environment**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure database**:
   - Create a PostgreSQL database named `kuberns_crm`
   - Update database credentials in `config/settings.py` or use environment variables

4. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser**:
```bash
python manage.py createsuperuser
```

6. **Run development server**:
```bash
python manage.py runserver
```

### Frontend Setup

1. **Install dependencies**:
```bash
cd frontend
npm install
```

2. **Run development server**:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000` and will proxy API requests to `http://localhost:8000`.

## Environment Variables

Create a `.env` file in the `backend` directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=kuberns_crm
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Features

### User Roles
- **Sales Executive**: Can view and manage only assigned leads
- **Sales Manager**: Can view all leads, assign leads, review activities
- **Admin**: Full access including user management

### Core Modules
1. **Lead Management**: Complete lead lifecycle tracking
2. **Task & Activity Management**: Visit, call, meeting, WhatsApp tracking
3. **Visit Flow**: Detailed on-field visit forms with meeting outcomes
4. **Follow-up System**: Automatic next action creation
5. **Activity Tracking**: Daily activity logs for sales executives
6. **Audit Logging**: Complete change history for leads and tasks
7. **Dashboards**: Role-based dashboards with key metrics

## API Endpoints

### Authentication
- `POST /api/auth/users/login/` - User login
- `GET /api/auth/users/me/` - Get current user

### Leads
- `GET /api/leads/leads/` - List leads
- `POST /api/leads/leads/` - Create lead
- `GET /api/leads/leads/{id}/` - Get lead details
- `PUT /api/leads/leads/{id}/` - Update lead
- `GET /api/leads/leads/stats/` - Get lead statistics
- `GET /api/leads/leads/at_risk/` - Get at-risk leads

### Tasks
- `GET /api/tasks/tasks/` - List tasks
- `POST /api/tasks/tasks/` - Create task
- `POST /api/tasks/tasks/{id}/complete/` - Complete task
- `GET /api/tasks/tasks/calendar/` - Get calendar view

### Visits
- `POST /api/tasks/visits/` - Log visit

## Development

### Running Tests
```bash
cd backend
python manage.py test
```

### Code Formatting
```bash
# Backend
black .
isort .

# Frontend
npm run format
```

## Production Deployment

1. Set `DEBUG=False` in settings
2. Configure proper database credentials
3. Set up static file serving
4. Configure CORS for production domain
5. Set up Celery workers for background tasks
6. Configure email settings for notifications

## License

Proprietary - Kuberns Internal Use Only
