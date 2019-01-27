from django.contrib import admin

from .models import Tag, User


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'idate')


admin.site.register(Tag)
admin.site.register(User)
