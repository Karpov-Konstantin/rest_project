import json
import os
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_api_app.models import *


TEST_DIR = 'rest_api_app/tests/payloads'


class CitizensTests(APITestCase):
    def test_import_create_200(self):
        """
        Ensure we can create a new Import object.
        """
        url = reverse('imports')
        with open(os.path.join(TEST_DIR, 'post_import/import_create_200.json'), 'r') as f:
                data = json.load(f)
        response = self.client.post(url, data, format='json')
        import_id = Import.objects.last().id
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
                'data': {
                        'import_id': import_id
                }
        })
        self.assertEqual(Citizen.objects.filter(import_id=import_id).count(), 5)

    def test_import_create_two_side_relatives_400(self):
        """
        Ensure we can't create a new Import object when citizen's citizen_id in his relatives.
        """
        url = reverse('imports')
        with open(os.path.join(TEST_DIR, 'post_import/import_create_two_side_relatives.json'), 'r') as f:
                data = json.load(f)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Import.objects.last(), None)

    def test_import_create_not_all_fields_400(self):
        """
        Ensure we can't create a new Import object without all fields.
        """
        url = reverse('imports')
        with open(os.path.join(TEST_DIR, 'post_import/import_create_not_all_fields.json'), 'r') as f:
                data = json.load(f)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Import.objects.last(), None)

