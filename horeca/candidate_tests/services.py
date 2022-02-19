import random

from django.db.models import F

from . import models, utils
from horeca_utils import constants


class TPointsResultHandler:
    def __init__(self, session):
        self.session = session
        self.answer_list = session.MMPI_testing_answer_list

    def calculate_raw_points_without_k_coef(self):
        '''Подсчитывает сырые баллы, без учета шкалы K

        constants.MMPIAnswers - варианты ответа

        Ключи и Шклаы
        https://docs.google.com/spreadsheets/d/1azBz_2wNZ5u-60EbFpiKLA31IrMuF-aT/edit#gid=241181739
        '''
        self.answer_list.raw_points.update(points=0)
        for answer in self.answer_list.answers.all():
            scales = self.get_scales_by_answer(answer)
            for scale in scales:
                result, _ = models.MMPITestingUserRawPointsResult.objects.get_or_create(
                    answer_list=self.answer_list,
                    scale=scale,
                )
                result.points = F('points') + 1
                result.save(update_fields=['points'])

    def get_scales_by_answer(self, answer: models.MMPITestingUserAnswer):
        '''Возвращает шкалу, если ответ является ее ключом'''
        if answer.answer == constants.MMPIAnswers.YES.value:
            scales = models.MMPIScale.objects.filter(positive_keys=answer.question)
        else:
            scales = models.MMPIScale.objects.filter(negative_keys=answer.question)
        return scales

    def k_coef_processing(self):
        '''Делает корректировку сырых баллов шкалой K

        Шкалы которые подлежат корректировке см. constants.MMPI_SCALES_K_COEFS
        '''
        raw_points = self.answer_list.raw_points.all()
        k_scale_raw_points = raw_points.filter(scale__name=constants.MMPIScales.K.value).first()
        k_scale_raw_points = k_scale_raw_points.points if k_scale_raw_points else 0

        for r in raw_points:
            if r.scale.name in constants.MMPI_SCALES_K_COEFS:
                k_coef = constants.MMPI_SCALES_K_COEFS[r.scale.name]
                r.points = r.points + (k_coef * k_scale_raw_points)
                r.save(update_fields=['points'])

    def calculate_raw_points(self):
        '''Подсчитывает сырые баллы с учетом шкалы К'''
        self.calculate_raw_points_without_k_coef()
        self.k_coef_processing()

    def get_t_points_table_variables(self, scale, gender):
        '''Возвращает значения m и delta для шкал, в зависимости от пола

        m и delta - необходимы для расчета T-баллов
        '''
        table = scale.t_points_tables.get(gender=gender)
        return table.m, table.delta

    def get_raw_points_by_gender(self, gender):
        '''Возвращает сырые баллы относящиеся к полу кандидата'''
        raw_points = self.answer_list.raw_points.all()

        if gender == constants.Genders.MALE.value:
            raw_points = raw_points.exclude(scale__name=constants.MMPIScales.MF_M.value)
        else:
            raw_points = raw_points.exclude(scale__name=constants.MMPIScales.MM.value)

        return raw_points

    def calculate_t_points(self):
        '''Подсчитывает T-баллы кандидата

        расчет производится исходя от значений сырых баллов по каждой шкале
        и значений m, delta для каждой шкалы (см. таблицу TPointsTable)

        Если шкала перевернутая (is_inverted), формула отличается
        '''
        self.set_t_points_default_values()

        gender = self.session.candidate.gender
        raw_points = self.get_raw_points_by_gender(gender)

        for r in raw_points:
            m, delta = self.get_t_points_table_variables(r.scale, gender)
            t_points = 100-(50+10*(r.points-m)/delta) if r.scale.is_inverted else 50+10*(r.points-m)/delta

            if t_points > 100:
                t_points = 100
            elif t_points < 0:
                t_points = 0

            t_points_result, _ = models.MMPITestingUserTPointsResult.objects.get_or_create(
                scale=r.scale,
                answer_list=self.answer_list
            )
            t_points_result.points = round(t_points)
            t_points_result.save(update_fields=['points'])

    def set_t_points_default_values(self):
        self.answer_list.t_points.all().delete()
        self.answer_list.t_points.bulk_create([
            models.MMPITestingUserTPointsResult(
                answer_list=self.answer_list,
                scale=i,
                points=0
            ) for i in models.MMPIScale.objects.all()
        ])


class MMPITestResultFilters:
    '''Класс контроллер дополнительных полей фильтрации,
    которые используются в методе get_test_result класса MMPITestResultHandler
    '''
    def __init__(self, model=None, fields={}):
        if not self._match_fields(model, fields):
            raise Exception(f'Provided filters fields {fields} are not valid')
        self.model = model
        self.fields = fields

    @staticmethod
    def _match_fields(model, fields) -> bool:
        model_fields = [f.name for f in model._meta.get_fields()]
        return all(e in model_fields for e in fields)

    def to_kwargs(self) -> dict:
        return self.fields


