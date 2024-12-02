# Generated by Django 5.1.2 on 2024-12-02 16:33

import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Campaign",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(max_length=500)),
                ("date_begin", models.DateField()),
                ("date_end", models.DateField()),
                ("time_begin", models.TimeField()),
                ("time_end", models.TimeField()),
                ("points", models.IntegerField(default=0)),
                ("news", models.BooleanField(default=True)),
                (
                    "location",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Lower", "Lower"),
                            ("McElroy", "McElroy"),
                            ("Stuart", "Stuart"),
                            ("Addie's", "Addie's"),
                            ("Eagle's Nest", "Eagle's Nest"),
                        ],
                        max_length=41,
                    ),
                ),
                (
                    "validation",
                    models.CharField(
                        choices=[
                            ("photo validation", "photo validation"),
                            ("QR", "QR"),
                        ],
                        default="photo validation",
                        max_length=100,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="News",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("display_title", models.CharField(max_length=500)),
                (
                    "external_url",
                    models.URLField(blank=True, max_length=500, null=True),
                ),
                ("date_posted", models.DateTimeField(auto_now_add=True)),
                ("date_begin", models.DateField()),
                ("date_end", models.DateField()),
                ("time_begin", models.TimeField()),
                ("time_end", models.TimeField()),
                (
                    "news_image",
                    models.ImageField(blank=True, null=True, upload_to="news_images/"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Rewards",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=500)),
                ("date_begin", models.DateField()),
                ("date_end", models.DateField()),
                ("time_begin", models.TimeField()),
                ("time_end", models.TimeField()),
                ("description", models.TextField(max_length=500)),
                ("points", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "bc_email",
                    models.EmailField(
                        default="default@bc.edu", max_length=254, unique=True
                    ),
                ),
                (
                    "school",
                    models.CharField(
                        choices=[
                            ("", "Select School"),
                            ("CSOM", "CSOM"),
                            ("MCAS", "MCAS"),
                            ("LSEHD", "LSEHD"),
                            ("CSON", "CSON"),
                            ("LAW", "LAW"),
                        ],
                        max_length=100,
                    ),
                ),
                ("graduation_year", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "major",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Accounting", "Accounting"),
                            (
                                "Accounting_Finance_Consulting",
                                "Accounting for Finance and Consulting",
                            ),
                            ("African_Studies", "African and African Diaspora Studies"),
                            ("American_Heritages", "American Heritages"),
                            ("Applied_Physics", "Applied Physics"),
                            (
                                "Applied_Psychology_Human_Development",
                                "Applied Psychology and Human Development",
                            ),
                            ("Art_History", "Art History"),
                            ("Biochemistry", "Biochemistry"),
                            ("Biology", "Biology"),
                            ("Business_Analytics", "Business Analytics"),
                            ("Chemistry", "Chemistry"),
                            ("Classical_Studies", "Classical Studies"),
                            ("Communication", "Communication"),
                            ("Computer_Science", "Computer Science"),
                            ("Economics", "Economics"),
                            ("Elementary_Education", "Elementary Education"),
                            ("English", "English"),
                            ("Environmental_Geoscience", "Environmental Geoscience"),
                            ("Environmental_Studies", "Environmental Studies"),
                            ("Film_Studies", "Film Studies"),
                            ("Finance", "Finance"),
                            ("French", "French"),
                            ("General_Management", "General Management"),
                            ("Geological_Sciences", "Geological Sciences"),
                            ("German_Studies", "German Studies"),
                            (
                                "Global_Public_Health",
                                "Global Public Health and the Common Good",
                            ),
                            ("History", "History"),
                            ("Hispanic_Studies", "Hispanic Studies"),
                            (
                                "Human_Centered_Engineering",
                                "Human-Centered Engineering",
                            ),
                            ("Independent", "Independent"),
                            ("International_Studies", "International Studies"),
                            (
                                "Islamic_Civilization_Societies",
                                "Islamic Civilization and Societies",
                            ),
                            ("Italian", "Italian"),
                            ("Linguistics", "Linguistics"),
                            ("Management_Leadership", "Management and Leadership"),
                            ("Marketing", "Marketing"),
                            ("Mathematics", "Mathematics"),
                            (
                                "Mathematics_Computer_Science",
                                "Mathematics/Computer Science",
                            ),
                            ("Music", "Music"),
                            ("Neuroscience", "Neuroscience"),
                            ("Nursing", "Nursing"),
                            (
                                "Perspectives_on_Spanish_America",
                                "Perspectives on Spanish America",
                            ),
                            ("Philosophy", "Philosophy"),
                            ("Physics", "Physics"),
                            ("Political_Science", "Political Science"),
                            ("Psychology", "Psychology"),
                            ("Russian", "Russian"),
                            ("Secondary_Education", "Secondary Education"),
                            ("Slavic_Studies", "Slavic Studies"),
                            ("Sociology", "Sociology"),
                            ("Studio_Art", "Studio Art"),
                            ("Theatre", "Theatre"),
                            ("Theology", "Theology"),
                            (
                                "Transformative_Educational_Studies",
                                "Transformative Educational Studies",
                            ),
                        ],
                        max_length=861,
                    ),
                ),
                (
                    "minor",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Accounting_CPAs", "Accounting for CPAs"),
                            (
                                "Accounting_Finance_Consulting",
                                "Accounting for Finance & Consulting",
                            ),
                            ("African_Studies", "African and African Diaspora Studies"),
                            ("American_Studies", "American Studies"),
                            ("Ancient_Civilization", "Ancient Civilization"),
                            ("Ancient_Greek", "Ancient Greek"),
                            ("Arabic", "Arabic"),
                            (
                                "Applied_Psychology_Human_Development",
                                "Applied Psychology and Human Development",
                            ),
                            ("Art_History", "Art History"),
                            ("Asian_Studies", "Asian Studies"),
                            ("Biology", "Biology"),
                            ("Catholic_Studies", "Catholic Studies"),
                            ("Chemistry", "Chemistry"),
                            ("Chinese", "Chinese"),
                            ("Communication", "Communication"),
                            ("Computer_Science", "Computer Science"),
                            ("Cyberstrategy_Design", "Cyberstrategy and Design"),
                            ("Dance", "Dance"),
                            ("Data_Science", "Data Science"),
                            (
                                "Design_Thinking_Innovation",
                                "Design Thinking and Innovation",
                            ),
                            (
                                "East_European_Eurasian_Studies",
                                "East European and Eurasian Studies",
                            ),
                            ("Economics", "Economics"),
                            ("Educational_Theatre", "Educational Theatre"),
                            ("English", "English"),
                            ("Environmental_Studies", "Environmental Studies"),
                            ("Faith_Peace_Justice", "Faith, Peace & Justice"),
                            ("Film_Studies", "Film Studies"),
                            ("Finance", "Finance"),
                            ("Foundation_in_Education", "Foundation in Education"),
                            ("French", "French"),
                            ("General_Business", "General Business"),
                            ("Geological_Sciences", "Geological Sciences"),
                            ("German", "German"),
                            ("German_Studies", "German Studies"),
                            (
                                "Global_Public_Health",
                                "Global Public Health and the Common Good",
                            ),
                            ("Hispanic_Studies", "Hispanic Studies"),
                            ("History", "History"),
                            (
                                "Immigration_Education_Humanitarian_Studies",
                                "Immigration, Education, and Humanitarian Studies",
                            ),
                            ("Inclusive_Education", "Inclusive Education"),
                            ("International_Studies", "International Studies"),
                            ("Irish_Studies", "Irish Studies"),
                            (
                                "Islamic_Civilization_Societies",
                                "Islamic Civilization & Societies",
                            ),
                            ("Italian", "Italian"),
                            ("Jewish_Studies", "Jewish Studies"),
                            ("Journalism", "Journalism"),
                            ("Latin_American_Studies", "Latin American Studies"),
                            (
                                "Leadership_Higher_Education_Community",
                                "Leadership in Higher Education and Community Settings",
                            ),
                            ("Linguistics", "Linguistics"),
                            ("Management_Leadership", "Management & Leadership"),
                            (
                                "Managing_Social_Impact_Public_Good",
                                "Managing for Social Impact and the Public Good",
                            ),
                            ("Marketing", "Marketing"),
                            ("Mathematics", "Mathematics"),
                            (
                                "Medical_Humanities_Health_Culture",
                                "Medical Humanities, Health, and Culture",
                            ),
                            (
                                "Middle_School_Mathematics_Teaching",
                                "Middle School Mathematics Teaching",
                            ),
                            ("Music", "Music"),
                            ("Philosophy", "Philosophy"),
                            ("Physics", "Physics"),
                            (
                                "Religion_American_Public_Life",
                                "Religion and American Public Life",
                            ),
                            (
                                "Research_Evaluation_Measurement",
                                "Research, Evaluation, and Measurement",
                            ),
                            (
                                "Restorative_Transformational_Justice",
                                "Restorative and Transformational Justice",
                            ),
                            ("Russian", "Russian"),
                            ("Secondary_Education", "Secondary Education"),
                            ("Sociology", "Sociology"),
                            ("Special_Education", "Special Education"),
                            ("Studio_Art", "Studio Art"),
                            ("TELL_Certificate", "TELL Certificate"),
                            ("Theatre", "Theatre"),
                            ("Theology", "Theology"),
                            ("Womens_Gender_Studies", "Women's & Gender Studies"),
                        ],
                        max_length=1224,
                        null=True,
                    ),
                ),
                (
                    "picture",
                    models.ImageField(blank=True, null=True, upload_to="profile_pics/"),
                ),
                ("bio", models.TextField(blank=True, null=True)),
                ("points", models.IntegerField(default=0)),
                ("total_points", models.IntegerField(default=0)),
                ("previous_rank", models.IntegerField(blank=True, null=True)),
                (
                    "last_points_update",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("rank_change", models.IntegerField(default=0)),
                ("streak_status", models.IntegerField(default=0)),
                (
                    "username",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Redeemed",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=500)),
                ("date_begin", models.DateField()),
                ("date_end", models.DateField()),
                ("time_begin", models.TimeField()),
                ("time_end", models.TimeField()),
                ("description", models.TextField(max_length=500)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReferralTask",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("referee_email", models.EmailField(max_length=254)),
                ("points", models.IntegerField(default=10)),
                ("completed", models.BooleanField(default=False)),
                ("completion_date", models.DateField(blank=True, null=True)),
                (
                    "referrer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="referrals",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WeeklyTask",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("points", models.IntegerField(default=0)),
                ("completed", models.BooleanField(default=False)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("completion_criteria", models.JSONField(default=dict)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weekly_tasks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DailyTask",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("points", models.IntegerField(default=0)),
                ("completed", models.BooleanField(default=False)),
                ("is_static", models.BooleanField(default=True)),
                ("completion_criteria", models.JSONField(default=dict)),
                ("date_created", models.DateField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="daily_tasks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {
                    ("user", "title", "is_static", "completion_criteria")
                },
            },
        ),
    ]
