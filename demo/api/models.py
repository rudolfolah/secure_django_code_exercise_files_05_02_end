from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core import serializers
from guardian.shortcuts import assign_perm
import django.utils.timezone

def now():
    return django.utils.timezone.now().date()

class Package(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    promo = models.TextField()
    price = models.FloatField()
    rating = models.CharField(max_length=50)
    tour_length = models.IntegerField()
    start = models.DateField(default=now)

    def __str__(self):
        return self.name

class Booking(models.Model):
    package = models.ForeignKey(Package, null=True, on_delete=models.SET_NULL)
    start = models.DateField()
    name = models.CharField(max_length=200)
    email_address = models.CharField(max_length=200)

    def __str__(self):
        return '{} for {} on {}'.format(self.name, self.package.name, self.start)

@receiver(post_save, sender=Booking)
def set_booking_permissions(sender, instance, **kwargs):
    user = User.objects.get(email=instance.email_address)
    assign_perm('api.change_booking', user)
    assign_perm('api.change_booking', user, instance)

class PackagePermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    is_owner = models.BooleanField(blank=False, default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'package'], name='unique_owner'),
        ]

    def __str__(self):
        if self.is_owner:
            fmt = '{} ({}) can write to {} ({})'
        else:
            fmt = '{} ({}) cannot write to {}'
        return fmt.format(self.user.username, self.user.id, self.package.name, self.package.id)

    @classmethod
    def can_write(cls, user, package):
        try:
            permission = cls.objects.get(user=user, package=package)
            return permission.is_owner
        except ObjectDoesNotExist:
            return False

    @classmethod
    def set_can_write(cls, user, package):
        obj, created = cls.objects.get_or_create(user=user, package=package, defaults={'is_owner': True})
        if not created:
            obj.is_owner = True
            obj.save()

class ActivityLog(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=300)

@receiver(post_save, sender=Booking)
def post_save_activity_log(sender, instance, **kwargs):
    user = User.objects.get(email=instance.email_address)
    ActivityLog.objects.create(
        user=user,
        action='User #{} "{}" saved booking #{}'.format(
            user.id,
            user.email,
            instance.id
        )
    )

class DeletedData(models.Model):
    model_type = models.CharField(max_length=200)
    model_id = models.IntegerField()
    data = models.TextField()

@receiver(post_delete, sender=Booking)
def archive_booking(sender, instance, **kwargs):
    data = serializers.serialize('json', [instance])
    DeletedData.objects.create(
        model_type='Booking',
        model_id=instance.id,
        data=data
    )

def restore_booking(id):
    deleted = DeletedData.objects.get(model_type='Booking', model_id=id)
    for instance in serializers.deserialize('json', deleted.data):
        instance.save()
        deleted.delete()
