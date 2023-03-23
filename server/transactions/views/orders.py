from rest_framework import generics
from drf_spectacular.utils import extend_schema_view, extend_schema
from transactions.models.orders import Order
from rest_framework.permissions import IsAuthenticated, AllowAny
from transactions.serializers.orders import CreateOrderSerializer, UpdateOrderSerializer

@extend_schema_view(
    post=extend_schema(summary='Создание заявки', tags=['Заявки']),
)
class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer
    # permission_classes = (IsAuthenticated,)
    # FOR TESTS ONLY
    permission_classes = (AllowAny,)
    http_method_names = ('post',)


@extend_schema_view(
    patch=extend_schema(summary='Частичное редактирование заявки', tags=['Редактирование заявки'])
)
class UpdateOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = UpdateOrderSerializer
    # permission_classes = (IsAuthenticated,)
    # FOR TESTS ONLY
    permission_classes = (AllowAny,)
    http_method_names = ('patch',)



            















