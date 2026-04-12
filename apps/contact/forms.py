from django import forms
from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    """Contact form with honeypot anti-spam."""

    # Honeypot — bots fill this, humans won't see it
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactSubmission
        fields = ('name', 'email', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your full name',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'you@example.com',
                'autocomplete': 'email',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': "What's this about?",
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Tell me about your project, role, or question...',
                'rows': 6,
            }),
        }

    def clean_website(self):
        value = self.cleaned_data.get('website', '')
        if value:
            raise forms.ValidationError('Spam detected.')
        return value

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError('Please write at least 10 characters.')
        return message
