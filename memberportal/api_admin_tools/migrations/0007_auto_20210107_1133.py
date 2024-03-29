# Generated by Django 3.1.4 on 2021-01-07 01:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api_admin_tools", "0006_membertier_featured"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentplan",
            name="member_tier",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="plans",
                to="api_admin_tools.membertier",
            ),
        ),
    ]
