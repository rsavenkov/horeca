import time

from django.db.models import F
from django.utils import timezone

from . import models, utils
# from users.selectors import get_candidate_testing_status
from horeca_utils import constants


def generate_tests_general_default_info(candidate):
    status_code = candidate.testing_status
    # status_code = get_candidate_testing_status(candidate)
    test_date = get_test_date(candidate)
    total_time = get_total_tests_time(candidate)
    general_info = {
        'test_status_code': status_code,
        'test_status_title': constants.TESTING_STATUSES_TITLES.get(status_code, 'Устарешвая версия'),
        'test_date': test_date,
        'time': test_time_to_str(total_time),
        'tests': [
            {
                'test_code': test.value,
                'title': constants.TEST_TITLES[test.value],
                'answers_count': 0,
                'correct_answers_count': 0,
                'questions_count': 0,
                'status_code': constants.TestingStatuses.NOT_SEND.value,
                'status': 'Не отправлено',
                'time': '00:00:00'
            } for test in constants.TestTypes
        ],
    }
    return general_info


def get_test_date(candidate):
    test = models.TestingSessionTest.objects.filter(
        session__candidate=candidate,
        status=constants.TestingStatuses.COMPLETED.value
    ).order_by('start_at').first()
    date = test.start_at if test else None
    return str(date)


def get_tests_general_info(candidate):
    general_info = generate_tests_general_default_info(candidate)

    for test_session in candidate.testing_sessions.all():
        for test in test_session.tests.exclude(status=constants.TestingStatuses.RESEND.value):
            if test.name == constants.TestTypes.MMPI.value:
                question_model = models.MMPIQuestion
                answer_list = test_session.MMPI_testing_answer_list

            elif test.name == constants.TestTypes.VERBAL_LOGIC.value:
                question_model = models.VerbalLogicQuestion
                answer_list = test_session.verbal_logic_user_answer_list

            elif test.name == constants.TestTypes.NON_VERBAL_LOGIC.value:
                question_model = models.NonVerbalLogicQuestion
                answer_list = test_session.non_verbal_logic_user_answer_list

            elif test.name == constants.TestTypes.NUMERIC_LOGIC.value:
                question_model = models.NumericLogicQuestion
                answer_list = test_session.numeric_logic_user_answer_list

            elif test.name == constants.TestTypes.PROF_INTERESTS.value:
                question_model = models.ProfInterestsQuestion
                answer_list = test_session.prof_interests_user_answer_list

            test_general_info = get_test_general_info(test, question_model, answer_list)
            general_info['tests'] = [
                t for t in general_info['tests'] if t['test_code'] != test_general_info['test_code']
            ]
            general_info['tests'].append(test_general_info)

    return general_info


def get_test_general_info(test, question_model, answer_list):
    test_name = test.name
    user_answers = answer_list.answers.distinct('question')

    questions_count = question_model.objects.all().count()
    answers_count = user_answers.count()
    time = get_test_time(test)

    general_info = {
        'test_code': test_name,
        'title': constants.TEST_TITLES[test_name],
        'answers_count': answers_count,
        'questions_count': questions_count,
        'correct_answers_count': 0,
        'status_code': test.status,
        'status': constants.TESTING_STATUSES_TITLES[test.status],
        'time': test_time_to_str(time),
    }

    if test.name in constants.LOGIC_TESTS:
        correct_answers_count = user_answers.filter(answer__point__gte=1).count()
        general_info['correct_answers_count'] = correct_answers_count
        general_info['questions_count'] = constants.LOGIC_TEST_NUMBER_QUESTIONS

    return general_info


def get_total_tests_time(candidate):
    total_tests_time = 0

    for test_session in candidate.testing_sessions.all():
        for test in test_session.tests.exclude(status=constants.TestingStatuses.RESEND.value):
            test_time = get_test_time(test)
            total_tests_time += test_time

    return total_tests_time


def get_test_time(test: models.TestingSessionTest):
    if test.start_at and test.end_at:
        diff = (test.end_at - test.start_at).total_seconds()
    elif test.start_at:
        diff = (timezone.now() - test.start_at).total_seconds()
    else:
        diff = 0

    return diff


