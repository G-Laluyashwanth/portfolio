# Portfolio — Lalu Yashwanth

A minimal, typography-first personal portfolio built with **Django 5**. All content is managed through the Django admin — projects, skills, experience, and contact submissions are stored in the database, not hardcoded. The front-end is intentionally simple: a single dark theme, one font, one narrow column, and no animations or gradients. The words do the work.

**Live tech showcase:** Python · Django · PostgreSQL · REST APIs · Machine Learning · Hyderabad, India

---

## ✨ Features

- **Dynamic content** — every section (intro, projects, experience, education) is database-driven and editable through Django admin
- **Minimal UI** — single dark theme, one font (Inter), one narrow column, hairline borders, no gradients/cards/animation
- **Fast & lightweight** — no client-side JavaScript, no icon libraries, one small stylesheet
- **Responsive** — fluid single-column layout that reads well on any screen
- **Accessible** — semantic HTML, `prefers-reduced-motion` support, keyboard-friendly
- **SEO-ready** — meta tags, Open Graph, canonical URLs, semantic structure
- **Contact form** — SMTP delivery with HTML + plain text emails, spam honeypot, submission tracking in admin
- **Project case studies** — clean detail pages with overview, problem, solution, impact, features, gallery
- **Social links** — Twitter/X, LinkedIn, GitHub, and email in the footer of every page
- **Seed command** — populate the entire site with one command

---

## 🛠 Tech Stack

| Layer | Tools |
|---|---|
| **Backend** | Python 3.11+, Django 5 |
| **Database** | SQLite (dev) · PostgreSQL (prod) |
| **Frontend** | Django Templates, custom CSS (no framework, no JavaScript) |
| **Email** | Django SMTP backend |
| **Static files** | WhiteNoise |
| **Deployment** | Gunicorn · Heroku / Railway / Render / VPS |

---

## 📁 Project Structure

```
portfolio/
├── config/                  # Django project settings
│   ├── settings.py          # Env-driven, SQLite default, PostgreSQL ready
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/                # Home, SiteSettings, HeroSection, seed command
│   │   └── management/commands/seed_portfolio.py
│   ├── projects/            # Project, TechStack, ProjectFeature, ProjectImage
│   ├── skills/              # SkillCategory, Skill
│   ├── experience/          # Experience, Education
│   └── contact/             # ContactSubmission, contact form, SMTP email
├── templates/
│   ├── base.html            # Shell: name, nav, footer with social links
│   ├── core/home.html       # Single-page home (intro, work, experience, education)
│   ├── projects/detail.html # Case-study detail page
│   └── contact/             # Contact page + email templates
├── static/
│   └── css/style.css        # Minimal dark design system (~250 lines, no JS)
├── media/                   # User-uploaded project images
├── manage.py
├── requirements.txt
├── .env.example
├── Procfile                 # Deployment
└── .gitignore
```

---

## 🚀 Quick Start

### 1. Clone and set up environment

```bash
cd portfolio

# Virtual environment
python -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate            # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and set at minimum:
```env
SECRET_KEY=your-long-random-string
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Email (for contact form)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password   # Gmail App Password (not regular password)
DEFAULT_FROM_EMAIL=Portfolio <your-email@gmail.com>
CONTACT_RECIPIENT=laluyashwanth.dev@gmail.com
```

> **Gmail tip:** Use an App Password from <https://myaccount.google.com/apppasswords> — your regular Gmail password won't work with SMTP.
>
> **Local testing without SMTP:** Leave `EMAIL_BACKEND` blank or set it to `django.core.mail.backends.console.EmailBackend` — emails will print to your terminal instead of sending.

### 3. Database + admin user

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Seed the portfolio with real content

```bash
python manage.py seed_portfolio
```

This populates:
- Site settings (name, email, social links, SEO meta)
- Hero section with typing phrases
- 5 featured projects (ISO Audit Document Generator, CQAL Client Management System, Concept QA Labs Website, PQE Platform, Jira Automation)
- 6 skill categories with 50+ skills (Backend, Database, Frontend, ML/Data Science, Big Data, Tools)
- 2 experience entries (Concept QA Labs, Nvest Solutions internship)
- 1 placeholder education entry (edit via admin)

To re-seed from scratch:
```bash
python manage.py seed_portfolio --reset
```

### 5. Run the server

```bash
python manage.py runserver
```

- Site: <http://127.0.0.1:8000/>
- Admin: <http://127.0.0.1:8000/admin/>

---

## ✏️ Editing Content

All content lives in the Django admin — no code changes needed.

| What you want to edit | Admin path |
|---|---|
| Site name, email, social links, SEO meta | `Core → Site Settings` |
| Hero headline, typing phrases, CTAs | `Core → Hero Section` |
| Add/edit projects | `Projects → Projects` |
| Project tech tags | `Projects → Tech Stack Items` |
| Skills (grouped) | `Skills → Skill Categories` |
| Work experience | `Experience → Work Experience` |
| Education | `Experience → Education` |
| View contact submissions | `Contact → Contact Submissions` |

---

## 🌐 Switching to PostgreSQL (production)

Edit `.env`:
```env
DB_ENGINE=postgres
DB_NAME=portfolio
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

Then re-run migrations:
```bash
python manage.py migrate
python manage.py seed_portfolio
```

---

## 🚢 Deployment

### Option A — Railway / Render / Heroku

1. Push to GitHub
2. Create a new web service pointing at your repo
3. Set environment variables (`SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=yourdomain.com`, database URL, email creds)
4. Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
5. Start command: `gunicorn config.wsgi`

### Option B — VPS (Ubuntu)

```bash
# On the server
git clone <your-repo>
cd portfolio
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # edit with production values
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py seed_portfolio
gunicorn config.wsgi --bind 0.0.0.0:8000
```

Then put Nginx in front of Gunicorn for SSL and static file serving.

### Production checklist

- [ ] `DEBUG=False`
- [ ] `SECRET_KEY` is a long random string (use `python -c "import secrets; print(secrets.token_urlsafe(64))"`)
- [ ] `ALLOWED_HOSTS` includes your real domain
- [ ] PostgreSQL configured
- [ ] Email credentials set
- [ ] HTTPS / SSL enabled
- [ ] `python manage.py collectstatic --noinput` run
- [ ] Static files served by WhiteNoise (already configured) or CDN

---

## 🎨 Customizing the Design

Colors, spacing, and the content width are CSS variables at the top of `static/css/style.css`:

```css
:root {
  --bg:     #0e0f11;   /* near-black background */
  --text:   #e8e9eb;   /* primary text / links   */
  --muted:  #9aa0a8;   /* body copy, secondary   */
  --faint:  #6b7178;   /* meta, dates, captions  */
  --border: #22252a;   /* hairlines              */
  --max:    660px;     /* content column width   */
}
```

Adjust these six tokens and the whole site re-themes. Keeping it near-monochrome is what preserves the minimal look.

---

## 🤖 Next Steps with Claude Code

This project is ready for further enhancement with [Claude Code](https://docs.claude.com/claude-code):

- Add a **Blog app** with markdown posts
- Build a **REST API** layer with Django REST Framework
- Add **ML project pages** as you complete more coursework
- Integrate **Plotly / Chart.js** for an interactive certification trend dashboard
- Add **PDF resume generation** using the existing site data
- Add **testimonials** and a **case studies** section
- Set up **CI/CD** with GitHub Actions

---

## 📝 License

Personal portfolio — feel free to fork and adapt for your own use.

---

Built with ❤️ in Hyderabad by **Lalu Yashwanth**.
