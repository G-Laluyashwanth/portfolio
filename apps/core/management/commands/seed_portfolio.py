"""
Seed the portfolio database with Lalu Yashwanth's real content.
Run with: python manage.py seed_portfolio

Without --reset nothing is ever deleted: seeded records are updated in place
and anything added by hand in the admin is left alone. Use --reset to wipe the
portfolio tables and rebuild them from scratch.
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
        self._seed_hero(reset=reset)

        self.stdout.write('Seeding tech stack...')
        tech = self._seed_tech_stack()

        self.stdout.write('Seeding projects...')
        self._seed_projects(tech, reset=reset)

        self.stdout.write('Seeding skills...')
        self._seed_skills(reset=reset)

        self.stdout.write('Seeding experience...')
        self._seed_experience(reset=reset)

        self.stdout.write('Seeding education...')
        self._seed_education(reset=reset)

        self.stdout.write('Seeding writing...')
        self._seed_writing()

        self.stdout.write(self.style.SUCCESS('\n✓ Portfolio seeded successfully!'))
        self.stdout.write('  Visit / to see the home page')
        self.stdout.write('  Visit /admin/ to manage content')


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

    def _seed_hero(self, reset=False):
        # Singleton-ish: one active hero, updated in place so re-runs do not
        # drop the row (and its pk) out from under anything referencing it.
        if reset:
            HeroSection.objects.all().delete()

        defaults = {
            'eyebrow': 'Full-Stack Developer · Python · Django · ML',
            'headline': 'Building scalable web applications with Python, Django, and Machine Learning.',
            'subheadline': (
                'I build full-stack systems with Python and Django - enterprise web apps, '
                'REST APIs, and automation tools that remove hours of manual work. Lately I have '
                'been drawn to the seam where clean engineering meets machine learning, and what '
                'becomes possible when software can learn instead of just follow rules.'
            ),
            'cta_primary_label': 'View Projects',
            'cta_primary_url': '#projects',
            'cta_secondary_label': 'Get in Touch',
            'cta_secondary_url': '#contact',
            'is_active': True,
        }

        hero = HeroSection.objects.order_by('pk').first()
        if hero is None:
            HeroSection.objects.create(**defaults)
        else:
            for field, value in defaults.items():
                setattr(hero, field, value)
            hero.save()


    def _seed_tech_stack(self):
        from apps.projects.seed_data import TECH_STACK_ITEMS

        objs = {}
        for i, (name, color) in enumerate(TECH_STACK_ITEMS):
            obj, _ = TechStack.objects.get_or_create(
                name=name, defaults={'color': color, 'order': i}
            )
            objs[name] = obj
        return objs

    def _upsert_project(self, tech, data):
        tech_names = data['tech']
        features = data.get('features') or []
        defaults = {
            key: data[key]
            for key in (
                'title', 'subtitle', 'short_description', 'description', 'problem',
                'solution', 'impact', 'technical_highlights', 'roles_and_users',
                'workflows', 'scope_notes', 'category', 'company', 'role',
                'start_date', 'end_date', 'live_url', 'github_url',
                'is_proprietary', 'is_featured', 'is_published', 'order',
            )
            if key in data
        }
        # Ensure optional new fields exist even if missing from a dict.
        for key in (
            'subtitle', 'technical_highlights', 'roles_and_users',
            'workflows', 'scope_notes',
        ):
            defaults.setdefault(key, '')

        project, _ = Project.objects.update_or_create(
            slug=data['slug'],
            defaults=defaults,
        )
        missing = [n for n in tech_names if n not in tech]
        if missing:
            raise ValueError(f"Missing tech stack items for {data['slug']}: {missing}")
        project.tech_stack.set([tech[n] for n in tech_names])
        project.features.all().delete()
        for i, text in enumerate(features):
            ProjectFeature.objects.create(project=project, text=text, order=i)
        return project

    def _seed_projects(self, tech, reset=False):
        from apps.projects.seed_data import PROJECTS

        if reset:
            Project.objects.all().delete()

        for data in PROJECTS:
            self._upsert_project(tech, data)

    def _seed_skills(self, reset=False):
        if reset:
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
            category, _ = SkillCategory.objects.update_or_create(
                name=cat['name'],
                defaults={
                    'description': cat['description'],
                    'order': cat['order'],
                },
            )
            for i, (name, prof, years, featured) in enumerate(cat['skills']):
                Skill.objects.update_or_create(
                    category=category,
                    name=name,
                    defaults={
                        'proficiency': prof,
                        'years_experience': years,
                        'is_featured': featured,
                        'order': i,
                    },
                )


    def _seed_experience(self, reset=False):
        if reset:
            Experience.objects.all().delete()

        self._upsert_experience(
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
                'Designed and developed the ISO Audit Document Generator - automating creation of 29 documents per engagement using python-docx, openpyxl, and Celery\n'
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

        self._upsert_experience(
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

    def _upsert_experience(self, company, role, **defaults):
        """Company + role is the natural key for a job entry."""
        Experience.objects.update_or_create(
            company=company, role=role, defaults=defaults,
        )

    def _seed_education(self, reset=False):
        if reset:
            Education.objects.all().delete()

        self._upsert_education(
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

        self._upsert_education(
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

    def _upsert_education(self, institution, degree, **defaults):
        """Institution + degree is the natural key for an education entry."""
        Education.objects.update_or_create(
            institution=institution, degree=degree, defaults=defaults,
        )


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
                    'For the last few years I have lived in production Django. Not demos - '
                    'systems that had to run for real teams: audit tracking, document generation, '
                    'RBAC, reminders, Excel exports, Celery jobs that actually finish. That work '
                    'taught me a particular kind of care. Schemas that survive growth. APIs that '
                    'fail loudly instead of silently. Features that are boring on day one because '
                    'they are correct.\n\n'
                    'I still like that kind of software. What changed is the ceiling I care about. '
                    'A lot of the pain in those products was pattern recognition with a human in '
                    'the loop - scheduling, classification of edge cases, trend views stitched '
                    'together in Pandas and Matplotlib. The natural next question for me was: '
                    'what if the system could learn some of those patterns instead of only encoding '
                    'them as rules?\n\n'
                    'That is why I am moving deeper into machine learning. Not because ML is '
                    'fashionable, and not because I want to abandon web engineering. I want to '
                    'build products where models are a component - the same way a queue or a '
                    'database is a component - and where the surrounding product still has the '
                    'discipline I already trust: clear problem statements, honest metrics, '
                    'versioned code, and a path from notebook to something someone can use.\n\n'
                    'There is more overlap than people admit. Debugging a bad train/test split '
                    'is not so different from debugging a bad queryset. Feature leakage is a '
                    'data-integrity bug. Hyperparameter search without a fixed evaluation story '
                    'is shipping without acceptance criteria. The habits that made Django apps '
                    'reliable - small interfaces, reproducible environments, writing down what '
                    '"done" means - are the same habits that keep ML work from becoming a '
                    'slideshow of accuracy numbers.\n\n'
                    'I am currently building an ML project for this portfolio. It will stay '
                    'unpublished until it earns a place: a concrete problem, a public repo (or '
                    'an honest proprietary note), and metrics I am willing to defend. Until then '
                    'the draft slot on the projects page is intentional - a reminder not to '
                    'perform competence before the work is ready.\n\n'
                    'If you are reading this as a recruiter or collaborator: my baseline is still '
                    'Python and Django in production. The direction of travel is classical ML '
                    'and the tooling around it - Pandas, NumPy, scikit-learn, careful EDA - with '
                    'TensorFlow/Keras as something I am actively learning, not pretending to '
                    'master overnight. I care about shipping systems that learn where learning '
                    'helps, and that stay maintainable where rules still win.'
                ),
                'external_url': '',
                'is_published': True,
            },
        )
