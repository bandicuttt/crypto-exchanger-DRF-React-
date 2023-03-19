from django.shortcuts import get_object_or_404
from rest_framework import generics
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from transactions.models.assets import Asset
from transactions.serializers.assets import UpdatePriceAssetSerializer

@extend_schema_view(
    patch=extend_schema(summary='Редактирование цены актива', tags=['Активы'])
)
class UpdateAssetPriceView(generics.UpdateAPIView):
    queryset = Asset.objects.all()
    serializer_class = UpdatePriceAssetSerializer
    permission_classes = (IsAdminUser,)
    http_method_names = ('patch',)
    lookup_field = 'symbol'

    def get_object(self):
        symbol = self.request.data.get('symbol')
        obj = get_object_or_404(Asset, symbol=symbol)
        self.check_object_permissions(self.request, obj)
        return obj