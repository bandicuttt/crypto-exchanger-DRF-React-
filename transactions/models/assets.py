from django.db import models


class Asset(models.Model):
    name = models.CharField(
        max_length=20,
        )
    symbol = models.CharField(
        max_length=5,
        )
    current_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        )

    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name='Asset'
        verbose_name_plural='Assets'
    
    