class MMPITestResultHandler:
    '''Класс отвещающий за вывод отчета по тесту ММИЛ'''
    def __init__(self, session):
        self.session = session
        self.answer_list = session.MMPI_testing_answer_list
        self.t_points = utils.get_values_by_gender(
            self.answer_list.t_points.all(),
            self.session.candidate.gender,
        )

    def get_test_result(self, model, t_points=None, filters=None):
        '''Возвращает результат ММИЛ тестирования

        model - модель результата
        t_points - T-баллы, если ничего не передано - поиск будет проходить по всем T-баллам
        extra_filter_fields - дополнительные поля фильтрации

        '''
        values = []
        t_points = t_points if t_points else self.t_points.all()
        filters = filters.to_kwargs() if filters else {}

        for t in t_points:
            value = model.objects.filter(
                scale=t.scale,
                from_point__lte=t.points,
                to_point__gte=t.points,
                **filters,
            ).first()

            if value:
                values.append(value)

        return values

    def calculate_motivators(self):
        '''Подсчитывает мотиваторы'''
        self.session.motivators.all().delete()
        motivators = self.get_test_result(models.MMPIMotivator)
        self.session.motivators.bulk_create([
            models.MMPIUserMotivator(
                testing_session=self.session,
                motivator=m,
            ) for m in motivators
        ])

    def calculate_destructors(self):
        '''Подсчитывает деструкторы'''
        self.session.destructors.all().delete()
        destructors = self.get_test_result(models.MMPIDestructor)
        self.session.destructors.bulk_create([
            models.MMPIUserDestructor(
                testing_session=self.session,
                destructor=d,
            ) for d in destructors
        ])

    def calculate_risk_factors(self, is_attantion_factor=False):
        '''Подсчитывает факторы риска у кандидата

        is_attantion_factor если True - подсчитывает факторы внимания

        '''
        self.session.risk_factors.filter(risk_factor__is_attantion_factor=is_attantion_factor).delete()
        risk_factors = self.get_test_result(
            models.MMPIRiskFactor,
            filters=MMPITestResultFilters(
                models.MMPIRiskFactor,
                {'is_attantion_factor': is_attantion_factor}
            )
        )
        self.session.risk_factors.bulk_create([
            models.MMPIUserRiskFactor(
                risk_factor=r,
                testing_session=self.session
            ) for r in risk_factors
        ])

    def _get_competence_inaccuracy(self, competence_type, competence_scales):
        '''Возвращает значение неточности T-баллов в расчетах компетенций'''
        if competence_type == constants.MMPICompetences.HIGHT.value:
            inaccuracy = 0
        else:
            inaccuracy = 10 if len(competence_scales) == 1 else 0

        return inaccuracy

    def _get_competence_succes_condition(self, competence_type, competence_scales, t_points_scales):
        '''Возвращает условие при котором компетенция попадает в тот или иной тип'''
        if competence_type == constants.MMPICompetences.HIGHT.value:
            condition = len(competence_scales) == len(t_points_scales)
        elif competence_type == constants.MMPICompetences.MEDIUM.value:
            condition = bool(t_points_scales)
        elif competence_type == constants.MMPICompetences.LOW.value:
            condition = not bool(t_points_scales)

        return condition

    def get_competences_by_type(self, competence_type):
        '''Возвращает компетенции по типу'''
        competences = []
        for c in models.MMPICompetence.objects.all():
            t_points_scales = []
            competence_scales = utils.get_values_by_gender(c.scales.all(), self.session.candidate.gender)
            inaccuracy = self._get_competence_inaccuracy(competence_type, competence_scales)

            for s in competence_scales:
                t_points_scale = self.t_points.filter(
                    scale=s.scale,
                    points__gte=s.from_point-inaccuracy,
                    points__lte=s.to_point+inaccuracy,
                ).all()
                if t_points_scale:
                    t_points_scales.append(t_points_scale)

            is_valid = self._get_competence_succes_condition(competence_type, competence_scales, t_points_scales)
            if is_valid:
                competences.append(c)

        return competences

    def _calculate_leadership_styles_types(self, leadership_styles):
        peak_max = max(leadership_styles, key=lambda s: s['points'])['points']
        peak_min = min(leadership_styles, key=lambda s: s['points'])['points']

        for style in leadership_styles:
            points = style['points']

            if points == peak_max:
                type = constants.MMPILeadershipStyles.HIGHT.value
            elif points == peak_min:
                type = constants.MMPILeadershipStyles.LOW.value
            else:
                type = constants.MMPILeadershipStyles.MEDIUM.value

            style['type'] = type
        return leadership_styles

    def _get_leadership_styles(self):
        leadership_styles = []

        for leadership_style in models.MMPILeadershipStyle.objects.all():
            t_points_scales = []
            leadership_style_scales = utils.get_values_by_gender(
                leadership_style.scales.all(),
                self.session.candidate.gender,
            )

            for s in leadership_style_scales:
                t_points_scale = self.t_points.filter(
                    scale=s.scale,
                    points__gte=s.from_point,
                    points__lte=s.to_point,
                ).all()
                if t_points_scale:
                    t_points_scales.append(t_points_scale)

            value = len(t_points_scales)/len(leadership_style_scales) * 100 if t_points_scales else 0
            leadership_styles.append({'style': leadership_style, 'points': value})

        return self._calculate_leadership_styles_types(leadership_styles)

    def calculate_leadership_styles(self):
        self.session.leadership_styles.all().delete()
        leadership_styles = self._get_leadership_styles()
        self.session.leadership_styles.bulk_create([
            models.MMPIUserLeadershipStyle(
                testing_session=self.session,
                style=s['style'],
                type=s['type'],
            ) for s in leadership_styles
        ])

    def calculate_competences_by_type(self, competence_type):
        '''Подсчитывает компетенции по типу'''
        self.session.competences.filter(type=competence_type).all().delete()

        if competence_type == constants.MMPICompetences.MEDIUM.value:
            hight_competences = self.get_competences_by_type(constants.MMPICompetences.HIGHT.value)
            medium_competences = self.get_competences_by_type(competence_type)
            competences = [i for i in medium_competences if i not in hight_competences]
        else:
            competences = self.get_competences_by_type(competence_type)

        self.session.competences.bulk_create([
            models.MMPIUserCompetence(
                testing_session=self.session,
                competence=c,
                type=competence_type,
            ) for c in competences
        ])

    def calculate_competences(self):
        '''Подсчитывает компетенции всех типов'''
        for competence_type in constants.MMPICompetences:
            self.calculate_competences_by_type(competence_type.value)

    def calculate_team_roles(self):
        roles = []
        self.session.team_roles.all().delete()

        for r in models.MMPITeamRole.objects.all():
            role_scales = utils.get_values_by_gender(r.scales.all(), self.session.candidate.gender)
            points = self._calculate_team_role_points(role_scales)
            roles.append({'team_role': r, 'points': points})

        self.session.team_roles.bulk_create([
            models.MMPIUserTeamRole(
                testing_session=self.session,
                team_role=r['team_role'],
                points=r['points'],
            ) for r in roles
        ])

    def _calculate_team_role_points(self, role_scales: models.MMPITeamRoleScale):
        '''Подсчитывает набранные баллы для каждой командной роли'''
        t_points = self.t_points.filter(scale__in=role_scales.values_list('scale', flat=True))
        sum_deviations_squares = sum([
            (r.points-t.points)**2 for r in role_scales for t in t_points.filter(scale=r.scale)
        ])
        points = round(100 - sum_deviations_squares * 9 / 1000)
        points = 0 if points < 0 else points  # TODO: проверить алгоритм - 0 быть не должно

        return points

    def _get_stress_tolerance_success_scales_combinations(self):
        combinations = {
            constants.MMPIStressTolerances.HIGHT.value: [],
            constants.MMPIStressTolerances.MEDIUM.value: [],
            constants.MMPIStressTolerances.LOW.value: [],
        }

        for combination in models.MMPIStressToleranceScalesCombination.objects.all():
            t_points_scales = []
            combination_scales = utils.get_values_by_gender(combination.scales.all(), self.session.candidate.gender)
            for s in combination_scales:
                t_points_scale = self.t_points.filter(
                    scale=s.scale,
                    points__gte=s.from_point,
                    points__lte=s.to_point,
                ).first()
                if t_points_scale:
                    t_points_scales.append(t_points_scale)

            if len(t_points_scales) == len(combination.scales.all()):
                combinations[combination.stress_tolerance.name].append(combination)

        return combinations

    def calculate_stress_tolerance(self):
        scales_combinations = self._get_stress_tolerance_success_scales_combinations()

        HIGHT = constants.MMPIStressTolerances.HIGHT.value
        MEDIUM = constants.MMPIStressTolerances.MEDIUM.value
        LOW = constants.MMPIStressTolerances.LOW.value

        if scales_combinations[HIGHT] and not scales_combinations[LOW]:
            stress_tolerance = models.MMPIStressTolerance.objects.get(name=HIGHT)
        elif scales_combinations[LOW] and not scales_combinations[HIGHT]:
            stress_tolerance = models.MMPIStressTolerance.objects.get(name=LOW)
        else:
            stress_tolerance = models.MMPIStressTolerance.objects.get(name=MEDIUM)

        models.MMPIUserStressTolerance.objects.update_or_create(
            testing_session=self.session,
            defaults={'stress_tolerance': stress_tolerance},
        )

    def calculate_test_result(self):
        self.calculate_risk_factors()
        self.calculate_risk_factors(is_attantion_factor=True)
        self.calculate_competences()
        self.calculate_destructors()
        self.calculate_motivators()
        self.calculate_stress_tolerance()
        self.calculate_team_roles()
        self.calculate_leadership_styles()


