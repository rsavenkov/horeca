from random import randint

import factory
from factory.django import DjangoModelFactory
from factory import fuzzy

from users import models as users_models
from candidate_tests import models as tests_models
from horeca_utils import constants


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


class ManagerFactory(DjangoModelFactory):
    class Meta:
        model = users_models.Manager

    email = factory.Faker('email')
    first_name = factory.Faker('name')
    last_name = factory.Faker('last_name')
    taxpayer_id_number = f'{random_with_N_digits(12)}'


class CandidateCreatorFactory(DjangoModelFactory):
    class Meta:
        model = users_models.CandidateCreator

    manager = factory.SubFactory(ManagerFactory)


class CandidateFactory(DjangoModelFactory):
    class Meta:
        model = users_models.Candidate

    email = factory.Faker('email')
    first_name = factory.Faker('name')
    last_name = factory.Faker('last_name')
    creator = factory.SubFactory(CandidateCreatorFactory)
    # gender = fuzzy.FuzzyChoice(constants.GENDERS)
    gender = constants.Genders.MALE.value


class TestingSessionFactory(DjangoModelFactory):
    class Meta:
        model = tests_models.TestingSession

    candidate = factory.SubFactory(CandidateFactory)
