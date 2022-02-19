from datetime import timedelta

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from .models import TestingSessionToken


def expires_in(token):
    '''Возвращает оставшееся время жизни токена'''
    try:
        time_left = token.ttl - timezone.now()
    except TypeError:
        raise Exception(f'This token {token} has no ttl')

    return time_left


def check_is_token_expired(token):
    return expires_in(token) < timedelta(seconds=0)


class TestingSessionAuthentication(TokenAuthentication):
    """
    Простая токен аутентификация, с опциональным временем жизни токена, для прохождения тестирования

    Время жизни токена выставляется в переменной token_ttl в модели TestingSession,
    к которой относится токен

    Для аутентификации клиент должен поместить ключ токена в query параметр запроса "token"
    Пример: api/testing-session?token=401f7ac837da42b97f613d789819ff93537bee6a
    """
    model = TestingSessionToken

    def authenticate(self, request):
        token = request.query_params.get('token', None)

        if token is None:
            msg = _('Invalid token query. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.select_related('session').get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        is_expired = self._token_expire_handler(token)
        if is_expired:
            raise exceptions.AuthenticationFailed('Token has expired')

        return token.user, token

    def _token_expire_handler(self, token):
        is_expired = False

        if token.ttl:
            is_expired = check_is_token_expired(token)
        if is_expired:
            token.delete()

        return is_expired
