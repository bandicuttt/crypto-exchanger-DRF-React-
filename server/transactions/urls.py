from django.urls import path, include
from transactions.views.assets import GetCrossesAssetView, UpdateAssetPriceView
from transactions.views.orders import CreateOrderView, UpdateOrderView
from transactions.views.transactions import CreateTransactionView


urlpatterns = [
    path('orders/createneworder/', CreateOrderView.as_view(), name='create-new-order'),
    path('orders/updateorder/<int:pk>/', UpdateOrderView.as_view(), name='update-new-order'),
    path('tranasction/create/', CreateTransactionView.as_view(), name='create-new-transaction'),
    path('assets/updateasset/<str:symbol>/', UpdateAssetPriceView.as_view(), name='update-asset-price'),
    path('assets/getassetscross/', GetCrossesAssetView.as_view(), name='asset-crosses'),
]