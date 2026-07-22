from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


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
    twitter_url = models.URLField(blank=True, default='', help_text='Full URL to your Twitter/X profile.')
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
    cta_primary_label = models.CharField(max_length=60, default='View Projects')
    cta_primary_url = models.CharField(max_length=200, default='#projects')
    cta_secondary_label = models.CharField(max_length=60, default='Get in Touch')
    cta_secondary_url = models.CharField(max_length=200, default='#contact')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Section'

    def __str__(self):
        return self.headline[:60]


class Post(models.Model):
    """A short writing/notes entry. Links to an internal page, or out via external_url."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    date = models.DateField(default=timezone.localdate)
    excerpt = models.CharField(max_length=280, blank=True, help_text='One-line summary shown in the list.')
    content = models.TextField(blank=True, help_text='Body of the post. Leave blank if using an external link.')
    external_url = models.URLField(blank=True, help_text='If set, the post links here instead of an internal page.')
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.external_url or reverse('core:post', kwargs={'slug': self.slug})

    @property
    def is_external(self):
        return bool(self.external_url)
