from rest_framework import serializers
from transactions.models.assets import Asset

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'