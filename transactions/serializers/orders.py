from rest_framework import serializers
from transactions.models.orders import Order
from users.serializers.users import UserSerializer
from transactions.serializers.assets import AssetSerializer
from rest_framework.exceptions import ParseError


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    asset = AssetSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class UpdateOrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    asset = serializers.CharField(read_only=True)
    order_type = serializers.CharField(read_only=True)
    order_price  = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    order_quantity = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields =  '__all__'

        def update(self, instance, validated_data):
            user = self.context['request'].user
            if instance.user.id == user.id:
                return super().update(instance, validated_data)
            return ParseError(
                'Validate Error'
            )
        

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'order_type',
            'order_price',
            'order_quantity',
            'order_status',
            'asset',
        )
    
    def create(self, validated_data):
        user = self.context['request'].user
        order_type = validated_data['order_type']
        order_price = validated_data['order_price']
        order_quantity = validated_data['order_quantity']
        order_status  = validated_data['order_status']
        asset = validated_data['asset']
        order = Order.objects.create(
            user=user,
            order_type=order_type,
            order_price=order_price,
            order_quantity=order_quantity,
            order_status=order_status,
            asset=asset,
        )
        return order
    