# Generated by Django 5.1.2 on 2024-11-03 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainApp", "0009_rename_title_news_display_title_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="date_begin",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="news",
            name="date_end",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="news",
            name="time_begin",
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name="news",
            name="time_end",
            field=models.TimeField(),
        ),
    ]