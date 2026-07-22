"""Smoke and unit tests for the portfolio site."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.core.models import SiteSettings, Post, HeroSection
from apps.projects.models import Project


class PageRenderTests(TestCase):
    """Every public page should render without error."""

    def setUp(self):
        self.project = Project.objects.create(
            title='Test Project',
            short_description='A short description.',
            description='Full description.',
            impact='Cut processing time by 80%. Extra detail here.',
            is_proprietary=True,
        )
        self.post = Post.objects.create(title='Test Post', excerpt='An excerpt.')
        HeroSection.objects.create(
            headline='Hello',
            subheadline='Sub',
            cta_primary_label='Projects',
            cta_primary_url='#projects',
            cta_secondary_label='Contact',
            cta_secondary_url='#contact',
        )

    def test_home_renders(self):
        resp = self.client.get(reverse('core:home'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'contact-cards')
        self.assertContains(resp, 'Test Project')
        self.assertContains(resp, 'Source private')
        self.assertContains(resp, '#contact')

    def test_project_detail_renders(self):
        resp = self.client.get(self.project.get_absolute_url())
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Project')
        self.assertContains(resp, 'Source private')

    def test_post_detail_renders(self):
        resp = self.client.get(self.post.get_absolute_url())
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Post')
        self.assertContains(resp, 'og:title')

    def test_unpublished_post_is_404(self):
        draft = Post.objects.create(title='Draft', is_published=False)
        self.assertEqual(self.client.get(draft.get_absolute_url()).status_code, 404)

    def test_removed_contact_page_is_gone(self):
        self.assertEqual(self.client.get('/contact/').status_code, 404)

    def test_resume_static_link_present(self):
        resp = self.client.get(reverse('core:home'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '/static/resume/')


class ModelTests(TestCase):
    """Model helpers behave as expected."""

    def test_project_slug_and_url(self):
        p = Project.objects.create(
            title='My Cool App', short_description='x', description='y',
        )
        self.assertEqual(p.slug, 'my-cool-app')
        self.assertTrue(p.get_absolute_url().endswith('/my-cool-app/'))

    def test_project_impact_headline(self):
        p = Project.objects.create(
            title='Metrics App', short_description='x', description='y',
            impact='Reduced errors by 90%. And other things.',
        )
        self.assertEqual(p.impact_headline, 'Reduced errors by 90%.')

    def test_project_impact_headline_empty(self):
        p = Project.objects.create(
            title='No Impact', short_description='x', description='y', impact='',
        )
        self.assertEqual(p.impact_headline, '')

    def test_post_internal_vs_external(self):
        internal = Post.objects.create(title='Internal Post')
        self.assertEqual(internal.slug, 'internal-post')
        self.assertFalse(internal.is_external)
        self.assertIn('/writing/internal-post/', internal.get_absolute_url())

        external = Post.objects.create(
            title='External Post', external_url='https://example.com/x',
        )
        self.assertTrue(external.is_external)
        self.assertEqual(external.get_absolute_url(), 'https://example.com/x')

    def test_sitesettings_is_singleton(self):
        first = SiteSettings.load()
        first.site_name = 'Changed'
        first.save()
        second = SiteSettings.load()
        self.assertEqual(second.pk, 1)
        self.assertEqual(second.site_name, 'Changed')
        self.assertEqual(SiteSettings.objects.count(), 1)


class SeoEndpointTests(TestCase):
    """Feed, sitemap, and robots endpoints respond correctly."""

    def setUp(self):
        self.post = Post.objects.create(title='Feed Post', excerpt='hi')
        self.external = Post.objects.create(
            title='External Feed',
            external_url='https://example.com/ext',
            is_published=True,
        )
        self.project = Project.objects.create(
            title='Feed Project', short_description='x', description='y',
        )

    def test_sitemap(self):
        resp = self.client.get('/sitemap.xml')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '/writing/feed-post/')
        self.assertContains(resp, self.project.get_absolute_url())
        self.assertNotContains(resp, 'example.com/ext')

    def test_robots(self):
        resp = self.client.get('/robots.txt')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Sitemap:')
        self.assertIn('text/plain', resp['Content-Type'])

    def test_feed(self):
        resp = self.client.get('/feed/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Feed Post')
        self.assertIn('application/rss+xml', resp['Content-Type'])


class AdminPanelTests(TestCase):
    """Unfold admin should load for staff users."""

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'pass')

    def test_admin_index_renders(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/admin/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Portfolio')

    def test_project_changelist_renders(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('admin:projects_project_changelist'))
        self.assertEqual(resp.status_code, 200)


class DeployConfigTests(TestCase):
    """Production-oriented settings wiring."""

    def test_storages_and_resume_configured(self):
        from django.conf import settings
        backend = settings.STORAGES['staticfiles']['BACKEND']
        self.assertTrue(
            backend.endswith('StaticFilesStorage')
            or 'CompressedManifestStaticFilesStorage' in backend
        )
        self.assertTrue(settings.RESUME_STATIC.startswith('resume/'))

    def test_home_serves_static_resume_link(self):
        resp = self.client.get(reverse('core:home'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '/static/resume/')
        self.assertNotContains(resp, '/media/resume/')
