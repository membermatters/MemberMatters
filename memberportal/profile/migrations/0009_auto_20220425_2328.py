# Generated by Django 3.2.12 on 2022-04-25 13:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0008_auto_20220425_2310"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profile",
            options={
                "permissions": [
                    ("change_staff", "Can change if the user is a staff member or not"),
                    ("manage_access", "Can manage a user's access permissions"),
                    ("deactivate_member", "Can deactivate or activate a member"),
                    (
                        "see_personal_details",
                        "Can see and update a member's personal details",
                    ),
                    (
                        "manage_memberbucks_balance",
                        "Can see and modify memberbucks balance",
                    ),
                    ("member_logs", "Can see a members log"),
                ]
            },
        ),
        migrations.RemoveField(
            model_name="profile",
            name="xero_account_id",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="xero_account_number",
        ),
    ]
