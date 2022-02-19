import os
import typing
import requests

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from . import models, serializers
from horeca_utils import constants
from candidate_tests.selectors import get_logic_test_results


class EmailUser:
    '''Класс для работы с email'''
    def __init__(self, template: str, subject: str, required_fields: list):
        self._template = template
        self._subject = subject
        self._horeca_host = os.environ['HORECA_HOST']
        self._default_context = {'horeca_host': self._horeca_host}
        self._required_fields = required_fields

    def _validate_context(self, context: dict) -> bool:
        '''Проверяет контекст на наличие нужных полей'''
        for field in self._required_fields:
            if field not in context:
                return False
        return True

    def send_invite_message(self, email: str, context: dict) -> None:
        '''Отправляет приветствующие сообщение на email'''
        if not self._validate_context(context):
            raise Exception("Sending context is not valid")
        email_html_message = render_to_string(
            self._template,
            {
                **self._default_context,
                **context,
            }
        )
        send_mail(
            self._subject,
            'Здравствуйте!',
            settings.EMAIL_HOST_USER,
            [email],
            html_message=email_html_message,
        )

    def send_reset_password_message(self, email, token):
        email_html_message = render_to_string(
            'users/reset_password_massage.html',
            {
                **self._default_context,
                'link': f'{self._horeca_host}/update-password?token={token}',
            },
        )
        send_mail(
            'Восстановление пароля',
            'Здравствуйте!',
            settings.EMAIL_HOST_USER,
            [email],
            html_message=email_html_message,
        )

    def send_start_test_message(self, email, token):
        email_html_message = render_to_string(
            'users/start-test-message.html',
            {
                **self._default_context,
                'link': f'{self._horeca_host}/test/{token}',
            }
        )
        send_mail(
            # 'Тестирование от Team.Assessment',
            'ТЕСТИРОВАНИЕ «МОЙ БИЗНЕС»',
            'Здравствуйте!',
            # settings.EMAIL_HOST_USER,
            None,
            [email],
            html_message=email_html_message,
        )

    def send_logic_test_result(self, candidate):
        logic_tests_results = get_logic_test_results(candidate)
        logic_tests_results = '\n'.join(
            f'{r["title"]}: {r["value"]}%'.format(r) for r in logic_tests_results['results']
        )
        send_mail(
            'Результаты логического тестирования',
            logic_tests_results,
            settings.EMAIL_HOST_USER,
            [candidate.email],
        )

    def send_test_success_message(self, email):
        email_html_message = render_to_string('users/test-success-message.html', self._default_context)
        send_mail(
            'Успешное прохождение теста',
            'Здравствуйте!',
            settings.EMAIL_HOST_USER,
            [email],
            html_message=email_html_message,
        )


def get_pdf_download_links(pk):
    url = f'{os.environ["PDF_GENERATOR_HOST"]}'
    candidate = models.Candidate.objects.get(pk=pk)
    candidate_data = serializers.CandidateSerializer(candidate).data
    candidate_data.pop('creator')
    data = requests.post(url, json=candidate_data).json()
    link = data['url']
    # link = link.replace('http', 'https')
    return {'link': link}


def create_user(user: typing.Union[models.Candidate, models.Manager, models.Admin]):
    User = get_user_model()
    user.user, _ = User.objects.get_or_create(  # TODO: get_or_create херовая тема, костыль из-за кандидатов
        is_staff=False,
        is_superuser=False,
        is_active=True,
        email=user.email,
    )
    password = User.objects.make_random_password()
    user.user.set_password(password)
    user.save(update_fields=['user'])
    user.user.save(update_fields=['password'])

    return user.user, password


def create_candidate_creator(instance):
    if isinstance(instance, models.Admin):
        creator = models.CandidateCreator.objects.create(admin=instance)
    else:
        creator = models.CandidateCreator.objects.create(manager=instance)

    for test in constants.TestTypes:
        creator.tests_amount.create(test=test.value, amount=50)


default_email_sender = EmailUser(
    'users/corporate_client_invite_message.html',
    'Информация для авторизации',
    ['login', 'password'],
)

candidate_email_sender = EmailUser(
    'users/candidate_test_result_pdf.html',
    'Информация для авторизации',
    ['login', 'password'],
)
