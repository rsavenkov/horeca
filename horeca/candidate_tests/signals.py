from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models, services
from users.services import candidate_email_sender, create_user
from users.selectors import get_candidate_testing_status
from horeca_utils import constants


@transaction.atomic
@receiver(post_save, sender=models.TestingSession)
def send_testing_session(sender, instance=None, created=False, **kwargs):
    '''Сигнал отправляющий сообщение с ссылкой для начала тестирования'''
    if created:
        token, _ = models.TestingSessionToken.objects.get_or_create(session=instance)
        services.create_answer_lists(instance)
        candidate_email_sender.send_start_test_message(instance.candidate.email, token)


@transaction.atomic
@receiver(post_save, sender=models.TestingSessionState)
def handle_testing_session_state(sender, instance=None, created=False, **kwargs):
    if instance.state == constants.TestingSessionStates.FINISH.value:
        user, password = create_user(instance.session.candidate)
        candidate_email_sender.send_invite_message(
            instance.session.candidate.email,
            {
                'login': user.email,
                'password': password,
            }
        )


@transaction.atomic
@receiver(post_save, sender=models.TestingSessionTest)
def handle_test_status(sender, instance=None, created=False, **kwargs):
    if instance.status == constants.TestingStatuses.COMPLETED.value:
        if instance.name == constants.TestTypes.MMPI.value:
            # services.generate_MMPI_user_answers(instance.session)
            t_h = services.TPointsResultHandler(instance.session)
            t_h.calculate_raw_points()
            t_h.calculate_t_points()
            r_h = services.MMPITestResultHandler(instance.session)
            r_h.calculate_test_result()

        if instance.name in constants.LOGIC_TESTS:
            l_h = services.LogicTestResultHandler(instance.session, test_types=[instance.name])
            l_h.calculate_tests_results()

        if instance.name == constants.TestTypes.PROF_INTERESTS.value:
            # services.generate_prof_interest_user_answers(instance.session)
            services.calculate_prof_interest(instance.session)
            services.convert_prof_interest_to_percent(instance.session)

    candidate = instance.session.candidate
    candidate.testing_status = get_candidate_testing_status(candidate)
    candidate.save(update_fields=['testing_status'])
