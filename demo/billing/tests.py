from django.contrib.auth.models import User
from django.db import connection
from django.test import TestCase

from billing.models import Payment

class PaymentTestCase(TestCase):
    def test_encryption(self):
        secret = 'ABC123'
        payment = Payment.objects.create(
            payer=User.objects.first(),
            passport_confirmation=secret,
        )
        self.assertEqual(payment.passport_confirmation, secret)
        with connection.cursor() as cursor:
            cursor.execute('SELECT passport_confirmation FROM billing_payment WHERE id = %s', [payment.id])
            encrypted = cursor.fetchone()[0]
            print(encrypted)
            self.assertNotEqual(encrypted, secret)
        self.assertEqual(
            Payment.objects.get(id=payment.id).passport_confirmation,
            secret
        )
