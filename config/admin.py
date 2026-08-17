"""Unfold admin branding, sidebar navigation, and dashboard callbacks."""

from django.urls import reverse_lazy


def environment_callback(request):
    from django.conf import settings

    if settings.DEBUG:
        return ['Development', 'info']
    return ['Production', 'success']


def dashboard_callback(request, context):
    from apps.core.models import Post
    from apps.projects.models import Project

    context.update({
        'portfolio_stats': {
            'projects': Project.objects.filter(is_published=True).count(),
            'posts': Post.objects.filter(is_published=True).count(),
            'drafts': Project.objects.filter(is_published=False).count(),
        },
    })
    return context


def _nav_item(title, icon, link):
    return {'title': title, 'icon': icon, 'link': link}


UNFOLD_SIDEBAR = [
    {
        'title': 'Overview',
        'separator': True,
        'items': [
            _nav_item('Dashboard', 'dashboard', reverse_lazy('admin:index')),
            _nav_item('View site', 'public', '/'),
        ],
    },
    {
        'title': 'Site',
        'collapsible': True,
        'items': [
            _nav_item('Site settings', 'settings', reverse_lazy('admin:core_sitesettings_change', args=[1])),
            _nav_item('Hero section', 'home', reverse_lazy('admin:core_herosection_changelist')),
        ],
    },
    {
        'title': 'Portfolio',
        'collapsible': True,
        'items': [
            _nav_item('Projects', 'work', reverse_lazy('admin:projects_project_changelist')),
            _nav_item('Tech stack', 'code', reverse_lazy('admin:projects_techstack_changelist')),
            _nav_item('Writing', 'edit_note', reverse_lazy('admin:core_post_changelist')),
        ],
    },
    {
        'title': 'Profile',
        'collapsible': True,
        'items': [
            _nav_item('Experience', 'business_center', reverse_lazy('admin:experience_experience_changelist')),
            _nav_item('Education', 'school', reverse_lazy('admin:experience_education_changelist')),
            _nav_item('Skill categories', 'category', reverse_lazy('admin:skills_skillcategory_changelist')),
            _nav_item('Skills', 'psychology', reverse_lazy('admin:skills_skill_changelist')),
        ],
    },
]
