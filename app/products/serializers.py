from rest_framework import serializers

from .models import Product


class ODataProductSerializer(serializers.ModelSerializer):
    Ref_Key = serializers.CharField(source="ref_key")
    Description = serializers.CharField(source="description")

    class Meta:
        model = Product
        fields = ("Ref_Key", "Description")
