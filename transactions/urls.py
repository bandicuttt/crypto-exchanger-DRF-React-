from django.urls import path, include
from transactions.views.orders import CreateOrderView, UpdateOrderView
from transactions.views.transactions import CreateTransactionView
from users.views.users import UserRegistrationView

urlpatterns = [
    path('orders/createneworder/', CreateOrderView.as_view(), name='create-new-order'),
    path('orders/updateorder/<int:pk>/', UpdateOrderView.as_view(), name='update-new-order'),
    path('tranasction/create/', CreateTransactionView.as_view(), name='create-new-transaction'),
    path('user/registration/', UserRegistrationView.as_view(), name='create-new-transaction'),
]