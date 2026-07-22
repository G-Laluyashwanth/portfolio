from django.shortcuts import render, get_object_or_404
from .models import Project


def project_detail(request, slug):
    """Full case-study page for a single project."""
    project = get_object_or_404(
        Project.objects.prefetch_related('tech_stack', 'features', 'images'),
        slug=slug,
        is_published=True,
    )
    related = (
        Project.objects.filter(is_published=True, category=project.category)
        .exclude(pk=project.pk)
        .order_by('order', '-created_at')[:3]
    )
    if related.count() < 3:
        extras = (
            Project.objects.filter(is_published=True)
            .exclude(pk=project.pk)
            .exclude(pk__in=related.values_list('pk', flat=True))
            .order_by('order', '-created_at')[: 3 - related.count()]
        )
        related = list(related) + list(extras)

    return render(request, 'projects/detail.html', {
        'project': project,
        'related_projects': related,
    })
