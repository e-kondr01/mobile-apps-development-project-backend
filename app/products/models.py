import uuid

from django.db import models


class Product(models.Model):

    ref_key = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Ключ"
    )

    description = models.CharField(max_length=255, verbose_name="Описание")

    size = models.CharField(max_length=127, blank=True, verbose_name="Размер")

    def __str__(self) -> str:
        return self.description

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
