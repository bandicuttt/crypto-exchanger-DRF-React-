import pytest
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from transactions.consumers import AssetConsumer, GetOrdersConsumer
from transactions.models.assets import Asset
from transactions.serializers.assets import AssetSerializer
from transactions.serializers.orders import OrderSerializer
from transactions.models.orders import Order
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async


User = get_user_model()


class CreateTransactionTestCase(APITestCase):
    def setUp(self):
        self.asset_pay = Asset.objects.create(name='Etherium', symbol='ETH', current_price=Decimal('50000.00'))
        self.asset = Asset.objects.create(name='Bitcoin', symbol='BTC', current_price=Decimal('50000.00'))
        self.basic_user = User.objects.create(username='user1', email='user1@example.com', password='password123')
        self.basic_user_2 = User.objects.create(username='user', email='user@example.com', password='password123')
        self.order_2 = Order.objects.create(user=self.basic_user_2, asset=self.asset, asset_pay=self.asset_pay, order_type='sell', order_price=222, order_quantity=433)
        self.order_3 = Order.objects.create(user=self.basic_user, asset=self.asset, asset_pay=self.asset_pay, order_type='buy', order_price=222, order_quantity=433)
        self.order = Order.objects.create(user=self.basic_user, asset=self.asset, asset_pay=self.asset_pay, order_type='buy', order_price=222, order_quantity=433)
        self.order_4 = Order.objects.create(user=self.basic_user_2, asset=self.asset, asset_pay=self.asset_pay, order_type='buy', order_price=222, order_quantity=433)


    def test_create_transaction_success(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-transaction')
        response = self.client.post(url, data={'buy_order':self.order.id, 'sell_order': self.order_2.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_transactions_with_equal_users(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-transaction')
        response = self.client.post(url, data={'buy_order':self.order.id, 'sell_order': self.order_3.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_transactions_with_equal_order_types(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-transaction')
        response = self.client.post(url, data={'buy_order':self.order.id, 'sell_order': self.order_4.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_transaction_unauth(self):
        url = reverse('create-new-transaction')
        response = self.client.post(url, data={'buy_order':self.order.id, 'sell_order': self.order_2.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_transaction_invalid_buy_order(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-transaction')
        response = self.client.post(url, data={'buy_order':'222', 'sell_order': self.order_2.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_transaction_invalid_sell_order(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-transaction')
        response = self.client.post(url, data={'buy_order':self.order.id, 'sell_order': '222'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_transaction_invalid_request_method(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-transaction')
        response = self.client.patch(url, data={'buy_order':self.order.id, 'sell_order': self.order_2.id})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class UpdateOrderTestCase(APITestCase):
    def setUp(self):
        self.asset_pay = Asset.objects.create(name='Etherium', symbol='ETH', current_price=Decimal('50000.00'))
        self.asset = Asset.objects.create(name='Bitcoin', symbol='BTC', current_price=Decimal('50000.00'))
        self.basic_user = User.objects.create(username='user', email='user@example.com', password='password123')
        self.basic_user_2 = User.objects.create(username='user2', email='use2r@example.com', password='password123')
        self.order = Order.objects.create(user=self.basic_user, asset=self.asset, asset_pay=self.asset_pay, order_type='buy', order_price=222, order_quantity=433)

    def test_update_order_success(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('update-new-order', kwargs={'pk': self.order.id})
        response = self.client.patch(url, data={'order_status':'cancelled'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order_unauth(self):
        url = reverse('update-new-order', kwargs={'pk': self.order.id})
        response = self.client.patch(url, data={'order_status':'cancelled'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_order_invalid_order_status(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('update-new-order', kwargs={'pk': self.order.id})
        response = self.client.patch(url, data={'order_status':'test'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_invalid_user(self):
        self.client.force_authenticate(user=self.basic_user_2)
        url = reverse('update-new-order', kwargs={'pk': self.order.id})
        response = self.client.patch(url, data={'order_status':'test'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_invalid_order_id(self):
        self.client.force_authenticate(user=self.basic_user_2)
        url = reverse('update-new-order', kwargs={'pk': 111})
        response = self.client.patch(url, data={'order_status':'cancelled'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateOrdersTestCase(APITestCase):
    def setUp(self):
        self.asset = Asset.objects.create(name='Bitcoin', symbol='BTC', current_price=Decimal('50000.00'))
        self.asset_pay = Asset.objects.create(name='Etherium', symbol='ETH', current_price=Decimal('50000.00'))
        self.basic_user = User.objects.create(username='user', email='user@example.com', password='password123')

    def test_create_order_buy_success(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-order')
        response = self.client.post(url, data={'asset':self.asset.id, 'asset_pay':self.asset_pay.id, 'order_type':'buy', 'order_price':222, 'order_quantity':433})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_order_sell_success(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-order')
        response = self.client.post(url, data={'asset':self.asset.id, 'asset_pay':self.asset_pay.id, 'order_type':'sell', 'order_price':222, 'order_quantity':433})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_unauth(self):
        url = reverse('create-new-order')
        response = self.client.post(url, data={'asset':self.asset.id, 'asset_pay':self.asset_pay.id, 'order_type':'sell', 'order_price':222, 'order_quantity':433})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_invalid_order_type(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-order')
        response = self.client.post(url, data={'asset':self.asset.id, 'asset_pay':self.asset_pay.id, 'order_type':'test', 'order_price':222, 'order_quantity':433})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_asset_not_found(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-order')
        response = self.client.post(url, data={'asset':2222, 'asset_pay':self.asset_pay.id, 'order_type':'buy', 'order_price':222, 'order_quantity':433})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_asset_pay_not_found(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-order')
        response = self.client.post(url, data={'asset':self.asset.id, 'asset_pay':333, 'order_type':'buy', 'order_price':222, 'order_quantity':433})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_asset_equal_asset_pay(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-order')
        response = self.client.post(url, data={'asset':self.asset.id, 'asset_pay':self.asset.id, 'order_type':'buy', 'order_price':222, 'order_quantity':433})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_invalid_order_price(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-order')
        response = self.client.post(url, data={'asset':self.asset.id, 'asset_pay':self.asset.id, 'order_type':'buy', 'order_price':'fff', 'order_quantity':433})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_negative_order_price(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-order')
        response = self.client.post(url, data={'asset':self.asset.id, 'asset_pay':self.asset.id, 'order_type':'buy', 'order_price':-200, 'order_quantity':433})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_order_zero_order_price(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-order')
        response = self.client.post(url, data={'asset':self.asset.id, 'asset_pay':self.asset.id, 'order_type':'buy', 'order_price':0, 'order_quantity':433})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_invalid_order_quantity(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-order')
        response = self.client.post(url, data={'asset':self.asset.id, 'asset_pay':self.asset.id, 'order_type':'buy', 'order_price':222, 'order_quantity':'333'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_negative_order_quantity(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-order')
        response = self.client.post(url, data={'asset':self.asset.id, 'asset_pay':self.asset.id, 'order_type':'buy', 'order_price':222, 'order_quantity':-20})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_zero_quantity(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('create-new-order')
        response = self.client.post(url, data={'asset':self.asset.id, 'asset_pay':self.asset.id, 'order_type':'buy', 'order_price':222, 'order_quantity':0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
class AssetTestCase(APITestCase):
    def setUp(self):
        self.asset = Asset.objects.create(name='Bitcoin', symbol='BTC', current_price=Decimal('50000.00'))
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='password123')
        self.basic_user = User.objects.create(username='user', email='user@example.com', password='password123')

    def test_update_asset_price(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('update-asset-price')
        response = self.client.patch(url, data={'symbol': self.asset.symbol, 'current_price': Decimal('60000.00')})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_price'], '60000.00')

    def test_update_asset_price_is_not_asset(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('update-asset-price')
        response = self.client.patch(url, data={'symbol': 'BCDA', 'current_price': Decimal('60000.00')})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_is_not_permissions(self):
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('update-asset-price')
        response = self.client.patch(url, data={'symbol': self.asset.symbol, 'current_price': Decimal('60000.00')})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_is_not_auth(self):
        url = reverse('update-asset-price')
        response = self.client.patch(url, data={'symbol': self.asset.symbol, 'current_price': Decimal('60000.00')})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_crosses_assets(self):
        Asset.objects.create(name='Ethereum', symbol='ETH', current_price=Decimal('2000.00'))
        Asset.objects.create(name='Litecoin', symbol='LTC', current_price=Decimal('150.00'))
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('asset-crosses')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_asset_consumer():
    communicator = WebsocketCommunicator(
        AssetConsumer.as_asgi(),
        "/ws/get-all-assets/",
    )

    connected, _ = await communicator.connect()
    assert connected

    data = await communicator.receive_json_from()
    assert data['messageType'] == 10
    assert data['message']['messageText'] == 'GetAsset'
    assert len(data['message']['asset']) == Asset.objects.count()

    asset_data = {'name': 'Test asset', 'symbol': 'TEST', 'current_price': 123.45}
    asset_serializer = AssetSerializer(data=asset_data)
    assert asset_serializer.is_valid()
    asset = asset_serializer.save()
    event_data = {'type': 'asset_saved_handler', 'instance': asset_data}
    await communicator.send_json_to(event_data)
    data = await communicator.receive_json_from(5)
    assert data['messageType'] == 10
    assert data['message']['messageText'] == 'GetAsset'
    assert data['message']['asset'] == AssetSerializer(asset).data

    await communicator.disconnect()

@database_sync_to_async
def create_test_order(user):
    asset_1 = Asset.objects.create(symbol='ETH')
    asset_2 = Asset.objects.create(symbol='BTC')
    order = Order.objects.create(
        user=user,
        asset=asset_1,
        asset_pay=asset_2,
        order_type='buy',
        order_price='1000.00',
        order_quantity='1.0',
        order_status='active'
    )
    return order

@pytest.mark.asyncio
async def test_get_orders_consumer():
    user = get_user_model().objects.create(username='testuser')
    order = await create_test_order(user)
    communicator = WebsocketCommunicator(
        GetOrdersConsumer.as_asgi(),
        f"/ws/orders/?token={user.auth_token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    message = {
        'messageType': 9,
        'message': {
            'messageText': 'GetOrder',
        }
    }
    await communicator.send_json_to(message)
    response = await communicator.receive_json_from()
    assert response == {
        'messageType': 9,
        'message': {
            'messageText': 'GetOrder',
            'orders': [OrderSerializer(order).data],
        }
    }
    await communicator.disconnect()
