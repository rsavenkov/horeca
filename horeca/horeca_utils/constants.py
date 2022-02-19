from enum import Enum

from .utils import enum_choices_factory


class Groups(Enum):
    ADMINS = 'Administrators'
    MANAGERS = 'Managers'
    CANDIDATES = 'Candidates'


class MMPIScales(Enum):
    L = 'L'
    F = 'F'
    K = 'K'
    HS = 'Hs'
    D = 'D'
    HY = 'Hy'
    PD = 'Pd'
    MM = 'Mm'
    MF_M = 'Mf-m'
    PA = 'Pa'
    PT = 'Pt'
    SC = 'Sc'
    MA = 'Ma'
    SI = 'Si'


class MMPIAnswers(Enum):
    YES = 1
    NO = 2


class TestResultGradations(Enum):
    HIGHT = 'HIGHT'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'


class MMPICompetences(Enum):  # TODO: вынести это в класс который не относится к типам тестов
    HIGHT = 'HIGHT'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'


class MMPILeadershipStyles(Enum):
    HIGHT = 'HIGHT'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'


class MMPIStressTolerances(Enum):
    HIGHT = 'Высокий'
    MEDIUM = 'Средний'
    LOW = 'Низкий'


MMPI_SCALES_K_COEFS = {
    MMPIScales.HS.value: 0.5,
    MMPIScales.PD.value: 0.4,
    MMPIScales.PT.value: 1,
    MMPIScales.SC.value: 1,
    MMPIScales.MA.value: 0.2,
}


class TestTypes(Enum):
    MMPI = 'MMPI'
    NUMERIC_LOGIC = 'NUMERIC_LOGIC'
    VERBAL_LOGIC = 'VERBAL_LOGIC'
    NON_VERBAL_LOGIC = 'NON_VERBAL_LOGIC'
    PROF_INTERESTS = 'PROF_INTERESTS'


class TestingSessionStates(Enum):
    PENDING_START = 'PENDING_START'
    MMPI = TestTypes.MMPI.value
    NUMERIC_LOGIC = TestTypes.NUMERIC_LOGIC.value
    VERBAL_LOGIC = TestTypes.VERBAL_LOGIC.value
    NON_VERBAL_LOGIC = TestTypes.NON_VERBAL_LOGIC.value
    PROF_INTERESTS = TestTypes.PROF_INTERESTS.value
    FINISH = 'FINISH'


class TestingSessionSteps(Enum):
    DATA_PROCESSING_POLICY = 'DATA_PROCESSING_POLICY'
    INPUT_PERSONAL_DATA = 'INPUT_PERSONAL_DATA'
    TEST_DESCRIPTION = 'TEST_DESCRIPTION'
    TEST = 'TEST'
    FINISH = 'FINISH'


class TestingStatuses(Enum):
    NOT_SEND = 'NOT_SEND'
    RESEND = 'RESEND'
    NOT_STARTED = 'NOT_STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    NOT_COMPLETED = 'NOT_COMPLETED'
    COMPLETED = 'COMPLETED'


class TestTimers(Enum):
    MMPI = None
    NUMERIC_LOGIC = 30
    VERBAL_LOGIC = 48
    NON_VERBAL_LOGIC = 40
    PROF_INTERESTS = None


TEST_TITLES = {
    TestTypes.MMPI.value: 'Опрос ММИЛ',
    TestTypes.VERBAL_LOGIC.value: 'Вербальная логика',
    TestTypes.NON_VERBAL_LOGIC.value: 'Невербальная логика',
    TestTypes.NUMERIC_LOGIC.value: 'Числовая логика',
    TestTypes.PROF_INTERESTS.value: 'Карта интересов',
}


CREDIBILITY_SCALES = [MMPIScales.L.value, MMPIScales.F.value, MMPIScales.K.value]


