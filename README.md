# JobTrack ΓÇö Job Application Tracking System

## Overview

JobTrack is a web-based application developed using Python, Django, and PostgreSQL to help students and job seekers organize and manage their job applications.

The system allows users to track applications submitted to different companies, update their application status, and monitor their job search progress through an interactive dashboard.

The application also provides REST APIs for managing job applications and uses Django's authentication system to secure user data.

## Technologies Used

- **Backend:** Python, Django, Django REST Framework
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Data Visualization:** Chart.js
- **Version Control:** Git, GitHub
- **Authentication:** Django Session Authentication

## Features

- User registration, login, and logout
- Create, view, update, and delete job applications
- Track application status
- Search applications by company name or job role
- Filter applications by status
- Dashboard with application statistics and charts
- REST APIs for application management
- User-specific data access and authentication
- Automated tests for application functionality and API permissions

## Project Structure

```text
job_application_tracker/
Γöé
Γö£ΓöÇΓöÇ config/                 # Django project configuration
Γö£ΓöÇΓöÇ tracker/                # Application models, views and APIs
Γö£ΓöÇΓöÇ templates/              # HTML templates
Γö£ΓöÇΓöÇ manage.py               # Django management script
Γö£ΓöÇΓöÇ requirements.txt        # Python dependencies
Γö£ΓöÇΓöÇ .env.example            # Environment variable template
ΓööΓöÇΓöÇ README.md               # Project documentation
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/rishipatil35/job-application-tracker.git
cd job-application-tracker
```

### 2. Create a Virtual Environment

```powershell
py -m venv .venv
```

### 3. Install Dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database named `jobtracker`.

Copy the environment configuration:

```powershell
Copy-Item .env.example .env
```

Update your `.env` file:

```env
DJANGO_SECRET_KEY=your-generated-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=jobtracker
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
DB_HOST=localhost
DB_PORT=5432

USE_SQLITE=False
```

Replace the example secret key and password with your own values. Do not commit the `.env` file to GitHub.

### 5. Apply Database Migrations

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

### 6. Run the Application

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Open the application:

http://127.0.0.1:8000/

Register a new account to start managing job applications.

## REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/applications/` | Retrieve applications |
| POST | `/api/applications/` | Create an application |
| GET | `/api/applications/{id}/` | Retrieve application details |
| PATCH | `/api/applications/{id}/` | Update an application |
| DELETE | `/api/applications/{id}/` | Delete an application |
| GET | `/api/applications/?q=python&status=applied` | Search and filter |
| GET | `/api/applications/stats/` | Retrieve application statistics |

The APIs use Django session authentication. Users can access and modify only their own application records.

## Testing

Run the automated tests using:

```powershell
.\.venv\Scripts\python.exe manage.py test
```

The test suite covers authentication, CRUD operations, API access permissions, data isolation, filtering, and statistics.

## Application Screenshots

Add screenshots of the running application here.

### Dashboard

*Dashboard screenshot*

### Job Application Management

*Application list screenshot*

### REST API

*Django REST Framework API screenshot*

## Key Technical Concepts

This project demonstrates:

- Django's Model-View-Template (MVT) architecture
- Relational database integration using PostgreSQL
- REST API development with Django REST Framework
- CRUD operations and data validation
- User authentication and authorization
- Database querying, searching, and filtering
- Backend testing and API security

## Future Improvements

- Email notifications for upcoming interviews
- Interview scheduling and reminders
- CSV export for application records
- Additional dashboard analytics
- Deployment to a cloud hosting platform
