from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import SiteSettings, HeroSection, Post


@admin.action(description='Publish selected posts')
def publish_posts(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action(description='Unpublish selected posts')
def unpublish_posts(modeladmin, request, queryset):
    queryset.update(is_published=False)


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    list_display = ('site_name', 'email', 'location', 'updated_at')
    compressed_fields = True
    warn_unsaved_form = True

    fieldsets = (
        ('Identity', {
            'fields': ('site_name', 'tagline'),
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',),
        }),
        ('Contact', {
            'fields': ('email', 'phone', 'location'),
        }),
        ('Social & links', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url'),
        }),
        ('Résumé', {
            'fields': ('resume',),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroSection)
class HeroSectionAdmin(ModelAdmin):
    list_display = ('headline_preview', 'eyebrow', 'active_badge')
    list_editable = ()
    compressed_fields = True
    warn_unsaved_form = True
    fieldsets = (
        ('Content', {
            'fields': ('eyebrow', 'headline', 'subheadline'),
        }),
        ('Call to action', {
            'fields': ('cta_primary_label', 'cta_primary_url',
                       'cta_secondary_label', 'cta_secondary_url'),
        }),
        ('Visibility', {
            'fields': ('is_active',),
        }),
    )

    @display(description='Headline', header=True)
    def headline_preview(self, obj):
        return [obj.headline[:72], obj.eyebrow or 'Hero section', 'H']

    @display(description='Active', label={True: 'success', False: 'warning'})
    def active_badge(self, obj):
        return obj.is_active


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('title', 'date', 'published_badge', 'type_badge')
    list_editable = ()
    list_filter = ('is_published',)
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date'
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_submit = True
    actions = [publish_posts, unpublish_posts]

    fieldsets = (
        ('Post', {
            'fields': ('title', 'slug', 'date', 'excerpt'),
        }),
        ('Content', {
            'fields': ('content', 'external_url'),
            'description': 'Write content here, or set an external URL to link out instead.',
        }),
        ('Visibility', {
            'fields': ('is_published',),
        }),
    )

    @display(description='Published', label={True: 'success', False: 'warning'})
    def published_badge(self, obj):
        return obj.is_published

    @display(description='Type', label={'internal': 'info', 'external': 'primary'})
    def type_badge(self, obj):
        return 'external' if obj.is_external else 'internal'
