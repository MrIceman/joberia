from django.contrib import admin

from .models import User


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'idate')


admin.site.register(User)
