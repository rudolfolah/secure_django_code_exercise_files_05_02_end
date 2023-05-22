from django.db import models
from django.contrib.auth.models import User

from billing.fields import EncryptedTextField

class Payment(models.Model):
    payer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    passport_confirmation = EncryptedTextField()
