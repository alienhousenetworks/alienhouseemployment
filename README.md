# Employee Management System

This is a Django-based Employee Management System for handling tasks, submissions, notifications, projects, and analytics. It uses Celery for background tasks with Redis as the broker, and includes features like user authentication, role-based permissions (Admin, Manager, Employee), email notifications, and Google OAuth integration.

## Prerequisites

- **Python 3.12+**: The project uses Python 3.12.
- **Redis**: Required for Celery task queue (version 7.0+ recommended).
- **Virtual Environment**: Recommended to isolate dependencies.
- **Database**: SQLite is used by default (no additional setup needed).
- **Git**: For cloning the repository (if applicable).
- **Optional**: Gmail account for email notifications and Google Developer Console for OAuth setup.

## Setup Instructions

### 1. Clone the Repository (if not already local)
If the project is in a Git repository:
```
git clone <repository-url>
cd employee_mgmt
```

### 2. Set Up Virtual Environment
The project uses a virtual environment named `alm`. If it's not set up:
```
python3 -m venv alm
source alm/bin/activate  # On macOS/Linux
# On Windows: alm\Scripts\activate
```

### 3. Install Dependencies
The `requirements.txt` file lists the project dependencies. Install them:
```
pip install -r requirements.txt
```

If `requirements.txt` is empty or incomplete, install the core dependencies manually:
```
pip install django==4.2 celery==5.3.4 redis==5.0.1 djangorestframework==3.14.0 django-celery-beat==2.5.0 django-celery-results==2.5.1 pillow==10.1.0 google-auth==2.23.4 google-auth-oauthlib==1.1.0 google-auth-httplib2==0.1.1
```

This includes Django, Celery, Redis, DRF, and Google Auth libraries.

### 4. Configure Environment Variables
Update `employee_mgmt/settings.py` or use environment variables for sensitive data:

- **Email Configuration** (for notifications):
  - Set `EMAIL_HOST_USER` to your Gmail address.
  - Set `EMAIL_HOST_PASSWORD` to your Gmail App Password (enable 2FA and generate an app password in Google Account settings).

- **Google OAuth** (for Google sync/login):
  - Go to [Google Developer Console](https://console.developers.google.com/).
  - Create a project and enable Google+ API or People API.
  - Create OAuth 2.0 credentials (Client ID and Secret).
  - Set `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `GOOGLE_REDIRECT_URI` in settings.py.
  - Authorized redirect URIs: `http://localhost:8000/accounts/google/callback/`.

- **SECRET_KEY**: Change the default Django secret key in `settings.py` for production.

- **Redis**: Defaults to `localhost:6379`. Update `CELERY_BROKER_URL` if using a different host/port.

### 5. Run Database Migrations
Apply migrations to set up the database:
```
cd employee_mgmt  # Ensure you're in the project root
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser
Create an admin account:
```
python manage.py createsuperuser
```
Follow the prompts to set username, email, and password. This user will have 'ADMIN' role.

### 7. Start Redis Server
Redis is required for Celery. Install and start it (on macOS via Homebrew):
```
brew install redis  # If not installed
brew services start redis  # Start as service
# Or manually: redis-server
```

Verify it's running:
```
redis-cli ping  # Should return "PONG"
```

### 8. Start Celery Worker and Beat
In separate terminals (with virtual env activated and in project root):

- **Celery Worker** (handles background tasks like notifications):
```
celery -A employee_mgmt worker -l info
```

- **Celery Beat** (for scheduled tasks, e.g., periodic notifications):
```
celery -A employee_mgmt beat -l info
```

### 9. Collect Static Files (Optional for Development)
```
python manage.py collectstatic --noinput
```

### 10. Run the Django Development Server
```
python manage.py runserver
```
Access the application at `http://localhost:8000/`.

- Admin panel: `http://localhost:8000/admin/` (login with superuser credentials).
- Signup/Login: Available via `/accounts/signup/` or Google OAuth.

### 11. Create Initial Data (Optional)
- Log in as admin and create Managers/Employees via the admin interface or bulk upload features.
- Assign roles: Users have roles like 'ADMIN', 'MANAGER', 'EMPLOYEE' set in their profile.

## Running the Application

- **Frontend**: Navigate to `http://localhost:8000/` for the main dashboard.
- **API Endpoints**: DRF is configured. Access analytics APIs at `/analytics/` (requires authentication).
- **Background Tasks**: Task assignments, notifications, and contract expirations are handled by Celery.
- **Email Testing**: Test email by triggering a password reset or task notification.

## Project Structure
- `employee_mgmt/`: Core Django project (settings, URLs, Celery config).
- `apps/`: Installed apps (accounts, core, organization, tasks, submissions, notifications, projects).
- `analytics/`: DRF-based analytics module.
- `templates/`: HTML templates.
- `static/`: CSS/JS files.

## Commands Summary
| Command | Description |
|---------|-------------|
| `python manage.py makemigrations` | Create migration files for model changes. |
| `python manage.py migrate` | Apply migrations to the database. |
| `python manage.py createsuperuser` | Create admin user. |
| `celery -A employee_mgmt worker -l info` | Start Celery worker. |
| `celery -A employee_mgmt beat -l info` | Start Celery scheduler. |
| `python manage.py runserver` | Start Django server. |
| `python manage.py collectstatic` | Collect static files for production. |

## Troubleshooting
- **ImportError or Missing Modules**: Ensure all dependencies are installed. Run `pip list` to verify.
- **Redis Connection Error**: Check if Redis is running (`redis-cli ping`). Update broker URL if needed.
- **Celery Not Starting**: Ensure `CELERY_BROKER_URL` points to a valid Redis instance. Check logs for errors.
- **Email Not Sending**: Verify Gmail app password and TLS settings. For testing, switch to `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`.
- **Migrations Fail**: Delete `db.sqlite3` and `__pycache__` folders, then re-run migrations (loses data).
- **Google OAuth Issues**: Ensure redirect URI matches exactly in Google Console.
- **Permission Denied**: Roles must be set correctly (e.g., 'MANAGER' for manager features).
- **No Requirements.txt Output**: If empty, install dependencies manually as listed above.

## Production Deployment
- Use PostgreSQL/MySQL instead of SQLite.
- Set `DEBUG = False` and configure `ALLOWED_HOSTS`.
- Use a proper email service (e.g., SendGrid) and secure secret keys.
- Deploy Celery with a supervisor (e.g., Supervisor or systemd).
- Serve static files with Nginx/Apache.
- Use Gunicorn/ uWSGI for the Django app.

For issues, check Django logs or Celery worker output.
