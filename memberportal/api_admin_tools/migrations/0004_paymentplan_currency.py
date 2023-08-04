# Generated by Django 3.1.4 on 2021-01-02 06:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_admin_tools", "0003_auto_20210102_1536"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentplan",
            name="currency",
            field=models.CharField(
                default="aud",
                max_length=3,
                verbose_name="Three letter ISO currency code.",
            ),
        ),
    ]
