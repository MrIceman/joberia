import json

from django.contrib.auth.models import User
from django.db import models

from joberon.apps.company.models import Organization
from joberon.apps.core.models import Base


class Alert(Base):
    TYPE = (
        ('dev', 'Developer'),
        ('org', 'Organization')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription', null=True, unique=True)
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, null=True, unique=True)
    type = models.CharField(choices=TYPE, default=TYPE[0], max_length=3)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{}: {} - Active: {}'.format(self.user.id, self.organization, self.is_active)

    def to_dict(self):
        return {
            'id': self.pk,
            'user_id': self.user.id,
            'type': self.type,
            'active': self.is_active
        }

    def to_json(self):
        return json.dumps(self.to_dict())
