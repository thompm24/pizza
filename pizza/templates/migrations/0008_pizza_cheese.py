# Generated by Django 5.0.2 on 2024-02-18 15:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("templates", "0007_cheese"),
    ]

    operations = [
        migrations.AddField(
            model_name="pizza",
            name="cheese",
            field=models.ForeignKey(
                default=1,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="templates.cheese",
            ),
        ),
    ]