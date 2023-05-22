from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import TemplateView

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from rest_framework import viewsets

from ugc.models import Comment, Journal
from ugc.serializers import CommentSerializer, JournalSerializer
from ugc.tasks import create_comment
from ugc.permissions import OnlyCreatorPermission

class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [BasePermission]

    def post(self, request, *args, **kwargs):
        task = create_comment.apply_async(
            args=(request.data.get('user_id'), request.data.get('text'),),
            retry=True,
            retry_policy={
                'max_retries': 3,
                'interval_start': 60,
                'interval_step': 30,
                'interval_max': 300,
            }
        )
        return Response(status=200)

class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    permission_classes = [OnlyCreatorPermission]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Journal.objects.none()
        return Journal.objects.filter(
            created_by=self.request.user
        )

@method_decorator(csrf_protect, name='dispatch')
class JournalView(TemplateView):
    template_name = 'journal.html'

    def get_context_data(self, **kwargs):
        entries = Journal.objects.filter(
            created_by=self.request.user
        )
        return {
            'user': self.request.user,
            'entries': entries,
        }

    def post(self, request, *args, **kwargs):
        if 'entry_to_delete' in request.POST:
            entry = Journal.objects.filter(
                id=request.POST['entry_to_delete'],
                created_by=request.user,
            )
            entry.delete()
        else:
            entry = Journal.objects.create(
                created_by=request.user,
                encrypted_text=request.POST['encrypted_text']
            )
            entry.save()
        return HttpResponseRedirect('/journal/')

