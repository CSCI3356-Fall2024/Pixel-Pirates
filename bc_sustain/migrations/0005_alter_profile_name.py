# Generated by Django 5.1.2 on 2024-10-20 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bc_sustain', '0004_rename_major1_profile_major_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
