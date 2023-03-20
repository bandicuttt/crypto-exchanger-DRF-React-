from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from transactions.models.transcations import Transaction
from transactions.serializers.transactions import CreateTransactionSerializer


@extend_schema_view(
    post=extend_schema(summary='Создание транзакции', tags=['Транзакции']),
)
class CreateTransactionView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = CreateTransactionSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('post',)