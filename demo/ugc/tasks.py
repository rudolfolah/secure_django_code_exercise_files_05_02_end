from django.core.cache import cache
from django.contrib.auth.models import User

from demo.celery import app
from ugc.models import Comment

@app.task(name='celery.ping')
def ping():
    pass

@app.task(bind=True)
def create_comment(self, user_id, text):
    cache_key = '{}/comment_created'.format(user_id)
    if cache.has_key(cache_key):
        raise self.retry()
    obj = Comment.objects.create(
        created_by=User.objects.get(id=user_id),
        text=text,
    )
    obj.save()
    cache.set(cache_key, obj.id, timeout=300)