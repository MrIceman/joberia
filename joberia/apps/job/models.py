from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from joberia.apps.core.models import Base
from joberia.apps.user.models import User


def __str__(self):
    return self.name


class DesiredProfileItem(Base):
    label = models.CharField(max_length=150, db_index=True)
    amount_of_times_used = models.IntegerField(default=0)

    def __str__(self):
        return self.label


class OfferedItem(Base):
    label = models.CharField(max_length=150, db_index=True)
    amount_of_times_used = models.IntegerField(default=0)

    def __str__(self):
        return self.label


class Job(Base):
    STATUS = (
        ('off', 'Offline'),
        ('on', 'Online'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.TextField(default='')
    status = models.CharField(choices=STATUS, default='off', max_length=5)
    desired_profile = models.ManyToManyField(DesiredProfileItem, related_name='job_desired_profile_items', default=None)
    offered_items = models.ManyToManyField(OfferedItem, related_name='job_offefred_items', default=None)

    # set only if payment is done
    expires_at = models.DateTimeField(null=True)

    created_by = models.ForeignKey(User, related_name='created_jobs', on_delete=models.DO_NOTHING)

    picture = models.FileField(verbose_name='job_picture', default=None)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('udate',)

    def get_absolute_url(self):
        return reverse('job_detail', kwargs={
            'job_hash': self.hash_id, 'slug': slugify(self.title)
        })


class Bonus(Base):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50, default='')
    job_id = models.ForeignKey(to=Job, related_name='bonuses', null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Comment(Base):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    reply = models.OneToOneField('self', on_delete=models.CASCADE, related_name='comment_replies', null=True,
                                 blank=True)
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING, related_name='comments', default=None,
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
    job = models.ForeignKey(to=Job, related_name='tags', null=True, blank=True, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(to=User, related_name='tags', null=True, blank=True, on_delete=models.DO_NOTHING)
