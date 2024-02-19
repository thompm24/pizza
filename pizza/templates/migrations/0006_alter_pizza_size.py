# Generated by Django 5.0.2 on 2024-02-18 15:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("templates", "0005_pizza_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pizza",
            name="size",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="templates.size",
            ),
        ),
    ]
