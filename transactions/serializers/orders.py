from rest_framework import serializers
from transactions.models.orders import Order
from users.serializers.users import UserSerializer
from transactions.serializers.assets import AssetSerializer

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    asset = AssetSerializer()

    class Meta:
        model = Order
        fields = '__all__'