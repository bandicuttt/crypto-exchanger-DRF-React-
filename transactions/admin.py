from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from transactions.models.assets import Asset
from transactions.models.orders import Order
from transactions.models.transcations import Transaction

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'name',
        'symbol',
        'current_price',
    )
    list_display_links=(
        'symbol',
    )
    ordering=(
        '-id',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'user',
        'asset',
        'asset_pay',
        'order_type',
        'order_price',
        'order_quantity',
        'order_status',
        'created_at',
        'updated_at',
    )
    list_display_links=(
        'id',
    )
    ordering=(
        '-id',
    )

@admin.register(Transaction)
class TranscationAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'asset',
        'buy_order',
        'sell_order',
        'price',
        'quantity',
        'executed_at',
    )
    list_display_links=(
        'id',
    )
    ordering=(
        '-id',
    )