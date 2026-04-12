from django.db import models


class Experience(models.Model):
    """Work experience entry."""

    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ]

    company = models.CharField(max_length=160)
    role = models.CharField(max_length=160)
    employment_type = models.CharField(
        max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='full_time'
    )
    location = models.CharField(max_length=120, blank=True)
    company_url = models.URLField(blank=True)
    company_logo = models.ImageField(upload_to='experience/logos/', blank=True, null=True)

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text='Leave blank for current role.')

    summary = models.TextField(help_text='Short overview shown on the timeline.')
    responsibilities = models.TextField(
        blank=True,
        help_text='One bullet per line — shown as a list on detail.'
    )
    technologies = models.CharField(
        max_length=400,
        blank=True,
        help_text='Comma-separated list, e.g. Python, Django, PostgreSQL'
    )

    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-start_date', 'order']
        verbose_name = 'Work Experience'
        verbose_name_plural = 'Work Experience'

    def __str__(self):
        return f'{self.role} @ {self.company}'

    @property
    def is_current(self):
        return self.end_date is None

    def get_responsibilities_list(self):
        return [line.strip() for line in self.responsibilities.splitlines() if line.strip()]

    def get_technologies_list(self):
        return [t.strip() for t in self.technologies.split(',') if t.strip()]


class Education(models.Model):
    """Education entry."""
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    grade = models.CharField(max_length=60, blank=True, help_text='e.g. CGPA 8.4 / 10')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-end_date', 'order']
        verbose_name = 'Education'
        verbose_name_plural = 'Education'

    def __str__(self):
        return f'{self.degree} — {self.institution}'
