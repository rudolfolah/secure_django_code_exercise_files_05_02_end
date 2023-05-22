from random import choice

from twilio.rest import Client

from django.db import models
from django.contrib.auth.models import User

from api.models import ActivityLog

class TwoFactorAuthCode(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=6)
    sent_on = models.DateTimeField(auto_now_add=True)

    @classmethod
    def send_code(cls, user, to_phone):
        account_sid = '' # your Twilio account sid goes here
        auth_token = '' # your Twilio auth token goes here
        client = Client(account_sid, auth_token)
        digits = '0123456789'
        code = ''.join([choice(digits) for i in range(6)])
        cls.objects.create(
            user=user,
            code=code,
        )
        message = client.messages.create(
            to=to_phone,
            from_='+1234567890', # your Twilio phone number goes here
            body='Your auth code:' + code
        )

    @classmethod
    def validate_code(cls, user, code):
        if user.is_anonymous:
            return False
        existing = cls.objects.filter(
            user=user, code=code
        ).order_by('-sent_on').first()
        if existing is None:
            ActivityLog.objects.create(
                user=user,
                action='User entered incorrect two-factor auth code'
            )
            return False
        existing.delete()
        ActivityLog.objects.create(
            user=user,
            action='User entered correct two-factor auth code'
        )
        return True

