from django.db import models
from django.utils.translation import gettext_lazy as _


class NumericLogicQuestion(models.Model):
    class Meta:
        verbose_name = _('Числовая логика вопрос')
        verbose_name_plural = _('Числовая логика вопросы')

    id = models.PositiveIntegerField(unique=True, primary_key=True)
    question = models.TextField()

    def __str__(self):
        return f'Question {self.id}'


class NumericLogicAnswer(models.Model):
    class Meta:
        verbose_name = _('Числовая логика вариант ответа')
        verbose_name_plural = _('Числовая логика варианты ответов')

    question = models.ForeignKey(
        NumericLogicQuestion,
        related_name='answers',
        on_delete=models.CASCADE,
    )
    answer = models.IntegerField()
    point = models.PositiveIntegerField()

    def __str__(self):
        return f'Answer {self.pk} {self.question}'


class NumericLogicUserAnswerList(models.Model):
    class Meta:
        verbose_name = _('Числовая логика список ответов пользователя')
        verbose_name_plural = _('Числовая логика списки ответов пользователей')

    session = models.OneToOneField(
        'candidate_tests.TestingSession',
        related_name='numeric_logic_user_answer_list',
        on_delete=models.CASCADE,
    )
    questions = models.ManyToManyField(
        NumericLogicQuestion,
        through='candidate_tests.NumericLogicUserAnswer',
    )
    result = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.session} Numeric logic Testing Result'


# TODO: AHC-260 Добавить CheckConstraint на проверку относится ли ответ к вопросу
class NumericLogicUserAnswer(models.Model):
    class Meta:
        verbose_name = _('Числовая логика ответ пользователья')
        verbose_name_plural = _('Числовая логика ответы пользователей')
        unique_together = ('answer_list', 'question')

    answer_list = models.ForeignKey(
        NumericLogicUserAnswerList,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        NumericLogicQuestion,
        on_delete=models.CASCADE,
    )
    answer = models.ForeignKey(
        NumericLogicAnswer,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return f'{self.answer_list} {self.question}'
