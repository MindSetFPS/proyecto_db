from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
import json
from shopApp.views.payment import PaymentView, NotificationView

class PaymentViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('mercadopago.SDK.preference')
    def test_payment_view(self, mock_preference):
        # Mock the response from mercadopago
        mock_preference().create.return_value = {
            "response": {
                "id": "123456789",
                "init_point": "https://www.mercadopago.com/init_point",
                "sandbox_init_point": "https://www.mercadopago.com/sandbox_init_point"
            }
        }

        response = self.client.get(reverse('payment'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn('id', json.loads(response.content))
        self.assertIn('init_point', json.loads(response.content))

    @patch('shopApp.views.payment.hmac.new')
    @patch('shopApp.views.payment.os.environ.get')
    def test_notification_view(self, mock_os_environ_get, mock_hmac_new):
        # Mock environment variable and HMAC object
        mock_os_environ_get.return_value = 'dummy_secret'
        mock_hmac_obj = mock_hmac_new.return_value
        mock_hmac_obj.hexdigest.return_value = 'valid_hmac_signature'

        headers = {
            'HTTP_X_SIGNATURE': 'ts=1234567890,v1=valid_hmac_signature',
            'HTTP_X_REQUEST_ID': 'request_id_123'
        }
        response = self.client.post(reverse('notification'), data={'id': 'data_id_123'}, **headers)
        self.assertEqual(response.status_code, 200)

        # Test invalid HMAC signature
        mock_hmac_obj.hexdigest.return_value = 'invalid_hmac_signature'
        response = self.client.post(reverse('notification'), data={'id': 'data_id_123'}, **headers)
        self.assertEqual(response.status_code, 400)

