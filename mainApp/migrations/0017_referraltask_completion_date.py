# Generated by Django 5.1.2 on 2024-11-08 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0016_rename_is_satic_dailytask_is_static'),
    ]

    operations = [
        migrations.AddField(
            model_name='referraltask',
            name='completion_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
