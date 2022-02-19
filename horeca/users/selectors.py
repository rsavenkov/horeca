from . import models
from candidate_tests.models import TestingSessionTest
from horeca_utils import constants


def get_candidate_testing_status(candidate):
    status = None

    NOT_SEND = constants.TestingStatuses.NOT_SEND.value
    RESEND = constants.TestingStatuses.RESEND.value
    NOT_STARTED = constants.TestingStatuses.NOT_STARTED.value
    IN_PROGRESS = constants.TestingStatuses.IN_PROGRESS.value
    NOT_COMPLETED = constants.TestingStatuses.NOT_COMPLETED.value
    COMPLETED = constants.TestingStatuses.COMPLETED.value

    tests = TestingSessionTest.objects.filter(session__candidate=candidate)

    if not tests.all():
        status = NOT_SEND
    elif not tests.exclude(status__in=[COMPLETED, RESEND, NOT_SEND]):
        status = COMPLETED
    elif tests.filter(status=NOT_COMPLETED):
        status = NOT_COMPLETED
    elif not tests.exclude(status__in=[NOT_STARTED, RESEND]):
        status = NOT_STARTED
    elif tests.filter(status=IN_PROGRESS):
        status = IN_PROGRESS
    elif not tests.exclude(status__in=[NOT_STARTED, COMPLETED, RESEND]):
        status = constants.TestingStatuses.IN_PROGRESS.value

    return status


def get_candidate_creator(user):
    if isinstance(user, models.Candidate):
        creator = user.creator
    else:
        creator = user.candidatecreator

    return creator
