import uuid

from django.db import models


class Product(models.Model):

    ref_key = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Ключ"
    )

    name = models.CharField(max_length=255, verbose_name="Описание")

    sku = models.CharField(max_length=31, verbose_name="Артикул")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class PriceType(models.Model):

    ref_key = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Ключ"
    )

    name = models.CharField(max_length=31, verbose_name="Название")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Вид цены"
        verbose_name_plural = "Виды цен"


class Characteristic(models.Model):

    ref_key = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Ключ"
    )

    name = models.CharField(max_length=31, verbose_name="Название")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Характеристика товара"
        verbose_name_plural = "Характеристики товаров"
