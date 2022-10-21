from rest_framework.generics import ListAPIView

from .models import (
    Barcode,
    Characteristic,
    PriceChange,
    PriceType,
    Product,
    ProductMovement,
)
from .serializers import (
    BarcodeSerializer,
    CharacteristicSerializer,
    PriceChangeSerializer,
    PriceTypeSerializer,
    ProductMovementSerializer,
    ProductSerializer,
)


class BarcodeListView(ListAPIView):
    queryset = Barcode.objects.all()
    serializer_class = BarcodeSerializer


class CharacteristicListView(ListAPIView):
    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicSerializer


class PriceChangeListView(ListAPIView):
    queryset = PriceChange.objects.all()
    serializer_class = PriceChangeSerializer


class PriceTypeListView(ListAPIView):
    queryset = PriceType.objects.all()
    serializer_class = PriceTypeSerializer


class ProductMovementListView(ListAPIView):
    queryset = ProductMovement.objects.all()
    serializer_class = ProductMovementSerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
