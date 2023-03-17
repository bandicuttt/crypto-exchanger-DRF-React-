from django.db import models
from users.models.users import User
from transactions.models.assets import Asset


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('active', 'Active',),
        ('rejected', 'Rejected',),
        ('filled', 'Filled',),
        ('cancelled', 'Cancelled',),
    ]
    ORDER_TYPE_CHOICES = [
        ('buy', 'Buy',),
        ('sell', 'Sell',),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE
        )
    order_type = models.CharField(
        max_length=4,
        choices=ORDER_TYPE_CHOICES
        )
    order_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
        )
    order_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
        )
    order_status = models.CharField(
        max_length=15,
        choices=ORDER_STATUS_CHOICES,
        default='Active')
    created_at = models.DateTimeField(
        auto_now_add=True
        )
    updated_at = models.DateTimeField(
        auto_now=True
        )

    def __str__(self):
        return f"{self.order_type} {self.order_quantity} {self.asset.symbol} at {self.order_price}"
    
    class Meta:
        verbose_name='Order'
        verbose_name_plural='Orders'