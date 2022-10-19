from django.contrib import admin

from .models import (
    Barcode,
    Characteristic,
    PriceChange,
    PriceType,
    Product,
    ProductMovement,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("ref_key",)


@admin.register(PriceType)
class PriceTypeAdmin(admin.ModelAdmin):
    readonly_fields = ("ref_key",)


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    readonly_fields = ("ref_key",)


@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductMovement)
class ProductMovementAdmin(admin.ModelAdmin):
    pass


@admin.register(PriceChange)
class PriceChangeAdmin(admin.ModelAdmin):
    pass
