from django.contrib import admin
from .models import SiteSettings, HeroSection, Post


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'email', 'location', 'updated_at')

    def has_add_permission(self, request):
        # Singleton — only one allowed
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('headline', 'eyebrow', 'is_active')
    list_editable = ('is_active',)
    fieldsets = (
        ('Content', {
            'fields': ('eyebrow', 'headline', 'subheadline'),
        }),
        ('Call to Action', {
            'fields': ('cta_primary_label', 'cta_primary_url',
                       'cta_secondary_label', 'cta_secondary_url'),
        }),
        ('Visibility', {
            'fields': ('is_active',),
        }),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_published', 'is_external')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date'
