from rest_framework import serializers
from transactions.models.orders import Order
from transactions.models.transcations import Transaction
from django.forms.models import model_to_dict
from rest_framework.exceptions import ParseError


class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'buy_order',
            'sell_order',
        )

    def validate(self, attrs):
        buy_order_id = attrs.get('buy_order')
        sell_order_id = attrs.get('sell_order')

        buy_order = Order.objects.get(id=buy_order_id.id)
        sell_order = Order.objects.get(id=sell_order_id.id)
        
        if buy_order.order_type == sell_order.order_type:
            raise ParseError('You can not create transactions with equal order tyoes')

        if buy_order.user.id == sell_order.user.id:
            raise ParseError('You can not create transaction with your own orders')

        return attrs


    def create(self,validated_data):
        buy_order_id = validated_data['buy_order']
        sell_order_id = validated_data['sell_order']

        order_to_dict = model_to_dict(buy_order_id)
        order = Order.objects.get(
            id=order_to_dict.pop('id')
        )

        transaction = Transaction.objects.create(
            buy_order = buy_order_id,
            sell_order=sell_order_id,
            asset = order.asset,
            price =  order_to_dict.pop('order_price'),
            quantity = order_to_dict.pop('order_quantity'),
        )
        return transaction