# Generated by Django 3.2.13 on 2022-11-13 08:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("access", "0008_accesscontrolleddevice_report_online_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="accesscontrolleddevice",
            name="post_to_discord",
            field=models.BooleanField(
                default=True, verbose_name="Post to discord on door swipe"
            ),
        ),
    ]
