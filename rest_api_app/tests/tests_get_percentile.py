import json
import os
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


TEST_DIR = 'rest_api_app/tests/payloads'


class PercentileTests(APITestCase):
    def setUp(self):
        url = reverse('imports')
        with open(os.path.join(TEST_DIR, 'post_import/import_create_200.json'), 'r') as f:
            data = json.load(f)
        self.client.post(url, data, format='json')

    def test_get_percentile_200(self):
        """
        Ensure we can get percentile for import's data by his id
        """
        url = reverse('percentile', kwargs={'import_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_percentile_404(self):
        """
        Ensure we can't get percentile for import's data by his id that doesn't exist.
        """
        url = reverse('birthdays', kwargs={'import_id': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
