from django.contrib import admin
from .models import Experience, Education


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'employment_type', 'start_date', 'end_date', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    list_filter = ('employment_type', 'is_published')
    search_fields = ('company', 'role', 'technologies')
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


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_date', 'end_date', 'grade', 'order')
    list_editable = ('order',)
    search_fields = ('institution', 'degree', 'field_of_study')
