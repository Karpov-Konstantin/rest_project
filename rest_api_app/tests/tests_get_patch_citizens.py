import json
import os
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_api_app.models import *
TEST_DIR = 'rest_api_app/tests/payloads'


class CitizensTests(APITestCase):
    def setUp(self):
        url = reverse('imports')
        with open(os.path.join(TEST_DIR, 'post_import/import_create_200.json'), 'r') as f:
            data = json.load(f)
        self.client.post(url, data, format='json')

        # with open(os.path.join(TEST_DIR, 'get_patch_citizens/get_citizens_200.json'), 'r') as f:
        #     data = json.load(f)
        # for citizen in data:
        #     citizen.birth_date =
        #     Citizen.objects.create(**citizen)

    def test_get_citizens_200(self):
        """
        Ensure we can get citizens by import_id.
        """
        url = reverse('citizens', kwargs={'import_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_citizen_200(self):
        """
            Ensure we can patch single citizen.
        """
        # url = reverse('citizens', kwargs={'import_id': 1})
        # response = self.client.get(url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('patch_citizen', kwargs={'import_id': 1, 'citizen_id': 1})
        response = self.client.get(url)
        # self.assertEqual(Citizen.objects.all().count() > 0, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CitizensPatchTests(APITestCase):
    def setUp(self):
        url = reverse('imports')
        with open(os.path.join(TEST_DIR, 'post_import/import_create_200.json'), 'r') as f:
            data = json.load(f)
        self.client.post(url, data, format='json')

        # with open(os.path.join(TEST_DIR, 'get_patch_citizens/get_citizens_200.json'), 'r') as f:
        #     data = json.load(f)
        # for citizen in data:
        #     citizen.birth_date =
        #     Citizen.objects.create(**citizen)

    def test_patch_citizen_200(self):
        """
            Ensure we can patch single citizen.
        """
        # url = reverse('citizens', kwargs={'import_id': 1})
        # response = self.client.get(url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('patch_citizen', kwargs={'import_id': 1, 'citizen_id': 1})
        response = self.client.patch(url, data={"street": "Улица далекая"}, format='json')
        # self.assertEqual(Citizen.objects.all().count() > 0, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_citizen_400(self):
        """
            Ensure we can patch single citizen.
        """
        # url = reverse('citizens', kwargs={'import_id': 1})
        # response = self.client.get(url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('patch_citizen', kwargs={'import_id': 1, 'citizen_id': 1})
        response = self.client.patch(url)
        # self.assertEqual(Citizen.objects.all().count() > 0, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

