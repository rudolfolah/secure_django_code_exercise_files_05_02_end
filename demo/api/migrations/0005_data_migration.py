from random import choice
from datetime import datetime, timedelta

from django.db import migrations
from django.contrib.auth.hashers import make_password

def user_creation(UserModelClass):
    def make_user(username, email, is_admin=False):
        user = UserModelClass(
            username=username,
            email=email,
            password=make_password(username)
        )
        if is_admin:
            user.is_superuser = True
            user.is_staff = True
        user.save()
        return user
    return make_user

def create_sample_data(apps, schema_editor):
    make_user = user_creation(apps.get_model('auth', 'User'))
    # Get model classes
    Package = apps.get_model('api', 'Package')
    PackagePermission = apps.get_model('api', 'PackagePermission')
    PackageDate = apps.get_model('api', 'PackageDate')
    Booking = apps.get_model('api', 'Booking')

    # Create admin user
    make_user('admin', 'admin@localhost', is_admin=True)

    # Create users
    users = [
        make_user('user_a', 'user_a@localhost'),
        make_user('user_b', 'user_b@localhost'),
        make_user('user_c', 'user_c@localhost'),
    ]

    # Create packages
    categories = ['hiking', 'tour', 'restaurants']
    prices = [30.00, 49.99, 100.0, 199.99, 200.00, 399.99]
    ratings = ['easy', 'medium', 'hard']
    tour_lengths = [1, 2, 3, 4]
    for i in range(500):
        owner = choice(users)
        category = choice(categories)
        package = Package.objects.create(
            category=category,
            name='Package {}{}'.format(
                owner.username.replace('User ', ''),
                i
            ),
            promo='This is an amazing package for {}'.format(category),
            price=choice(prices),
            rating=choice(ratings),
            tour_length=choice(tour_lengths),
        )
        # Set up package permissions
        PackagePermission.objects.create(
            user=owner,
            package=package,
            is_owner=True,
        )
        # Create package date range
        package_date = PackageDate.objects.create(
            package=package,
            start=datetime.today(),
            end=datetime.today() + timedelta(days=10),
        )
        # Create bookings
        for count in range(3):
            name = choice(['DEF', 'GHI', 'JKL'])
            Booking(
                package_date=package_date,
                start=datetime.today() + timedelta(days=choice(range(10))),
                name='Customer {}'.format(name),
                email_address='customer{}@localhost'.format(name),
            )

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190805_2336'),
    ]

    operations = [
        migrations.RunPython(create_sample_data),
    ]
