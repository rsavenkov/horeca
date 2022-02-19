import binascii
import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from candidate_tests.utils import get_state_context_default_value
from horeca_utils import constants


class TestingSession(models.Model):
    class Meta:
        verbose_name = _('Сессия тестирования')
        verbose_name_plural = _('Сессии тестирования')

    candidate = models.ForeignKey(
        'users.Candidate',
        on_delete=models.CASCADE,
        related_name='testing_sessions',
    )
    created = models.DateTimeField(auto_now_add=True)
    token_ttl = models.DateTimeField(null=True, blank=True)

    @property
    def tests_names(self):
        tests = [t.value for t in constants.TestTypes]
        test_names = list(self.tests.values_list('name', flat=True))
        sorted_test_names = [t for t in tests if t in test_names]
        return sorted_test_names

    def __str__(self):
        return f'Test session {self.candidate} - {self.created}'


class TestingSessionTest(models.Model):
    class Meta:
        verbose_name = _('Cессия тестирования тест')
        verbose_name_plural = _('Cессии тестирования тесты')

    session = models.ForeignKey(
        TestingSession,
        on_delete=models.CASCADE,
        related_name='tests',
    )
    name = models.CharField(choices=constants.TEST_TYPES, max_length=100)
    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        choices=constants.TESTING_STATUSES,
        default=constants.TestingStatuses.NOT_STARTED.value,
        max_length=100,
    )

    def __str__(self):
        return f'{self.session} - {self.name}'


class TestingSessionToken(models.Model):
    class Meta:
        verbose_name = _("Токен для прохождения тестирования")
        verbose_name_plural = _("Токены для прохождения тестирования")

    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    session = models.OneToOneField(
        TestingSession,
        related_name='token',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    @property
    def ttl(self):
        return self.session.token_ttl

    @property
    def user(self):
        return self.session.candidate.user

    def __str__(self):
        return self.key


class TestAmount(models.Model):
    class Meta:
        verbose_name = _('Количество отправок теста')
        verbose_name_plural = _('Количества отправок тестов')
        unique_together = ('candidate_creator', 'test')

    candidate_creator = models.ForeignKey(
        'users.CandidateCreator',
        related_name='tests_amount',
        on_delete=models.CASCADE,
    )
    test = models.CharField(
        choices=constants.TEST_TYPES,
        max_length=100,
    )
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.candidate_creator} - {self.test}'


class TestingSessionState(models.Model):
    '''Отвечает за хранение информации, о состоянии каждой сессии тестирования

    Модель TestingSessionState необходима для работы конечного автомата

    state - текущее состояние. Список всех возможных состояний хранится в constants.TestingSessionStates
    context - контекст состояния. Вспомогательная переменная, для хранения полезной информации
    '''
    class Meta:
        verbose_name = _('Состояние сессии')
        verbose_name_plural = _('Состояния сесий')

    session = models.OneToOneField(
        TestingSession,
        on_delete=models.CASCADE,
        related_name='state',
    )
    state = models.CharField(
        max_length=100,
        choices=constants.TESTING_SESSION_STATES,
        default=constants.TestingSessionStates.PENDING_START.value,
    )
    context = models.JSONField(
        blank=True,
        default=get_state_context_default_value,
    )

    def __str__(self):
        return f'{self.session} State'
