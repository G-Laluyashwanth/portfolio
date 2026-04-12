from django.shortcuts import render, get_object_or_404
from .models import Project


def project_list(request):
    """All published projects with optional category filter."""
    projects = Project.objects.filter(is_published=True).prefetch_related('tech_stack', 'features')

    category = request.GET.get('category', '').strip()
    if category:
        projects = projects.filter(category=category)

    context = {
        'projects': projects,
        'categories': Project.CATEGORY_CHOICES,
        'active_category': category,
        'total_count': projects.count(),
    }
    return render(request, 'projects/list.html', context)


def project_detail(request, slug):
    """Full case-study page for a single project."""
    project = get_object_or_404(
        Project.objects.prefetch_related('tech_stack', 'features', 'images'),
        slug=slug,
        is_published=True,
    )
    related = Project.objects.filter(
        is_published=True
    ).exclude(pk=project.pk).order_by('order', '-created_at')[:3]

    return render(request, 'projects/detail.html', {
        'project': project,
        'related_projects': related,
    })
