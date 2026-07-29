"""Authoritative project seed content for seed_portfolio."""

# Each project dict keys:
# slug, title, subtitle, short_description, description, problem, solution, impact,
# technical_highlights (newline-separated), roles_and_users (newline-separated),
# workflows (newline-separated), scope_notes (newline-separated),
# features (list of strings),
# tech (list of TechStack name strings that must exist),
# category, company, role, start_date (date or None), end_date, live_url, github_url,
# is_proprietary, is_featured, is_published, order

from datetime import date

TECH_STACK_ITEMS = [
    ('Python', 'primary'),
    ('Django', 'primary'),
    ('Django REST Framework', 'primary'),
    ('HTMX', 'primary'),
    ('Celery', 'primary'),
    ('python-docx', 'primary'),
    ('openpyxl', 'primary'),
    ('PostgreSQL', 'accent'),
    ('MySQL', 'accent'),
    ('SQLite', 'accent'),
    ('Redis', 'accent'),
    ('Pandas', 'accent'),
    ('NumPy', 'accent'),
    ('Matplotlib', 'accent'),
    ('scikit-learn', 'accent'),
    ('TensorFlow', 'accent'),
    ('Google Colab', 'accent'),
    ('Jupyter', 'accent'),
    ('JavaScript', 'warning'),
    ('HTML5', 'warning'),
    ('CSS3', 'warning'),
    ('Bootstrap', 'warning'),
    ('jQuery', 'warning'),
    ('Git', 'success'),
    ('GitHub', 'success'),
    ('Jira', 'success'),
    ('Confluence', 'success'),
    ('JQL', 'success'),
    ('WhiteNoise', 'success'),
    ('Gunicorn', 'success'),
]

