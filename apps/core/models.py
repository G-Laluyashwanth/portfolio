from django.db import models


class SiteSettings(models.Model):
    """Singleton model holding site-wide settings shown in nav, footer, meta tags."""
    site_name = models.CharField(max_length=120, default='Lalu Yashwanth')
    tagline = models.CharField(max_length=240, default='Full-Stack Developer | Python & Django Engineer')
    meta_description = models.TextField(
        default='Full-Stack Developer specializing in Python, Django, PostgreSQL, '
                'REST APIs, and Machine Learning. 3+ years building scalable web applications.'
    )
    meta_keywords = models.CharField(
        max_length=500,
        default='Full-Stack Developer, Python Developer, Django Developer, '
                'PostgreSQL, REST API, Machine Learning, Data Science, Hyderabad'
    )

    # Contact / social
    email = models.EmailField(default='laluyashwanth.dev@gmail.com')
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=120, default='Hyderabad, India')
    github_url = models.URLField(blank=True, default='https://github.com/G-Laluyashwanth')
    linkedin_url = models.URLField(blank=True, default='https://linkedin.com/in/laluyashwanth')
    resume = models.FileField(upload_to='resume/', blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce singleton
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HeroSection(models.Model):
    """Hero block on the home page."""
    eyebrow = models.CharField(max_length=120, default='Full-Stack Developer')
    headline = models.CharField(
        max_length=240,
        default='Building scalable web applications with Python, Django, and Machine Learning.'
    )
    subheadline = models.TextField(
        default='3+ years of professional experience designing enterprise-grade systems, '
                'RESTful APIs, and data-driven applications. Currently expanding into ML and Deep Learning.'
    )
    typing_phrases = models.TextField(
        default="Full-Stack Developer\nPython & Django Engineer\nMachine Learning Enthusiast\nAPI Architect",
        help_text='One phrase per line — used by the typing animation in the hero.'
    )
    cta_primary_label = models.CharField(max_length=60, default='View Projects')
    cta_primary_url = models.CharField(max_length=200, default='#projects')
    cta_secondary_label = models.CharField(max_length=60, default='Get in Touch')
    cta_secondary_url = models.CharField(max_length=200, default='/contact/')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Section'

    def __str__(self):
        return self.headline[:60]

    def get_typing_phrases_list(self):
        return [line.strip() for line in self.typing_phrases.splitlines() if line.strip()]
