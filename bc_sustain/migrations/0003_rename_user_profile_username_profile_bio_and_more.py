# Generated by Django 5.1.2 on 2024-10-20 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bc_sustain', '0002_profile_bc_email_profile_minor1_profile_minor2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user',
            new_name='username',
        ),
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default='username', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='school',
            field=models.CharField(choices=[('CSOM', 'CSOM'), ('MCAS', 'MCAS'), ('LSEHD', 'LSEHD'), ('CSON', 'CSON'), ('LAW', 'LAW')], max_length=100),
        ),
    ]