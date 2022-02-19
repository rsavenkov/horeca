from django.db import models
from django.utils.translation import gettext_lazy as _

from horeca_utils import constants


class MMPIQuestion(models.Model):
    class Meta:
        verbose_name = _('ММИЛ вопрос')
        verbose_name_plural = _('ММИЛ вопросы')

    id = models.PositiveIntegerField(unique=True, primary_key=True)
    question = models.TextField()

    def __str__(self):
        return f'{self.id} Question'


class MMPIScale(models.Model):
    class Meta:
        verbose_name = _('ММИЛ шкала')
        verbose_name_plural = _('ММИЛ шкалы')

    name = models.CharField(
        unique=True,
        max_length=100,
        choices=constants.MMPI_SCALES,
    )
    number = models.PositiveIntegerField(default=1)
    verbose_name = models.CharField(
        max_length=255,
        blank=True,
    )
    positive_keys = models.ManyToManyField(
        MMPIQuestion,
        related_name='positive_keys',
        blank=True,
    )
    negative_keys = models.ManyToManyField(
        MMPIQuestion,
        related_name='negative_keys',
        blank=True,
    )
    is_inverted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.verbose_name}'


class TPointsTable(models.Model):
    class Meta:
        verbose_name = _('ММИЛ Tаблица T-баллов')
        verbose_name_plural = _('ММИЛ Таблицы T-баллов')
        unique_together = ('scale', 'gender')

    scale = models.ForeignKey(
        MMPIScale,
        related_name='t_points_tables',
        on_delete=models.CASCADE,
    )
    gender = models.CharField(
        max_length=50,
        choices=constants.GENDERS,
        default=constants.Genders.MALE.value,
    )
    m = models.FloatField(default=0)
    delta = models.FloatField(default=0)


class MMPITestingUserAnswerList(models.Model):
    class Meta:
        verbose_name = _('ММИЛ список ответов пользователя')
        verbose_name_plural = _('ММИЛ списки ответов пользователей')

    session = models.OneToOneField(
        'candidate_tests.TestingSession',
        related_name='MMPI_testing_answer_list',
        on_delete=models.CASCADE,
    )
    questions = models.ManyToManyField(
        MMPIQuestion,
        through='candidate_tests.MMPITestingUserAnswer',
        related_name='answers'
    )

    def __str__(self):
        return f'{self.session} MMPI Testing Result'


class MMPITestingUserAnswer(models.Model):
    class Meta:
        verbose_name = _('ММИЛ ответ пользователья')
        verbose_name_plural = _('ММИЛ ответы пользователей')
        unique_together = ('answer_list', 'question')

    answer_list = models.ForeignKey(
        MMPITestingUserAnswerList,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    question = models.ForeignKey(
        MMPIQuestion,
        on_delete=models.CASCADE,
    )
    answer = models.IntegerField(choices=constants.MMPI_ANSWERS)

    def __str__(self):
        return f'{self.answer_list} {self.question}'


class MMPITestingUserRawPointsResult(models.Model):
    class Meta:
        verbose_name = _('ММИЛ сырые баллы пользователя')
        verbose_name_plural = _('ММИЛ сырые баллы пользователей')
        unique_together = ('answer_list', 'scale')

    answer_list = models.ForeignKey(
        MMPITestingUserAnswerList,
        related_name='raw_points',
        on_delete=models.CASCADE,
    )
    scale = models.ForeignKey(
        MMPIScale,
        related_name='raw_points',
        on_delete=models.PROTECT,
    )
    points = models.FloatField(default=0)

    def __str__(self):
        return f'{self.scale}'


class MMPITestingUserTPointsResult(models.Model):
    class Meta:
        verbose_name = _('ММИЛ T-баллы пользователя')
        verbose_name_plural = _('ММИЛ T-баллы пользователей')
        unique_together = ('answer_list', 'scale')

    answer_list = models.ForeignKey(
        MMPITestingUserAnswerList,
        related_name='t_points',
        on_delete=models.CASCADE,
    )
    scale = models.ForeignKey(
        MMPIScale,
        related_name='t_points',
        on_delete=models.PROTECT,
    )
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.scale} - {self.points}'


class MMPIScaleDescription(models.Model):
    class Meta:
        verbose_name = _('ММИЛ шкалы описание')
        verbose_name_plural = _('ММИЛ шкалы описание')

    scale = models.ForeignKey(
        MMPIScale,
        related_name='descriptions',
        on_delete=models.CASCADE,
    )
    from_point = models.PositiveIntegerField()
    to_point = models.PositiveIntegerField()
    description = models.TextField()
    description_detail = models.TextField(blank=True)

    def __str__(self):
        return f'{self.scale}. {self.from_point}-{self.to_point}'


