from django.contrib import admin

from .models import Profile, Tag


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'idate')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag)
