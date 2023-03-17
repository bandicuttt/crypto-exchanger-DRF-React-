from django.db import models
from transactions.models.orders import Order
from transactions.models.assets import Asset


class Transaction(models.Model):
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE
        )
    buy_order = models.ForeignKey(
        Order,
        related_name='buy_order',
        on_delete=models.CASCADE
        )
    sell_order = models.ForeignKey(
        Order,
        related_name='sell_order',
        on_delete=models.CASCADE
        )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
        )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
        )
    executed_at = models.DateTimeField(
        auto_now_add=True
        )

    def __str__(self):
        return f"{self.quantity} {self.asset.symbol} at {self.price}"
    
    class Meta:
        verbose_name='Transaction'
        verbose_name_plural='Transactions'

    
    