class MMPIMotivator(models.Model):
    class Meta:
        verbose_name = _('ММИЛ мотиватор')
        verbose_name_plural = _('ММИЛ мотиваторы')

    scale = models.ForeignKey(
        MMPIScale,
        related_name='motivators',
        on_delete=models.CASCADE,
    )
    from_point = models.PositiveIntegerField()
    to_point = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)

    def __str__(self):
        return f'{self.scale}. {self.from_point}-{self.to_point}'


class MMPIUserMotivator(models.Model):
    class Meta:
        verbose_name = _('ММИЛ мотиватор пользователя')
        verbose_name_plural = _('ММИЛ мотиваторы пользователей')

    testing_session = models.ForeignKey(
        'candidate_tests.TestingSession',
        related_name='motivators',
        on_delete=models.CASCADE,
    )
    motivator = models.ForeignKey(
        MMPIMotivator,
        related_name='users_motivators',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.testing_session} - {self.motivator}'


class MMPIDestructor(models.Model):
    class Meta:
        verbose_name = _('ММИЛ деструктор')
        verbose_name_plural = _('ММИЛ деструкторы')

    scale = models.ForeignKey(
        MMPIScale,
        related_name='destructors',
        on_delete=models.CASCADE,
    )
    from_point = models.PositiveIntegerField()
    to_point = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)

    def __str__(self):
        return f'{self.scale}. {self.from_point}-{self.to_point}'


class MMPIUserDestructor(models.Model):
    class Meta:
        verbose_name = _('ММИЛ деструктор пользователя')
        verbose_name_plural = _('ММИЛ деструкторы пользователей')

    testing_session = models.ForeignKey(
        'candidate_tests.TestingSession',
        related_name='destructors',
        on_delete=models.CASCADE,
    )
    destructor = models.ForeignKey(
        MMPIDestructor,
        related_name='users_destructors',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.testing_session} - {self.destructor}'


class MMPIRiskFactor(models.Model):
    class Meta:
        verbose_name = _('ММИЛ фактор риска')
        verbose_name_plural = _('ММИЛ факторы риска')

    scale = models.ForeignKey(
        MMPIScale,
        related_name='risk_factors',
        on_delete=models.CASCADE,
    )
    from_point = models.PositiveIntegerField()
    to_point = models.PositiveIntegerField()
    factor = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_attantion_factor = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.scale}. {self.from_point}-{self.to_point}'


class MMPIUserRiskFactor(models.Model):
    class Meta:
        verbose_name = _('ММИЛ фактор риска пользователя')
        verbose_name_plural = _('ММИЛ факторы риска пользователей')
        unique_together = ('risk_factor', 'testing_session')

    risk_factor = models.ForeignKey(
        MMPIRiskFactor,
        related_name='users_risk_factors',
        on_delete=models.CASCADE,
    )
    testing_session = models.ForeignKey(
        'candidate_tests.TestingSession',
        related_name='risk_factors',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.testing_session.candidate} - {self.risk_factor}'


class MMPICompetenceCategory(models.Model):
    class Meta:
        verbose_name = _('ММИЛ категория компетентностей')
        verbose_name_plural = _('ММИЛ категории компетентностей')

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'


class MMPICompetence(models.Model):
    class Meta:
        verbose_name = _('ММИЛ компетентность')
        verbose_name_plural = _('ММИЛ компетентности')

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        MMPICompetenceCategory,
        related_name='competences',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.name} - {self.category}'


class MMPIUserCompetence(models.Model):
    class Meta:
        verbose_name = _('ММИЛ компетентность пользователя')
        verbose_name_plural = _('ММИЛ компетентности пользователей')
        unique_together = ('testing_session', 'competence')

    testing_session = models.ForeignKey(
        'candidate_tests.TestingSession',
        related_name='competences',
        on_delete=models.CASCADE,
    )
    competence = models.ForeignKey(
        MMPICompetence,
        related_name='users_competences',
        on_delete=models.CASCADE,
    )
    type = models.CharField(
        choices=constants.MMPI_COMPETENCES,
        max_length=100,
    )

    def __str__(self):
        return f'{self.testing_session} - {self.competence} - {self.type}'


class MMPIUserCompetenceRecomendation(models.Model):
    class Meta:
        verbose_name = _('ММИЛ компетентности рекомендация')
        verbose_name_plural = _('ММИЛ компетентности рекомендации')

    type = models.CharField(
        choices=constants.MMPI_COMPETENCES,
        max_length=100,
        unique=True,
    )
    recommendation = models.TextField()

    def __str__(self):
        return f'{self.type}'


class MMPICompetenceScale(models.Model):
    class Meta:
        verbose_name = _('ММИЛ шкала компетентности')
        verbose_name_plural = _('ММИЛ шкалы компетентности')

    competence = models.ForeignKey(
        MMPICompetence,
        related_name='scales',
        on_delete=models.CASCADE,
    )
    scale = models.ForeignKey(
        MMPIScale,
        related_name='competences',
        on_delete=models.CASCADE,
    )
    from_point = models.PositiveIntegerField()
    to_point = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.competence} - {self.scale}'


