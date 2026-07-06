"""Context processors injecting site-wide data into every template."""
import json

from .models import SiteSettings, HeroSection, Post


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

    structured_data = ''
    if settings_obj:
        same_as = [
            url for url in (
                settings_obj.github_url,
                settings_obj.linkedin_url,
                settings_obj.twitter_url,
            ) if url
        ]
        person = {
            '@context': 'https://schema.org',
            '@type': 'Person',
            'name': settings_obj.site_name,
            'jobTitle': settings_obj.tagline,
            'url': request.build_absolute_uri('/'),
        }
        if settings_obj.email:
            person['email'] = settings_obj.email
        if settings_obj.location:
            person['address'] = settings_obj.location
        if same_as:
            person['sameAs'] = same_as
        structured_data = json.dumps(person)

    return {
        'site_settings': settings_obj,
        'site_name': getattr(settings_obj, 'site_name', 'Lalu Yashwanth'),
        'site_tagline': getattr(settings_obj, 'tagline', 'Full-Stack Developer'),
        'hero': hero,
        'has_writing': has_writing,
        'structured_data': structured_data,
    }
