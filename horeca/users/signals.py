from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django_rest_passwordreset.signals import reset_password_token_created

from . import models, services
from horeca_utils import constants


@transaction.atomic
@receiver(post_save, sender=models.Admin)
@receiver(post_save, sender=models.Manager)
@receiver(post_save, sender=models.Candidate)
def create_user(sender, instance=None, created=False, **kwargs):
    '''Сигнал создаюший user'а для сущностей Admin, Manager, Candidate'''
    # TODO(Hleb_S): AHC 96 добавить проверку на существующего юзера
    if created:
        user, password = services.create_user(instance)
        if not isinstance(user.related_object, models.Candidate):
            services.default_email_sender.send_invite_message(
                instance.user.email,
                {
                    'login': user.email,
                    'password': password,
                }
            )


@transaction.atomic
@receiver(post_save, sender=models.Admin)
@receiver(post_save, sender=models.Manager)
def create_candidate_creator(sender, instance=None, created=False, **kwargs):
    if created:
        services.create_candidate_creator(instance)


@transaction.atomic
@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    '''Сигнал создающий токен для новых пользователей'''
    if created and not instance.is_superuser and not instance.is_staff:
        Token.objects.get_or_create(user=instance)


@transaction.atomic
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    '''Сигнал отправляющий сообщение с ссылкой для восстановления пароля'''
    services.default_email_sender.send_reset_password_message(
        reset_password_token.user.email,
        reset_password_token.key,
    )