def test_time_to_str(test_time):
    return time.strftime('%H:%M:%S', time.gmtime(test_time))


class MMPITestResultSelector:
    DEFAULT_PEAK_POINT = 55

    def __init__(self, session):
        self.session = session
        self.answer_list = self.session.MMPI_testing_answer_list
        self.t_points = utils.get_values_by_gender(
            self.answer_list.t_points.all(),
            self.session.candidate.gender,
        )

    def _get_peak_point(self) -> int:
        '''Реализация алгоритма повышения-понижения пиков'''
        t_points = self.t_points.exclude(scale__name__in=constants.CREDIBILITY_SCALES)

        if t_points.filter(points__gt=70).exists():
            peak_point = 70
        elif t_points.filter(points__gte=self.DEFAULT_PEAK_POINT).exists():
            peak_point = self.DEFAULT_PEAK_POINT
        else:
            peak_point = 45

        return peak_point

    def get_risk_factors(self, is_attantion_factor=False) -> dict:
        '''Возвращает факторы риска'''
        risk_factors = models.MMPIRiskFactor.objects.filter(
            users_risk_factors__testing_session=self.session,
            is_attantion_factor=is_attantion_factor,
        ).values('description', title=F('factor'))

        return list(risk_factors)

    def get_all_scales(self) -> dict:
        '''Возвращает все шкалы
        Использовать во View и для генерации pdf отчета
        '''
        scales = {
            'scales': {
                'title': 'Шкалы',
                'description': 'Через значение 50 проходит условное разделение каждой шкалы. Шкалы имеют двойное '
                               'название.' 'Например: Замкнутость/Общительность. При значениях на шкале выше 50 - '
                               'соответствующее качество указано вторым в названии. При значениях на шкале '
                               'менее 50 - качество указано первым.',
                'scales': self.get_scales(),
            },
            'peak_scales': {
                'title': 'Поведение',
                'description': '',
                'scales': self.get_peak_scales(),
            }
        }

        return scales

    def get_scales(self) -> list:
        '''Возвращает все шкалы без описания, если только это не шкалы достоверности (см. CREDIBILITY_SCALES)

        value - значение T-баллов
        description - описание шкалы, в зависимости от набранных баллов

        '''
        scales = []

        for t in self.t_points.order_by('scale__number'):
            description = ''

            if t.scale.name in constants.CREDIBILITY_SCALES:
                description = t.scale.descriptions.filter(
                    from_point__lte=t.points,
                    to_point__gte=t.points,
                ).first().description

            scale = {
                **self._generate_scale_base_info(t.scale),
                'value': t.points,
                'description': description,
            }
            scales.append(scale)

        return scales

    def get_peak_scales(self) -> list:
        '''Возвращает пиковые шкалы с их описанием

        value - значение T-баллов
        description - описание шкалы, в зависимости от набранных баллов
        peak_point - пиковое значение T-баллов

        '''
        peak_scales = []
        peak_point = self._get_peak_point()
        t_points = self.t_points.filter(points__gte=peak_point).exclude(
            scale__name__in=constants.CREDIBILITY_SCALES
        ).order_by('-points')[:5]

        for t in t_points:
            description = models.MMPIScaleDescription.objects.filter(
                scale=t.scale,
                from_point__lte=t.points,
                to_point__gte=t.points,
            ).first().description

            scale = {
                **self._generate_scale_base_info(t.scale),
                'value': t.points,
                'description': description,
            }
            peak_scales.append(scale)

        return peak_scales

    def _generate_scale_base_info(self, scale: models.MMPIScale) -> dict:
        title_start, title_end = scale.verbose_name.split('/')

        return {
            'scale': scale.name,
            'number': scale.number,
            'title_start': title_start,
            'title_end': title_end,
        }

    def get_competences(self) -> dict:
        HIGHT = constants.MMPICompetences.HIGHT.value
        MEDIUM = constants.MMPICompetences.MEDIUM.value
        LOW = constants.MMPICompetences.LOW.value

        competences = {
            'title': 'Компетенции',
            HIGHT: {
                'title': 'Высокоразвитые',
                'competences': [],
                'recommendation': ''
            },
            MEDIUM: {
                'title': 'Среднеразвитые',
                'competences': [],
                'recommendation':  models.MMPIUserCompetenceRecomendation.objects.get(type=MEDIUM).recommendation
            },
            LOW: {
                'title': 'Низкоразвитые',
                'competences': [],
                'recommendation': models.MMPIUserCompetenceRecomendation.objects.get(type=LOW).recommendation
            },
        }

        for competence_type in constants.MMPICompetences:
            competences_by_type = models.MMPICompetence.objects.filter(
                users_competences__testing_session=self.session,
                users_competences__type=competence_type.value,
            ).values('description', title=F('name'))

            competences[competence_type.value]['competences'] = list(competences_by_type)

        return competences

    def get_stress_tolerance(self) -> dict:
        const = {
           constants.MMPIStressTolerances.HIGHT.value: 'HIGHT',
           constants.MMPIStressTolerances.LOW.value: 'LOW',
           constants.MMPIStressTolerances.MEDIUM.value: 'MEDIUM',
        }

        stress_tolerance = {
            'title': 'Стессоустойчивость',
            'stress_tolerance_code': const[self.session.stress_tolerance.stress_tolerance.name],
            'stress_tolerance_name': self.session.stress_tolerance.stress_tolerance.name,
            'description': self.session.stress_tolerance.stress_tolerance.description,
        }
        return stress_tolerance

    def get_motivators_and_destructors(self):
        motivators_and_destructors = {
            'motivators': {
                'title': 'Мотиваторы',
                'description': 'Указаны доминирующие мотивы и рекомендации по поддержанию мотивации',
                'motivators': [
                    {
                        'title': m.motivator.name,
                        'description': m.motivator.description,
                        'recomendation': m.motivator.recommendations,
                    } for m in self.session.motivators.all()
                ]
            },
            'destructors': {
                'title': 'Деструкторы',
                'description': '',
                'destructors': [
                    {
                        'title': d.destructor.name,
                        'description': d.destructor.description,
                        'recomendation': d.destructor.recommendations,
                    } for d in self.session.destructors.all()
                ]
            }
        }

        return motivators_and_destructors

    def get_team_roles(self):
        team_roles = {
            'team_roles': {
                'team_roles': [
                    {
                        'title': r.team_role.name,
                        'points': r.points,
                        'description': r.team_role.description,
                    } for r in self.session.team_roles.order_by('-points')
                ],
            },
        }
        return team_roles

    def get_leadership_styles(self):
        HIGHT = constants.MMPILeadershipStyles.HIGHT.value
        MEDIUM = constants.MMPILeadershipStyles.MEDIUM.value
        LOW = constants.MMPILeadershipStyles.LOW.value
        leadership_style_titles = dict(constants.MMPI_LEADERSHIP_STYLES)

        leadership_styles = {
            'title': 'Стиль управления',
            HIGHT: {
                'title': leadership_style_titles[HIGHT],
                'leadership_styles': []
            },
            MEDIUM: {
                'title': leadership_style_titles[MEDIUM],
                'leadership_styles': []
            },
            LOW: {
                'title': leadership_style_titles[LOW],
                'leadership_styles': []
            },
        }

        for type in constants.MMPILeadershipStyles:
            leadership_styles_by_type = models.MMPILeadershipStyle.objects.filter(
                users_leadership_styles__testing_session=self.session,
                users_leadership_styles__type=type.value,
            ).values('description', title=F('name'))

            leadership_styles[type.value]['leadership_styles'] = list(leadership_styles_by_type)

        return leadership_styles


