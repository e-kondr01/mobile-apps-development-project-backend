# Generated by Django 4.1.2 on 2022-10-16 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="size",
            field=models.CharField(blank=True, max_length=127, verbose_name="Размер"),
        ),
    ]