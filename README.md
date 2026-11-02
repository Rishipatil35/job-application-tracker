# JobTrack — Job Application Tracking System

A resume-friendly **Python Django backend project** with a Bootstrap dashboard and REST API. Build it, run it, read the code and practice explaining your decisions before adding it to your resume.

## Features
- Register, login, logout using Django's built-in authentication
- Create, view, edit, and delete only **your own** job applications
- Search company/role and filter by status
- Dashboard totals and a status chart (Chart.js via CDN)
- REST API with Django REST Framework, session authentication and pagination
- Tests for authentication, API CRUD, isolation, filtering and statistics
- PostgreSQL by default, optional SQLite for a quick local trial

## Folder overview
- `tracker/models.py` — database table structure
- `tracker/views.py` — HTML pages and dashboard numbers
- `tracker/forms.py` — validated HTML forms
- `tracker/api.py` — JSON API routes, filtering and user isolation
- `tracker/serializers.py` — API input/output fields and validation
- `tracker/tests.py`, `tracker/tests_api.py` — automated tests
- `templates/` — Bootstrap pages
- `config/` — Django configuration and routes

## Run on Windows (PowerShell in VS Code)

Install Python 3.10+ and PostgreSQL (if using the default database). Create a PostgreSQL database called `jobtracker` in pgAdmin or `psql`.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env`: set a long random `DJANGO_SECRET_KEY`, configure your PostgreSQL user/password. For a trial without PostgreSQL, set `USE_SQLITE=True` in `.env` (SQLite is only an optional local convenience; the portfolio stack uses PostgreSQL).

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Open **http://127.0.0.1:8000/register/** and create an account. Dashboard is `/`; API endpoints are listed below.

### Test

```powershell
.\.venv\Scripts\python.exe manage.py test
```

If using PostgreSQL, the test runner typically needs permission to create a test database. For a quick SQLite test, set `USE_SQLITE=True` in `.env`.

## API routes (session authentication)

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/applications/` | List my applications (paginated) |
| POST | `/api/applications/` | Add an application |
| GET | `/api/applications/{id}/` | Get one application |
| PATCH | `/api/applications/{id}/` | Update fields |
| DELETE | `/api/applications/{id}/` | Delete application |
| GET | `/api/applications/?q=python&status=applied` | Search/filter |
| GET | `/api/applications/stats/` | My status totals |

**How to try the API:** Sign in using `/login/` and open `/api/applications/` in the *same browser*. Django REST Framework's browsable API allows you to submit API requests. Session-based write requests require CSRF protection. The API does **not** use public API keys or JWT tokens.

Example response for `GET /api/applications/stats/`:

```json
{"total": 4, "applied": 2, "interviews": 1, "offers": 1, "rejected": 0}
```

## Why user data stays private

`JobApplication` links to Django's User using `ForeignKey`. Both HTML and API queries always filter by `request.user`. An attempt to read/edit another user's ID returns 404. Authentication is required for all application endpoints. HTML POST forms and session-based API writes use CSRF checks.

## Production/deployment checklist

1. Use a managed PostgreSQL database and set the `DB_*` variables.
2. Create a unique Django secret, set `DJANGO_DEBUG=False` and `DJANGO_ALLOWED_HOSTS=your-domain.example`.
3. For an HTTPS frontend or host, set `CSRF_TRUSTED_ORIGINS=https://your-domain.example`. Set `TRUST_PROXY_SSL=True` **only behind a trusted HTTPS proxy** that sets `X-Forwarded-Proto` correctly.
4. Run `python manage.py migrate` and `python manage.py collectstatic --noinput`.
5. Run via a WSGI server such as `gunicorn config.wsgi:application` on Linux hosting; HTTPS termination must be configured on the hosting platform.
6. Run `python manage.py check --deploy` and address all security warnings; configure secure host/HTTPS redirects on your platform.
7. Do not commit `.env` or actual applicant information to GitHub. Chart.js and Bootstrap load from external CDNs and need an internet connection.

**Note:** The project is built for learning and portfolio demonstrations. No live deployment is included; test in your environment before claiming it is production-ready.

## What to say in an interview

> I created JobTrack using Python, Django and PostgreSQL. Users can track applications using forms or REST endpoints. I used Django ORM for queries and linked every application to its user, so users can access only their own data. I added filtering, a status dashboard and automated tests for permission checks.

Be ready to explain: models vs serializers, GET/POST/PATCH/DELETE, session authentication and CSRF, PostgreSQL relationships, queryset filtering, API pagination and why ownership checks matter.

## Resume bullet example (only after running and testing)

**JobTrack — Django, PostgreSQL, DRF, Bootstrap** — Built a job-application tracker with authenticated CRUD APIs, user-scoped data access, search/filtering and a status dashboard; wrote automated tests for API permissions and data isolation.
