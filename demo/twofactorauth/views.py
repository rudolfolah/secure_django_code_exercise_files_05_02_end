from rest_framework.views import APIView
from rest_framework.response import Response

from twofactorauth.permissions import TwoFactorAuthRequired

class ValidateCodeView(APIView):
    permission_classes = [TwoFactorAuthRequired]

    def post(self, request, *args, **kwargs):
        return Response(status=200)
