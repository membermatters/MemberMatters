# Generated by Django 3.2.25 on 2024-05-23 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("access", "0016_auto_20240523_1550"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accesscontrolleddevice",
            name="play_theme",
            field=models.BooleanField(
                default=False, verbose_name="Play theme on successful swipe"
            ),
        ),
        migrations.AlterField(
            model_name="accesscontrolleddevice",
            name="post_to_discord",
            field=models.BooleanField(
                default=True, verbose_name="Post to discord on swipe"
            ),
        ),
        migrations.AlterField(
            model_name="accesscontrolleddevice",
            name="report_online_status",
            field=models.BooleanField(
                default=True,
                verbose_name="Report the online status of this device and fail the uptime check if it's offline.",
            ),
        ),
        migrations.AlterField(
            model_name="memberbucksdevice",
            name="supports_products",
            field=models.BooleanField(
                default=False, verbose_name="Supports the MM products API."
            ),
        ),
    ]
