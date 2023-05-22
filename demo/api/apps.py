from django.apps import AppConfig
from django.db.models.signals import post_migrate

from api.utils import assign_perms

def setup_group_permissions(sender, **kwargs):
    assign_perms({
        'account_manager': [
            'api.change_package',
            'api.view_package',
        ],
        'customer_support': [
            'api.view_package',
            'api.change_booking',
            'api.view_booking',
        ]
    })

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        post_migrate.connect(setup_group_permissions, sender=self)
