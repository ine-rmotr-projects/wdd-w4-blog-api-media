from rest_framework import exceptions, authentication, permissions

from django.core.exceptions import ValidationError

from blog.models import User, validate_authkey


class UserAccesskeyAuthentication(authentication.BaseAuthentication):
    """Authentication against User accesskey using GET parameters"""

    def authenticate(self, request):
        access_key = request.query_params.get('accesskey')
        if not access_key:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')

        try:
            validate_authkey(access_key)
        except ValidationError:
            raise exceptions.AuthenticationFailed('Invalid Accesskey')
        try:
            user = User.objects.get(accesskey=access_key)
            if user.is_active:
                return (user, None)
            else:
                raise User.DoesNotExist
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid Accesskey')


class UserSecretkeyAuthentication(authentication.BaseAuthentication):
    """Authentication against User accesskey and secretkey
       Accesskey should be sent in query_params, and Secretkey in
       custom X-Secret-Key header.
    """

    def authenticate(self, request):
        if request.method in permissions.SAFE_METHODS:
            # secretkey authentication is not needed in GET/HEAD/OPTION requests
            return None

        access_key = request.query_params.get('accesskey')
        secret_key = request.META.get('HTTP_X_SECRET_KEY')
        if not access_key or not secret_key:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')

        try:
            validate_authkey(access_key)
        except ValidationError:
            raise exceptions.AuthenticationFailed('Invalid Accesskey')
        try:
            validate_authkey(secret_key)
        except ValidationError:
            raise exceptions.AuthenticationFailed('Invalid Secretkey')

        try:
            user = User.objects.get(accesskey=access_key)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid Accesskey')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('Invalid Accesskey')

        if user.secretkey != secret_key:
            raise exceptions.AuthenticationFailed('Invalid Secretkey')

        return (user, None)
