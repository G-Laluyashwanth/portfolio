"""RSS feed for the Writing section."""
from datetime import datetime, time

from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils import timezone

from .models import Post, SiteSettings


class LatestPostsFeed(Feed):
    def title(self):
        return f'{SiteSettings.load().site_name} — Writing'

    def description(self):
        return 'Notes on full-stack engineering and machine learning.'

    def link(self):
        return reverse('core:home')

    def items(self):
        return Post.objects.filter(is_published=True)[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt or item.content

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return timezone.make_aware(datetime.combine(item.date, time.min))
