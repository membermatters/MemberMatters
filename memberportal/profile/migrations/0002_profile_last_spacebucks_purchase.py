# Generated by Django 2.0 on 2018-10-05 13:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_spacebucks_purchase',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
