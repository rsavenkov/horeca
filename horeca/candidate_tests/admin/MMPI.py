from django.contrib import admin

from candidate_tests import models


@admin.register(models.MMPIScale)
class MMPIScaleAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_filter = ('is_inverted',)
    search_fields = ('name',)
    list_display = ('name', 'verbose_name', 'number', 'is_inverted')


@admin.register(models.MMPIQuestion)
class MMPIQuestionAdmin(admin.ModelAdmin):
    ordering = ('id',)
    search_fields = ('id', 'question')


@admin.register(models.TPointsTable)
class TPointsTableAdmin(admin.ModelAdmin):
    list_display = ('scale', 'gender')


@admin.register(models.MMPITestingUserAnswerList)
class MMPITestingUserAnswerListAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MMPITestingUserAnswer)
class MMPITestingUserAnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_list', 'question', 'answer')


@admin.register(models.MMPITestingUserRawPointsResult)
class MMPITestingUserRawPointsResultAdmin(admin.ModelAdmin):
    list_display = ('answer_list', 'scale', 'points')


@admin.register(models.MMPITestingUserTPointsResult)
class MMPITestingUserTPointsResultAdmin(admin.ModelAdmin):
    list_display = ('answer_list', 'scale', 'points')


@admin.register(models.MMPIScaleDescription)
class MMPIScaleDescriptionAdmin(admin.ModelAdmin):
    list_display = ('scale', 'from_point', 'to_point')


@admin.register(models.MMPIMotivator)
class MMPIMotivatorAdmin(admin.ModelAdmin):
    list_display = ('scale', 'from_point', 'to_point')


@admin.register(models.MMPIDestructor)
class MMPIDestructorAdmin(admin.ModelAdmin):
    list_display = ('scale', 'from_point', 'to_point')


@admin.register(models.MMPIRiskFactor)
class MMPIRiskFactorAdmin(admin.ModelAdmin):
    list_display = ('scale', 'from_point', 'to_point', 'is_attantion_factor')


@admin.register(models.MMPICompetenceCategory)
class MMPICompetenceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.MMPICompetence)
class MMPICompetenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')


@admin.register(models.MMPICompetenceScale)
class MMPICompetenceScaleAdmin(admin.ModelAdmin):
    list_display = ('competence', 'scale', 'from_point', 'to_point')


@admin.register(models.MMPITeamRole)
class MMPITeamRoleAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.MMPITeamRoleScale)
class MMPITeamRoleScaleAdmin(admin.ModelAdmin):
    list_display = ('role', 'scale', 'points')


@admin.register(models.MMPIStressTolerance)
class MMPIStressToleranceAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.MMPIStressToleranceScalesCombination)
class MMPIStressToleranceScalesCombinationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MMPIStressToleranceScale)
class MMPIStressToleranceScaleAdmin(admin.ModelAdmin):
    list_display = ('scale', 'from_point', 'to_point')


@admin.register(models.MMPIUserRiskFactor)
class MMPIUserRiskFactorAdmin(admin.ModelAdmin):
    list_display = ('testing_session', 'risk_factor')


@admin.register(models.MMPIUserCompetence)
class MMPIUserCompetenceAdmin(admin.ModelAdmin):
    list_display = ('testing_session', 'competence', 'type')


@admin.register(models.MMPIUserCompetenceRecomendation)
class MMPIUserCompetenceRecomendationAdmin(admin.ModelAdmin):
    list_display = ('type',)


@admin.register(models.MMPIUserStressTolerance)
class MMPIUserStressToleranceAdmin(admin.ModelAdmin):
    list_display = ('testing_session', 'stress_tolerance')


@admin.register(models.MMPIUserDestructor)
class MMPIUserDestructorAdmin(admin.ModelAdmin):
    list_display = ('testing_session', 'destructor')


@admin.register(models.MMPIUserMotivator)
class MMPIUserMotivatorAdmin(admin.ModelAdmin):
    list_display = ('testing_session', 'motivator')


@admin.register(models.MMPIUserTeamRole)
class MMPIUserTeamRoleAdmin(admin.ModelAdmin):
    list_display = ('testing_session', 'team_role', 'points')


@admin.register(models.MMPILeadershipStyle)
class MMPILeadershipStyleAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.MMPILeadershipStyleScale)
class MMPILeadershipStyleScaleAdmin(admin.ModelAdmin):
    list_display = ('style', 'scale', 'from_point', 'to_point')


@admin.register(models.MMPIUserLeadershipStyle)
class MMPIUserLeadershipStyleAdmin(admin.ModelAdmin):
    list_display = ('testing_session', 'style', 'type')
