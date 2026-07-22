"""
Seed the portfolio database with Lalu Yashwanth's real content.
Run with: python manage.py seed_portfolio
Use --reset to wipe existing data first.
"""
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.core.models import SiteSettings, HeroSection, Post
from apps.projects.models import Project, TechStack, ProjectFeature
from apps.skills.models import SkillCategory, Skill
from apps.experience.models import Experience, Education


class Command(BaseCommand):
    help = "Seed the portfolio database with real content."

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset', action='store_true',
            help='Wipe existing portfolio data before seeding.'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        reset = options['reset']

        if reset:
            self.stdout.write(self.style.WARNING('Wiping existing data...'))
            Project.objects.all().delete()
            TechStack.objects.all().delete()
            Skill.objects.all().delete()
            SkillCategory.objects.all().delete()
            Experience.objects.all().delete()
            Education.objects.all().delete()
            HeroSection.objects.all().delete()
            Post.objects.all().delete()

        self.stdout.write('Seeding site settings...')
        self._seed_site_settings()

        self.stdout.write('Seeding hero...')
        self._seed_hero()

        self.stdout.write('Seeding tech stack...')
        tech = self._seed_tech_stack()

        self.stdout.write('Seeding projects...')
        self._seed_projects(tech, reset=reset)

        self.stdout.write('Seeding skills...')
        self._seed_skills()

        self.stdout.write('Seeding experience...')
        self._seed_experience()

        self.stdout.write('Seeding education...')
        self._seed_education()

        self.stdout.write('Seeding writing...')
        self._seed_writing()

        self.stdout.write(self.style.SUCCESS('\n✓ Portfolio seeded successfully!'))
        self.stdout.write('  Visit / to see the home page')
        self.stdout.write('  Visit /admin/ to manage content')

    # -----------------------------------------------------------------
    def _seed_site_settings(self):
        s = SiteSettings.load()
        s.site_name = 'Lalu Yashwanth'
        s.tagline = 'Full-Stack Developer · Python, Django & Machine Learning'
        s.meta_description = (
            'Full-Stack Software Developer with 3+ years of experience building '
            'enterprise-grade web applications with Python, Django, PostgreSQL, '
            'REST APIs, and Machine Learning. Based in Hyderabad, India.'
        )
        s.meta_keywords = (
            'Full-Stack Developer, Python Developer, Django Developer, '
            'PostgreSQL, REST API, Machine Learning, Data Science, scikit-learn, '
            'TensorFlow, Pandas, NumPy, Hyderabad, India, Lalu Yashwanth'
        )
        s.email = 'laluyashwanth.dev@gmail.com'
        s.location = 'Hyderabad, India'
        s.github_url = 'https://github.com/G-Laluyashwanth'
        s.linkedin_url = 'https://linkedin.com/in/laluyashwanth'
        s.twitter_url = 'https://x.com/laluyashwanth'
        s.save()

    def _seed_hero(self):
        # Singleton-ish: always replace with one active hero.
        HeroSection.objects.all().delete()
        HeroSection.objects.create(
            eyebrow='Full-Stack Developer · Python · Django · ML',
            headline='Building scalable web applications with Python, Django, and Machine Learning.',
            subheadline=(
                'I build full-stack systems with Python and Django — enterprise web apps, '
                'REST APIs, and automation tools that remove hours of manual work. Lately I have '
                'been drawn to the seam where clean engineering meets machine learning, and what '
                'becomes possible when software can learn instead of just follow rules.'
            ),
            cta_primary_label='View Projects',
            cta_primary_url='#projects',
            cta_secondary_label='Get in Touch',
            cta_secondary_url='#contact',
            is_active=True,
        )

    # -----------------------------------------------------------------
    def _seed_tech_stack(self):
        items = [
            ('Python', 'primary'), ('Django', 'primary'),
            ('Django REST Framework', 'primary'), ('PostgreSQL', 'accent'),
            ('MySQL', 'accent'), ('JavaScript', 'warning'),
            ('HTML5', 'warning'), ('CSS3', 'warning'),
            ('Bootstrap', 'warning'), ('Celery', 'primary'),
            ('Redis', 'accent'), ('python-docx', 'primary'),
            ('openpyxl', 'primary'), ('Pandas', 'accent'),
            ('NumPy', 'accent'), ('Matplotlib', 'accent'),
            ('scikit-learn', 'accent'), ('TensorFlow', 'accent'),
            ('Google Colab', 'accent'), ('Jupyter', 'accent'),
            ('Git', 'success'), ('GitHub', 'success'),
            ('Jira', 'success'), ('Confluence', 'success'),
            ('JQL', 'success'), ('WhiteNoise', 'success'),
            ('jQuery', 'warning'),
        ]
        objs = {}
        for i, (name, color) in enumerate(items):
            obj, _ = TechStack.objects.get_or_create(
                name=name, defaults={'color': color, 'order': i}
            )
            objs[name] = obj
        return objs

    def _upsert_project(self, tech, slug, defaults, tech_names, features):
        project, created = Project.objects.update_or_create(
            slug=slug,
            defaults=defaults,
        )
        project.tech_stack.set([tech[n] for n in tech_names])
        project.features.all().delete()
        for i, text in enumerate(features):
            ProjectFeature.objects.create(project=project, text=text, order=i)
        return project

    def _seed_projects(self, tech, reset=False):
        if reset:
            Project.objects.all().delete()

        # 0. Personal Portfolio — public, featured first
        self._upsert_project(
            tech,
            slug='personal-portfolio',
            defaults={
                'title': 'Personal Portfolio',
                'short_description': (
                    'Minimal dark Django portfolio with SEO, Unfold admin, self-hosted '
                    'fonts, and WhiteNoise — built to showcase work without framework noise.'
                ),
                'description': (
                    'A typography-first personal portfolio built with Django. Content is '
                    'managed in the admin (projects, skills, experience, writing), served '
                    'with self-hosted fonts and WhiteNoise for static assets, and structured '
                    'for clear SEO (meta tags, Person JSON-LD, skip-to-content). The design '
                    'stays intentionally quiet so the work and writing do the talking.'
                ),
                'problem': (
                    'I needed a place to present client and personal work honestly — with '
                    'editable content, decent SEO, and a calm dark layout — without shipping '
                    'another generic template site.'
                ),
                'solution': (
                    'Built a small Django app with Unfold admin, model-driven sections, '
                    'manifest static files via WhiteNoise, and a minimal dark UI. Projects '
                    'carry problem / solution / impact so recruiters can scan outcomes, not '
                    'just screenshots.'
                ),
                'impact': (
                    'One place to keep projects, skills, and writing current. Public source '
                    'on GitHub. Deploy-ready structure once production hardening is done.'
                ),
                'category': 'web',
                'company': '',
                'role': 'Full-Stack Developer',
                'start_date': date(2025, 1, 1),
                'end_date': None,
                'is_featured': True,
                'is_published': True,
                'order': 0,
                'github_url': 'https://github.com/G-Laluyashwanth/portfolio',
                'live_url': '',
                'is_proprietary': False,
            },
            tech_names=[
                'Python', 'Django', 'PostgreSQL', 'WhiteNoise',
                'HTML5', 'CSS3', 'JavaScript', 'Git', 'GitHub',
            ],
            features=[
                'Minimal dark, typography-first layout with subtle dot background',
                'Content managed via Unfold Django admin (projects, skills, experience, posts)',
                'SEO basics: meta tags, Person JSON-LD, skip-to-content link',
                'Self-hosted fonts and WhiteNoise for static asset serving',
                'Problem / solution / impact fields on project detail pages',
            ],
        )

        # 1. ISO Audit Document Generator — flagship (proprietary)
        self._upsert_project(
            tech,
            slug='iso-audit-document-generator',
            defaults={
                'title': 'ISO Audit Document Generator',
                'short_description': (
                    'Django-based platform that auto-generates 29 audit documents per client '
                    'engagement from a single multi-step form — replacing 2-4 hours of manual work.'
                ),
                'description': (
                    'A production Django web application built for Concept QA Labs to eliminate '
                    'manual document creation across ISO audit engagements. The team previously '
                    'created 29 audit documents per client by hand, taking 2-4 hours with high '
                    'error rates and zero version control. This system captures audit information '
                    'once via a 4-step wizard and auto-generates every required document from '
                    'templates — Word and Excel — using python-docx and openpyxl.'
                ),
                'problem': (
                    'Team members manually created 29 audit documents per client engagement, '
                    'spending 2-4 hours per project with frequent errors, inconsistent formatting, '
                    'and no version history. As the client base grew, this became a major bottleneck.'
                ),
                'solution': (
                    'Designed and built a Django + PostgreSQL application with a multi-step audit '
                    'entry wizard, a template-driven document engine using python-docx and openpyxl, '
                    'asynchronous document generation via Celery + Redis, version tracking, and a '
                    'tree-view sidebar for browsing generated documents per engagement. Includes '
                    'auditor-day calculation logic that adjusts for head count, standard, complexity, '
                    'remote/multi-site factors, and produces consistent outputs across the team.'
                ),
                'impact': (
                    'Reduced document generation time from 2-4 hours to under 5 minutes per '
                    'engagement. Eliminated manual transcription errors. Introduced version control '
                    'and audit history for compliance. Standardized document formatting across all '
                    'team members and engagements.'
                ),
                'category': 'automation',
                'company': 'Concept QA Labs Pvt. Ltd.',
                'role': 'Full-Stack Developer',
                'start_date': date(2024, 9, 1),
                'end_date': None,
                'is_featured': True,
                'is_published': True,
                'order': 1,
                'github_url': '',
                'live_url': '',
                'is_proprietary': True,
            },
            tech_names=[
                'Python', 'Django', 'Django REST Framework', 'PostgreSQL',
                'Celery', 'Redis', 'python-docx', 'openpyxl', 'JavaScript', 'HTML5', 'CSS3',
            ],
            features=[
                'Multi-step audit entry wizard with field validation and auto-save',
                'Template-driven generation of 29 documents (Word + Excel) per engagement',
                'Asynchronous document generation via Celery + Redis for non-blocking UX',
                'Auditor-day calculation engine with remote/multi-site adjustments',
                'Version control and document history per engagement',
                'Tree-view sidebar for browsing generated documents by stage',
                'Role-based access control and authentication',
            ],
        )

        # 2. CQAL Client Management System
        self._upsert_project(
            tech,
            slug='cqal-client-management-system',
            defaults={
                'title': 'CQAL Client Management System',
                'short_description': (
                    'Enterprise audit tracking platform with automated scheduling, RBAC, '
                    'real-time dashboards, and ISO certification trend analysis using Pandas + Matplotlib.'
                ),
                'description': (
                    'A full-featured client management and audit tracking system built for '
                    'Concept QA Labs to streamline ISO 9001, ISO 20000, ISO 27001, ISO 14001, '
                    'and CMMI engagements. The system automates audit reminder scheduling '
                    '(45 days before audits), provides one-click email reminders with pre-defined '
                    'templates, supports role-based access control, and generates Excel exports '
                    'with custom formatting. Also includes a Trend Analysis module that visualizes '
                    'ISO certification growth across years using Python, Pandas, and Matplotlib.'
                ),
                'problem': (
                    'Manual tracking of audit schedules across multiple ISO standards led to '
                    'missed deadlines, inefficient client communication, and no visibility into '
                    'historical certification trends.'
                ),
                'solution': (
                    'Built a Django + PostgreSQL application with normalized schemas supporting '
                    'complex many-to-many audit-client relationships, automated date calculation '
                    '(surveillance, recertification, reminder dates), an ISO Monthly Tracker, '
                    'role-based access control, integrated email notifications, and Excel exports '
                    'using openpyxl. Added a Business Intelligence module with ISO certification '
                    'trend analysis (ISO 27001, ISO 9001:2015, ISO 20000) using Pandas for data '
                    'processing and Matplotlib for visualization, generated via Google Colab.'
                ),
                'impact': (
                    'Significantly reduced manual follow-up effort. Eliminated missed audit '
                    'deadlines. Provided real-time dashboards with KPI metrics. Enabled data-driven '
                    'business insights via the certification trend analysis module.'
                ),
                'category': 'web',
                'company': 'Concept QA Labs Pvt. Ltd.',
                'role': 'Full-Stack Developer',
                'start_date': date(2023, 6, 1),
                'end_date': None,
                'is_featured': True,
                'is_published': True,
                'order': 2,
                'github_url': '',
                'live_url': '',
                'is_proprietary': True,
            },
            tech_names=[
                'Python', 'Django', 'PostgreSQL', 'MySQL', 'JavaScript',
                'HTML5', 'CSS3', 'Bootstrap', 'jQuery', 'openpyxl',
                'Pandas', 'Matplotlib', 'Google Colab',
            ],
            features=[
                'Automated audit reminder scheduling (45 days before audits)',
                'Role-based access control (RBAC) with secure authentication',
                'ISO Monthly Tracker with year/month filtering and detailed views',
                'Real-time dashboards: total clients, ISO/CMMI breakdowns, task status',
                'One-click email reminders with pre-defined templates',
                'Excel export with custom formatting via openpyxl',
                'ISO Trend Analysis module: certification growth visualizations using Pandas + Matplotlib',
                'Task Management and Leave Management workflows',
            ],
        )

        # 3. Concept QA Labs Corporate Website
        self._upsert_project(
            tech,
            slug='concept-qa-labs-corporate-website',
            defaults={
                'title': 'Concept QA Labs Corporate Website',
                'short_description': (
                    'Fully responsive, SEO-optimized corporate website built with Django + MySQL — '
                    'dynamic content management, contact workflows, and mobile-first design.'
                ),
                'description': (
                    'Architected and delivered a production corporate website for Concept QA Labs '
                    'from requirements to deployment. Built with Django and MySQL with a focus on '
                    'SEO optimization, performance, and mobile-first responsive design. Includes '
                    'dynamic content management, contact form workflows, and optimized static '
                    'asset delivery for fast page loads.'
                ),
                'problem': (
                    'The company needed a professional, content-managed corporate presence to '
                    'showcase services and capture leads.'
                ),
                'solution': (
                    'Designed and built a Django-based site with custom admin for content '
                    'management, MySQL backend, Bootstrap-powered responsive layout, and '
                    'SEO-optimized templates.'
                ),
                'impact': (
                    "Established the company's professional digital presence with cross-browser "
                    'compatibility, mobile-first design, and fast load times.'
                ),
                'category': 'website',
                'company': 'Concept QA Labs Pvt. Ltd.',
                'role': 'Full-Stack Developer',
                'start_date': date(2022, 10, 1),
                'end_date': date(2023, 3, 1),
                'is_featured': True,
                'is_published': True,
                'order': 3,
                'github_url': '',
                'live_url': 'https://conceptqalabs.org/',
                'is_proprietary': True,
            },
            tech_names=[
                'Python', 'Django', 'MySQL', 'Bootstrap', 'HTML5', 'CSS3', 'JavaScript', 'jQuery',
            ],
            features=[
                'Fully responsive, mobile-first corporate website',
                'SEO-optimized templates with semantic HTML and meta tags',
                'Dynamic content management via Django admin',
                'Contact form with email workflows',
                'Cross-browser compatibility and performance optimization',
            ],
        )

        # 4. Process Quality Excellence (PQE) Website
        self._upsert_project(
            tech,
            slug='process-quality-excellence-platform',
            defaults={
                'title': 'Process Quality Excellence Platform',
                'short_description': (
                    'High-performance static site for CMMI/ISO training services with '
                    'optimized load times and clear content architecture.'
                ),
                'description': (
                    'Developed a high-performance static website for Process Quality Excellence (PQE) '
                    'showcasing CMMI and ISO training services. Built with vanilla HTML5, CSS3, '
                    'JavaScript, and Bootstrap with a focus on clear content architecture for '
                    'training courses, schedules, and trainer profiles.'
                ),
                'problem': (
                    'PQE needed a clear, fast, professional web presence to showcase training '
                    'services and trainer credentials.'
                ),
                'solution': (
                    'Built a hand-crafted static site with optimized assets, semantic markup, '
                    'and a content structure designed for end-user clarity.'
                ),
                'impact': (
                    'Delivered a fast-loading, accessible, professional site that effectively '
                    "communicates PQE's training offerings."
                ),
                'category': 'website',
                'company': 'Concept QA Labs Pvt. Ltd.',
                'role': 'Frontend Developer',
                'start_date': date(2023, 4, 1),
                'end_date': date(2023, 7, 1),
                'is_featured': True,
                'is_published': True,
                'order': 4,
                'github_url': '',
                'live_url': 'https://pqellp.com',
                'is_proprietary': True,
            },
            tech_names=['HTML5', 'CSS3', 'JavaScript', 'Bootstrap'],
            features=[
                'High-performance static site with optimized load times',
                'Clear content architecture for courses, schedules, and trainers',
                'Mobile-first responsive design',
                'Semantic HTML for accessibility and SEO',
            ],
        )

        # 5. Jira Automation & Audit Tracking System
        self._upsert_project(
            tech,
            slug='jira-automation-audit-tracking-system',
            defaults={
                'title': 'Jira Automation & Audit Tracking System',
                'short_description': (
                    'CMMI and ISO audit tracking workflows built with advanced JQL filters, '
                    'chained Jira Automation rules, and 7 custom dashboards.'
                ),
                'description': (
                    'Designed and configured comprehensive CMMI and ISO audit tracking workflows '
                    'in Jira using advanced JQL filters, Jira Automation rules, and Confluence '
                    'documentation. Built chained automation rules for CMMI Benchmark Appraisal '
                    'workflows, certificate approvals, compliance deadline management, and '
                    'stakeholder notifications.'
                ),
                'problem': (
                    'Manual coordination across CMMI and ISO audit workflows led to missed '
                    'deadlines and inconsistent process tracking.'
                ),
                'solution': (
                    'Configured Jira projects, custom fields, JQL filters, automation rules, and '
                    'dashboards to fully automate audit tracking, certificate approvals, and '
                    'compliance reporting.'
                ),
                'impact': (
                    'Built 7 custom Jira dashboards with KPI metrics, filter-based gadgets, and '
                    'stakeholder-ready reporting views — eliminating manual status tracking.'
                ),
                'category': 'automation',
                'company': 'Concept QA Labs Pvt. Ltd.',
                'role': 'Jira Administrator',
                'start_date': date(2023, 1, 1),
                'end_date': None,
                'is_featured': True,
                'is_published': True,
                'order': 5,
                'github_url': '',
                'live_url': '',
                'is_proprietary': True,
            },
            tech_names=['Jira', 'JQL', 'Confluence'],
            features=[
                'CMMI and ISO audit tracking workflows with advanced JQL filters',
                'Chained Jira Automation rules for benchmark appraisals and approvals',
                '7 custom Jira dashboards with KPI metrics and stakeholder views',
                'Confluence documentation for processes and standards',
            ],
        )

        # 99. ML project draft — unpublished until metrics + public repo are ready
        self._upsert_project(
            tech,
            slug='ml-project-draft',
            defaults={
                'title': 'ML project (draft)',
                'short_description': (
                    'Placeholder for the machine-learning project currently in progress — '
                    'publish when metrics and a public repo are ready.'
                ),
                'description': (
                    'This is a draft entry reserved for an ML project I am building for the '
                    'portfolio. It will stay unpublished until there is a clear problem statement, '
                    'honest metrics, and a public repository (or an explicit note that the work '
                    'is proprietary). The goal is not to pad the site with unfinished work — it '
                    'is to leave a slot that becomes real when the model and evaluation story '
                    'are ready to ship.'
                ),
                'problem': '',
                'solution': '',
                'impact': '',
                'category': 'ml',
                'company': '',
                'role': 'ML Engineer',
                'start_date': None,
                'end_date': None,
                'is_featured': False,
                'is_published': False,
                'order': 99,
                'github_url': '',
                'live_url': '',
                'is_proprietary': False,
            },
            tech_names=['Python', 'Pandas', 'NumPy', 'scikit-learn', 'Matplotlib'],
            features=[],
        )

    # -----------------------------------------------------------------
    def _seed_skills(self):
        # Skills list is authoritative when seeding — wipe then recreate.
        Skill.objects.all().delete()
        SkillCategory.objects.all().delete()

        categories = [
            {
                'name': 'Backend Development',
                'description': 'Python frameworks, APIs, and server-side architecture',
                'order': 1,
                'skills': [
                    # (name, proficiency, years, is_featured)
                    ('Python', 'expert', 3.5, True),
                    ('Django', 'expert', 3.5, True),
                    ('Django REST Framework', 'advanced', 2.5, True),
                    ('REST APIs', 'advanced', 3.0, True),
                    ('Celery', 'intermediate', 1.5, True),
                    ('Auth & RBAC', 'advanced', 3.0, True),
                ],
            },
            {
                'name': 'Databases',
                'description': 'Relational databases and ORM design',
                'order': 2,
                'skills': [
                    ('PostgreSQL', 'advanced', 3.0, True),
                    ('Django ORM', 'expert', 3.5, True),
                    ('Schema Design', 'advanced', 3.0, True),
                ],
            },
            {
                'name': 'Frontend Development',
                'description': 'Responsive UIs and progressive enhancement',
                'order': 3,
                'skills': [
                    ('JavaScript', 'advanced', 3.5, True),
                    ('HTML/CSS', 'expert', 4.0, True),
                    ('Responsive Design', 'expert', 3.5, True),
                ],
            },
            {
                'name': 'Machine Learning',
                'description': 'Classical ML, data analysis, and model workflows',
                'order': 4,
                'skills': [
                    ('Pandas', 'advanced', 1.5, True),
                    ('NumPy', 'advanced', 1.5, True),
                    ('scikit-learn', 'advanced', 1.5, True),
                    ('Matplotlib', 'advanced', 1.5, True),
                    ('EDA', 'advanced', 1.5, True),
                    ('TensorFlow/Keras', 'intermediate', 1.0, True),
                ],
            },
            {
                'name': 'Tools',
                'description': 'Version control, notebooks, and delivery tools',
                'order': 5,
                'skills': [
                    ('Git', 'advanced', 3.5, True),
                    ('Jupyter', 'advanced', 1.5, True),
                    ('Jira', 'advanced', 3.0, True),
                ],
            },
        ]

        for cat in categories:
            category = SkillCategory.objects.create(
                name=cat['name'],
                description=cat['description'],
                order=cat['order'],
            )
            for i, (name, prof, years, featured) in enumerate(cat['skills']):
                Skill.objects.create(
                    category=category,
                    name=name,
                    proficiency=prof,
                    years_experience=years,
                    is_featured=featured,
                    order=i,
                )

    # -----------------------------------------------------------------
    def _seed_experience(self):
        # Small fixed set — delete and recreate so re-runs stay in sync.
        Experience.objects.all().delete()

        Experience.objects.create(
            company='Concept QA Labs Pvt. Ltd.',
            role='Full-Stack Web Developer',
            employment_type='full_time',
            location='Hyderabad, India',
            company_url='https://conceptqalabs.org/',
            start_date=date(2022, 8, 1),
            end_date=None,
            summary=(
                'Lead full-stack developer building enterprise-grade web applications and '
                'automation systems for ISO and CMMI consulting workflows. Architected and '
                'shipped multiple production systems end-to-end.'
            ),
            responsibilities=(
                'Architected and built the CQAL Client Management System (Django + PostgreSQL) for ISO/CMMI audit tracking with RBAC, automated reminders, and Excel export\n'
                'Designed and developed the ISO Audit Document Generator — automating creation of 29 documents per engagement using python-docx, openpyxl, and Celery\n'
                'Built and deployed the Concept QA Labs corporate website (Django + MySQL) and PQE Process Quality Excellence platform\n'
                'Implemented ISO certification trend analysis using Python, Pandas, and Matplotlib via Google Colab\n'
                'Designed normalized PostgreSQL schemas supporting complex many-to-many audit-client relationships\n'
                'Built role-based access control, authentication, and secure form handling across all applications\n'
                'Configured Jira Automation, JQL filters, and 7 custom dashboards for CMMI and ISO audit tracking workflows\n'
                'Maintained Confluence documentation and collaborated with cross-functional teams in Agile sprints'
            ),
            technologies='Python, Django, Django REST Framework, PostgreSQL, MySQL, Celery, Redis, JavaScript, HTML5, CSS3, Bootstrap, jQuery, python-docx, openpyxl, Pandas, Matplotlib, Git, GitHub, Jira, Confluence',
            order=1,
            is_published=True,
        )

        Experience.objects.create(
            company='Nvest Solutions',
            role='Web Developer Intern',
            employment_type='internship',
            location='India',
            start_date=date(2021, 12, 1),
            end_date=date(2022, 5, 31),
            summary=(
                '6-month internship learning frontend fundamentals, version control, and '
                'C# basics while contributing to product features.'
            ),
            responsibilities=(
                'Learned HTML, CSS, GitHub fundamentals, and C# basics through hands-on projects\n'
                'Built and shipped product features including a WhatsApp content sharing module\n'
                'Contributed to frontend implementation work across multiple internal projects\n'
                'Collaborated with senior developers on code reviews and feature planning\n'
                'Gained foundational experience with version control workflows and team collaboration'
            ),
            technologies='HTML, CSS, JavaScript, C#, Git, GitHub',
            order=2,
            is_published=True,
        )

    # -----------------------------------------------------------------
    def _seed_education(self):
        Education.objects.all().delete()

        Education.objects.create(
            institution='Vidya Vikas Degree College',
            degree='Bachelor of Science (B.Sc)',
            field_of_study='Mathematics & Computer Science',
            location='Akividu, AP, India',
            start_date=date(2018, 7, 1),
            end_date=date(2021, 10, 1),
            grade='A Grade',
            description='',
            order=1,
        )

        Education.objects.create(
            institution='Vidya Vikas Junior College',
            degree='Intermediate (MPC)',
            field_of_study='Mathematics, Physics & Chemistry',
            location='Akividu, AP, India',
            start_date=date(2016, 6, 1),
            end_date=date(2018, 4, 1),
            grade='A Grade',
            description='',
            order=2,
        )

    # -----------------------------------------------------------------
    def _seed_writing(self):
        Post.objects.update_or_create(
            slug='moving-from-full-stack-into-machine-learning',
            defaults={
                'title': 'Moving from full-stack into machine learning',
                'date': date(2025, 6, 1),
                'excerpt': (
                    'Why I am shifting focus, what production Django taught me, and how '
                    'engineering discipline carries into ML.'
                ),
                'content': (
                    'For the last few years I have lived in production Django. Not demos — '
                    'systems that had to run for real teams: audit tracking, document generation, '
                    'RBAC, reminders, Excel exports, Celery jobs that actually finish. That work '
                    'taught me a particular kind of care. Schemas that survive growth. APIs that '
                    'fail loudly instead of silently. Features that are boring on day one because '
                    'they are correct.\n\n'
                    'I still like that kind of software. What changed is the ceiling I care about. '
                    'A lot of the pain in those products was pattern recognition with a human in '
                    'the loop — scheduling, classification of edge cases, trend views stitched '
                    'together in Pandas and Matplotlib. The natural next question for me was: '
                    'what if the system could learn some of those patterns instead of only encoding '
                    'them as rules?\n\n'
                    'That is why I am moving deeper into machine learning. Not because ML is '
                    'fashionable, and not because I want to abandon web engineering. I want to '
                    'build products where models are a component — the same way a queue or a '
                    'database is a component — and where the surrounding product still has the '
                    'discipline I already trust: clear problem statements, honest metrics, '
                    'versioned code, and a path from notebook to something someone can use.\n\n'
                    'There is more overlap than people admit. Debugging a bad train/test split '
                    'is not so different from debugging a bad queryset. Feature leakage is a '
                    'data-integrity bug. Hyperparameter search without a fixed evaluation story '
                    'is shipping without acceptance criteria. The habits that made Django apps '
                    'reliable — small interfaces, reproducible environments, writing down what '
                    '"done" means — are the same habits that keep ML work from becoming a '
                    'slideshow of accuracy numbers.\n\n'
                    'I am currently building an ML project for this portfolio. It will stay '
                    'unpublished until it earns a place: a concrete problem, a public repo (or '
                    'an honest proprietary note), and metrics I am willing to defend. Until then '
                    'the draft slot on the projects page is intentional — a reminder not to '
                    'perform competence before the work is ready.\n\n'
                    'If you are reading this as a recruiter or collaborator: my baseline is still '
                    'Python and Django in production. The direction of travel is classical ML '
                    'and the tooling around it — Pandas, NumPy, scikit-learn, careful EDA — with '
                    'TensorFlow/Keras as something I am actively learning, not pretending to '
                    'master overnight. I care about shipping systems that learn where learning '
                    'helps, and that stay maintainable where rules still win.'
                ),
                'external_url': '',
                'is_published': True,
            },
        )