class TestDescriptions(Enum):
    MMPI = {
        'title': 'Уважаемый кандидат!',
        'first_paragraph': 'Заложите 40-60 минут на тестирование. Убедитесь, '
                           'что находитесь в привычном для себя состоянии и вас '
                           'ничего не отвлекает от ответов на вопросы.',
        'timer': TestTimers.MMPI.value,
        'second_paragraph': 'Удачного тестирования!',
    }
    NUMERIC_LOGIC = {
        'title': 'Тест на числовую логику',
        'first_paragraph': 'В этом блоке Вам будет необходимо решить 20 задания.',
        'timer': TestTimers.NUMERIC_LOGIC.value,
        'second_paragraph': 'Выделите, пожалуйста, 10 минут времени для прохождения теста, '
                            'чтобы Вас ничего не отвлекало от теста в этот период.',
    }
    VERBAL_LOGIC = {
        'title': 'Тест на вербальную логику',
        'first_paragraph': 'В этом блоке Вам будет необходимо решить 20 задания.',
        'timer': TestTimers.VERBAL_LOGIC.value,
        'second_paragraph': 'Выделите, пожалуйста, 16 минут времени для прохождения теста, '
                            'чтобы Вас ничто не отвлекало от теста в этот период.'
    }
    NON_VERBAL_LOGIC = {
        'title': 'Тест на невербальную логику',
        'first_paragraph': 'В каждом задании Вам предлагается одна фигура, разбитая на несколько частей. '
                           'Эти части даются в произвольном порядке. Соедините мысленно части, и ту фигуру, '
                           'которая у вас при этом получится, найдите в ряду фигур А, Б, В, Г, Д..',
        'timer': TestTimers.NON_VERBAL_LOGIC.value,
        'second_paragraph': 'Перед выполнением теста пройдите тренировочное задание.'
    }
    PROF_INTERESTS = {
        'title': 'Профессиональные интересы',
        'first_paragraph': 'В этом блоке вам необходимо выбрать наиболее подходящие для вас виды деятельности. '
                           'Вам нужно будет распределить 8 баллов между вариантами деятельности в компании по '
                           'степени привлекательности для себя (предыдущий опыт можно не учитывать). '
                           'Чем Вам в принципе было бы интересно заниматься? Вы можете поставить 8 баллов одному '
                           'типу деятельности или примерно равномерно распределить между всеми вариантами.',
        'timer': TestTimers.PROF_INTERESTS.value,
        'second_paragraph': 'Удачного тестирования!'
    }


class Genders(Enum):
    MALE = 'Male'
    FEMALE = 'Female'


GENDERS = enum_choices_factory(Genders)

TEST_TYPES = enum_choices_factory(TestTypes)
TEST_RESULT_GRADATIONS = enum_choices_factory(TestResultGradations)
TESTING_SESSION_STATES = enum_choices_factory(TestingSessionStates)
TESTING_STATUSES = enum_choices_factory(TestingStatuses)
TESTING_STATUSES_TITLES = {
    TestingStatuses.NOT_SEND.value: 'Не отправлено',
    TestingStatuses.RESEND.value: 'Переотправлено',
    TestingStatuses.NOT_STARTED.value: 'Не начато',
    TestingStatuses.IN_PROGRESS.value: 'В процессе',
    TestingStatuses.NOT_COMPLETED.value: 'Не завершено',
    TestingStatuses.COMPLETED.value: 'Завершено'

}

LOGIC_TESTS = [
    TestTypes.NUMERIC_LOGIC.value,
    TestTypes.VERBAL_LOGIC.value,
    TestTypes.NON_VERBAL_LOGIC.value,
]

LOGIC_TESTS_TITLES = {
    TestTypes.NUMERIC_LOGIC.value: 'Числовая логика',
    TestTypes.VERBAL_LOGIC.value: 'Вербальная логика',
    TestTypes.NON_VERBAL_LOGIC.value: 'Невербальная логика',
}

LOGIC_TEST_RESULT_TITLES = {
    TestResultGradations.HIGHT.value: 'Высокий уровень',
    TestResultGradations.MEDIUM.value: 'Средний уровень',
    TestResultGradations.LOW.value: 'Низкий уровень',
}

LOGIC_TEST_NUMBER_QUESTIONS = 20

LOGIC_TESTS_CHOICES = [(i, i) for i in LOGIC_TESTS]

MMPI_SCALES = enum_choices_factory(MMPIScales)
MMPI_STRESS_TOLERANCES = enum_choices_factory(MMPIStressTolerances)
MMPI_ANSWERS = [
    (MMPIAnswers.YES.value, 'Да'),
    (MMPIAnswers.NO.value, 'Нет'),
]
MMPI_COMPETENCES = [
    (MMPICompetences.HIGHT.value, 'Высокоразвитые'),
    (MMPICompetences.MEDIUM.value, 'Среднеразвитые'),
    (MMPICompetences.LOW.value, 'Низкоразвитые'),
]

MMPI_LEADERSHIP_STYLES = [
    (MMPILeadershipStyles.HIGHT.value, 'Характерно'),
    (MMPILeadershipStyles.MEDIUM.value, 'Условно характерно'),
    (MMPILeadershipStyles.LOW.value, 'Не характерно'),
]
