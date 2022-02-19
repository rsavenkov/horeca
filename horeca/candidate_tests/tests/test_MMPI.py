from django.test import TestCase
from unittest import mock

from . import factories
from candidate_tests import models, utils, services, selectors


class MMPITestCase(TestCase):
    @mock.patch('users.services.create_candidate_creator')
    def setUp(self, mock_create_candidate_creator):
        self.session = factories.TestingSessionFactory()
        answers = utils.testing_data_parser.parse_test_answers_file('Овчаренко Павел')
        self.session.MMPI_testing_answer_list.answers.bulk_create([
            models.MMPITestingUserAnswer(
                answer_list=self.session.MMPI_testing_answer_list,
                question=models.MMPIQuestion.objects.get(question=i['question']),
                answer=i['answer'],
            ) for i in answers
        ])
        t_h = services.TPointsResultHandler(self.session)
        t_h.calculate_raw_points()
        t_h.calculate_t_points()

    def test_all_scales(self):
        scales_for_comparison = self._get_scales_for_comparison('Овчаренко Павел')
        selector = selectors.MMPITestResultSelector(self.session)
        scales = selector.get_scales()
        for scale in scales:
            for scale_for_comparison in scales_for_comparison:
                if scale['scale'] == scale_for_comparison['scale']:
                    self.assertEqual(scale['value'], scale_for_comparison['value'])

    def test_peak_scales(self):
        scales_for_comparison = self._get_scales_for_comparison('Овчаренко Павел', is_peak=True)
        selector = selectors.MMPITestResultSelector(self.session)
        scales = selector.get_peak_scales()
        for scale in scales:
            self.assertTrue(scale['scale'] in scales_for_comparison)

    def _get_scales_for_comparison(self, candidate_name, is_peak=False):
        scales_for_comparison = None
        scales_type = 'peak_scales' if is_peak else 'scales'
        MMPI_tests_results = utils.testing_data_parser.parse_json_file('tests_results.json')['MMPI']
        for index, value in enumerate(MMPI_tests_results):
            if value['candidate'] == candidate_name:
                scales_for_comparison = MMPI_tests_results[index][scales_type]

        return scales_for_comparison
