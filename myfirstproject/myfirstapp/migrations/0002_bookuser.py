# Generated by Django 5.0.1 on 2024-02-06 11:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myfirstapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BookUser",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("date_ordered", models.DateTimeField(auto_now_add=True)),
                ("review", models.TextField(null=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="myfirstapp.book",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
