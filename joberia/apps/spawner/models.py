from django.db import models

from joberia.apps.core.models import Base


class Platform(Base):
    platform_name = models.CharField(max_length=20)
