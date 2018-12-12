# Generated by Django 2.1.3 on 2018-12-01 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0011_auto_20181201_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='job',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='job_comments', to='job.Job'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='reply',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_replies', to='job.Comment'),
        ),
    ]