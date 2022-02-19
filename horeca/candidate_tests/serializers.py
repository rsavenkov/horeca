import os

# from django.db.models import F
from rest_framework import fields, serializers

from . import models, selectors
from users.selectors import get_candidate_testing_status
from horeca_utils import constants


class TestingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestingSession
        fields = ('candidate', 'token_ttl', 'tests')
        # validators = [TestAmountValidator()]

    tests = fields.MultipleChoiceField(choices=constants.TEST_TYPES)

    def create(self, validated_data):
        candidate = validated_data['candidate']
        tests = validated_data.pop('tests')
        instance = super().create(validated_data)
        models.TestingSessionTest.objects.filter(  # TODO костыль, обговорить логику, мб переписать answers lists
            session__candidate=candidate,
            name__in=tests,
        ).update(status=constants.TestingStatuses.RESEND.value)
        instance.tests.bulk_create([
            models.TestingSessionTest(
                session=instance,
                name=t,
            ) for t in tests
        ])
        # candidate.creator.tests_amount.filter(test__in=tests).update(amount=F('amount') - 1)
        candidate.testing_status = get_candidate_testing_status(candidate)
        candidate.save(update_fields=['testing_status'])
        return instance


class MMPIQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MMPIQuestion
        fields = '__all__'


class NumericLogicQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NumericLogicQuestion
        fields = '__all__'


class VerbalLogicQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VerbalLogicQuestion
        fields = '__all__'


class NonVerbalLogicQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NonVerbalLogicQuestion
        fields = ('id', 'question', 'image')

    image = serializers.SerializerMethodField()

    def get_image(self, question):
        return f'{os.environ["HORECA_HOST"]}{question.image.url}'


class ProfInterestsQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfInterestsQuestion
        fields = ('id', 'question', 'points', 'remaining_points')

    remaining_points = serializers.SerializerMethodField()

    def get_remaining_points(self, question):
        request = self.context.get('request')
        answer_list = request.auth.session.prof_interests_user_answer_list
        return selectors.get_prof_interests_question_remaning_points(answer_list, question)


# TODO: можно это дело запихнуть в UserAnswerSerializer
class TestTypeSerializer(serializers.Serializer):
    test_type = serializers.ChoiceField(constants.TEST_TYPES, required=True)


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'
        validators = []

    def to_internal_value(self, data):
        session = self.context['request'].auth.session

        if data['test_type'] == constants.TestTypes.MMPI.value:
            answer_list = session.MMPI_testing_answer_list.pk
        elif data['test_type'] == constants.TestTypes.NUMERIC_LOGIC.value:
            answer_list = session.numeric_logic_user_answer_list.pk
        elif data['test_type'] == constants.TestTypes.VERBAL_LOGIC.value:
            answer_list = session.verbal_logic_user_answer_list.pk
        elif data['test_type'] == constants.TestTypes.NON_VERBAL_LOGIC.value:
            answer_list = session.non_verbal_logic_user_answer_list.pk

        data.update({
            'question': data['question_id'],
            'answer': data['answer_id'],
            'answer_list': answer_list,
        })

        return super().to_internal_value(data)

    def create(self, validated_data):
        answer = validated_data.pop('answer')
        instance, _ = self.Meta.model.objects.update_or_create(
            **validated_data,
            defaults={'answer': answer},
        )
        return instance


class ProfInterestsUserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfInterestsUserAnswer
        fields = ('answer_list', 'question', 'answer', 'points', 'remaining_points')
        validators = []

    remaining_points = serializers.SerializerMethodField(read_only=True)

    def get_remaining_points(self, obj):
        request = self.context.get('request')
        answer_list = request.auth.session.prof_interests_user_answer_list
        return selectors.get_prof_interests_question_remaning_points(answer_list, obj.question)

    def to_internal_value(self, data):
        session = self.context['request'].auth.session
        data.update({
            'question': data['question_id'],
            'answer': data['answer_id'],
            'points': data['points'],
            'answer_list': session.prof_interests_user_answer_list.pk,
        })

        return super().to_internal_value(data)

    # TODO: Добавить валидацию относится ли вопрос к ответу
    def create(self, validated_data):
        points = validated_data.pop('points')
        instance, _ = self.Meta.model.objects.update_or_create(
            **validated_data,
            defaults={'points': points},
        )
        return instance
