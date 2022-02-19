from django.utils.translation import gettext_lazy as _
from rest_framework.validators import qs_filter, qs_exists
from rest_framework.exceptions import ValidationError

from .models import User


class UniqueEmailValidator:
    requires_context = True

    def __init__(self):
        self.field_name = 'email'
        self.queryset = User.objects.all()

    def filter_queryset(self, attrs, queryset):
        """
        Фильтрует queryset по всем экземпрярам, соответствующим данному атрибуту
        """
        filter_kwargs = {self.field_name: attrs[self.field_name]}
        return qs_filter(queryset, **filter_kwargs)

    def exclude_current_instance(self, queryset, instance):
        """
        Убирает экземпляр, елси он обновляется, из queryset,
        для избежания конфликта уникальности
        """
        if instance and instance.user:
            return queryset.exclude(pk=instance.user.pk)
        return queryset

    def __call__(self, attrs, serializer):
        queryset = self.queryset
        queryset = self.filter_queryset(attrs, queryset)
        queryset = self.exclude_current_instance(queryset, serializer.instance)

        if qs_exists(queryset):
            raise ValidationError(
                # TODO: AHC-106 если ошибка на английском, django не переводит ее
                {self.field_name: _('Пользователь с таким email уже существует')},
                code='unique',
            )
