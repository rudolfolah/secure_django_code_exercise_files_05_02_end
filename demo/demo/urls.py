from django.conf import settings
from django.conf.urls.static import static, serve
from django.contrib import admin
from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter

import api.views
import ugc.views
import twofactorauth.views

router = DefaultRouter()
router.register(r'packages', api.views.PackageViewSet)
router.register(r'public/packages', api.views.PublicPackageViewSet)
router.register(r'bookings', api.views.BookingViewSet)
router.register(r'journal', ugc.views.JournalViewSet)

urlpatterns = [
    re_path(r'^api/v1/create_package', api.views.PackageCreateView.as_view()),
    re_path(r'^api/v1/create_comment', ugc.views.CommentCreateView.as_view()),
    re_path(r'^api/v1/download', api.views.UserDataDownloadView.as_view()),
    re_path(r'^api/v1/validate', twofactorauth.views.ValidateCodeView.as_view()),
    re_path(r'^api/v1/', include(router.urls)),
    # path('journal/', ugc.views.JournalView.as_view()),
    path('admin/', admin.site.urls),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    re_path(r'^(?P<path>.*)$', serve, { 'document_root': settings.FRONTEND_ROOT}),
]
