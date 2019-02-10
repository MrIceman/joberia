from datetime import timedelta, datetime

from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from joberia.apps.core.models import Base
from joberia.apps.spawner.models import Platform
from joberia.apps.user.models import User


def __str__(self):
    return self.name


class Job(Base):
    STATUS = (
        ('off', 'Offline'),
        ('on', 'Online'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.TextField(default='')
    status = models.CharField(choices=STATUS, default='off', max_length=5)

    # set only if payment is done
    expires_at = models.DateTimeField(default=datetime.now() + timedelta(days=30))

    created_by = models.ForeignKey(User, related_name='created_jobs', on_delete=models.CASCADE, null=True)
    picture = models.ImageField(upload_to='job_images', verbose_name='job_picture', default=None)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('udate',)

    def get_absolute_url(self):
        return reverse('job_detail', kwargs={
            'job_hash': self.hash_id, 'slug': slugify(self.title)
        })


class DesiredProfileItem(Base):
    name = models.CharField(max_length=150, db_index=True)
    job = models.ForeignKey(to=Job, related_name='desired_profile', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class OfferedItem(Base):
    label = models.CharField(max_length=150, db_index=True)
    job = models.ForeignKey(to=Job, related_name='offers', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.label


class Bonus(Base):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50, default='')
    job = models.ForeignKey(to=Job, related_name='bonuses', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Comment(Base):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    reply = models.OneToOneField('self', on_delete=models.CASCADE, related_name='comment_replies', null=True,
                                 blank=True
                                 )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='comments', null=True,
                            default=None,
                            unique=False)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.author.username + " - " + self.job.title + " - " + self.idate.__str__()


class Tag(Base):
    TYPES = (
        ('loc', 'Location'),
        ('skill', 'Skill'),
        ('other', 'Other')
    )
    type = models.CharField(choices=TYPES, default='skill', db_index=True, max_length=10)
    name = models.CharField(max_length=100, unique=True)
    job = models.ForeignKey(to=Job, related_name='tags', null=True, on_delete=models.CASCADE,
                            unique=False)
    user = models.ForeignKey(to=User, related_name='tags', null=True, on_delete=models.CASCADE,
                             unique=False)

    def __str__(self):
        return self.name
