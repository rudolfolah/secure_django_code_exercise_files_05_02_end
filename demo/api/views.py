import csv

from django.core.cache import cache
from django.http.response import HttpResponse

from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import BaseFilterBackend
from rest_framework.permissions import BasePermission, DjangoModelPermissions

from oauth2_provider.views.mixins import ProtectedResourceMixin
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from api.models import Package, PackagePermission, Booking, ActivityLog
from api.serializers import PackageSerializer, BookingSerializer
from ugc.models import Comment

class PackageCreateView(CreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [BasePermission]

    def post(self, *args, **kwargs):
        if cache.has_key('package_created'):
            return Response(status=200)
        response = super().post(*args, **kwargs)
        if response.status_code == 201:
            cache.set('package_created', True, timeout=300)
        return response

class PackagePagination(PageNumberPagination):
    page_size = 10

class CanWritePackageFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = self.check_permission(request, queryset, view)
        filters = {}
        tour_length = request.query_params.get('tourLength', None)
        if tour_length:
            filters['tour_length'] = tour_length
        return queryset.filter(**filters).order_by('id')

    def check_permission(self, request, queryset, view):
        if request.user is None:
            return queryset.none()
        if request.user.username == 'admin':
            return queryset
        package_ids = queryset.values_list('id', flat=True)
        own_package_ids = PackagePermission.objects.filter(
            is_owner=True, package__in=package_ids, user=request.user,
        ).values_list('package__id', flat=True)
        return queryset.filter(id__in=own_package_ids)

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    pagination_class = PackagePagination
    filter_backends = (CanWritePackageFilterBackend,)
    permission_classes = [TokenHasScope, TokenHasReadWriteScope]
    required_scopes = ['packages']

class PublicPackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all().order_by('-price')
    serializer_class = PackageSerializer
    pagination_class = PackagePagination
    permission_classes = [BasePermission]
    search_fields = ('name', 'promo')

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [DjangoModelPermissions]

class UserDataDownloadView(RetrieveAPIView, ProtectedResourceMixin):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename="data.csv"'

        writer = csv.writer(response, dialect='unix')
        writer.writerow(['Data for {}'.format(request.user.email)])
        writer.writerow(['Comments'])
        comments = Comment.objects.filter(created_by=request.user)
        writer.writerows([comment.text for comment in comments])

        writer.writerow(['Bookings'])
        writer.writerow(['package_name', 'package_price', 'start', 'name'])
        bookings = Booking.objects.filter(email_address=request.user.email)
        writer.writerows([
            [
                booking.package.name,
                booking.package.price,
                booking.start,
                booking.name
            ] for booking in bookings
        ])

        writer.writerow(['Activity Log'])
        logs = ActivityLog.objects.filter(user=request.user)
        writer.writerows([[log.action] for log in logs])

        return response

