# Generated by Django 4.1.2 on 2022-10-21 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0016_remove_pricechange_unique_price_change_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="pricechange",
            options={
                "ordering": ("-period",),
                "verbose_name": "Изменение цены",
                "verbose_name_plural": "Изменения цены",
            },
        ),
    ]
