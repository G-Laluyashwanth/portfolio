from django.db import models


class ContactSubmission(models.Model):
    """Inbound message from the contact form."""
    name = models.CharField(max_length=160)
    email = models.EmailField()
    subject = models.CharField(max_length=240, blank=True)
    message = models.TextField()

    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)
    notes = models.TextField(blank=True, help_text='Internal notes — not visible to sender.')

    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=400, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'

    def __str__(self):
        return f'{self.name} <{self.email}> — {self.created_at:%Y-%m-%d}'
