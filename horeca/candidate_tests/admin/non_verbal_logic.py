from django.contrib import admin

from candidate_tests import models


@admin.register(models.NonVerbalLogicQuestion)
class NonVerbalLogicQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.NonVerbalLogicAnswerOption)
class NonVerbalLogicAnswerOptionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.NonVerbalLogicAnswer)
class NonVerbalLogicAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'point')


@admin.register(models.NonVerbalLogicUserAnswerList)
class NonVerbalLogicUserAnswerListAdmin(admin.ModelAdmin):
    pass


@admin.register(models.NonVerbalLogicUserAnswer)
class NonVerbalLogicUserAnswerAdmin(admin.ModelAdmin):
    pass
