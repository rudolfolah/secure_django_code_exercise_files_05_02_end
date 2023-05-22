from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.create(name='account_manager')
    Group.objects.create(name='customer_support')

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20190829_1245'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]
