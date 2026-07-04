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
        if options['reset']:
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
        self._seed_projects(tech)

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
        s.twitter_url = 'https://x.com/laluyashwanth'  # TODO: update to your real handle
        s.save()

    def _seed_hero(self):
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
            cta_secondary_url='/contact/',
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
            ('Seaborn', 'accent'), ('scikit-learn', 'accent'),
            ('TensorFlow', 'accent'), ('Google Colab', 'accent'),
            ('Jupyter', 'accent'), ('Git', 'success'),
            ('GitHub', 'success'), ('Jira', 'success'),
            ('Confluence', 'success'), ('JQL', 'success'),
            ('jQuery', 'warning'),
        ]
        objs = {}
        for i, (name, color) in enumerate(items):
            obj, _ = TechStack.objects.get_or_create(
                name=name, defaults={'color': color, 'order': i}
            )
            objs[name] = obj
        return objs

    def _seed_projects(self, tech):
        Project.objects.all().delete()

        # 1. ISO Audit Document Generator (Doc Generator) — flagship
        p1 = Project.objects.create(
            title='ISO Audit Document Generator',
            short_description=(
                'Django-based platform that auto-generates 29 audit documents per client '
                'engagement from a single multi-step form — replacing 2-4 hours of manual work.'
            ),
            description=(
                'A production Django web application built for Concept QA Labs to eliminate '
                'manual document creation across ISO audit engagements. The team previously '
                'created 29 audit documents per client by hand, taking 2-4 hours with high '
                'error rates and zero version control. This system captures audit information '
                'once via a 4-step wizard and auto-generates every required document from '
                'templates — Word and Excel — using python-docx and openpyxl.'
            ),
            problem=(
                'Team members manually created 29 audit documents per client engagement, '
                'spending 2-4 hours per project with frequent errors, inconsistent formatting, '
                'and no version history. As the client base grew, this became a major bottleneck.'
            ),
            solution=(
                'Designed and built a Django + PostgreSQL application with a multi-step audit '
                'entry wizard, a template-driven document engine using python-docx and openpyxl, '
                'asynchronous document generation via Celery + Redis, version tracking, and a '
                'tree-view sidebar for browsing generated documents per engagement. Includes '
                'auditor-day calculation logic that adjusts for head count, standard, complexity, '
                'remote/multi-site factors, and produces consistent outputs across the team.'
            ),
            impact=(
                'Reduced document generation time from 2-4 hours to under 5 minutes per '
                'engagement. Eliminated manual transcription errors. Introduced version control '
                'and audit history for compliance. Standardized document formatting across all '
                'team members and engagements.'
            ),
            category='automation',
            company='Concept QA Labs Pvt. Ltd.',
            role='Full-Stack Developer',
            start_date=date(2024, 9, 1),
            end_date=None,
            is_featured=True,
            is_published=True,
            order=1,
        )
        p1.tech_stack.set([tech[n] for n in [
            'Python', 'Django', 'Django REST Framework', 'PostgreSQL',
            'Celery', 'Redis', 'python-docx', 'openpyxl', 'JavaScript', 'HTML5', 'CSS3'
        ]])
        for i, f in enumerate([
            'Multi-step audit entry wizard with field validation and auto-save',
            'Template-driven generation of 29 documents (Word + Excel) per engagement',
            'Asynchronous document generation via Celery + Redis for non-blocking UX',
            'Auditor-day calculation engine with remote/multi-site adjustments',
            'Version control and document history per engagement',
            'Tree-view sidebar for browsing generated documents by stage',
            'Role-based access control and authentication',
        ]):
            ProjectFeature.objects.create(project=p1, text=f, order=i)

        # 2. CQAL Client Management System — with ISO Trend Analysis sub-feature
        p2 = Project.objects.create(
            title='CQAL Client Management System',
            short_description=(
                'Enterprise audit tracking platform with automated scheduling, RBAC, '
                'real-time dashboards, and ISO certification trend analysis using Pandas + Matplotlib.'
            ),
            description=(
                'A full-featured client management and audit tracking system built for '
                'Concept QA Labs to streamline ISO 9001, ISO 20000, ISO 27001, ISO 14001, '
                'and CMMI engagements. The system automates audit reminder scheduling '
                '(45 days before audits), provides one-click email reminders with pre-defined '
                'templates, supports role-based access control, and generates Excel exports '
                'with custom formatting. Also includes a Trend Analysis module that visualizes '
                'ISO certification growth across years using Python, Pandas, and Matplotlib.'
            ),
            problem=(
                'Manual tracking of audit schedules across multiple ISO standards led to '
                'missed deadlines, inefficient client communication, and no visibility into '
                'historical certification trends.'
            ),
            solution=(
                'Built a Django + PostgreSQL application with normalized schemas supporting '
                'complex many-to-many audit-client relationships, automated date calculation '
                '(surveillance, recertification, reminder dates), an ISO Monthly Tracker, '
                'role-based access control, integrated email notifications, and Excel exports '
                'using openpyxl. Added a Business Intelligence module with ISO certification '
                'trend analysis (ISO 27001, ISO 9001:2015, ISO 20000) using Pandas for data '
                'processing and Matplotlib for visualization, generated via Google Colab.'
            ),
            impact=(
                'Significantly reduced manual follow-up effort. Eliminated missed audit '
                'deadlines. Provided real-time dashboards with KPI metrics. Enabled data-driven '
                'business insights via the certification trend analysis module.'
            ),
            category='web',
            company='Concept QA Labs Pvt. Ltd.',
            role='Full-Stack Developer',
            start_date=date(2023, 6, 1),
            end_date=None,
            is_featured=True,
            is_published=True,
            order=2,
        )
        p2.tech_stack.set([tech[n] for n in [
            'Python', 'Django', 'PostgreSQL', 'MySQL', 'JavaScript',
            'HTML5', 'CSS3', 'Bootstrap', 'jQuery', 'openpyxl',
            'Pandas', 'Matplotlib', 'Google Colab',
        ]])
        for i, f in enumerate([
            'Automated audit reminder scheduling (45 days before audits)',
            'Role-based access control (RBAC) with secure authentication',
            'ISO Monthly Tracker with year/month filtering and detailed views',
            'Real-time dashboards: total clients, ISO/CMMI breakdowns, task status',
            'One-click email reminders with pre-defined templates',
            'Excel export with custom formatting via openpyxl',
            'ISO Trend Analysis module: certification growth visualizations using Pandas + Matplotlib',
            'Task Management and Leave Management workflows',
        ]):
            ProjectFeature.objects.create(project=p2, text=f, order=i)

        # 3. Concept QA Labs Corporate Website
        p3 = Project.objects.create(
            title='Concept QA Labs Corporate Website',
            short_description=(
                'Fully responsive, SEO-optimized corporate website built with Django + MySQL — '
                'dynamic content management, contact workflows, and mobile-first design.'
            ),
            description=(
                'Architected and delivered a production corporate website for Concept QA Labs '
                'from requirements to deployment. Built with Django and MySQL with a focus on '
                'SEO optimization, performance, and mobile-first responsive design. Includes '
                'dynamic content management, contact form workflows, and optimized static '
                'asset delivery for fast page loads.'
            ),
            problem='The company needed a professional, content-managed corporate presence to showcase services and capture leads.',
            solution='Designed and built a Django-based site with custom admin for content management, MySQL backend, Bootstrap-powered responsive layout, and SEO-optimized templates.',
            impact="Established the company's professional digital presence with cross-browser compatibility, mobile-first design, and fast load times.",
            category='website',
            company='Concept QA Labs Pvt. Ltd.',
            role='Full-Stack Developer',
            start_date=date(2022, 10, 1),
            end_date=date(2023, 3, 1),
            is_featured=True,
            is_published=True,
            order=3,
            live_url='https://conceptqalabs.org/',
        )
        p3.tech_stack.set([tech[n] for n in [
            'Python', 'Django', 'MySQL', 'Bootstrap', 'HTML5', 'CSS3', 'JavaScript', 'jQuery',
        ]])
        for i, f in enumerate([
            'Fully responsive, mobile-first corporate website',
            'SEO-optimized templates with semantic HTML and meta tags',
            'Dynamic content management via Django admin',
            'Contact form with email workflows',
            'Cross-browser compatibility and performance optimization',
        ]):
            ProjectFeature.objects.create(project=p3, text=f, order=i)

        # 4. Process Quality Excellence (PQE) Website
        p4 = Project.objects.create(
            title='Process Quality Excellence Platform',
            short_description=(
                'High-performance static site for CMMI/ISO training services with '
                'optimized load times and clear content architecture.'
            ),
            description=(
                'Developed a high-performance static website for Process Quality Excellence (PQE) '
                'showcasing CMMI and ISO training services. Built with vanilla HTML5, CSS3, '
                'JavaScript, and Bootstrap with a focus on clear content architecture for '
                'training courses, schedules, and trainer profiles.'
            ),
            problem='PQE needed a clear, fast, professional web presence to showcase training services and trainer credentials.',
            solution='Built a hand-crafted static site with optimized assets, semantic markup, and a content structure designed for end-user clarity.',
            impact="Delivered a fast-loading, accessible, professional site that effectively communicates PQE's training offerings.",
            category='website',
            company='Concept QA Labs Pvt. Ltd.',
            role='Frontend Developer',
            start_date=date(2023, 4, 1),
            end_date=date(2023, 7, 1),
            is_featured=True,
            is_published=True,
            order=4,
            live_url='https://pqellp.com',
        )
        p4.tech_stack.set([tech[n] for n in [
            'HTML5', 'CSS3', 'JavaScript', 'Bootstrap',
        ]])
        for i, f in enumerate([
            'High-performance static site with optimized load times',
            'Clear content architecture for courses, schedules, and trainers',
            'Mobile-first responsive design',
            'Semantic HTML for accessibility and SEO',
        ]):
            ProjectFeature.objects.create(project=p4, text=f, order=i)

        # 5. Jira Automation & Audit Tracking System
        p5 = Project.objects.create(
            title='Jira Automation & Audit Tracking System',
            short_description=(
                'CMMI and ISO audit tracking workflows built with advanced JQL filters, '
                'chained Jira Automation rules, and 7 custom dashboards.'
            ),
            description=(
                'Designed and configured comprehensive CMMI and ISO audit tracking workflows '
                'in Jira using advanced JQL filters, Jira Automation rules, and Confluence '
                'documentation. Built chained automation rules for CMMI Benchmark Appraisal '
                'workflows, certificate approvals, compliance deadline management, and '
                'stakeholder notifications.'
            ),
            problem='Manual coordination across CMMI and ISO audit workflows led to missed deadlines and inconsistent process tracking.',
            solution='Configured Jira projects, custom fields, JQL filters, automation rules, and dashboards to fully automate audit tracking, certificate approvals, and compliance reporting.',
            impact='Built 7 custom Jira dashboards with KPI metrics, filter-based gadgets, and stakeholder-ready reporting views — eliminating manual status tracking.',
            category='automation',
            company='Concept QA Labs Pvt. Ltd.',
            role='Jira Administrator',
            start_date=date(2023, 1, 1),
            end_date=None,
            is_featured=True,
            is_published=True,
            order=5,
        )
        p5.tech_stack.set([tech[n] for n in ['Jira', 'JQL', 'Confluence']])
        for i, f in enumerate([
            'CMMI and ISO audit tracking workflows with advanced JQL filters',
            'Chained Jira Automation rules for benchmark appraisals and approvals',
            '7 custom Jira dashboards with KPI metrics and stakeholder views',
            'Confluence documentation for processes and standards',
        ]):
            ProjectFeature.objects.create(project=p5, text=f, order=i)

    # -----------------------------------------------------------------
    def _seed_skills(self):
        SkillCategory.objects.all().delete()

        categories = [
            {
                'name': 'Backend Development',
                'description': 'Python frameworks, APIs, and server-side architecture',
                'order': 1,
                'skills': [
                    ('Python', 'expert', 3.5),
                    ('Django', 'expert', 3.5),
                    ('Django REST Framework', 'advanced', 2.5),
                    ('RESTful API Design', 'advanced', 3.0),
                    ('Celery', 'intermediate', 1.5),
                    ('Authentication & RBAC', 'advanced', 3.0),
                ],
            },
            {
                'name': 'Databases',
                'description': 'Relational databases and ORM design',
                'order': 2,
                'skills': [
                    ('PostgreSQL', 'advanced', 3.0),
                    ('MySQL', 'advanced', 3.0),
                    ('Django ORM', 'expert', 3.5),
                    ('Schema Design', 'advanced', 3.0),
                    ('Query Optimization', 'intermediate', 2.5),
                ],
            },
            {
                'name': 'Frontend Development',
                'description': 'Responsive UIs and progressive enhancement',
                'order': 3,
                'skills': [
                    ('JavaScript (ES6+)', 'advanced', 3.5),
                    ('HTML5', 'expert', 4.0),
                    ('CSS3', 'expert', 4.0),
                    ('Bootstrap', 'advanced', 3.5),
                    ('jQuery', 'advanced', 3.0),
                    ('Responsive Design', 'expert', 3.5),
                ],
            },
            {
                'name': 'Machine Learning & Data Science',
                'description': 'Classical ML, deep learning, and end-to-end workflows',
                'order': 4,
                'skills': [
                    ('Python 3 for Data Science', 'advanced', 1.5),
                    ('NumPy', 'advanced', 1.5),
                    ('Pandas', 'advanced', 1.5),
                    ('Matplotlib', 'advanced', 1.5),
                    ('Seaborn', 'advanced', 1.5),
                    ('scikit-learn', 'advanced', 1.5),
                    ('TensorFlow 2.0 & Keras', 'intermediate', 1.0),
                    ('Neural Networks & Deep Learning', 'intermediate', 1.0),
                    ('Supervised Learning', 'advanced', 1.5),
                    ('Classification & Regression', 'advanced', 1.5),
                    ('Decision Trees & Random Forests', 'advanced', 1.5),
                    ('Ensemble Learning', 'intermediate', 1.0),
                    ('K-Nearest Neighbours (KNN)', 'advanced', 1.5),
                    ('Support Vector Machines (SVM)', 'advanced', 1.5),
                    ('Linear & Polynomial Regression', 'advanced', 1.5),
                    ('Time Series Analysis', 'intermediate', 1.0),
                    ('Train/Test & Cross Validation', 'advanced', 1.5),
                    ('Hyperparameter Tuning', 'advanced', 1.5),
                    ('Transfer Learning', 'intermediate', 1.0),
                    ('Image Recognition & Classification', 'intermediate', 1.0),
                    ('Model Evaluation & Analysis', 'advanced', 1.5),
                    ('Data Cleaning & Preparation', 'advanced', 1.5),
                    ('Exploratory Data Analysis', 'advanced', 1.5),
                    ('Data Visualization', 'advanced', 1.5),
                ],
            },
            {
                'name': 'Big Data & Distributed Systems',
                'description': 'Large-scale data processing frameworks',
                'order': 5,
                'skills': [
                    ('Apache Hadoop', 'beginner', 0.5),
                    ('Apache Spark', 'beginner', 0.5),
                    ('Apache Kafka', 'beginner', 0.5),
                    ('Apache Flink', 'beginner', 0.5),
                ],
            },
            {
                'name': 'Tools & Environment',
                'description': 'Development tools, version control, and platforms',
                'order': 6,
                'skills': [
                    ('Git', 'advanced', 3.5),
                    ('GitHub', 'advanced', 3.5),
                    ('Jupyter Notebooks', 'advanced', 1.5),
                    ('Google Colab', 'advanced', 1.5),
                    ('Conda / Miniconda', 'intermediate', 1.0),
                    ('Kaggle', 'intermediate', 1.0),
                    ('GPU Acceleration (Colab)', 'intermediate', 1.0),
                    ('Jira Administration', 'advanced', 3.0),
                    ('JQL', 'advanced', 3.0),
                    ('Confluence', 'advanced', 3.0),
                    ('Agile / Scrum', 'advanced', 3.0),
                ],
            },
        ]

        for cat in categories:
            category = SkillCategory.objects.create(
                name=cat['name'],
                description=cat['description'],
                order=cat['order'],
            )
            for i, (name, prof, years) in enumerate(cat['skills']):
                Skill.objects.create(
                    category=category,
                    name=name,
                    proficiency=prof,
                    years_experience=years,
                    is_featured=True,
                    order=i,
                )

    # -----------------------------------------------------------------
    def _seed_experience(self):
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
        Post.objects.all().delete()
        Post.objects.create(
            title='Moving from full-stack into machine learning',
            excerpt=(
                'Why I am shifting focus, what I am learning, and how I think about the '
                'overlap between solid engineering and ML.'
            ),
            content=(
                'This is a starter note — replace or delete it from the Django admin '
                '(Core → Posts).\n\n'
                'After a few years building production Django systems, I have been going '
                'deeper into machine learning. The goal is to build software that can learn '
                'from data, not just follow hand-written rules — and to keep the same '
                'engineering discipline while doing it.'
            ),
            is_published=True,
        )
