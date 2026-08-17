# Portfolio - Lalu Yashwanth

A minimal, typography-first personal portfolio built with **Django 6**. Content is managed in Django admin (Unfold UI). The public site is a single dark theme, one font, one narrow column - with contact cards and a subtle ambient dot background.

**Focus:** Python · Django · PostgreSQL · REST APIs · Machine Learning · Hyderabad, India

~

## Features

- **Database-driven content** - projects, skills, experience, education, writing
- **Minimal public UI** - typography-first, native system font, no client-side JavaScript, no webfont downloads
- **Case studies** - problem / solution / impact pages with tech stack
- **Writing + RSS** - posts with `/feed/`, plus `sitemap.xml` and `robots.txt`
- **SEO** - meta tags, Open Graph, Person JSON-LD, skip-to-content link
- **Admin** - django-unfold dark/light UI, structured sidebar, status badges
- **Seed command** - `python manage.py seed_portfolio` updates seeded rows in place and never deletes; `--reset` wipes the portfolio tables and rebuilds

~

## Tech stack

| Layer | Tools |
| - | - |
| Backend | Python 3.13 · Django 6 |
| Database | SQLite (dev) · PostgreSQL (prod via `DATABASE_URL` or `DB_ENGINE`) |
| Frontend | Django templates · custom CSS |
| Admin | django-unfold |
| Static | WhiteNoise (`CompressedManifestStaticFilesStorage`) |
| Deploy | Gunicorn · `Procfile` (`migrate` + `collectstatic` on release) |

~

## Quick start

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # optional for local
python manage.py migrate
python manage.py seed_portfolio --reset
python manage.py createsuperuser
python manage.py runserver
```

- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Résumé PDF: served from `static/resume/` (works with `DEBUG=False`)

~

## Project structure

```
portfolio/
├── apps/
│   ├── core/          # Home, writing, settings, hero, feed/sitemap helpers
│   ├── projects/      # Projects + tech stack
│   ├── skills/        # Skill categories
│   ├── experience/    # Work + education
│   └── contact/       # Legacy ContactSubmission model (admin only; no public form)
├── config/            # Settings, URLs, Unfold sidebar
├── static/            # CSS, favicon, OG image, résumé PDF
├── templates/         # Public + admin templates
└── manage.py
```

~

## Environment

See `.env.example`. Important production notes:

- Set a strong `SECRET_KEY` (50+ chars) when `DEBUG=False`
- Prefer `DATABASE_URL` on hosted platforms
- Set `CSRF_TRUSTED_ORIGINS` to your HTTPS origin
- Résumé is in **static**, not media - so it survives production without a media CDN

~

## Tests

```bash
python manage.py test
python manage.py check --deploy   # expect warnings only when DEBUG=True locally
```

~

## License

Personal portfolio - all rights reserved.
