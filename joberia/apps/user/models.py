from django.contrib.auth.models import AbstractUser
from django.db import models

from joberia.apps.company.models import Organization
from joberia.apps.core.models import Base
from joberia.apps.spawner.models import Platform


class User(AbstractUser):
    ROLES = (('dev', 'Developer'), ('org', 'Organization'))
    role = models.CharField(choices=ROLES, max_length=3)
    confirmed = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)
    confirm_hash = models.CharField(max_length=160, default='')
    organization = models.ForeignKey(Organization, null=True, related_name='users', on_delete=models.DO_NOTHING)
    platform = models.ForeignKey(Platform, null=False, related_name='users', on_delete=models.DO_NOTHING)

    def __str__(self):
        return '{} / {}'.format(self.email, self.username)


class Bio(Base):
    user = models.ForeignKey(User, related_name='user_bios', on_delete=models.CASCADE)



