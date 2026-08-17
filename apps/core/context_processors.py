"""Context processors injecting site-wide data into every template."""
import json
from pathlib import Path

from django.conf import settings
from django.templatetags.static import static

from .models import SiteSettings, HeroSection, Post


def _resume_url(settings_obj):
    """Resolve the résumé link.

    A PDF committed under static/ wins over the admin upload, because media
    files are not served once DEBUG is off. The admin upload is only a
    fallback for local use until cloud storage exists.
    """
    static_dir = getattr(settings, 'RESUME_STATIC_DIR', '')
    if static_dir:
        pdfs = sorted((Path(settings.BASE_DIR) / 'static' / static_dir).glob('*.pdf'))
        if pdfs:
            return static(f'{static_dir}/{pdfs[0].name}')
    if settings_obj and settings_obj.resume:
        return settings_obj.resume.url
    return ''


def site_context(request):
    """Returns global context: site settings + active hero + nav flags."""
    try:
        settings_obj = SiteSettings.load()
    except Exception:
        settings_obj = None

    try:
        hero = HeroSection.objects.filter(is_active=True).first()
    except Exception:
        hero = None

    try:
        has_writing = Post.objects.filter(is_published=True).exists()
    except Exception:
        has_writing = False

    resume_url = _resume_url(settings_obj)

    structured_data = ''
    if settings_obj:
        same_as = [
            url for url in (
                settings_obj.github_url,
                settings_obj.linkedin_url,
                settings_obj.twitter_url,
            ) if url
        ]
        # Shorter job title for schema - first segment of the tagline.
        job_title = (settings_obj.tagline or '').split('·')[0].strip() or settings_obj.tagline
        person = {
            '@context': 'https://schema.org',
            '@type': 'Person',
            'name': settings_obj.site_name,
            'jobTitle': job_title,
            'url': request.build_absolute_uri('/'),
        }
        if settings_obj.email:
            person['email'] = settings_obj.email
        if settings_obj.location:
            person['homeLocation'] = {
                '@type': 'Place',
                'name': settings_obj.location,
            }
        if same_as:
            person['sameAs'] = same_as
        structured_data = json.dumps(person)

    # Canonical without query string.
    canonical = request.build_absolute_uri(request.path)

    return {
        'site_settings': settings_obj,
        'site_name': getattr(settings_obj, 'site_name', 'Lalu Yashwanth'),
        'site_tagline': getattr(settings_obj, 'tagline', 'Full-Stack Developer'),
        'hero': hero,
        'has_writing': has_writing,
        'resume_url': resume_url,
        'structured_data': structured_data,
        'canonical_url': canonical,
    }
