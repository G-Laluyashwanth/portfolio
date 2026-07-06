"""XML sitemaps for search engines."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.projects.models import Project
from .models import Post


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return ['core:home']

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Project.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class PostSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        # Only internal posts — external ones live on other domains.
        return Post.objects.filter(is_published=True, external_url='')

    def lastmod(self, obj):
        return obj.date
