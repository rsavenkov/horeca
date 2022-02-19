from rest_framework.validators import qs_exists
from rest_framework.exceptions import ValidationError


class TestAmountValidator:
    requires_context = True

    def _generate_response_message(self, queryset):
        response = {q.test: 'Не хватает кол-ва отправок' for q in queryset}
        return response

    def __call__(self, attrs, serializer):
        queryset = attrs['candidate'].creator.tests_amount.filter(test__in=attrs['tests'], amount=0)
        if qs_exists(queryset):
            raise ValidationError(self._generate_response_message(queryset))
