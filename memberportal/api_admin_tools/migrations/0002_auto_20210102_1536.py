# Generated by Django 3.1.4 on 2021-01-02 05:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_admin_tools", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="paymentplan",
            name="period",
        ),
        migrations.AddField(
            model_name="paymentplan",
            name="interval_count",
            field=models.IntegerField(
                default=1,
                verbose_name="The interval the price is charged at (per billing period).",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="paymentplan",
            name="interval",
            field=models.CharField(
                choices=[("Months", "month"), ("Weeks", "week"), ("Days", "days")],
                max_length=10,
            ),
        ),
    ]
