# Generated by Django 4.1.2 on 2022-10-20 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0012_pricechange"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="pricechange",
            constraint=models.UniqueConstraint(
                fields=("product", "characteristic", "period"),
                name="unique_price_change",
            ),
        ),
        migrations.AddConstraint(
            model_name="productmovement",
            constraint=models.UniqueConstraint(
                fields=("product", "characteristic", "period"), name="unique_movement"
            ),
        ),
    ]