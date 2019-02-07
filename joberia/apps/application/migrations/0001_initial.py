# Generated by Django 2.1.3 on 2019-02-07 22:21

from django.db import migrations, models
import django.db.models.deletion
import joberia.apps.core.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('spawner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_id', models.CharField(default=joberia.apps.core.models.create_default_hash, editable=False, max_length=30)),
                ('idate', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('udate', models.DateTimeField(auto_now=True, verbose_name='changed at')),
                ('status', models.CharField(choices=[('rej', 'Rejected'), ('acc', 'Accepted')], max_length=3)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_id', models.CharField(default=joberia.apps.core.models.create_default_hash, editable=False, max_length=30)),
                ('idate', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('udate', models.DateTimeField(auto_now=True, verbose_name='changed at')),
                ('message', models.TextField()),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='application_communications', to='application.Application')),
                ('platform_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='spawner.Platform', verbose_name='platform')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