class MMPITeamRole(models.Model):
    class Meta:
        verbose_name = _('ММИЛ командная роль')
        verbose_name_plural = _('ММИЛ командные роли')

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name}'


class MMPIUserTeamRole(models.Model):
    class Meta:
        verbose_name = _('ММИЛ командная роль пользователя')
        verbose_name_plural = _('ММИЛ командные роли пользователей')

    testing_session = models.ForeignKey(
        'candidate_tests.TestingSession',
        related_name='team_roles',
        on_delete=models.CASCADE,
    )
    team_role = models.ForeignKey(
        MMPITeamRole,
        related_name='users_team_roles',
        on_delete=models.CASCADE,
    )
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.testing_session} - {self.team_role}'


class MMPITeamRoleScale(models.Model):
    class Meta:
        verbose_name = _('ММИЛ шкала командных ролей')
        verbose_name_plural = _('ММИЛ шкалы командных ролей')

    role = models.ForeignKey(
        MMPITeamRole,
        related_name='scales',
        on_delete=models.CASCADE,
    )
    scale = models.ForeignKey(
        MMPIScale,
        related_name='roles',
        on_delete=models.CASCADE,
    )
    points = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.role} - {self.scale}'


class MMPIStressTolerance(models.Model):
    class Meta:
        verbose_name = _('ММИЛ тип стрессоустойчивости')
        verbose_name_plural = _('ММИЛ типы стрессоустойчивости')

    name = models.CharField(
        max_length=255,
        choices=constants.MMPI_STRESS_TOLERANCES,
        unique=True
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name}'


class MMPIUserStressTolerance(models.Model):
    class Meta:
        verbose_name = _('ММИЛ стрессоустойчивость пользователя')
        verbose_name_plural = _('ММИЛ стрессоустойчивость пользователей')

    testing_session = models.OneToOneField(
        'candidate_tests.TestingSession',
        related_name='stress_tolerance',
        on_delete=models.CASCADE,
    )
    stress_tolerance = models.ForeignKey(
        MMPIStressTolerance,
        related_name='users_stress_tolerances',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.testing_session} - {self.stress_tolerance}'


class MMPIStressToleranceScalesCombination(models.Model):
    class Meta:
        verbose_name = _('ММИЛ стрессоустойчивость комбинация шкал')
        verbose_name_plural = _('ММИЛ стрессоустойчивость комбинации шкал')

    stress_tolerance = models.ForeignKey(
        MMPIStressTolerance,
        on_delete=models.CASCADE,
        related_name='scales_combinations'
    )

    def __str__(self):
        return f'{self.pk} - {self.stress_tolerance}'


class MMPIStressToleranceScale(models.Model):
    class Meta:
        verbose_name = _('ММИЛ шкала стрессоустойчивости')
        verbose_name_plural = _('ММИЛ шкалы стрессоустойчивости')

    scale = models.ForeignKey(
        MMPIScale,
        related_name='stress_tolerance_scales',
        on_delete=models.CASCADE,
    )
    combination = models.ForeignKey(
        MMPIStressToleranceScalesCombination,
        related_name='scales',
        on_delete=models.CASCADE,
    )
    from_point = models.PositiveIntegerField()
    to_point = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.scale}'


class MMPILeadershipStyle(models.Model):
    class Meta:
        verbose_name = _('ММИЛ стиль руководства')
        verbose_name_plural = _('ММИЛ стили руководства')

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name}'


class MMPILeadershipStyleScale(models.Model):
    class Meta:
        verbose_name = _('ММИЛ стиль руководства шкала')
        verbose_name_plural = _('ММИЛ стили руководства шкалы')
        unique_together = ('style', 'scale')

    style = models.ForeignKey(
        MMPILeadershipStyle,
        related_name='scales',
        on_delete=models.CASCADE,
    )
    scale = models.ForeignKey(
        MMPIScale,
        related_name='leadership_styles',
        on_delete=models.CASCADE,
    )
    from_point = models.PositiveIntegerField()
    to_point = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.style} - {self.scale}'


class MMPIUserLeadershipStyle(models.Model):
    class Meta:
        verbose_name = _('ММИЛ стиль руководства пользователя')
        verbose_name_plural = _('ММИЛ стили руководства пользователей')
        unique_together = ('testing_session', 'style')

    testing_session = models.ForeignKey(
        'candidate_tests.TestingSession',
        related_name='leadership_styles',
        on_delete=models.CASCADE,
    )
    style = models.ForeignKey(
        MMPILeadershipStyle,
        related_name='users_leadership_styles',
        on_delete=models.CASCADE,
    )
    type = models.CharField(
        choices=constants.MMPI_LEADERSHIP_STYLES,
        max_length=100,
    )

    def __str__(self):
        return f'{self.testing_session} - {self.style} - {self.type}'
