# Generated by Django 2.1.3 on 2018-12-01 18:09

from django.db import migrations, models
import joberon.apps.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_job_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='DesiredProfileItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_id', models.CharField(default=joberon.apps.core.models.create_default_hash, editable=False, max_length=30)),
                ('idate', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('udate', models.DateTimeField(auto_now=True, verbose_name='changed at')),
                ('description', models.CharField(max_length=150)),
                ('amount_of_times_used', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OfferedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_id', models.CharField(default=joberon.apps.core.models.create_default_hash, editable=False, max_length=30)),
                ('idate', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('udate', models.DateTimeField(auto_now=True, verbose_name='changed at')),
                ('description', models.CharField(max_length=150)),
                ('amount_of_times_used', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='job',
            name='desired_profile',
            field=models.ManyToManyField(default=None, related_name='job_desired_profile_items', to='job.DesiredProfileItem'),
        ),
        migrations.AddField(
            model_name='job',
            name='offered_items',
            field=models.ManyToManyField(default=None, related_name='job_offered_items', to='job.OfferedItem'),
        ),
    ]