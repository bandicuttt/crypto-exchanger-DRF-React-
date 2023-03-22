from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from transactions.models.assets import Asset
from transactions.serializers.assets import UpdatePriceAssetSerializer
from transactions.views.assets import UpdateAssetPriceView, get_intersections
from unittest.mock import patch


User = get_user_model()


class AssetTestCase(APITestCase):
    def setUp(self):
        self.asset = Asset.objects.create(name='Bitcoin', symbol='BTC', current_price=Decimal('50000.00'))
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='password123')
        self.basic_user = User.objects.create(username='user', email='user@example.com', password='password123')

    def test_update_asset_price(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('update-asset-price', kwargs={'symbol': self.asset.symbol})
        response = self.client.patch(url, data={'symbol': self.asset.symbol, 'current_price': Decimal('60000.00')})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_price'], '60000.00')

    def test_update_asset_price_is_not_asset(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('update-asset-price', kwargs={'symbol': 'ABCD'})
        response = self.client.patch(url, data={'symbol': 'BCDA', 'current_price': Decimal('60000.00')})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_is_not_permissions(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('update-asset-price', kwargs={'symbol': self.asset.symbol})
        response = self.client.patch(url, data={'symbol': self.asset.symbol, 'current_price': Decimal('60000.00')})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_is_not_auth(self):
        url = reverse('update-asset-price', kwargs={'symbol': self.asset.symbol})
        response = self.client.patch(url, data={'symbol': self.asset.symbol, 'current_price': Decimal('60000.00')})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_crosses_assets(self):
        Asset.objects.create(name='Ethereum', symbol='ETH', current_price=Decimal('2000.00'))
        Asset.objects.create(name='Litecoin', symbol='LTC', current_price=Decimal('150.00'))
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('asset-crosses')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.data, ['BTC/ETH', 'BTC/LTC', 'ETH/LTC'])
