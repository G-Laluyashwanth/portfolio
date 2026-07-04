"""Context processors injecting site-wide data into every template."""
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

    return {
        'site_settings': settings_obj,
        'site_name': getattr(settings_obj, 'site_name', 'Lalu Yashwanth'),
        'site_tagline': getattr(settings_obj, 'tagline', 'Full-Stack Developer'),
        'hero': hero,
        'has_writing': has_writing,
    }
