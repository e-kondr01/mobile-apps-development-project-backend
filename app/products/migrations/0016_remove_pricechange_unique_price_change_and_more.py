# Generated by Django 4.1.2 on 2022-10-20 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0015_alter_pricechange_price"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="pricechange",
            name="unique_price_change",
        ),
        migrations.AddConstraint(
            model_name="pricechange",
            constraint=models.UniqueConstraint(
                fields=("product", "characteristic", "period", "price"),
                name="unique_price_change",
            ),
        ),
    ]
