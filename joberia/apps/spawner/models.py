from django.db import models


class Theme(models.Model):
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

    theme = models.CharField(choices=THEMES, default='def', max_length=3, unique=True)
    primary_color = models.CharField(max_length=6, default='000000')
    primary_color_dark = models.CharField(max_length=6, default='000000')
    secondary_color = models.CharField(max_length=6, default='000000')
    secondary_color_dark = models.CharField(max_length=6, default='000000')
    accent_color = models.CharField(max_length=6, default='000000')
    accent_color_dark = models.CharField(max_length=6, default='000000')
    background_color = models.CharField(max_length=6, default='FFFFFF')
    home_header_color = models.CharField(max_length=6, default='000000')
    home_jobs_color = models.CharField(max_length=6, default='000000')
    home_dev_color = models.CharField(max_length=6, default='000000')
    text_color = models.CharField(max_length=6, default='FEFEFE')

    def __str__(self):
        if self.theme in Theme.THEMES[0]:
            for short, long in Theme.THEMES:
                if short == self.theme:
                    return long
        else:
            return 'not found'


class Platform(models.Model):
    platform_name = models.CharField(max_length=20)
    hash = models.CharField(max_length=100, default='')
    home_text_header = models.TextField(default='')
    home_text_sub_header = models.TextField(default='')
    home_text_body = models.TextField(default='')
    description = models.TextField(default='')
    footer_text = models.TextField(default='')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} / {}'.format(self.pk, self.platform_name)
