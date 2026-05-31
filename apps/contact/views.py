import logging

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import ContactForm

logger = logging.getLogger(__name__)


def _client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.ip_address = _client_ip(request)
            submission.user_agent = request.META.get('HTTP_USER_AGENT', '')[:400]
            submission.save()

            # Send email notification
            try:
                subject = f'[Portfolio] {submission.subject or "New message from " + submission.name}'
                text_body = render_to_string('contact/email/notification.txt', {'submission': submission})
                html_body = render_to_string('contact/email/notification.html', {'submission': submission})

                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_RECIPIENT],
                    reply_to=[submission.email],
                )
                email.attach_alternative(html_body, 'text/html')
                email.send(fail_silently=False)
            except Exception:
                # Log but don't break user flow — submission is saved
                logger.exception('Contact notification email failed to send')

            messages.success(request, "Thanks for reaching out! I'll get back to you within 24-48 hours.")
            return redirect(reverse('contact:contact'))
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})
