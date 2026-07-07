from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import ContactSubmission


@admin.action(description='Mark selected as read')
def mark_as_read(modeladmin, request, queryset):
    queryset.update(is_read=True)


@admin.action(description='Mark selected as replied')
def mark_as_replied(modeladmin, request, queryset):
    queryset.update(is_replied=True)


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(ModelAdmin):
    list_display = ('name', 'email', 'subject_preview', 'read_badge', 'replied_badge', 'created_at')
    list_filter = ('is_read', 'is_replied', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'ip_address', 'user_agent', 'created_at')
    actions = [mark_as_read, mark_as_replied]
    list_filter_submit = True
    ordering = ('-created_at',)

    fieldsets = (
        ('Message', {
            'fields': ('name', 'email', 'subject', 'message', 'created_at'),
        }),
        ('Status', {
            'fields': ('is_read', 'is_replied', 'notes'),
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',),
        }),
    )

    @display(description='Subject')
    def subject_preview(self, obj):
        return obj.subject[:72] if obj.subject else '—'

    @display(description='Read', label={True: 'success', False: 'warning'})
    def read_badge(self, obj):
        return obj.is_read

    @display(description='Replied', label={True: 'success', False: 'default'})
    def replied_badge(self, obj):
        return obj.is_replied

    def has_add_permission(self, request):
        return False
