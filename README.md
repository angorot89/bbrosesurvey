# BBrose — Employee Insight Platform

A full-stack internal web application for collecting employee information and work insights.

## Quick Start

```bash
cd bbrose_project
bash run.sh
```

Or manually:

```bash
pip install django pillow qrcode reportlab openpyxl
python manage.py migrate
python manage.py runserver
```

## Railway Deploy

This project now includes:
- `gunicorn` in `requirements.txt`
- `whitenoise` for static files
- a `Procfile` with:

```bash
python manage.py collectstatic --noinput && python manage.py migrate --noinput && gunicorn bbrose_project.wsgi --log-file -
```

If Railway still uses a custom start command, make sure it includes `gunicorn` and matches the command above.

## Access

| URL | Purpose |
|-----|---------|
| `http://127.0.0.1:8000/` | Main Application |
| `http://127.0.0.1:8000/admin/` | Django Admin Panel |

**Admin Credentials:** `amine` / `aminehd2004`

## Features

### Frontend
- Animated landing page with BBrose logo
- 3-language support (English, Chinese, Arabic) with full RTL
- Typing animation intro from the AI Developer
- One-question-per-screen questionnaire with progress bar
- Camera capture or file upload for photo
- Auto-generated Employee ID Card with QR code
- Smooth CSS transitions throughout

### Backend (Django + SQLite3)
- Employee model with personal info + JSON work responses
- Auto-generated unique Employee ID (BBR-XXXXXXXX)
- QR code generation (links to portfolio)
- ID card image generation with Pillow
- Full Django Admin with search, filter, and export (CSV/Excel)

### Questionnaire Phases
1. **Personal Info** — Name, phone, email, role, photo
2. **Role & Responsibilities** — Job title, daily tasks, tenure
3. **Workflow & Efficiency** — Typical day, time sinks, automation opportunities
4. **Pain Points** — Challenges, slowdowns, recurring problems
5. **Communication** — Team channels, info flow, improvements
6. **Tools & Technology** — Current tools, wishlist, tech comfort
7. **Ideas & Suggestions** — Changes, improvements, open comments

## Project Structure

```
bbrose_project/
├── manage.py
├── run.sh                    # One-command startup
├── db.sqlite3                # Database (auto-created)
├── media/                    # Uploaded photos, QR codes, ID cards
├── bbrose_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── questionnaire/
    ├── models.py             # Employee model
    ├── views.py              # Submit API + ID card generation
    ├── admin.py              # Admin panel config + export
    ├── urls.py
    ├── templates/
    │   └── questionnaire/
    │       └── index.html    # Single-page frontend
    └── static/
        └── questionnaire/
            └── img/
                └── logo.png  # BBrose logo
```

## API Endpoint

**POST** `/api/submit/` — Submit questionnaire  
- Form data with `data` (JSON string) and optional `photo` (file)
- Returns employee ID, ID card URL, QR code URL

## Tech Stack
- Python 3 / Django 6
- SQLite3
- Pillow (image generation)
- qrcode (QR generation)
- openpyxl (Excel export)
- Vanilla HTML/CSS/JS frontend
