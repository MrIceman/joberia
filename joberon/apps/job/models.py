from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from joberon.apps.company.models import Organization
from joberon.apps.core.models import Base
from joberon.apps.user.models import Tag


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


class Bonus(Base):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class BonusEntry(Base):
    bonus = models.OneToOneField(Bonus, related_name='entries', on_delete=models.CASCADE)
    entry = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.bonus.name


class Job(Base):
    STATUS = (
        ('off', 'Offline'),
        ('on', 'Online'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.TextField(default='')
    status = models.CharField(choices=STATUS, default='off', max_length=5)
    tags = models.ManyToManyField(Tag, related_name='job_tags', default=None)
    desired_profile = models.ManyToManyField(DesiredProfileItem, related_name='job_desired_profile_items', default=None)
    offered_items = models.ManyToManyField(OfferedItem, related_name='job_offered_items', default=None)
    bonuses = models.ManyToManyField(BonusEntry, related_name='job_bonuses', default=None)

    # set only if payment is done
    expires_at = models.DateTimeField(null=True)

    # fks
    organization = models.ForeignKey(Organization, related_name='org_jobs', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='created_jobs', on_delete=models.DO_NOTHING)

    picture = models.FileField(verbose_name='job_picture', default=None)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('job_detail', kwargs={
            'job_hash': self.hash_id, 'slug': slugify(self.title)
        })


class Comment(Base):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_user_comments')
    text = models.TextField()
    reply = models.OneToOneField('self', on_delete=models.CASCADE, related_name='comment_replies', null=True,
                                 blank=True)
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING, related_name='job_comments', default=None,
                            unique=False)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.author.username + " - " + self.job.title + " - " + self.idate.__str__()
