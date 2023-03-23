from django.shortcuts import get_object_or_404
from rest_framework import generics
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from transactions.models.assets import Asset
from transactions.serializers.assets import AssetSerializer, UpdatePriceAssetSerializer
from rest_framework.response import Response

@extend_schema_view(
    patch=extend_schema(summary='Редактирование цены актива', tags=['Активы'])
)
class UpdateAssetPriceView(generics.UpdateAPIView):
    queryset = Asset.objects.all()
    serializer_class = UpdatePriceAssetSerializer
    # permission_classes = (IsAdminUser,)
    # FOR TESTS ONLY
    permission_classes = (AllowAny,)
    http_method_names = ('patch',)
    lookup_field = 'symbol'

    def get_object(self):
        symbol = self.request.data.get('symbol')
        obj = get_object_or_404(Asset, symbol=symbol)
        self.check_object_permissions(self.request, obj)
        return obj
    

def get_intersections(assets_list):
    crosses = []
    for asset1 in assets_list:
        for asset2 in assets_list:
            if asset1 != asset2:
                asset_pair = f"{asset1['asset']}/{asset2['asset']}"
                cross = {
                    'asset': asset_pair,
                    'asset_id': asset1['asset_id'] if asset1['asset'] == asset_pair.split('/')[0] else asset2['asset_id']
                }
                crosses.append(cross)
    sorted_crosses = sorted(crosses, key=lambda c: c['asset'])
    return sorted_crosses

@extend_schema_view(
    get=extend_schema(summary='Получение пересечений всех активов', tags=['Активы'])
)
class GetCrossesAssetView(generics.ListAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    # permission_classes = (IsAuthenticated,)
    # FOR TESTS ONLY
    permission_classes = (AllowAny,)
    http_method_names = ('get',)

    def get(self, request, *args, **kwargs):
        assets_list = [{'asset':asset.symbol, 'asset_id':asset.id} for asset in self.get_queryset()]
        intersections = get_intersections(assets_list)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(intersections)
