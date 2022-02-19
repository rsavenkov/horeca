from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class CandidateTestsConfig(AppConfig):
    name = 'candidate_tests'

    def ready(self):
        autodiscover_modules('signals')
