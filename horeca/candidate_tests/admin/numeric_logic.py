from django.contrib import admin

from candidate_tests import models


@admin.register(models.NumericLogicQuestion)
class NumericLogicQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.NumericLogicAnswer)
class NumericLogicAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.NumericLogicUserAnswerList)
class NumericLogicUserAnswerListAdmin(admin.ModelAdmin):
    pass


@admin.register(models.NumericLogicUserAnswer)
class NumericLogicUserAnswerAdmin(admin.ModelAdmin):
    pass
