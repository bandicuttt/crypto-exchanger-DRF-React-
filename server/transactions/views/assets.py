from django.shortcuts import get_object_or_404
from rest_framework import generics
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from transactions.models.assets import Asset
from transactions.serializers.assets import AssetSerializer, UpdatePriceAssetSerializer
from rest_framework.response import Response

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
    

def get_intersections(assets_list):
    result = []
    for i in range(len(assets_list)):
        for j in range(i+1, len(assets_list)):
            intersection = f"{assets_list[i]}/{assets_list[j]}"
            result.append(intersection)
    return result

@extend_schema_view(
    get=extend_schema(summary='Получение пересечений всех активов', tags=['Активы'])
)
class GetCrossesAssetView(generics.ListAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get',)

    def get(self, request, *args, **kwargs):
        assets_list = [asset.symbol for asset in self.get_queryset()]
        intersections = get_intersections(assets_list)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(intersections)
