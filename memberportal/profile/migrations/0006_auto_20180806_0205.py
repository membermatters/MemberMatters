# Generated by Django 2.0 on 2018-08-05 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0005_profile_last_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_invoice',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='logtype',
            field=models.CharField(choices=[('generic', 'Generic log entry'), ('usage', 'Generic usage access'), ('stripe', 'Stripe related event'), ('spacebucks', 'Spacebucks related event'), ('profile', 'Member profile edited'), ('interlock', 'Interlock related event'), ('door', 'Door related event'), ('email', 'Email send event'), ('admin', 'Generic admin event'), ('error', 'Some event that causes an error'), ('xero', 'Generic xero log entry')], max_length=30, verbose_name='Type of action/event'),
        ),
    ]
