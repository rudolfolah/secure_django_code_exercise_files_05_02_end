# Secure Coding with Django
Created by Rudolf Olah <rudolf.olah.to@gmail.com>

## Docker Setup

```sh
docker compose up
docker compose exec django_app './manage.py' migrate
docker compose exec -d django_app './manage.py' runserver --noreload 0.0.0.0:8000

# rebuilding the images if needed, no cache is needed so migrations are run
docker compose build --no-cache
docker compose up --build --force-recreate
```

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

You can login with these users through the frontend application `http://localhost:4200` and through the Django admin `http://localhost:8000/admin/

If the code for the frontend application is not available, there is an OAuth2 endpoint available at `http://localhost:8000/oauth/` that you can use to get an access token. The client id and secret for the frontend app can be found in [`demo/api/migrations/0006_oauth_application_create.py`](./demo/api/migrations/0006_oauth_application_create.py).

## Testing the API

Using [HTTPie](https://httpie.io/):

```sh
brew install httpie
```
### Django admin

```sh
http GET localhost:8000/admin/
```

### OAuth2

Set the username and password and get the oauth2 token. You can change the username and password to one of the already created users.

```sh
API_USERNAME=admin
API_PASSWORD=admin
TOKEN=$(http --print=b POST localhost:8000/oauth/token/ 'client_id=wql5aqXepfkcF0JQOAoOo921zbvcrQSg1MUb2VUe' 'client_secret=tVnwobvL4C7D76AOsYkrtDLh1D1mahbUqkzSBfqVi2zXfsBBD9Jm8FNe6yWof1XYIOwBfxtKrZh4Eug3piGu94Oga2R0VHJVG2VxQn1pw5Y5xcBOva0IX1n4WrPXZn0N' 'grant_type=password' "username=$API_USERNAME" "password=$API_PASSWORD" | python -c "import sys, json; data = json.load(sys.stdin); print(data['access_token'])")
echo "Bearer $TOKEN" > headers_auth.txt
```

### Testing the endpoints

```sh
http GET localhost:8000/api/v1/packages/ 'Authorization:@headers_auth.txt'
http GET localhost:8000/api/v1/public/packages/ 'Authorization:@headers_auth.txt'
http GET localhost:8000/api/v1/journal/ 'Authorization:@headers_auth.txt'
http GET localhost:8000/api/v1/download/ 'Authorization:@headers_auth.txt'
```

Note: bookings are only accessible to the admin user

```sh
http POST localhost:8000/api/v1/bookings/ 'Authorization:@headers_auth.txt' 'name=Test Booking' 'start=2023-12-01' 'end=2023-12-24' 'package=1' 'email_address=user_a@localhost'
http GET localhost:8000/api/v1/bookings/ 'Authorization:@headers_auth.txt'
```

Other endpoints:

```sh
http POST localhost:8000/api/v1/create_package/ 'Authorization:@headers_auth.txt'
http POST localhost:8000/api/v1/create_comment/ 'Authorization:@headers_auth.txt'
http GET localhost:8000/api/v1/validate/ 'Authorization:@headers_auth.txt'
```
