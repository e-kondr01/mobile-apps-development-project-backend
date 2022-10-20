# Generated by Django 4.1.2 on 2022-10-19 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0010_delete_productmovement"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductMovement",
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
                ("amount", models.SmallIntegerField(verbose_name="Количество")),
                ("period", models.DateTimeField(verbose_name="Время и дата")),
                (
                    "characteristic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_movements",
                        to="products.characteristic",
                        verbose_name="Характеристика",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_movements",
                        to="products.product",
                        verbose_name="Товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "Движение товара",
                "verbose_name_plural": "Движения товаров",
            },
        ),
    ]