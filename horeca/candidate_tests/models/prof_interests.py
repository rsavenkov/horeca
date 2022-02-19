from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class ProfInterestsScale(models.Model):
    class Meta:
        verbose_name = _('Проф. интересы шкала')
        verbose_name_plural = _('Проф. интересы шкалы')

    number = models.PositiveIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Scale {self.number}'


class ProfInterestsQuestion(models.Model):
    class Meta:
        verbose_name = _('Проф. интересы вопрос')
        verbose_name_plural = _('Проф. интересы вопросы')

    id = models.PositiveIntegerField(unique=True, primary_key=True)
    question = models.TextField()
    points = models.PositiveIntegerField()

    def __str__(self):
        return f'Question {self.id}'


class ProfInterestsAnswer(models.Model):
    class Meta:
        verbose_name = _('Проф. интересы вариант ответа')
        verbose_name_plural = _('Проф. интересы варианты ответов')

    question = models.ForeignKey(
        ProfInterestsQuestion,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    scale = models.ForeignKey(
        ProfInterestsScale,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    answer = models.TextField()

    def __str__(self):
        return f'Ansewer {self.pk}'


class ProfInterestsUserAnswerList(models.Model):
    class Meta:
        verbose_name = _('Проф. интересы список ответов пользователя')
        verbose_name_plural = _('Проф. интересы списки ответов пользователей')

    session = models.OneToOneField(
        'candidate_tests.TestingSession',
        related_name='prof_interests_user_answer_list',
        on_delete=models.CASCADE,
    )
    questions = models.ManyToManyField(
        ProfInterestsQuestion,
        through='candidate_tests.ProfInterestsUserAnswer',
    )

    def __str__(self):
        return f'{self.session} Prof Interests Testing Result'


class ProfInterestsUserAnswer(models.Model):
    class Meta:
        verbose_name = _('Проф. интересы ответ пользователья')
        verbose_name_plural = _('Проф. интересы ответы пользователей')
        unique_together = ('answer_list', 'question', 'answer'),

    answer_list = models.ForeignKey(
        ProfInterestsUserAnswerList,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    question = models.ForeignKey(
        ProfInterestsQuestion,
        on_delete=models.CASCADE,
        related_name='user_answers'
    )
    answer = models.ForeignKey(
        ProfInterestsAnswer,
        on_delete=models.CASCADE,
    )
    points = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.answer_list}. {self.answer}'


class ProfInterestsResult(models.Model):
    class Meta:
        verbose_name = _('Проф. интересы результат тестирования')
        verbose_name_plural = _('Проф. интересы результаты тестирования')
        unique_together = ('testing_session', 'scale')

    testing_session = models.ForeignKey(
        'candidate_tests.TestingSession',
        on_delete=models.CASCADE,
        related_name='prof_interests'
    )
    scale = models.ForeignKey(
        ProfInterestsScale,
        on_delete=models.CASCADE,
        related_name='users_prof_interests'
    )
    points = models.PositiveIntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0),
        ]
    )

    def __str__(self):
        return f'{self.testing_session} - {self.scale}'
