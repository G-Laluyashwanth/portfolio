from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display

from .models import Project, TechStack, ProjectFeature, ProjectImage


@admin.action(description='Publish selected projects')
def publish_projects(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action(description='Unpublish selected projects')
def unpublish_projects(modeladmin, request, queryset):
    queryset.update(is_published=False)


@admin.action(description='Feature selected projects')
def feature_projects(modeladmin, request, queryset):
    queryset.update(is_featured=True)


class ProjectFeatureInline(TabularInline):
    model = ProjectFeature
    extra = 1
    fields = ('text', 'order')
    ordering = ('order',)


class ProjectImageInline(TabularInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption', 'order')
    ordering = ('order',)


@admin.register(TechStack)
class TechStackAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'color', 'order')
    list_editable = ('color', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('order', 'name')


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = (
        'title_preview', 'category_badge', 'company',
        'featured_badge', 'published_badge', 'order', 'updated_at',
    )
    list_editable = ('order',)
    list_filter = ('category', 'is_featured', 'is_published', 'tech_stack')
    search_fields = ('title', 'short_description', 'description', 'company')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tech_stack',)
    inlines = [ProjectFeatureInline, ProjectImageInline]
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_submit = True
    actions = [publish_projects, unpublish_projects, feature_projects]
    ordering = ('order', '-updated_at')

    fieldsets = (
        ('Basic info', {
            'fields': ('title', 'subtitle', 'slug', 'category', 'company', 'role', 'cover_image'),
        }),
        ('Content', {
            'fields': (
                'short_description', 'description', 'problem', 'solution', 'impact',
            ),
        }),
        ('Case study depth', {
            'fields': (
                'technical_highlights', 'roles_and_users', 'workflows', 'scope_notes',
            ),
            'description': 'One item per line for list sections on the public case study.',
        }),
        ('Tech & links', {
            'fields': ('tech_stack', 'live_url', 'github_url'),
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date'),
            'classes': ('collapse',),
        }),
        ('Visibility', {
            'fields': ('is_featured', 'is_published', 'is_proprietary', 'order'),
        }),
    )

    @display(description='Project', header=True)
    def title_preview(self, obj):
        initials = ''.join(word[0] for word in obj.title.split()[:2]).upper()
        return [obj.title, obj.short_description[:80], initials]

    @display(
        description='Category',
        label={
            'web': 'info',
            'website': 'primary',
            'ml': 'success',
            'automation': 'warning',
            'other': 'default',
        },
    )
    def category_badge(self, obj):
        return obj.category

    @display(description='Featured', label={True: 'success', False: 'default'})
    def featured_badge(self, obj):
        return obj.is_featured

    @display(description='Published', label={True: 'success', False: 'warning'})
    def published_badge(self, obj):
        return obj.is_published
