from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def send_email_in_template(subject, receiver, template_name, **data):
    html_content = render_to_string(template_name, data)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        'joberon <info@joberon.com>', [receiver]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
