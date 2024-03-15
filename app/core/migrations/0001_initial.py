# Generated by Django 5.0.3 on 2024-03-14 20:37

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Loan",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Criado em")),
                ("modified_at", models.DateTimeField(auto_now=True, verbose_name="Modificado em")),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("nominal_value", models.DecimalField(decimal_places=2, max_digits=14)),
                ("interest_rate", models.DecimalField(decimal_places=2, max_digits=14)),
                ("register_ip", models.GenericIPAddressField()),
                ("bank", models.CharField(max_length=100)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="loans",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]