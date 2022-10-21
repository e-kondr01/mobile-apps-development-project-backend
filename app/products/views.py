from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

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
    ProductAmountSerializer,
    ProductMovementSerializer,
    ProductPriceSerializer,
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


@extend_schema(responses=ProductAmountSerializer(many=True))
class ProductAmountsView(GenericAPIView):
    queryset = Product.objects.all()
    pagination_class = None

    def get(self, _, *args, **kwargs):
        product: Product = self.get_object()
        return Response(product.get_amounts())


@extend_schema(responses=ProductPriceSerializer(many=True))
class ProductPricesView(GenericAPIView):
    queryset = Product.objects.all()
    pagination_class = None

    def get(self, _, *args, **kwargs):
        product: Product = self.get_object()
        return Response(product.get_prices())
