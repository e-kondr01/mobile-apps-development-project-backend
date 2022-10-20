# Generated by Django 4.1.2 on 2022-10-20 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0013_pricechange_unique_price_change_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="productmovement",
            name="unique_movement",
        ),
        migrations.AddConstraint(
            model_name="productmovement",
            constraint=models.UniqueConstraint(
                fields=("product", "characteristic", "period", "amount"),
                name="unique_movement",
            ),
        ),
    ]