class LogicTestResultHandler:
    def __init__(self, session, test_types: list = constants.LOGIC_TESTS):
        self.session = session
        self.test_types = test_types

    def get_answer_list(self, test_type):
        '''В зависимости от типа теста возвращает:
        answer_list - список ответов пользователей на вопросы
        answer_model - модель ответа
        '''
        if test_type == constants.TestTypes.VERBAL_LOGIC.value:
            answer_model = models.VerbalLogicAnswer
            answer_list = self.session.verbal_logic_user_answer_list
        elif test_type == constants.TestTypes.NON_VERBAL_LOGIC.value:
            answer_model = models.NonVerbalLogicAnswer
            answer_list = self.session.non_verbal_logic_user_answer_list
        elif test_type == constants.TestTypes.NUMERIC_LOGIC.value:
            answer_model = models.NumericLogicAnswer
            answer_list = self.session.numeric_logic_user_answer_list
        else:
            raise Exception(f'Provided test type {test_type} not valid')

        return answer_list, answer_model

    def calculate_tests_results(self):
        '''Подсчитывет результаты всех тестов на логику'''
        for test_type in self.test_types:
            answer_list, answer_model = self.get_answer_list(test_type)
            # points = sum([a.point for a in answer_model.objects.filter(point__gt=0)])
            points = 20  # Костыль так как оказывается у нас только 20 вопросов может быть

            user_points = sum([a.answer.point for a in answer_list.answers.filter(answer__point__gt=0)])
            user_points = round(user_points/points * 100) if user_points > 0 else user_points
            user_points = 100 if user_points > 100 else user_points

            answer_list.result = user_points
            answer_list.save(update_fields=['result'])


