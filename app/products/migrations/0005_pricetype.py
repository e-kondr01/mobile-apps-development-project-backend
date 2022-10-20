# Generated by Django 4.1.2 on 2022-10-17 19:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_remove_product_size_product_sku"),
    ]

    operations = [
        migrations.CreateModel(
            name="PriceType",
            fields=[
                (
                    "ref_key",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Ключ",
                    ),
                ),
                ("name", models.CharField(max_length=31, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Вид цены",
                "verbose_name_plural": "Виды цен",
            },
        ),
    ]