from rest_framework import serializers
from transactions.models.orders import Order
from users.serializers.users import UserSerializer
from transactions.serializers.assets import AssetSerializer
from rest_framework.exceptions import ParseError



class OrderPrices(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'order_price',
        )

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    asset = AssetSerializer()
    asset_pay = AssetSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class UpdateOrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    asset = AssetSerializer(read_only=True)
    asset_pay = AssetSerializer(read_only=True)
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
            'asset',
            'asset_pay',
        )
    
    def validate(self, attrs):
        asset = attrs.get('asset')
        asset_pay = attrs.get('asset_pay')
        order_price = attrs.get('order_price')
        order_quantity = attrs.get('order_quantity')

        if asset == asset_pay:
            raise ParseError("You cannot buy and sell the same currency")  
        
        if float(order_price) < 0:
            raise ParseError('Invalid order price')
        
        if float(order_quantity) < 0:
            raise ParseError('Invalid order quantity')
        return attrs
        
    def create(self, validated_data):
        user = self.context['request'].user
        order_type = validated_data['order_type']
        order_price = validated_data['order_price']
        order_quantity = validated_data['order_quantity']
        asset_pay = validated_data['asset_pay']
        asset = validated_data['asset']
        order = Order.objects.create(
            user=user,
            order_type=order_type,
            order_price=order_price,
            order_quantity=order_quantity,
            asset=asset,
            asset_pay=asset_pay,
            order_status='active',
        )
        return order
    