def get_prof_interests_question_remaning_points(answer_list, question):
    '''Возвращает кол-во оставшихся баллов для распределения на шкалу проф. интересов'''
    points = question.points

    for a in answer_list.answers.filter(answer__question=question):
        points -= a.points

    return points


def get_logic_test_result(session, test_type):
    '''Возвращает результат теста на логику
    test_type - тип теста (NUMERIC_LOGIC, VERBAL_LOGIC, NON_VERBAL_LOGIC и т.д)
    '''
    result = None

    if test_type == constants.TestTypes.VERBAL_LOGIC.value:
        result = session.verbal_logic_user_answer_list.result
    elif test_type == constants.TestTypes.NON_VERBAL_LOGIC.value:
        result = session.non_verbal_logic_user_answer_list.result
    elif test_type == constants.TestTypes.NUMERIC_LOGIC.value:
        result = session.numeric_logic_user_answer_list.result
    else:
        raise Exception(f'Provided test type {test_type} not valid')

    return result


def get_logic_test_results(candidate):
    '''Возвращает результаты тестов на логику
    test_types - список тестов (NUMERIC_LOGIC, VERBAL_LOGIC, NON_VERBAL_LOGIC и т.д)
    '''
    results = {
        'title': 'Логика',
        'results': [],
    }

    for session in candidate.testing_sessions.all():
        tests = session.tests.filter(
            name__in=constants.LOGIC_TESTS,
            status=constants.TestingStatuses.COMPLETED.value,
        )
        for test in tests:
            result = get_logic_test_result(session, test.name)
            result_description = models.LogicTestResultDescription.objects.filter(
                test=test.name,
                from_point__lte=result,
                to_point__gte=result,
            ).first()

            # subtitle = constants.LOGIC_TEST_RESULT_TITLES[result_description.result]
            # if result_description else 'Check',
            # description = result_description.description if result_description else 'Check',

            result = {
                'code': test.name,
                'title': constants.LOGIC_TESTS_TITLES[test.name],
                'subtitle': constants.LOGIC_TEST_RESULT_TITLES[result_description.result],
                'description': result_description.description,
                'value': result,
            }
            results['results'].append(result)

    results = results if results['results'] else None
    return results


