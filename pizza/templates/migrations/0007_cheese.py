# Generated by Django 5.0.2 on 2024-02-18 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("templates", "0006_alter_pizza_size"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cheese",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=1, max_digits=3),
                ),
            ],
        ),
    ]
