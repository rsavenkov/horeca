from django.contrib import admin

from candidate_tests import models


@admin.register(models.ProfInterestsScale)
class ProfInterestsScaleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProfInterestsQuestion)
class ProfInterestsQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProfInterestsAnswer)
class ProfInterestsAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'scale')


@admin.register(models.ProfInterestsUserAnswerList)
class ProfInterestsUserAnswerListAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProfInterestsUserAnswer)
class ProfInterestsUserAnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_list', 'question', 'answer', 'points')


@admin.register(models.ProfInterestsResult)
class ProfInterestsResultAdmin(admin.ModelAdmin):
    list_display = ('testing_session', 'scale', 'points')
