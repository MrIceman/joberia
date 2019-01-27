from django.db import models

from joberia.apps.job.models import Job
from joberia.apps.core.models import Base
from joberia.apps.user.models import User


class Application(Base):
    STATUS = (
        ('rej', 'Rejected'),
        ('acc', 'Accepted'),
    )
    job = models.ForeignKey(Job, related_name='job_applications', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, related_name='user_applications', on_delete=models.DO_NOTHING)

    # only for company
    status = models.CharField(max_length=3, choices=STATUS)


class Communication(Base):
    application = models.ForeignKey(Application, related_name='application_communications', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, related_name='user_messages', on_delete=models.DO_NOTHING)
    message = models.TextField()
