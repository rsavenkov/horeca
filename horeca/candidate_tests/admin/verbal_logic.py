from django.contrib import admin

from candidate_tests import models


@admin.register(models.VerbalLogicQuestion)
class VerbalLogicQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.VerbalLogicAnswer)
class VerbalLogicAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.VerbalLogicUserAnswerList)
class VerbalLogicUserAnswerListAdmin(admin.ModelAdmin):
    pass


@admin.register(models.VerbalLogicUserAnswer)
class VerbalLogicUserAnswerAdmin(admin.ModelAdmin):
    pass
