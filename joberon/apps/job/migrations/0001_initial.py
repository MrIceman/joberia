# Generated by Django 2.1.3 on 2018-11-25 05:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import joberon.apps.core.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_id', models.CharField(default=joberon.apps.core.models.create_default_hash, editable=False, max_length=30)),
                ('idate', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('udate', models.DateTimeField(auto_now=True, verbose_name='changed at')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('off', 'Offline'), ('on', 'Online')], default='off', max_length=5)),
                ('expires_at', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_jobs', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='org_jobs', to='company.Organization')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
