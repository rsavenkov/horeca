from django.db import models
from django.utils.translation import gettext_lazy as _


class VerbalLogicQuestion(models.Model):
    class Meta:
        verbose_name = _('Вербальная логика вопрос')
        verbose_name_plural = _('Вербальная логика вопросы')

    id = models.PositiveIntegerField(unique=True, primary_key=True)
    question = models.TextField()

    def __str__(self):
        return f'Question {self.id}'


class VerbalLogicAnswer(models.Model):
    class Meta:
        verbose_name = _('Вербальная логика вариант ответа')
        verbose_name_plural = _('Вербальная логика варианты ответов')

    question = models.ForeignKey(
        VerbalLogicQuestion,
        related_name='answers',
        on_delete=models.CASCADE,
    )
    answer = models.TextField()
    point = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.question} - Answer {self.pk}'


class VerbalLogicUserAnswerList(models.Model):
    class Meta:
        verbose_name = _('Вербальная логика список ответов пользователя')
        verbose_name_plural = _('Вербальная логика списки ответов пользователей')

    session = models.OneToOneField(
        'candidate_tests.TestingSession',
        related_name='verbal_logic_user_answer_list',
        on_delete=models.CASCADE,
    )
    questions = models.ManyToManyField(
        VerbalLogicQuestion,
        through='candidate_tests.VerbalLogicUserAnswer',
    )
    result = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.session} Numeric logic Testing Result'


class VerbalLogicUserAnswer(models.Model):
    class Meta:
        verbose_name = _('Вербальная логика ответ пользователья')
        verbose_name_plural = _('Вербальная логика ответы пользователей')
        unique_together = ('answer_list', 'question')

    answer_list = models.ForeignKey(
        VerbalLogicUserAnswerList,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    question = models.ForeignKey(
        VerbalLogicQuestion,
        on_delete=models.CASCADE,
    )
    answer = models.ForeignKey(
        VerbalLogicAnswer,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return f'{self.answer_list} {self.question}'
