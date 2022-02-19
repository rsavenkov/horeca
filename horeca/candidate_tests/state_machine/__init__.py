from . import states
from .storage import StateStorage
from horeca_utils.constants import TestingSessionStates


STATES = {
    TestingSessionStates.PENDING_START.value: states.PendingStartState,
    TestingSessionStates.MMPI.value: states.MMPITestState,
    TestingSessionStates.NUMERIC_LOGIC.value: states.NumericLogicState,
    TestingSessionStates.VERBAL_LOGIC.value: states.VerbalLogicState,
    TestingSessionStates.NON_VERBAL_LOGIC.value: states.NonVerbalLogicState,
    TestingSessionStates.PROF_INTERESTS.value: states.ProfInterestsState,
    TestingSessionStates.FINISH.value: states.FinishState,
}


def make_state_machine(session):
    storage = StateStorage(session)
    state = storage.get_state()
    state_class = STATES[state.state]
    return state_class(state, storage)
