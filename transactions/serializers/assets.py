from rest_framework import serializers
from rest_framework.exceptions import ParseError
from transactions.models.assets import Asset

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = (
            'id',
            'name',
            'symbol',
            'current_price',
            )

class UpdatePriceAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = (
            'current_price',
        )

        def update(self, instance, validated_data):
            return super().update(instance, validated_data)
            