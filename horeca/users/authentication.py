from datetime import timedelta

from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from horeca import settings


class ExpiringTokenAuthentication(TokenAuthentication):
    '''Класс для аутентификации с учетом
    времени жизни токена

    '''
    def expires_in(self, token):
        '''Вернуть оставшееся время жизни токена'''
        time_elapsed = timezone.now() - token.created
        time_left = timedelta(hours=settings.TOKEN_EXPIRED_AFTER_HOURS) - time_elapsed
        return time_left

    def is_token_expired(self, token):
        '''Проверить истекло ли время жизни токена или нет'''
        return self.expires_in(token) < timedelta(seconds=0)

    def token_expire_handler(self, token):
        '''Если время жизни текущего токена
        истекло, то удалить его и создать новый

        '''
        is_expired = self.is_token_expired(token)
        if is_expired:
            token.delete()
            token = Token.objects.create(user=token.user)
        return is_expired, token

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')

        is_expired, token = self.token_expire_handler(token)
        if is_expired:
            raise AuthenticationFailed("The token is expired.")

        return token.user, token


expiring_token_authentication = ExpiringTokenAuthentication()
