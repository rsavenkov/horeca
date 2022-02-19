from candidate_tests.models import TestingSessionState
from candidate_tests.utils import get_state_context_default_value


class StateStorage:
    '''Класс представляющий функционал для работы с хранилищем состояний сессий'''
    context_default = get_state_context_default_value()
    model = TestingSessionState

    def __init__(self, session: model):
        self.session = session

    def get_state(self):
        '''Возвращает текущее состояние сессии'''
        state, _ = self.model.objects.get_or_create(session=self.session)
        return state

    def set_state(self, value: str) -> TestingSessionState:
        '''Устанавливает новое значение состояния'''
        state = self.model.objects.get(session=self.session)
        state.state = value
        state.save(update_fields=['state'])
        return state

    def set_context(self, value: dict = context_default) -> dict:
        '''Устанавливает новое значение контекста

        Если в функцию ничего не было передано, установится дефолтное значение
        '''
        state = self.model.objects.get(session=self.session)
        state.context = value
        state.save(update_fields=['context'])
        return state.context
