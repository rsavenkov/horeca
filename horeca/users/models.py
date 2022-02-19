from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

from horeca_utils import constants


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def token(self):
        try:
            return self.auth_token
        except models.ObjectDoesNotExist:
            return None

    @property
    def related_object(self):
        related_object = None

        if hasattr(self, 'admin'):
            related_object = self.admin
        elif hasattr(self, 'manager'):
            related_object = self.manager
        elif hasattr(self, 'candidate'):
            related_object = self.candidate

        return related_object


class CommonInfo(models.Model):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=150)
    patronymic = models.CharField(_('patronymic'), max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    class Meta:
        abstract = True


class Admin(CommonInfo):
    class Meta:
        verbose_name = _('Администратор')
        verbose_name_plural = _('Администраторы')

    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='admin',
    )

    def __str__(self):
        return f'Admin {self.email}'


class Manager(CommonInfo):
    class Meta:
        verbose_name = _('Менеджер')
        verbose_name_plural = _('Менеджеры')

    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='manager',
    )
    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    company = models.CharField(max_length=100)
    taxpayer_id_number = models.CharField(
        null=True,
        blank=True,
        unique=True,
        max_length=12,
        validators=[MinLengthValidator(12)],
        verbose_name='ИНН',
    )

    def __str__(self):
        return f'Manager {self.email}'


class CandidateCreator(models.Model):
    class Meta:
        verbose_name = _('Создатель кандидата')
        verbose_name_plural = _('Создатели кандидата')
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                        admin__isnull=False,
                        manager__isnull=True,
                    ) | models.Q(
                        admin__isnull=True,
                        manager__isnull=False
                    ),
                name='only_one_not_null'
            )
        ]

    admin = models.OneToOneField(
        Admin,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    manager = models.OneToOneField(
        Manager,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    @property
    def creator(self):
        return self.admin if self.admin else self.manager

    def clean(self):
        if self.admin and self.manager:
            raise ValidationError('Please Choose only one creator')
        if not self.admin and not self.manager:
            raise ValidationError('Administrator and Manager cannot be both empty')
        return super().clean()

    def __str__(self):
        return f'Creator {self.creator}'


class Candidate(CommonInfo):
    class Meta:
        verbose_name = _('Кандидат')
        verbose_name_plural = _('Кандидаты')

    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='candidate',
    )
    creator = models.ForeignKey(
        CandidateCreator,
        on_delete=models.PROTECT,
        related_name='candidates',
    )
    position = models.CharField(max_length=100, blank=True)
    comment = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=50, choices=constants.GENDERS, blank=True)
    date_of_birth = models.DateField(max_length=8, blank=True, null=True)
    city = models.CharField(blank=True, max_length=255)
    testing_status = models.CharField(
        choices=constants.TESTING_STATUSES,
        max_length=100,
        default=constants.TestingStatuses.NOT_SEND.value,
    )

    def __str__(self):
        return f'Candidate {self.email}'


class Position(models.Model):
    class Meta:
        verbose_name = _('Должность')
        verbose_name_plural = _('Должности')

    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.title}'
