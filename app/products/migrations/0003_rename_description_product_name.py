# Generated by Django 4.1.2 on 2022-10-17 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_product_size"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="description",
            new_name="name",
        ),
    ]
