# Generated by Django 3.2.21 on 2023-10-12 09:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_spacedirectory", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="spaceapisensor",
            name="unit",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="spaceapisensor",
            name="value",
            field=models.DecimalField(
                blank=True, decimal_places=3, max_digits=10, null=True
            ),
        ),
    ]
