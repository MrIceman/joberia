from django.db import models

from joberia.apps.core.models import Base


class Theme(Base):
    primary_dark_color = models.CharField(max_length=6)
    primary_secondary_color = models.CharField(max_length=6)
    accent_color = models.CharField(max_length=6)
    dark_accent_color = models.CharField(max_length=6)
    background_color = models.CharField(max_length=6, default='FFFFFF')
    home_header_color = models.CharField(max_length=6, default='000000')
    home_jobs_color = models.CharField(max_length=6, default='000000')
    home_dev_color = models.CharField(max_length=6, default='000000')


class Platform(Base):
    THEMES = (
        ('def', 'Default'),
        ('orn', 'Orange'),
        ('mng', 'Mango'),
        ('mrc', 'Maracuja'),
        ('apl', 'Apple'),
        ('kwi', 'Kiwi'),
        ('bby', 'Blackberry'),
        ('bbl', 'Blueberry'),
        ('ccn', 'Coconut'),
        ('lmn', 'Lemon'),
        ('lim', 'Limette'),
        ('str', 'Strawberry'),
    )

    platform_name = models.CharField(max_length=20)
    home_text_header = models.TextField(default='')
    home_text_body = models.TextField(default='')
    footer_about_text = models.TextField(default='')
    theme = models.CharField(choices=THEMES, default='def', max_length=3)
