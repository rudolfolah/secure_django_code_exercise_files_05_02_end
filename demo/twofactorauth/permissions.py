from rest_framework import permissions

from twofactorauth.models import TwoFactorAuthCode

class TwoFactorAuthRequired(permissions.BasePermission):
    def has_permission(self, request, view):
        code = request.data['auth_code']
        return TwoFactorAuthCode.validate_code(
            user=request.user,
            code=code
        )

