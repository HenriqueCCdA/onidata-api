# Generated by Django 5.0.3 on 2024-03-18 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_rename_interest_rate_loan_rate_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="loan",
            name="request_date",
            field=models.DateField(default="2024-01-01"),
            preserve_default=False,
        ),
    ]
