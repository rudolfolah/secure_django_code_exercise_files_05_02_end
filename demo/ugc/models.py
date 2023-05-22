from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text = models.TextField()

class Journal(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    encrypted_text = models.TextField()
