# Generated by Django 5.1.2 on 2024-12-03 03:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_profile_last_points_update_profile_rank_change_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dailytask',
            unique_together={('user', 'title', 'is_static', 'completion_criteria')},
        ),
        migrations.RemoveField(
            model_name='dailytask',
            name='description',
        ),
    ]
