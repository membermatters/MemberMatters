# Generated by Django 3.1.4 on 2021-02-18 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0004_profile_subscription_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="picture",
        ),
        migrations.AlterField(
            model_name="profile",
            name="state",
            field=models.CharField(
                choices=[
                    ("noob", "Needs Induction"),
                    ("active", "Active"),
                    ("inactive", "Inactive"),
                ],
                default="noob",
                max_length=8,
            ),
        ),
    ]
