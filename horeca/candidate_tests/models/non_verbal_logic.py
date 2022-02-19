from django.db import models
from django.utils.translation import gettext_lazy as _


class NonVerbalLogicQuestion(models.Model):
    class Meta:
        verbose_name = _('Невербальная логика вопрос')
        verbose_name_plural = _('Невербальная логика вопросы')

    id = models.PositiveIntegerField(unique=True, primary_key=True)
    question = models.TextField()
    image = models.ImageField()
    answer_options = models.ManyToManyField(
        'candidate_tests.NonVerbalLogicAnswerOption',
        through='candidate_tests.NonVerbalLogicAnswer',
        related_name='questions'
    )

    def __str__(self):
        return f'Question {self.id}'


class NonVerbalLogicAnswerOption(models.Model):
    class Meta:
        verbose_name = _('Невербальная логика вариант ответа')
        verbose_name_plural = _('Невербальная логика варианты ответов')

    id = models.PositiveIntegerField(unique=True, primary_key=True)
    image = models.ImageField()
    title = models.CharField(max_length=1, blank=True)

    def __str__(self):
        return f'Answer option {self.id}'


class NonVerbalLogicAnswer(models.Model):
    class Meta:
        verbose_name = _('Невербальная логика ответ')
        verbose_name_plural = _('Невербальная логика ответы')
        unique_together = ('question', 'answer')

    question = models.ForeignKey(
        NonVerbalLogicQuestion,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    answer = models.ForeignKey(
        NonVerbalLogicAnswerOption,
        on_delete=models.CASCADE,
    )
    point = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.question} - {self.answer}'


class NonVerbalLogicUserAnswerList(models.Model):
    class Meta:
        verbose_name = _('Невербальная логика список ответов пользователя')
        verbose_name_plural = _('Невербальная логика списки ответов пользователей')

    session = models.OneToOneField(
        'candidate_tests.TestingSession',
        related_name='non_verbal_logic_user_answer_list',
        on_delete=models.CASCADE,
    )
    questions = models.ManyToManyField(
        NonVerbalLogicQuestion,
        through='candidate_tests.NonVerbalLogicUserAnswer',
    )
    result = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.session} Numeric logic Testing Result'


class NonVerbalLogicUserAnswer(models.Model):
    class Meta:
        verbose_name = _('Невербальная логика ответ пользователья')
        verbose_name_plural = _('Невербальная логика ответы пользователей')
        unique_together = ('answer_list', 'question')

    answer_list = models.ForeignKey(
        NonVerbalLogicUserAnswerList,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    question = models.ForeignKey(
        NonVerbalLogicQuestion,
        on_delete=models.CASCADE,
    )
    answer = models.ForeignKey(
        NonVerbalLogicAnswer,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return f'{self.answer_list} {self.question}'
