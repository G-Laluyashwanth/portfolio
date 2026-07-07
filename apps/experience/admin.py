from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import Experience, Education


@admin.register(Experience)
class ExperienceAdmin(ModelAdmin):
    list_display = (
        'role_preview', 'company', 'employment_badge',
        'start_date', 'end_date', 'published_badge', 'order',
    )
    list_editable = ('order',)
    list_filter = ('employment_type', 'is_published')
    search_fields = ('company', 'role', 'technologies')
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_submit = True
    ordering = ('-start_date', 'order')

    fieldsets = (
        ('Position', {
            'fields': ('company', 'role', 'employment_type', 'location', 'company_url', 'company_logo'),
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date'),
        }),
        ('Details', {
            'fields': ('summary', 'responsibilities', 'technologies'),
        }),
        ('Visibility', {
            'fields': ('is_published', 'order'),
        }),
    )

    @display(description='Role', header=True)
    def role_preview(self, obj):
        initials = ''.join(word[0] for word in obj.company.split()[:2]).upper()
        return [obj.role, obj.company, initials]

    @display(
        description='Type',
        label={
            'full_time': 'success',
            'part_time': 'info',
            'contract': 'primary',
            'internship': 'warning',
            'freelance': 'default',
        },
    )
    def employment_badge(self, obj):
        return obj.employment_type

    @display(description='Published', label={True: 'success', False: 'warning'})
    def published_badge(self, obj):
        return obj.is_published


@admin.register(Education)
class EducationAdmin(ModelAdmin):
    list_display = ('degree', 'institution', 'start_date', 'end_date', 'grade', 'order')
    list_editable = ('order',)
    search_fields = ('institution', 'degree', 'field_of_study')
    compressed_fields = True
    ordering = ('-end_date', 'order')

    fieldsets = (
        ('Program', {
            'fields': ('institution', 'degree', 'field_of_study', 'location'),
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'grade'),
        }),
        ('Notes', {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
        ('Display', {
            'fields': ('order',),
        }),
    )
