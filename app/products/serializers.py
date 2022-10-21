from rest_framework import serializers

from .models import (
    Barcode,
    Characteristic,
    PriceChange,
    PriceType,
    Product,
    ProductMovement,
)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class BarcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barcode
        fields = "__all__"


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = "__all__"


class PriceChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceChange
        fields = "__all__"


class PriceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceType
        fields = "__all__"


class ProductMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMovement
        fields = "__all__"
