from django.contrib.auth.models import User
from django.test import TestCase

from api.models import ActivityLog
from api.utils import create_access_token, auth_header

from twofactorauth.models import TwoFactorAuthCode

class ValidateCodeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.auth_user = auth_header(create_access_token(self.user))
        TwoFactorAuthCode.objects.create(
            user=self.user,
            code='123456'
        )

    def test_valid_code(self):
        response = self.client.post(
            '/api/v1/validate',
            { 'auth_code': '123456' },
            **self.auth_user
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TwoFactorAuthCode.objects.count(), 0)
        activity_log = ActivityLog.objects.last()
        self.assertEqual(
            activity_log.action,
            'User entered correct two-factor auth code'
        )

    def test_invalid_code(self):
        response = self.client.post(
            '/api/v1/validate',
            { 'auth_code': 'invalid' },
            **self.auth_user,
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(TwoFactorAuthCode.objects.count(), 1)
        activity_log = ActivityLog.objects.last()
        self.assertEqual(
            activity_log.action,
            'User entered incorrect two-factor auth code'
        )

