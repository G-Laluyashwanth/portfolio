from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class TechStack(models.Model):
    """Reusable tech tag (Python, Django, PostgreSQL, etc.) shown as chips on cards."""
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    color = models.CharField(
        max_length=20,
        default='primary',
        help_text='CSS color hint: primary, accent, success, warning, or hex like #1f67ff'
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Tech Stack Item'
        verbose_name_plural = 'Tech Stack Items'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    """A featured portfolio project."""

    CATEGORY_CHOICES = [
        ('web', 'Web Application'),
        ('website', 'Corporate Website'),
        ('ml', 'Machine Learning'),
        ('automation', 'Automation / Tooling'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    subtitle = models.CharField(
        max_length=240,
        blank=True,
        help_text='Short subtitle under the title on the case study page.',
    )
    short_description = models.CharField(
        max_length=400,
        help_text='One-liner shown on home cards and as the case-study lead.',
    )
    description = models.TextField(help_text='Overview shown on the detail page.')
    problem = models.TextField(blank=True, help_text='What problem did this solve?')
    solution = models.TextField(blank=True, help_text='How did you solve it?')
    impact = models.TextField(blank=True, help_text='Measurable outcomes / capability outcomes.')
    technical_highlights = models.TextField(
        blank=True,
        help_text='Architecture / technical highlights. One point per line.',
    )
    roles_and_users = models.TextField(
        blank=True,
        help_text='Who uses the system. One role per line.',
    )
    workflows = models.TextField(
        blank=True,
        help_text='Core workflows. One step or flow per line.',
    )
    scope_notes = models.TextField(
        blank=True,
        help_text='Honest scope notes (what this is / is not). One note per line.',
    )

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='web')
    company = models.CharField(max_length=160, blank=True, help_text='e.g. Concept QA Labs Pvt. Ltd.')
    role = models.CharField(max_length=120, blank=True, default='Full-Stack Developer')

    cover_image = models.ImageField(upload_to='projects/covers/', blank=True, null=True)
    tech_stack = models.ManyToManyField(TechStack, related_name='projects', blank=True)

    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    is_proprietary = models.BooleanField(
        default=False,
        help_text='If True and github_url is empty, show "Source private" on the site.',
    )

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True, help_text='Leave blank for ongoing.')

    is_featured = models.BooleanField(default=True, help_text='Show on home page.')
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})

    @property
    def is_ongoing(self):
        return self.end_date is None

    @property
    def impact_headline(self):
        """First sentence of the impact statement - the outcome recruiters scan for."""
        if not self.impact:
            return ''
        first = self.impact.strip().split('. ')[0].strip().rstrip('.')
        return f'{first}.' if first else ''

    def _lines(self, value):
        return [line.strip() for line in (value or '').splitlines() if line.strip()]

    def get_technical_highlights_list(self):
        return self._lines(self.technical_highlights)

    def get_roles_list(self):
        return self._lines(self.roles_and_users)

    def get_workflows_list(self):
        return self._lines(self.workflows)

    def get_scope_notes_list(self):
        return self._lines(self.scope_notes)


class ProjectFeature(models.Model):
    """Bullet-point features / outcomes shown on project cards and detail pages."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='features')
    text = models.CharField(max_length=240)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:60]


class ProjectImage(models.Model):
    """Additional screenshots for the project detail page."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=240, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.caption or f'Image for {self.project.title}'
