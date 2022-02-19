import os
import random

from abc import ABCMeta, abstractmethod

from django.utils import timezone

import candidate_tests
from candidate_tests import models, serializers
from horeca_utils import constants
from horeca_utils.constants import TestingSessionSteps as Steps
from users.serializers import CandidateSerializer


class State(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, state, storage):
        pass

    @abstractmethod
    def handle_request(self, request):
        pass

    @abstractmethod
    def next_step(self, request):
        pass

    @staticmethod
    def get_next_state(state):
        if state.state == constants.TestingSessionStates.PENDING_START.value:
            next_state = state.session.tests_names[0]
        elif state.state in state.session.tests_names:
            try:
                current_index = state.session.tests_names.index(state.state)
                next_state = state.session.tests_names[current_index+1]
            except IndexError:
                next_state = constants.TestingSessionStates.FINISH.value

        return next_state


class PendingStartState(State):
    def __init__(self, state, storage):
        super().__init__(state, storage)
        self.state = state
        self.storage = storage
        self.next_state = self.get_next_state(self.state)

    def handle_request(self, request):
        response = None

        if self.state.context['current_step'] == Steps.DATA_PROCESSING_POLICY.value:
            response = self.state.context
        if self.state.context['current_step'] == Steps.INPUT_PERSONAL_DATA.value:
            candidate_serializer = CandidateSerializer(self.state.session.candidate)
            response = {
                **self.state.context,
                'candidate': candidate_serializer.data,
            }

        return response

    def next_step(self, request):
        response = None

        if self.state.context['current_step'] == Steps.DATA_PROCESSING_POLICY.value:
            self.state.context = self.storage.set_context({'current_step': Steps.INPUT_PERSONAL_DATA.value})
            response = self.handle_request(request)

        elif self.state.context['current_step'] == Steps.INPUT_PERSONAL_DATA.value:
            self.storage.set_context({'current_step': Steps.TEST_DESCRIPTION.value})
            self.storage.set_state(self.next_state)
            next_state_machine = candidate_tests.state_machine.make_state_machine(self.state.session)
            response = next_state_machine.handle_request(request)

        return response


