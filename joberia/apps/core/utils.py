from functools import wraps

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from joberia.apps.spawner.models import Theme


def send_email_in_template(subject, receiver, template_name, **data):
    html_content = render_to_string(template_name, data)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        'joberia <admin@joberia.ai>', [receiver]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def themed_view(func):
    @wraps(func)
    def provide_theme(*args, **kwargs):
        theme = Theme.objects.all().first()
        kwargs.update({'theme': theme})
        return func(*args, **kwargs)

    return provide_theme