def calculate_prof_interest(session):
    set_prof_interest_default_values(session)
    answer_list = session.prof_interests_user_answer_list

    for i in answer_list.answers.all():
        result, _ = models.ProfInterestsResult.objects.get_or_create(testing_session=session, scale=i.answer.scale)
        result.points = F('points') + i.points
        result.save()


# s.prof_interests.update(points=Subquery(s.prof_interests.filter(id=OuterRef('id')).annotate(percent=100*F('points')/48).values('percent')[:1]))
def convert_prof_interest_to_percent(session):
    for i in session.prof_interests.all():
        i.points = round(100 * i.points / 48)
        i.save(update_fields=['points'])


def set_prof_interest_default_values(session):
    session.prof_interests.all().delete()
    session.prof_interests.bulk_create([
        models.ProfInterestsResult(
            testing_session=session,
            scale=i,
            points=0,
        ) for i in models.ProfInterestsScale.objects.all()
    ])


# Для разработки выводов результатов, потом убрать
def generate_MMPI_user_answers(session):
    answer_list = session.MMPI_testing_answer_list
    for q in models.MMPIQuestion.objects.all():
        models.MMPITestingUserAnswer.objects.update_or_create(
            answer_list=answer_list,
            question=q,
            defaults={'answer': random.choice([1, 2])}
        )


# Для разработки выводов результатов, потом убрать
def generate_prof_interest_user_answers(session):
    answer_list = session.prof_interests_user_answer_list
    for q in models.ProfInterestsQuestion.objects.all():
        models.ProfInterestsUserAnswer.objects.update_or_create(
            answer_list=answer_list,
            question=q,
            defaults={
                'answer': q.answers.first(),
                'points': random.choice([i for i in range(1, 8)]),
                }
        )


def create_answer_lists(session):
    models.MMPITestingUserAnswerList.objects.get_or_create(session=session)
    models.NumericLogicUserAnswerList.objects.get_or_create(session=session)
    models.VerbalLogicUserAnswerList.objects.get_or_create(session=session)
    models.NonVerbalLogicUserAnswerList.objects.get_or_create(session=session)
    models.ProfInterestsUserAnswerList.objects.get_or_create(session=session)
