from django.contrib import admin
from .models import Project, TechStack, ProjectFeature, ProjectImage


class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 1
    fields = ('text', 'order')


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption', 'order')


@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color', 'order')
    list_editable = ('color', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'company', 'is_featured', 'is_published', 'order', 'updated_at')
    list_editable = ('is_featured', 'is_published', 'order')
    list_filter = ('category', 'is_featured', 'is_published', 'tech_stack')
    search_fields = ('title', 'short_description', 'description', 'company')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tech_stack',)
    inlines = [ProjectFeatureInline, ProjectImageInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'category', 'company', 'role', 'cover_image'),
        }),
        ('Content', {
            'fields': ('short_description', 'description', 'problem', 'solution', 'impact'),
        }),
        ('Tech & Links', {
            'fields': ('tech_stack', 'live_url', 'github_url'),
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date'),
        }),
        ('Visibility', {
            'fields': ('is_featured', 'is_published', 'order'),
        }),
    )
