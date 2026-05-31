from django.shortcuts import render
from apps.projects.models import Project
from apps.skills.models import SkillCategory
from apps.experience.models import Experience, Education


def home(request):
    """Home page with all sections driven by the database."""
    context = {
        'featured_projects': Project.objects.filter(
            is_published=True, is_featured=True
        ).prefetch_related('tech_stack')[:6],
        'skill_categories': SkillCategory.objects.prefetch_related('skills').all(),
        'experiences': Experience.objects.filter(is_published=True),
        'educations': Education.objects.all(),
    }
    return render(request, 'core/home.html', context)
