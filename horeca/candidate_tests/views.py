from django.utils.translation import gettext_lazy as _
from rest_framework import status, viewsets
from rest_framework.response import Response

from . import (
    authentication,
    serializers,
    models,
)
from .state_machine import make_state_machine
from horeca_utils import constants
from users.serializers import CandidateSerializer


class TestingSessionView(viewsets.ViewSet):
    authentication_classes = [authentication.TestingSessionAuthentication]

    def get(self, request, format=None):
        state_machine = make_state_machine(request.auth.session)
        response = state_machine.handle_request(request)
        return Response(data=response, status=status.HTTP_200_OK)

    def next_step(self, request):
        state_machine = make_state_machine(request.auth.session)
        response = state_machine.next_step(request)
        return Response(data=response, status=status.HTTP_200_OK)

    def previous_step(self, request):
        try:
            state_machine = make_state_machine(request.auth.session)
            response = state_machine.previous_step(request)
            return Response(data=response, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                data={'message': _('На данном этапе тестирования невозможно вернуться назад.')},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def fill_personal_data(self, request):
        instance = self.request.auth.user.related_object
        serializer = CandidateSerializer(instance, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def answer_question(self, request):
        serializer = self._get_user_answer_serializer(request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _get_user_answer_serializer_class(self, request):
        serializer_class = None
        serializer = serializers.TestTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.data['test_type'] == constants.TestTypes.MMPI.value:
            serializers.UserAnswerSerializer.Meta.model = models.MMPITestingUserAnswer
        elif serializer.data['test_type'] == constants.TestTypes.NUMERIC_LOGIC.value:
            serializers.UserAnswerSerializer.Meta.model = models.NumericLogicUserAnswer
        elif serializer.data['test_type'] == constants.TestTypes.VERBAL_LOGIC.value:
            serializers.UserAnswerSerializer.Meta.model = models.VerbalLogicUserAnswer
        elif serializer.data['test_type'] == constants.TestTypes.NON_VERBAL_LOGIC.value:
            serializers.UserAnswerSerializer.Meta.model = models.NonVerbalLogicUserAnswer
        elif serializer.data['test_type'] == constants.TestTypes.PROF_INTERESTS.value:
            return serializers.ProfInterestsUserAnswerSerializer

        serializer_class = serializers.UserAnswerSerializer
        return serializer_class

    def _get_user_answer_serializer(self, request):
        serializer_class = self._get_user_answer_serializer_class(request)
        return serializer_class(data=request.data, context={'request': request})