class BaseTestState(State):
    def __init__(self, state, storage):
        super().__init__(state, storage)
        self.state = state
        self.storage = storage
        self.next_state = self.get_next_state(self.state)
        self.setup()
        self.questions_count = getattr(self, 'questions_count', self.question_model.objects.count())

    @abstractmethod
    def setup(self):
        '''Абстрактный метод, который должен быть обязательно реализован во всех классах наследниках
        В нем объявляются все необходимые переменные, зависящие от типа тестирования

        test_type - тип тестирования (см. constants.TestTypes)
        question_model - модель вопроса (MMPIQuestion, NonVerbalLogicQuestion и т.д)
        test_description - описание теста (см. constants.TestDescriptions)
        question_serializer_class - класс сериализатора вопроса (MMPIQuestionSerializer и т.д)
        timer - время на прохождения одного вопроса (см. constants.TestTimers)
        '''
        pass

    def set_test_status(self, status):
        test = self.state.session.tests.get(name=self.test_type)
        test.status = status
        test.save(update_fields=['status'])

    def init_question_number(self):
        self.state.context['question_number'] = 1
        self.state.context['question_id'] = self.question_model.objects.order_by('id').first().id

    def increment_question_number(self):
        self.state.context['question_number'] += 1
        self.state.context['previous_question_id'] = self.state.context['question_id']
        self.state.context['question_id'] = self.question_model.objects.filter(
            id__gt=self.state.context['question_id']
        ).order_by('id').first().id

    def handle_request(self, request):
        response = None

        if self.state.context['current_step'] == Steps.TEST_DESCRIPTION.value:
            self.set_test_status(constants.TestingStatuses.IN_PROGRESS.value)
            self.state.session.tests.filter(name=self.test_type).update(start_at=timezone.now())
            response = {
                **self.state.context,
                **self.test_description
            }

        elif self.state.context['current_step'] == Steps.TEST.value:
            response = {**self.generate_questions_info_response(request)}

        return response

    def next_step(self, request):
        response = None

        if self.state.context['current_step'] == Steps.TEST_DESCRIPTION.value:
            self.state.context = {
                'current_step': Steps.TEST.value,
                'test_type': self.test_type,
                'previous_question_id': None,
            }
            self.init_question_number()
            self.storage.set_context(self.state.context)
            response = self.handle_request(request)

        elif self.state.context['current_step'] == Steps.TEST.value:
            if self.state.context['question_number'] < self.questions_count:
                self.increment_question_number()
                self.storage.set_context(self.state.context)
                response = self.handle_request(request)
            else:
                self.set_test_status(constants.TestingStatuses.COMPLETED.value)
                self.state.session.tests.filter(name=self.test_type).update(end_at=timezone.now())
                next_step = self.get_next_step(self.next_state)
                self.storage.set_context({'current_step': next_step})
                self.storage.set_state(self.next_state)
                self.state.context['current_step'] = next_step
                next_state_state_machine = candidate_tests.state_machine.make_state_machine(self.state.session)
                response = next_state_state_machine.handle_request(request)

        return response

    def get_next_step(self, next_state):
        if next_state == constants.TestingSessionStates.FINISH.value:
            next_step = constants.TestingSessionSteps.FINISH.value
        else:
            next_step = constants.TestingSessionSteps.TEST_DESCRIPTION.value

        return next_step

    def previous_step(self, request):
        if self.state.context['previous_question_id'] is not None:
            self.state.context['question_number'] -= 1
            self.state.context['question_id'] = self.state.context['previous_question_id']
            self.storage.set_context(self.state.context)
        return self.handle_request(request)

    def generate_questions_info_response(self, request):
        question = self.question_model.objects.get(id=self.state.context['question_id'])
        answer_options = self.get_answer_options(question, request)

        response = {
            'current_step': self.state.context['current_step'],
            'test_type': self.state.context['test_type'],
            'questions_count': self.questions_count,
            'question_number': self.state.context['question_number'],
            'question': self.question_serializer_class(question, context={'request': request}).data,
            'timer': self.timer,
            'answer_options': answer_options,
        }

        if self.timer is None:
            response['is_can_go_back'] = self.check_is_can_go_back()

        return response

    def get_answer_options(self, question, request):
        return [{'id': a.pk, 'title': a.answer} for a in question.answers.all()]

    def check_is_can_go_back(self):
        ctx = self.state.context
        return ctx['question_number'] != 1 and ctx['question_id'] != ctx['previous_question_id']


class BaseLogicTestState(BaseTestState):
    def setup(self):
        '''Реализация асбтрактного метода BaseTestState
        В классах наследниках необходимо объявить дополнительно следующие переменные:

        user_answer_model - модель ответа (NonVerbalLogicUserAnswer, NumericLogicUserAnswer и т.д)
        user_answer_list_relation - связь сессии с соответствующим объектом модели
            (non_verbal_logic_user_answer_list, numeric_logic_user_answer_list и т.д)

        '''
        pass

    def _handle_missing_question(self):
        '''Создать пустой объект ответа для пропущенного вопроса'''
        question_id = self.state.context['previous_question_id'] if (
            self.state.context['current_step'] == Steps.TEST.value
        ) else self.state.context['question_id']

        user_answer_list = getattr(self.state.session, self.user_answer_list_relation)

        self.user_answer_model.objects.get_or_create(
            question_id=question_id, answer_list__id=user_answer_list.id, defaults={
                'question_id': question_id,
                'answer_list_id': user_answer_list.id
            }
        )

    def next_step(self, request):
        response = super().next_step(request)

        if self.state.context['previous_question_id'] is not None:
            self._handle_missing_question()

        return response


class RandomTestState(BaseLogicTestState):
    def __init__(self, state, storage):
        self.questions_count = constants.LOGIC_TEST_NUMBER_QUESTIONS
        super().__init__(state, storage)

    def init_question_number(self):
        self.state.context['question_ids'] = (
            sorted(random.sample(
                list(self.question_model.objects.values_list('id', flat=True)), self.questions_count
            ))
        )
        self.state.context['question_id'] = self.state.context['question_ids'][0]
        self.state.context['question_number'] = 1

    def increment_question_number(self):
        question_number = self.state.context['question_number']
        question_ids = self.state.context['question_ids']

        self.state.context['previous_question_id'] = self.state.context['question_id']
        self.state.context['question_id'] = question_ids[question_number]
        self.state.context['question_number'] += 1