PROJECTS = [
    # ------------------------------------------------------------------
    # 1. ISO Document Generator
    # ------------------------------------------------------------------
    {
        'slug': 'iso-audit-document-generator',
        'title': 'ISO Document Generator',
        'subtitle': 'Audit engagement platform for Concept QA Labs',
        'short_description': (
            'A Django web app that lets certification auditors enter an audit engagement once, '
            'complete a Certification Audit Report workflow, and auto-generate ~26 staged '
            'Word/PowerPoint documents instead of copy-pasting client data across templates by hand.'
        ),
        'description': (
            'ISO Document Generator is an internal operations platform built for Concept QA Labs '
            'auditors and staff. It centralizes audit engagement data, enforces a report '
            'review/finalize workflow, and fans that data into a catalog of certification documents '
            'across pre-audit, audit activities, post-audit, and surveillance stages.\n\n'
            'Users work in a browser UI (server-rendered Django templates with HTMX). Local '
            'development typically uses SQLite; production is configured for MySQL via PyMySQL on '
            'shared hosting, with optional Celery/Redis when enabled. Document generation defaults '
            'to a background thread when Celery is off.'
        ),
        'problem': (
            'Lead Auditors previously prepared each certification engagement\'s paperwork manually, '
            'opening the same pack of Word/PowerPoint templates and re-entering company, scope, '
            'dates, findings, and team details. A single field change forced regenerating or '
            're-editing multiple files, which wasted time and created inconsistency risk across '
            'the pack. There was no single source-of-truth workflow linking report drafting, team '
            'review, finalized content, and document generation.'
        ),
        'solution': (
            'The app treats the Certification Audit Report as the source of truth. Auditors capture '
            'the engagement once, draft and review the report section-by-section, finalize it, then '
            'generate phase-based document packs. Shared context (entry fields + report sections) is '
            'injected into Office templates via a generation pipeline (python-docx / python-pptx), '
            'with live progress polling and download/export logging.\n\n'
            'One engagement record gets an auto file number (e.g. US/IND-CQAL-{Mon}{YYYY}-{NNN}). '
            'Report state machine: Drafting → Review → Finalized (with reopen path). Phase-gated '
            'generation: Pre-Audit anytime; Audit & Post-Audit after finalize; Surveillance on demand. '
            'Role-aware access (Admin / Auditor / Viewer) plus per-engagement Lead Auditor assignment '
            'for notifications and ownership.'
        ),
        'impact': (
            'Replaces repetitive multi-template data entry with a single engagement + report editor '
            'that fans out into a seeded catalog of 26 active templates. Reduces inconsistency risk '
            'by generating documents from shared engagement/report context rather than independent '
            'manual copies. Adds operational controls: report review gates, generation status '
            'polling, document versioning on regenerate, export logging, and in-app notifications '
            'targeted to the engagement\'s Lead Auditor. Gives admins a Test Lab smoke suite for '
            'sanitizer, permissions, URL reverses, analytics API, DB connectivity, and related '
            'health checks.'
        ),
        'technical_highlights': (
            'Report-as-source-of-truth: AuditReport JSON sections + AuditEntry fields feed generators; '
            'Audit/Post-Audit packs gated on finalize\n'
            'Template catalog + token injectors: surgical {{placeholder}} injection into base Office '
            'files without rewriting layout\n'
            'Parallel fan-out generation via ThreadPoolExecutor; UI polls generation-status API\n'
            'Workflow status model (audit_pending → report_drafting → report_review → report_finalized '
            '→ docs_generated) with heal logic when packs are complete\n'
            'Notifications targeted by engagement ownership (Lead Auditor / Created By) rather than '
            'blasting all admins\n'
            'Security/ops: path-traversal guards on media, rich-text allow-list sanitizer, role mixins, '
            'admin-only Test Lab\n'
            'Seven Django apps: core, accounts, audits, documents, logs, notifications, testlab\n'
            'SQLite locally; MySQL/PyMySQL for shared-host production; Celery optional with thread fallback'
        ),
        'roles_and_users': (
            'Admin - full access; user management; Test Lab; operational controls\n'
            'Auditor - create/edit engagements, drive report workflow, generate documents\n'
            'Viewer - read engagement data and download documents (no mutate/generate)\n'
            'Lead Auditor - engagement assignment for ownership and notifications (not a fourth auth role)'
        ),
        'workflows': (
            'Create engagement → auto file number + empty Certification Audit Report\n'
            'Optionally generate Pre-Audit pack early from engagement fields\n'
            'Draft report sections → Submit for Review → Request Changes or Finalize\n'
            'After finalize: generate Audit Activities + Post-Audit packs; watch live pipeline → download\n'
            'Regenerate individual docs when needed (new DocumentVersion); Export All / stage ZIPs\n'
            'Surveillance 1 / 2 packs on demand (excluded from core completion %)\n'
            'Dashboard analytics + search + notifications for day-to-day ops'
        ),
        'scope_notes': (
            'Do not say PostgreSQL is the production database - runtime defaults to SQLite and '
            'production wiring uses MySQL/PyMySQL\n'
            'AI Assist / Audit Assist chat exist in code but are currently DISABLED - call them '
            'built, currently disabled, not live product features\n'
            'Calendar Gantt timeline UI is disabled; month/list calendar remains\n'
            'OneDrive upload is not implemented (smart download naming only)\n'
            'Seeded catalog is primarily DOCX + some PPTX - do not claim a live PDF or Excel pack pipeline\n'
            'Do not invent time-saved %, user counts, or revenue impact without measured evidence\n'
            'Lead Auditor is an engagement assignment, not a fourth auth role\n'
            'Claim WSGI + shared-hosting-aware design rather than a specific host brand unless confirmed'
        ),
        'features': [
            'Audit engagement wizard & record management (client, standard, scope, dates, team, sites, remote flags)',
            'IAF-based auditor-days calculator (head count → days, stage split, planning/offsite adjustments)',
            'Certification Audit Report editor (rich text via Quill, section cards, HTMX inline save)',
            'Report workflow actions: Submit for Review, Request Changes, Finalize, Reopen',
            'Document generation by phase (Pre-Audit, Audit Activities, Post-Audit) + surveillance packs',
            'Live generation pipeline UI with progress polling and pack completion UX',
            'Single / stage / bulk downloads with smart filenames; ExportLog audit trail',
            'Document version history on regenerate; entry revision history for record-level changes',
            'Dashboard KPIs + Chart.js analytics (docs over weeks, standards distribution)',
            'Global Cmd/Ctrl+K search; light/dark/system theme',
            'In-app notifications (workflow/docs), unread badge, monthly purge for shared hosting',
            'Admin Test Lab (smoke checks, demo seed, generation probe) and allow-list HTML sanitizer',
        ],
        'tech': [
            'Python', 'Django', 'HTMX', 'Bootstrap', 'MySQL', 'SQLite',
            'python-docx', 'Celery', 'Redis', 'JavaScript', 'HTML5', 'CSS3',
        ],
        'category': 'automation',
        'company': 'Concept QA Labs Pvt. Ltd.',
        'role': 'Full-Stack Developer',
        'start_date': date(2024, 9, 1),
        'end_date': None,
        'live_url': '',
        'github_url': '',
        'is_proprietary': True,
        'is_featured': True,
        'is_published': True,
        'order': 1,
    },

    # ------------------------------------------------------------------
    # 2. CQAL Certification Management System
    # ------------------------------------------------------------------
    {
        'slug': 'cqal-client-management-system',
        'title': 'CQAL Certification Management System',
        'subtitle': 'Internal operations platform for ISO & CMMI certification lifecycles',
        'short_description': (
            'Built an internal Django platform that replaces spreadsheet-driven certification ops - '
            'tracking ISO/CMMI client lifecycles, surveillance due dates, auditor assignment, '
            'reporting, and team workflows for a real certification body.'
        ),
        'description': (
            'CQAL Certification Management System is a production web application used by Concept QA '
            'Labs staff to manage certified-client companies across ISO and CMMI programs. It '
            'centralizes client records, certificate status, surveillance scheduling (SA1 / SA2 / RCA), '
            'role-based dashboards, Excel reporting, Kanban task boards, and leave approvals - '
            'deployed for internal use on conceptqalabs.org.\n\n'
            'This is not a public client portal. It is the operations backbone for employees, finance, '
            'lead auditors, and operations managers.'
        ),
        'problem': (
            'Certification bodies run multi-year client cycles: issue a certificate, then track '
            'surveillance audits, renewals, holds, suspensions, and withdrawals - often across many '
            'standards, accreditation bodies, and lead auditors. Without a dedicated system, that '
            'work usually lives in scattered Excel sheets that go stale, missed surveillance reminders '
            '(SA1 at +1 year, SA2 at +2, RCA at +3), weak visibility into who is due this month, and '
            'manual handoffs for tasks, leave, and reporting.'
        ),
        'solution': (
            'A Django-based Certification Management System that models the real domain '
            '(clients → ISO standards / CMMI models → audit cycle dates → status workflows) and gives '
            'operations teams structured client onboarding for ISO, CMMI, or both; automatic '
            'surveillance date calculation from certificate issue date; monthly ISO & CMMI trackers '
            'to surface what is due, update status/remarks, and trigger audit reminders; filtered '
            'client lists + Excel export for operational reporting; and role-aware dashboards with '
            'team tools (Kanban, leave workflow, employee directory).'
        ),
        'impact': (
            'Operational clarity - surveillance due dates and certificate statuses live in one system '
            'instead of fragmented sheets. Proactive follow-up - monthly trackers + reminder logic '
            '(due date - 45 days) help reduce missed client touchpoints. Faster reporting - '
            'multi-filter client views and styled Excel exports for audits/ops reviews. Better team '
            'coordination - Kanban boards, activity logging, and leave approval via email. Production '
            'deployment - HTTPS-hardened staff application used under Concept QA Labs\' domain.'
        ),
        'technical_highlights': (
            'Classic Django MVT monolith - strong fit for internal ops tools\n'
            'Domain-driven models: ClientsMasterList → ClientStandard (ISO) / ClientModel (CMMI)\n'
            '~40 business routes, soft-delete workflows, 60+ migrations (iterative product evolution)\n'
            'JSON endpoints for Kanban interactions; server-rendered UI for everything else\n'
            'Production security posture: SSL redirect, HSTS, session expiry on browser close\n'
            'MySQL backend with Django Auth + custom UserRole / Profile'
        ),
        'roles_and_users': (
            'Employee - clients, reports, BI view, leave, Kanban\n'
            'Finance Manager - above + leave approve/reject\n'
            'Lead Auditor - ops views + LA-oriented modules\n'
            'Operations Manager - full ops + team management'
        ),
        'workflows': (
            'Client onboarding: add company/contact + service ISO / CMMI / BOTH; add standards or '
            'models; issue date → auto SA1/SA2/RCA\n'
            'ISO Monthly Tracker: filter by year/month/auditor; update status/remarks; mailto audit reminders\n'
            'Soft delete: delete → trash list → restore or permanent delete\n'
            'Leave: employee applies → email Finance Manager → approve/reject → notify employee\n'
            'Kanban: create/assign tasks → drag across To Do → In Progress → In Review → Assigned → Done'
        ),
        'scope_notes': (
            'Internal staff tool on conceptqalabs.org - not a public client portal\n'
            'Invoice module, appraisal/training workflows, and BI trend charts that are placeholders '
            'or static should not be claimed as finished product features\n'
            'Do not invent client counts, time-saved %, or revenue impact without CQAL-measured evidence'
        ),
        'features': [
            'Client lifecycle management - create/edit clients with ISO, CMMI, or both; soft-delete → trash → restore',
            'ISO engagement tracking - standards, audit types (CA, SA1, SA2, RCA), accreditation bodies, certificate IDs/URLs, lead auditor assignment',
            'CMMI engagement tracking - DEV / SVC models, maturity levels ML2-ML5, appraisal IDs, certificate image uploads',
            'ISO & CMMI monthly trackers - filter by month/year/auditor; update workflow status & remarks; mailto audit reminders',
            'Advanced filtering & styled Excel export via openpyxl',
            'Ops dashboard - KPIs, status breakdowns, charts, recent activity feed',
            'Kanban task manager - drag-and-drop status updates via JSON endpoints',
            'Leave management - apply → email Finance Manager → approve/reject → notify employee',
            'Role-based navigation - Employee, Finance Manager, Lead Auditor, Operations Manager',
            'Team directory - employee records for assignment and ops visibility',
        ],
        'tech': [
            'Python', 'Django', 'MySQL', 'Bootstrap', 'JavaScript',
            'HTML5', 'CSS3', 'jQuery', 'openpyxl',
        ],
        'category': 'web',
        'company': 'Concept QA Labs Pvt. Ltd.',
        'role': 'Full-Stack Developer',
        'start_date': date(2023, 6, 1),
        'end_date': None,
        'live_url': 'https://conceptqalabs.org/',
        'github_url': '',
        'is_proprietary': True,
        'is_featured': True,
        'is_published': True,
        'order': 2,
    },

    # ------------------------------------------------------------------
    # 3. Certified Entity (CQAL Client Manager)
    # ------------------------------------------------------------------
    {
        'slug': 'certified-entity',
        'title': 'Certified Entity (CQAL Client Manager)',
        'subtitle': 'Digital certification registry and client portal for Concept QA Labs',
        'short_description': (
            'A Django web app that lets Concept QA Labs staff manage certified entities and ISO '
            'certifications, then lets those clients activate accounts via QR/token links to view '
            'their certificate details online.'
        ),
        'description': (
            'Certified Entity is an internal + client-facing certification management system built '
            'for Concept Quality Assurance Labs (CQAL). Staff use a secure admin UI to create company '
            'records, attach management-system certifications (e.g. ISO 9001, ISO 27001, ISO 20000), '
            'track cycles and statuses, and generate QR codes that point to a client activation portal.\n\n'
            'Certified clients receive an activation link/QR, register with email + password, and then '
            'log in to view their certification details, cycle history, and related company information. '
            'The project was configured for production on cqalcertsearch.com using Phusion Passenger '
            '(WSGI) with MySQL.'
        ),
        'problem': (
            'Certification bodies issue and renew ISO certificates across many client organizations, '
            'accreditation bodies, and multi-year cycles. Without a dedicated system, that work '
            'typically lives in spreadsheets, PDFs, and email threads - which makes it hard to keep a '
            'single source of truth, track re-certification cycles and expiry consistently, give '
            'clients a trustworthy digital way to access certificate status, and reduce back-and-forth '
            'when clients ask for verification.'
        ),
        'solution': (
            'This project centralizes certified-entity and certification records in a Django '
            'application with two clearly separated audiences: a staff portal (Django auth) for '
            'creating entities, entering certifications via formsets, browsing/searching, and editing '
            'via Django Admin; and a client portal (custom ClientUser + session auth) for token/QR-'
            'driven activation, login, and authenticated viewing.\n\n'
            'On save, the system generates a unique entity ID, a public UUID token, and a QR code '
            'pointing at the client activation URL. Certification expiry and surveillance dates are '
            'calculated automatically from the issue date (surveillance at +1/+2 years; expiry at +3 years).'
        ),
        'impact': (
            'Single operational registry for certified companies and their ISO certificates. Structured '
            'multi-cycle certification history (up to 8 cycles) per standard / accreditation body. '
            'Client self-service access to certificate details via activation link or QR code. Reduced '
            'dependency on ad-hoc file sharing for routine "show me my certificate" requests. Clearer '
            'status visibility (Active, Suspended, Expired, Withdrawn, etc.) for staff and clients. '
            'No quantified usage metrics are documented in the repository.'
        ),
        'technical_highlights': (
            'Three Django apps separate concerns: login (staff auth), certified_clients (domain + staff UI), '
            'client_auth (client identity + portal)\n'
            'Domain model: CertifiedEntity (1) → Certifications (many), with indexes and unique_together '
            'for cycle identity\n'
            'Public access control via UUID public_token (not guessable sequential IDs alone)\n'
            'Client auth isolated from Django User - avoids mixing CB staff accounts with client accounts\n'
            'QR generation on entity save; absolute activation URLs for staff outreach\n'
            'Prefetch + ordered querysets for reliable template regrouping of cycles by standard\n'
            'Transactional create flow for entity + certifications (rolls back if formset invalid)\n'
            'Production WSGI entrypoint and ALLOWED_HOSTS / SITE_DOMAIN wired for the CQAL domain'
        ),
        'roles_and_users': (
            'CQAL staff / internal users - Django User login; create/list entities, enter certifications, '
            'view details, edit via Admin, send activation mailto links\n'
            'Certified clients - ClientUser (email + password) after token activation; view certifications '
            'and cycle history\n'
            'Superuser / Admin operators - full CRUD, QR regenerate, client activate/deactivate'
        ),
        'workflows': (
            'Staff onboards a company: create Certified Entity → add certification rows → system assigns '
            'unique_id, public_token, and QR → share activation via mailto and/or QR\n'
            'Client activates: open token URL or scan QR → register (if new) or login → view certifications '
            'and cycle history\n'
            'Staff reviews/updates: browse/search entity list; open certificate detail (staff bypass); '
            'edit via Django Admin'
        ),
        'scope_notes': (
            'live_url left blank - host cqalcertsearch.com was observed as Account Suspended at brief '
            'time; verify uptime before claiming currently live\n'
            'Say client portal via QR/token activation, not public certification search engine\n'
            'Activation outreach is a mailto deep link, not automated SMTP onboarding\n'
            'Editing is routed to Django Admin, not a full custom CRUD UI for every action\n'
            'Entity table delete icon is a UI stub (confirm dialog only; no wired delete action)\n'
            'Vendor chart/editor bundles in templates are not product dashboards you implemented\n'
            'No usage metrics exist in-repo - do not invent them'
        ),
        'features': [
            'Certified entity management - company identity, address, optional additional site, confidentiality flag, unique sequential IDs',
            'Certification records - ISO standards, accreditation bodies (ANAB, NABCB, ACCAB), certificate numbers, scope, status',
            'Cycle tracking - cycles 1-8 with uniqueness per entity + standard + accreditation body + cycle',
            'Automatic date calculation - surveillance 1/2 and expiry derived from issue date',
            'QR code generation & download - entity-level QR linking to client activation URL',
            'Staff entity list - search, activation status, certification badges, mailto activation helper',
            'Inline multi-certification entry - Django formsets with JS helpers to add cycles',
            'Client activation & login - separate ClientUser model isolated from staff Django users',
            'Authenticated client certificate view - grouped by standard, with cycle-history modals',
            'Staff bypass - logged-in internal users can open certificate detail without client login',
            'Django Admin - entities, certifications, client users, QR regeneration, bulk activate/deactivate',
        ],
        'tech': [
            'Python', 'Django', 'MySQL', 'SQLite', 'Bootstrap',
            'JavaScript', 'HTML5', 'CSS3',
        ],
        'category': 'web',
        'company': 'Concept QA Labs Pvt. Ltd.',
        'role': 'Full-Stack Developer',
        'start_date': date(2023, 8, 1),
        'end_date': date(2024, 2, 1),
        'live_url': '',
        'github_url': '',
        'is_proprietary': True,
        'is_featured': True,
        'is_published': True,
        'order': 3,
    },

    # ------------------------------------------------------------------
    # 4. Concept QA Labs Corporate Website
    # ------------------------------------------------------------------
    {
        'slug': 'concept-qa-labs-corporate-website',
        'title': 'Concept QA Labs Corporate Website',
        'subtitle': 'Company website and public ISO certificate directory',
        'short_description': (
            'A Django company website that markets CQAL\'s CMMI/ISO services and lets visitors '
            'verify ISO certificates by category and certificate ID - with admin-managed updates '
            'and testimonials.'
        ),
        'description': (
            'This project is the official web presence for Concept Quality Assurance Labs (CQAL), '
            'an ISACA-licensed CMMI Premium Partner and an ISO / CMMI appraisal and certification '
            'company. The application serves two audiences: prospective clients and partners browsing '
            'services, accreditations, training, team, and contact information; and certificate holders '
            'or third parties who need to look up an ISO certificate image by category and ID.\n\n'
            'Content editors use Django Admin. The stack is production-oriented (Gunicorn + WhiteNoise). '
            'Live site: https://conceptqalabs.org/.'
        ),
        'problem': (
            'Prospective clients needed a credible, structured place to understand CQAL\'s CMMI and ISO '
            'offerings, accreditations, training, and how to engage the team. Certificate stakeholders '
            'needed a simple way to verify whether a given ISO certificate exists under CQAL\'s published '
            'directory - without emailing support for every lookup. Non-technical staff needed to publish '
            'short update posts and client testimonials without a developer deploying HTML changes.'
        ),
        'solution': (
            'A single Django application delivers a responsive marketing site (home, about, CMMI, ISO '
            'standards pages, AI & ML services page, accreditations, gallery, careers, contact) and an '
            'ISO Certificate Directory at /directory/. The directory accepts a category + certificate ID, '
            'validates input, and displays the matching certificate image from static storage when present. '
            'Django Admin drives Update pages and an active testimonials carousel on the homepage. '
            'WhiteNoise serves static assets under Gunicorn for deployable production use.'
        ),
        'impact': (
            'Public self-serve certificate lookup across seven ISO category folders backed by certificate '
            'image files in static storage. Non-developers can update homepage testimonials and Recent '
            'Posts / Updates pages via Admin without code changes. One deployable codebase covers '
            'marketing education and operational verification. Production hygiene: DEBUG off by default, '
            'env-based SECRET_KEY / ALLOWED_HOSTS, WhiteNoise + Gunicorn, basic automated tests for '
            'testimonials.'
        ),
        'technical_highlights': (
            'Classic Django MVT: cqal app (models, views, forms, admin, templates) + project package\n'
            'Certificate lookup: form validation + RegexValidator on certificate ID to avoid path '
            'traversal; filesystem existence check under CERTIFICATES_ROOT\n'
            'WhiteNoise middleware with WHITENOISE_USE_FINDERS so static assets work with DEBUG off '
            'under Gunicorn\n'
            'Content split: mostly static educational pages + a thin CMS surface (Update models + '
            'Testimonials) for frequent edits\n'
            'Test coverage focused on testimonials (model helpers, homepage filtering, seed command)'
        ),
        'roles_and_users': (
            'Public visitors / prospective clients - browse services, team, gallery, careers, contact\n'
            'Certificate verifiers - search the ISO Certificate Directory\n'
            'CQAL content editors / admins - manage Updates and Testimonials via Django Admin\n'
            'Job applicants - view open roles and email careers (no in-app application system)'
        ),
        'workflows': (
            'Explore services: homepage → Know More / CMMI / ISO / AI / Accreditations → contact\n'
            'Verify a certificate: /directory/ → choose ISO category → enter Certificate ID → view image '
            'or not-found guidance\n'
            'Publish an update: Admin edits Update pages → public pages and homepage cards reflect changes\n'
            'Manage social proof: Admin creates/activates testimonials → homepage carousel shows active only\n'
            'Deploy: install requirements → migrate → collectstatic → run Gunicorn with production env vars'
        ),
        'scope_notes': (
            'This is not an AI/ML application - /ai/ is a marketing/services description page only\n'
            'Certificate verification is image-file lookup by category + ID, not cryptographic verification '
            'or a relational certificate registry API\n'
            'Contact and careers are informational (mailto / phone / static role table) - no contact-form '
            'backend or applicant portal\n'
            'Auth is Django Admin for staff only - no public user accounts\n'
            'Database is SQLite by default - do not claim PostgreSQL/Redis/Celery/DRF\n'
            'Do not present company marketing claims (e.g. 200+ clients) as software-project metrics\n'
            'Confirm with stakeholders before claiming this exact Django build is what currently runs '
            'on conceptqalabs.org'
        ),
        'features': [
            'Marketing pages: home, CMMI overview, ISO standards, AI & ML services, accreditations, gallery, team, careers, contact',
            'ISO Certificate Directory (/directory/): search by category + certificate ID; shows image or contact-support message',
            'Supported directory categories across ISO 9001, 20000, and 27001 variants',
            'Admin-managed Update content pages linked from homepage Recent Posts',
            'Admin-managed Testimonials model rendered in a Swiper carousel when active',
            'Client logo carousel and static careers table (mailto apply)',
            'Responsive Bootstrap UI with AOS, Swiper, GLightbox, PureCounter',
            'Management command for sample testimonials; unit tests for testimonial model/homepage behavior',
        ],
        'tech': [
            'Python', 'Django', 'SQLite', 'Bootstrap', 'HTML5', 'CSS3',
            'JavaScript', 'jQuery', 'WhiteNoise', 'Gunicorn',
        ],
        'category': 'website',
        'company': 'Concept QA Labs Pvt. Ltd.',
        'role': 'Full-Stack Developer',
        'start_date': date(2022, 10, 1),
        'end_date': date(2023, 3, 1),
        'live_url': 'https://conceptqalabs.org/',
        'github_url': '',
        'is_proprietary': True,
        'is_featured': True,
        'is_published': True,
        'order': 4,
    },

    # ------------------------------------------------------------------
    # 5. Jira Workflow & Automation System
    # ------------------------------------------------------------------
    {
        'slug': 'jira-automation-audit-tracking-system',
        'title': 'Jira Workflow & Automation System',
        'subtitle': 'ISO & CMMI service delivery operations on interconnected Jira boards',
        'short_description': (
            'Centralized Jira ecosystem for Concept QA Labs that replaces Excel trackers and email '
            'follow-ups with automated boards spanning tracking, consulting, auditing, finance, '
            'and certification.'
        ),
        'description': (
            'Concept QA Labs established a centralized Jira-based digital ecosystem to manage ISO and '
            'CMMI service delivery in a structured, automated, and auditable manner. The system replaces '
            'traditional Excel trackers and email follow-ups with interconnected Jira projects that handle '
            'client onboarding, project execution, invoicing, certification, and ongoing surveillance or '
            'appraisal renewals.\n\n'
            'Each department operates on its own dedicated board. Automation rules move information across '
            'teams without manual intervention, so every phase of a client\'s lifecycle - from initial '
            'registration to certification issuance - is captured and tracked inside Jira, with Confluence '
            'documentation supporting process standards.'
        ),
        'problem': (
            'Manual coordination across ISO and CMMI client lifecycles lived in spreadsheets and email: '
            'missed surveillance and re-appraisal deadlines, inconsistent handoffs between tracking, '
            'consulting, audit/appraisal, finance, and certification committees, and weak management '
            'visibility into who had responded, who was in pipeline, and which invoices or certificates '
            'were blocked.'
        ),
        'solution': (
            'Configured a multi-project Jira ecosystem with dedicated boards (ISO/CMMI Trackers, PIPE, '
            'Consultant, Lead Auditor / Lead Appraiser, Training, Finance, Certification) plus chained '
            'Automation rules and advanced JQL filters. New and existing client flows auto-create epics, '
            'stories, and subtasks from forms; finance gates milestone invoicing; certification board '
            'enforces finance clearance before issue; and tracker boards auto-calculate next-cycle due '
            'dates with multi-stage reminder automations.'
        ),
        'impact': (
            'End-to-end operational backbone for ISO and CMMI engagements: centralized client data, '
            'role-based accountability across departments, automated reminders so certification and '
            'appraisal deadlines are harder to miss, and management visibility into pipeline, finance, '
            'and certification readiness without spreadsheet status chasing. Custom dashboards and '
            'filter-based gadgets support stakeholder reporting.'
        ),
        'technical_highlights': (
            'Multi-project board architecture: Trackers, PIPE, Consultant, Lead Auditor/Appraiser, '
            'Training, Finance, Certification\n'
            'Form-driven epic/story/subtask creation with service-type-specific story templates '
            '(ISO vs CMMI DEV/SVC/DEV+SVC)\n'
            'Chained Jira Automation for cross-board transitions, email notifications, and date field updates\n'
            'Finance gates: Required task? and Milestone Payment fields control which work appears and invoices\n'
            'Certification board blocks finance clearance until Finance Approval is set\n'
            'ISO 3-year cycle fields: Certificate Issued, SA1, SA2 auto-dates; CMMI re-appraisal at +3 years\n'
            'Advanced JQL year filters and custom dashboards for ops and management views\n'
            'Confluence documentation for process standards and board usage'
        ),
        'roles_and_users': (
            'Tracking Committee - ISO/CMMI tracker boards, reminders, dropped-client recovery\n'
            'Management - PIPE board visibility, agreement and assignment notifications\n'
            'Consultants - delivery stories on Consultant board through milestone reached\n'
            'Lead Auditor / Lead Appraiser - audit or appraisal queue through Done / Appraisal Completed\n'
            'Training team - service-type training stories and ATM nomination flow\n'
            'Finance Manager - milestone invoice pending, country-routed invoice fields, finance approval\n'
            'Certification Committee - review, approval, issue; gates on finance clearance'
        ),
        'workflows': (
            'New ISO/CMMI client: form → epic/story/subtask in Trackers → Client Responded → PIPE epic '
            '→ Agreement Signed → Tasks & Milestones review (auto stories) → finance sets Required/Milestone flags\n'
            'Delivery: Assign Consultant/LA → required stories on Consultant board → Milestone Reached → '
            'Finance Invoice Pending (India/USA routing)\n'
            'Audit/Appraisal: epic on Lead Auditor or Lead Appraiser board through planned → in progress → '
            'Done / Appraisal Completed → Certification Committee Review\n'
            'Certification: committee approval auto-stamps issue/end dates; Finance Approval required before '
            'clearance; Issued notifies Consultant and LA\n'
            'ISO existing clients: 3-year CA → SA1 → SA2 cycle with 45/30/15-day reminder automations; '
            'non-response → Dropped → On Hold (6 mo) → Inactive (1 yr) recovery\n'
            'CMMI existing clients: appraisal → re-appraisal at +3 years with 90/45/25-day reminders\n'
            'Cycle loop: on certificate/appraisal completion, next audit type and due date auto-created '
            'back into Tracker backlog\n'
            'Training path (CMMI): required training stories → Training board → ATM Nomination → '
            'Milestone Reached → Finance when milestone payment is Yes'
        ),
        'scope_notes': (
            'Configuration and automation work inside Jira Cloud/Server - not a custom-coded application\n'
            'Do not invent dashboard counts, time-saved %, or client volumes without measured evidence\n'
            'Person-specific invoice routing in rules reflects CQAL org practice, not a portable product feature\n'
            'Portfolio summary is a distillation of a large internal workflow doc - not every edge-case rule'
        ),
        'features': [
            'Interconnected ISO and CMMI Tracker boards with year-filtered Kanban views',
            'PIPE board for responded clients through agreement, milestone review, and assignment',
            'Service-type story templates for ISO audits and CMMI DEV / SVC / DEV+SVC training paths',
            'Chained Automation rules for cross-board epic/story creation and stakeholder email notifications',
            'Finance board with Invoice Pending, country-routed invoice fields, and certification finance gate',
            'Lead Auditor and Lead Appraiser boards for Stage 1/2 audits and appraisal lifecycle',
            'Certification Committee board with review → approval → issued and finance clearance lock',
            'Automated ISO reminders at 45/30/15 days and CMMI reminders at 90/45/25 days before due dates',
            'Dropped-client recovery: On Hold (6-month) and Inactive (1-year) follow-up automations',
            'Auto next-cycle subtask creation after certificate or appraisal completion',
            'Custom JQL filters and management/ops dashboards with KPI and filter-based gadgets',
            'Confluence process documentation aligned to board ownership',
        ],
        'tech': ['Jira', 'JQL', 'Confluence'],
        'category': 'automation',
        'company': 'Concept QA Labs Pvt. Ltd.',
        'role': 'Jira Administrator',
        'start_date': date(2023, 1, 1),
        'end_date': None,
        'live_url': '',
        'github_url': '',
        'is_proprietary': True,
        'is_featured': True,
        'is_published': True,
        'order': 5,
    },

    # ------------------------------------------------------------------
    # 6. Process Quality Excellence Platform
    # ------------------------------------------------------------------
    {
        'slug': 'process-quality-excellence-platform',
        'title': 'Process Quality Excellence (PQE)',
        'subtitle': 'Multi-page marketing website for ISO & CMMI consulting services',
        'short_description': (
            'A clean, multi-page web presence that explains ISO (9001, 27001, 20000, 14001) and CMMI '
            '(DEV, SVC, DEV+SVC) consulting services and routes prospects to contact the firm.'
        ),
        'description': (
            'Process Quality Excellence is a static, multi-page marketing website built to communicate '
            'consulting services around ISO quality, security, IT service, and environmental standards '
            'and CMMI process maturity models. It targets organizations seeking certification readiness '
            'and process improvement guidance.\n\n'
            'The site is branded as PQE, with contact details for Concept Quality Assurance Labs in '
            'Hyderabad. Technically it is a front-end-only site (HTML/CSS/JS) customized from the '
            'BootstrapMade FlexStart template (Bootstrap 5). Live URL: https://pqellp.com.'
        ),
        'problem': (
            'Consulting firms often struggle to clearly differentiate multiple ISO and CMMI service '
            'lines for non-specialist buyers, give prospects a scannable path from what we do to how '
            'to reach us, present domain-specific offerings without burying them in a single brochure '
            'page, and maintain a professional, mobile-friendly brand presence that matches enterprise '
            'consulting expectations.'
        ),
        'solution': (
            'PQE solves this with a structured service catalog site: a home overview, dedicated pages '
            'per ISO standard and CMMI model, and a contact page with firm location and contact '
            'channels. Navigation uses dropdown menus for ISO Consulting and CMMI Consulting so '
            'visitors can jump directly to the standard or model they care about, then convert via '
            'email/phone.'
        ),
        'impact': (
            'Creates a clear digital catalog of 4 ISO and 3 CMMI consulting offerings. Separates '
            'services into dedicated pages with Key Services and Benefits for buyer education. Provides '
            'a consistent brand frame (PQE logo/nav, shared footer/contact block) across pages. Supports '
            'mobile browsing via responsive Bootstrap layout. Centralizes contact CTAs for lead capture. '
            'No quantified traffic or conversion metrics appear in the repository.'
        ),
        'technical_highlights': (
            'Multi-page static site with shared layout patterns duplicated across HTML pages\n'
            'Structured information architecture: standards and maturity models mapped to discrete routes\n'
            'Template customization: adapted FlexStart into a domain-specific consulting catalog\n'
            'Responsive front-end polish: sticky header, mobile menu, AOS motion, SCSS variables/sections\n'
            'Maintainable content pattern: each service page follows Key Services / Benefits structure\n'
            'Hosting-friendly packaging: pure static assets suitable for conventional web hosting'
        ),
        'roles_and_users': (
            'Primary users - business owners, quality/compliance leads, IT managers, procurement '
            'stakeholders evaluating ISO/CMMI consulting partners\n'
            'Secondary users - internal sales/consulting staff directing prospects to specific standard pages\n'
            'Site operators - content/web maintainers updating copy and contact details (no CMS or RBAC)'
        ),
        'workflows': (
            'Visitor discovers offerings: home → ISO + CMMI overview → dropdown → standard/model page\n'
            'Visitor evaluates a service: read intro → Key Services → Benefits\n'
            'Visitor converts: Contact page or footer → address/phone → mailto links\n'
            'Broken URL handling: unknown path → 404.shtml'
        ),
        'scope_notes': (
            'Frontend / static marketing site only - not a full-stack platform, SaaS app, CMS, or '
            'consulting workflow tool\n'
            'No backend APIs, database, authentication, dashboards, or user accounts\n'
            'No live contact form submission on the contact page (vendored php-email-form unused as UI)\n'
            'Much of the UI chrome and JS behaviors come from the BootstrapMade FlexStart template; '
            'value-add is customization, content structure, and domain packaging\n'
            'Do not invent traffic, revenue, certification counts, or conversion metrics without evidence'
        ),
        'features': [
            'Home hero explaining ISO and CMMI consulting scope',
            'ISO Consulting pages: ISO 9001:2015, ISO 27001:2022, ISO 20000:2018, ISO 14001',
            'CMMI Consulting pages: CMMI DEV, CMMI SVC, CMMI DEV+SVC',
            'Per-service Key Services and Benefits of Consulting content blocks',
            'Dropdown navigation + breadcrumb trail on inner pages',
            'Contact page with address, phone, and email links',
            'Shared footer contact block on most pages',
            'Scroll-triggered animations (AOS), sticky header, scroll-to-top',
            'Responsive / mobile navigation',
            'Custom 404 error page (404.shtml)',
        ],
        'tech': ['HTML5', 'CSS3', 'JavaScript', 'Bootstrap'],
        'category': 'website',
        'company': 'Concept QA Labs Pvt. Ltd.',
        'role': 'Frontend Developer',
        'start_date': date(2023, 4, 1),
        'end_date': date(2023, 7, 1),
        'live_url': 'https://pqellp.com',
        'github_url': '',
        'is_proprietary': True,
        'is_featured': True,
        'is_published': True,
        'order': 6,
    },

    # ------------------------------------------------------------------
    # 7. Personal Portfolio
    # ------------------------------------------------------------------
    {
        'slug': 'personal-portfolio',
        'title': 'Personal Portfolio',
        'subtitle': 'Minimal dark Django portfolio for work and writing',
        'short_description': (
            'Minimal dark Django portfolio with SEO, Unfold admin, self-hosted fonts, and WhiteNoise - '
            'built to showcase work without framework noise.'
        ),
        'description': (
            'A typography-first personal portfolio built with Django. Content is managed in the admin '
            '(projects, skills, experience, writing), served with self-hosted fonts and WhiteNoise for '
            'static assets, and structured for clear SEO (meta tags, Person JSON-LD, skip-to-content). '
            'The design stays intentionally quiet so the work and writing do the talking.'
        ),
        'problem': (
            'I needed a place to present client and personal work honestly - with editable content, '
            'decent SEO, and a calm dark layout - without shipping another generic template site.'
        ),
        'solution': (
            'Built a small Django app with Unfold admin, model-driven sections, manifest static files '
            'via WhiteNoise, and a minimal dark UI. Projects carry problem / solution / impact and '
            'honest scope notes so recruiters can scan outcomes, not just screenshots.'
        ),
        'impact': (
            'One place to keep projects, skills, and writing current. Public source on GitHub. '
            'Deploy-ready structure once production hardening is done.'
        ),
        'technical_highlights': (
            'Django + Unfold admin for model-driven projects, skills, experience, and posts\n'
            'WhiteNoise + self-hosted fonts for static asset serving without a separate CDN\n'
            'SEO basics: meta tags, Person JSON-LD, sitemap, robots.txt, RSS feed\n'
            'Case-study fields: problem, solution, impact, technical highlights, workflows, scope notes\n'
            'Management command seed_portfolio for reproducible local content'
        ),
        'roles_and_users': (
            'Recruiters and collaborators - browse projects, experience, and writing\n'
            'Site owner (me) - update content via Unfold Django admin'
        ),
        'workflows': (
            'Visitor lands on home → scan featured projects → open case study detail\n'
            'Owner updates Project / Skill / Experience / Post in admin → public pages reflect changes\n'
            'Optional: run seed_portfolio to reset or refresh demo content locally'
        ),
        'scope_notes': (
            'Public GitHub repo - not a proprietary client deliverable\n'
            'Deployment intentionally deferred until content and hardening are finished\n'
            'Design stays minimal: no heavy animations, gradients, or marketing chrome beyond subtle dots'
        ),
        'features': [
            'Minimal dark, typography-first layout with subtle dot background',
            'Content managed via Unfold Django admin (projects, skills, experience, posts)',
            'SEO basics: meta tags, Person JSON-LD, skip-to-content, sitemap, robots, RSS',
            'Self-hosted fonts and WhiteNoise for static asset serving',
            'Problem / solution / impact plus technical highlights, workflows, and scope notes on case studies',
            'Contact cards for Email, LinkedIn, GitHub, X, and résumé',
        ],
        'tech': [
            'Python', 'Django', 'PostgreSQL', 'WhiteNoise',
            'HTML5', 'CSS3', 'JavaScript', 'Git', 'GitHub',
        ],
        'category': 'web',
        'company': '',
        'role': 'Full-Stack Developer',
        'start_date': date(2025, 1, 1),
        'end_date': None,
        'live_url': '',
        'github_url': 'https://github.com/G-Laluyashwanth/portfolio',
        'is_proprietary': False,
        'is_featured': True,
        'is_published': True,
        'order': 7,
    },

    # ------------------------------------------------------------------
    # 8. ML project draft (unpublished)
    # ------------------------------------------------------------------
    {
        'slug': 'ml-project-draft',
        'title': 'ML project (draft)',
        'subtitle': 'Placeholder until metrics and a public story are ready',
        'short_description': (
            'Placeholder for the machine-learning project currently in progress - publish when '
            'metrics and a public repo are ready.'
        ),
        'description': (
            'This is a draft entry reserved for an ML project I am building for the portfolio. It will '
            'stay unpublished until there is a clear problem statement, honest metrics, and a public '
            'repository (or an explicit note that the work is proprietary). The goal is not to pad the '
            'site with unfinished work - it is to leave a slot that becomes real when the model and '
            'evaluation story are ready to ship.'
        ),
        'problem': '',
        'solution': '',
        'impact': '',
        'technical_highlights': '',
        'roles_and_users': '',
        'workflows': '',
        'scope_notes': (
            'Unpublished draft - do not treat as a shipped portfolio project\n'
            'Will be filled when problem, metrics, and repo (or proprietary note) are ready'
        ),
        'features': [],
        'tech': ['Python', 'Pandas', 'NumPy', 'scikit-learn', 'Matplotlib'],
        'category': 'ml',
        'company': '',
        'role': 'ML Engineer',
        'start_date': None,
        'end_date': None,
        'live_url': '',
        'github_url': '',
        'is_proprietary': False,
        'is_featured': False,
        'is_published': False,
        'order': 99,
    },
]
