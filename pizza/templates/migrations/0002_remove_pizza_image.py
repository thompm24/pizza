# Generated by Django 5.0.2 on 2024-02-17 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("templates", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pizza",
            name="image",
        ),
    ]
