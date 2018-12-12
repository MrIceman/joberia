from django.contrib import admin

from joberia.apps.job.models import Job, DesiredProfileItem, OfferedItem, Bonus, BonusEntry, Comment

# Register your models here.

admin.site.register(Job)
admin.site.register(DesiredProfileItem)
admin.site.register(OfferedItem)
admin.site.register(Bonus)
admin.site.register(BonusEntry)
admin.site.register(Comment)
