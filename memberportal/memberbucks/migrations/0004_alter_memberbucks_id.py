# Generated by Django 3.2.2 on 2021-10-04 14:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("memberbucks", "0003_auto_20210427_1500"),
    ]

    operations = [
        migrations.AlterField(
            model_name="memberbucks",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
