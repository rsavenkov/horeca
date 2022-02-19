# flake8: noqa
from .MMPI import *
from .testing_session import *
from .numeric_logic import *
from .verbal_logic import *
from .non_verbal_logic import *
from .prof_interests import *

from candidate_tests import models


@admin.register(models.LogicTestResultDescription)
class LogicTestResultDescriptionAdmin(admin.ModelAdmin):
    list_display = ('test', 'result', 'from_point', 'to_point')