# Secure Coding with Django
Created by Rudolf Olah <rudolf.olah.to@gmail.com>

## Setup Django
Get started with Django:

```sh
# Install redis for background task queues
# On Linux:
sudo apt-get install redis-server
# On Mac OS X:
brew install redis

# Install Apache Benchmark tools for ab
# On Linux:
sudo apt install apache2-utils

# Set up the environment and install packages
virtualenv --python=python3 env
source env/bin/activate
pip install -r requirements.txt

# Django app
cd demo
# Run model and data migrations
python manage.py migrate

# Create admin user
# python manage.py createsuperuser --username admin

# Run redis server in another terminal:
redis-server

# Run the background worker in another terminal:
celery -A demo worker -l info

# Run tests
python manage.py test

# Run the server
python manage.py runserver
```

## Users and Data and Logging In
There is some data loaded into the database after you run `python manage.py migrate` and a few users are created.

**Use the username as the password to login**:
- `admin`
- `user_a`
- `user_b`
- `user_c`

You can login with these users through the frontend application `http://localhost:4200` and through the Django admin `http://localhost:8000/admin/`
