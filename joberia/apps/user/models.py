from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from joberia.apps.company.models import Organization
from joberia.apps.core.models import Base


class Profile(Base):
    ROLES = (
        ('dev', 'Developer'),
        ('org', 'Organization'),
    )
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    confirm_hash = models.CharField(max_length=60, default='')
    pw_onetime_hash = models.CharField(max_length=60, default='')
    email = models.EmailField()

    organization = models.ForeignKey(Organization, null=True, related_name='org_users', on_delete=models.DO_NOTHING)
    role = models.CharField(max_length=3, default='dev')

    def __str__(self):
        return self.user.username


class Bio(Base):
    user = models.ForeignKey(User, related_name='user_bios', on_delete=models.CASCADE)


class Tag(Base):
    TYPES = (
        ('loc', 'Location'),
        ('skill', 'Skill'),
    )
    type = models.CharField(choices=TYPES, default='skill', db_index=True, max_length=10)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# create user profile on the fly
@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        profile = Profile(user=user)
        profile.save()


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance=None, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()