class MMPITestState(BaseTestState):
    def __init__(self, state, storage):
        super().__init__(state, storage)

    def setup(self):
        self.test_type = constants.TestTypes.MMPI.value
        self.question_model = models.MMPIQuestion
        self.test_description = constants.TestDescriptions.MMPI.value
        self.question_serializer_class = serializers.MMPIQuestionSerializer
        self.timer = constants.TestTimers.MMPI.value

    def get_answer_options(self, *args):
        return [{'id': i[0], 'title': i[1]} for i in constants.MMPI_ANSWERS]


class NumericLogicState(RandomTestState):
    def __init__(self, state, storage):
        super().__init__(state, storage,)

    def setup(self):
        self.test_type = constants.TestTypes.NUMERIC_LOGIC.value
        self.question_model = models.NumericLogicQuestion
        self.user_answer_model = models.NumericLogicUserAnswer
        self.user_answer_list_relation = 'numeric_logic_user_answer_list'
        self.test_description = constants.TestDescriptions.NUMERIC_LOGIC.value
        self.question_serializer_class = serializers.NumericLogicQuestionSerializer
        self.timer = constants.TestTimers.NUMERIC_LOGIC.value


class VerbalLogicState(RandomTestState):

    def __init__(self, state, storage):
        super().__init__(state, storage)

    def setup(self):
        self.test_type = constants.TestTypes.VERBAL_LOGIC.value
        self.question_model = models.VerbalLogicQuestion
        self.user_answer_model = models.VerbalLogicUserAnswer
        self.user_answer_list_relation = 'verbal_logic_user_answer_list'
        self.test_description = constants.TestDescriptions.VERBAL_LOGIC.value
        self.question_serializer_class = serializers.VerbalLogicQuestionSerializer
        self.timer = constants.TestTimers.VERBAL_LOGIC.value


class NonVerbalLogicState(BaseLogicTestState):
    def __init__(self, state, storage):
        super().__init__(state, storage)

    def setup(self):
        self.test_type = constants.TestTypes.NON_VERBAL_LOGIC.value
        self.question_model = models.NonVerbalLogicQuestion
        self.user_answer_model = models.NonVerbalLogicUserAnswer
        self.user_answer_list_relation = 'non_verbal_logic_user_answer_list'
        self.test_description = constants.TestDescriptions.NON_VERBAL_LOGIC.value
        self.question_serializer_class = serializers.NonVerbalLogicQuestionSerializer
        self.timer = constants.TestTimers.NON_VERBAL_LOGIC.value

    def get_answer_options(self, question, request):
        return [{
            'id': i.pk,
            'title': i.answer.title,
            'image': f'{os.environ["HORECA_HOST"]}{i.answer.image.url}'
        } for i in question.answers.order_by('answer__id')]


class ProfInterestsState(BaseTestState):
    def __init__(self, state, storage):
        super().__init__(state, storage)

    def setup(self):
        self.test_type = constants.TestTypes.PROF_INTERESTS.value
        self.question_model = models.ProfInterestsQuestion
        self.test_description = constants.TestDescriptions.PROF_INTERESTS.value
        self.question_serializer_class = serializers.ProfInterestsQuestionSerializer
        self.timer = constants.TestTimers.PROF_INTERESTS.value

    def get_answer_options(self, question, request):
        answers = []
        user_answer_list = self.state.session.prof_interests_user_answer_list

        for a in question.answers.all():
            user_answer = models.ProfInterestsUserAnswer.objects.filter(
                answer_list=user_answer_list,
                question=question,
                answer=a,
            ).first()

            points = user_answer.points if user_answer else 0
            answer = {
                'id': a.pk,
                'title': a.answer,
                'values': [i for i in range(1, 11)],
                'points': points
            }
            answers.append(answer)

        return answers


class FinishState(State):
    def __init__(self, state, storage):
        super().__init__(state, storage)
        self.state = state
        self.storage = storage

    def handle_request(self, request):
        return {'current_step': Steps.FINISH.value}

    def next_step(self, request):
        return self.handle_request(request)
