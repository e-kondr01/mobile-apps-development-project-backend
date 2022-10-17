from django.contrib import admin

from .models import Characteristic, PriceType, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("ref_key",)


@admin.register(PriceType)
class PriceTypeAdmin(admin.ModelAdmin):
    readonly_fields = ("ref_key",)


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    readonly_fields = ("ref_key",)