def get_prof_interests(session):
    '''Возвращает результат тестирования на проф. интересы'''
    prof_interests = {
        'prof_interests': {
            'prof_interests': [],
        },
    }

    for r in session.prof_interests.order_by('scale__number'):
        prof_interests['prof_interests']['prof_interests'].append(
            {
                'title': r.scale.name,
                'points': r.points,
                'description': r.scale.description,
            }
        )

    return prof_interests


def get_raw_points(session):
    results = {}
    answer_list = session.MMPI_testing_answer_list

    for r in answer_list.raw_points.all():
        result = {r.scale.name: r.points}
        results.update(result)

    return results


def get_tests_results(candidate):
    general_info = get_tests_general_info(candidate)
    data = {'general_info': general_info}

    for session in candidate.testing_sessions.all():
        for test in session.tests.filter(status=constants.TestingStatuses.COMPLETED.value):
            if test.name == constants.TestTypes.MMPI.value:
                MMPI_result_selector = MMPITestResultSelector(session)
                risk_factors = MMPI_result_selector.get_risk_factors()
                attantion_factor = MMPI_result_selector.get_risk_factors(is_attantion_factor=True)
                scales = MMPI_result_selector.get_all_scales()
                competences = MMPI_result_selector.get_competences()
                stress_tolerance = MMPI_result_selector.get_stress_tolerance()
                motivators_and_destructors = MMPI_result_selector.get_motivators_and_destructors()
                team_roles = MMPI_result_selector.get_team_roles()
                leadership_styles = MMPI_result_selector.get_leadership_styles()

                data = {
                    **data,
                    'risk_factors': {
                        'title': 'Факторы риска',
                        'factors': risk_factors,
                    },
                    'attantion_factor': {
                        'title': 'Зоны внимания',
                        'factors': attantion_factor,
                    },
                    'scales': scales,
                    'competences': competences,
                    'stress_tolerance': stress_tolerance,
                    'motivators_and_destructors': motivators_and_destructors,
                    'team_roles': team_roles,
                    'leadership_styles': leadership_styles,
                }

            if test.name == constants.TestTypes.PROF_INTERESTS.value:
                prof_interests = get_prof_interests(session)
                data['prof_interests'] = prof_interests

    loigc_tests = get_logic_test_results(candidate)
    if loigc_tests:
        data['logic'] = loigc_tests

    return data
