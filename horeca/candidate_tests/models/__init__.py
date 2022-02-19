# flake8: noqa
from django.utils.translation import gettext_lazy as _

from .MMPI import *
from .testing_session import *
from .numeric_logic import *
from .verbal_logic import *
from .non_verbal_logic import *
from .prof_interests import *



class LogicTestResultDescription(models.Model):
    class Meta:
        verbose_name = _('Описание логического теста')
        verbose_name_plural = _('Описания логических тестов')
    
    test = models.CharField(
        choices=constants.LOGIC_TESTS_CHOICES,
        max_length=100,
    )
    result = models.CharField(
        choices=constants.TEST_RESULT_GRADATIONS,
        max_length=100,
    )
    from_point = models.PositiveIntegerField()
    to_point = models.PositiveIntegerField()
    description = models.TextField()