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


class Barcode(models.Model):

    product: Product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="barcodes",
        verbose_name="Товар",
    )

    characteristic: Characteristic = models.ForeignKey(
        to=Characteristic,
        on_delete=models.CASCADE,
        related_name="barcodes",
        verbose_name="Характеристика",
    )

    barcode = models.CharField(max_length=255, verbose_name="Штрикход")

    NOT_NATURAL_KEYS = tuple()

    def __str__(self) -> str:
        return f"Штрикод {self.product} {self.characteristic}"

    class Meta:
        verbose_name = "Штрихкод"
        verbose_name_plural = "Штрихкоды"
        constraints = [
            models.UniqueConstraint(
                name="unique_barcode", fields=("product", "characteristic", "barcode")
            )
        ]


class ProductMovement(models.Model):

    product: Product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="product_movements",
        verbose_name="Товар",
    )

    characteristic: Characteristic = models.ForeignKey(
        to=Characteristic,
        on_delete=models.CASCADE,
        related_name="product_movements",
        verbose_name="Характеристика",
    )

    amount = models.SmallIntegerField(verbose_name="Количество")

    period = models.DateTimeField(verbose_name="Время и дата")

    NOT_NATURAL_KEYS = tuple()

    def __str__(self) -> str:
        return f"Движение товара {self.product} {self.characteristic} {self.period} "

    class Meta:
        verbose_name = "Движение товара"
        verbose_name_plural = "Движения товаров"
        constraints = [
            models.UniqueConstraint(
                name="unique_movement",
                fields=("product", "characteristic", "period", "amount"),
            )
        ]


class PriceChange(models.Model):

    product: Product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="price_changes",
        verbose_name="Товар",
    )

    characteristic: Characteristic = models.ForeignKey(
        to=Characteristic,
        on_delete=models.CASCADE,
        related_name="price_changes",
        verbose_name="Характеристика",
    )

    price = models.PositiveIntegerField(verbose_name="Цена")

    period = models.DateTimeField(verbose_name="Время и дата")

    price_type: PriceType = models.ForeignKey(
        PriceType,
        on_delete=models.CASCADE,
        related_name="price_changes",
        verbose_name="Вид цены",
    )

    NOT_NATURAL_KEYS = ("price_type_id",)

    def __str__(self) -> str:
        return f"Изменение цены {self.product} {self.characteristic} {self.period}"

    class Meta:
        verbose_name = "Изменение цены"
        verbose_name_plural = "Изменения цены"
        constraints = [
            models.UniqueConstraint(
                name="unique_price_change",
                fields=("product", "characteristic", "period", "price"),
            )
        ]
