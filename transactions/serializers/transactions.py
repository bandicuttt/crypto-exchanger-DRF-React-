from rest_framework import serializers
from transactions.models.orders import Order
from transactions.models.transcations import Transaction
from django.forms.models import model_to_dict


class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'buy_order',
            'sell_order',
        )


    def create(self,validated_data):
        order_to_dict = model_to_dict(buy_order_id)
        order = Order.objects.get(
            id=order_to_dict.pop('id')
        )

        buy_order_id = validated_data['buy_order']
        sell_order_id = validated_data['sell_order']

        transaction = Transaction.objects.create(
            buy_order = buy_order_id,
            sell_order=sell_order_id,
            asset = order.asset,
            price =  order_to_dict.pop('order_price'),
            quantity = order_to_dict.pop('order_quantity'),
        )
        return transaction