from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Theme, Platform

# Register your models here.
admin.site.register(Theme)
admin.site.register(Platform)
