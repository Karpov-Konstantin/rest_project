import json
import os
from rest_framework import status
from django.urls import reverse
from rest_api_app.models import *
from datetime import datetime
from django.test import TestCase
TEST_DIR = 'rest_api_app/tests/payloads'


class CitizensTests(TestCase):
    @staticmethod
    def setUp():
        imp = Import.objects.create()
        with open(os.path.join(TEST_DIR, 'get_patch_citizens/get_citizens_200.json'), 'r') as f:
            data = json.load(f)
        for citizen in data:
            citizen['birth_date'] = datetime.strptime(citizen['birth_date'], '%d.%m.%Y').date()
            citizen['import_id'] = imp
            Citizen.objects.create(**citizen)

    def test_get_citizens_200(self):
        """
        Ensure we can get citizens by import_id.
        """
        imp_id = Import.objects.last().id
        url = reverse('citizens', kwargs={'import_id': imp_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_citizens_404(self):
        """
        Ensure we can get citizens by import_id.
        """
        url = reverse('citizens', kwargs={'import_id': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_citizen_200(self):
        """
            Ensure we can patch single citizen.
        """
        imp_id = Import.objects.last().id
        url = reverse('patch_citizen', kwargs={'import_id': imp_id, 'citizen_id': 3})
        response = self.client.patch(url, data=json.dumps({"street": "Улица далекая"}),
                                     content_type='application/json', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_citizen_404(self):
        """
            Ensure we can patch single citizen.
        """
        url = reverse('patch_citizen', kwargs={'import_id': 1000, 'citizen_id': 3})
        response = self.client.patch(url, data=json.dumps({"street": "Улица далекая"}),
                                     content_type='application/json', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_delete_some_citizen_relatives_200(self):
        """
            Ensure we can patch single citizen.
        """
        imp_id = Import.objects.last().id
        url = reverse('patch_citizen', kwargs={'import_id': imp_id, 'citizen_id': 4})
        # change citizen.relatives from [2,3,5] to [2,3] (citizen_id=4)
        response = self.client.patch(url, data=json.dumps({"relatives": [2, 3]}),
                                     content_type='application/json', format='json')
        citizen_4 = Citizen.objects.get(import_id=imp_id, citizen_id=4)
        citizen_5 = Citizen.objects.get(import_id=imp_id, citizen_id=5)
        self.assertEqual(citizen_4.relatives, [2, 3])
        self.assertEqual(citizen_5.relatives, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_add_some_citizen_relatives_200(self):
        """
            Ensure we can patch single citizen.
        """
        imp_id = Import.objects.last().id
        url = reverse('patch_citizen', kwargs={'import_id': imp_id, 'citizen_id': 4})
        # change citizen.relatives from [2,3,5] to [1,2,3,5] (citizen_id=4)
        response = self.client.patch(url, data=json.dumps({"relatives": [1, 2, 3, 5]}),
                                     content_type='application/json', format='json')
        citizen_1 = Citizen.objects.get(import_id=imp_id, citizen_id=1)
        citizen_2 = Citizen.objects.get(import_id=imp_id, citizen_id=2)
        citizen_3 = Citizen.objects.get(import_id=imp_id, citizen_id=3)
        citizen_4 = Citizen.objects.get(import_id=imp_id, citizen_id=4)
        citizen_5 = Citizen.objects.get(import_id=imp_id, citizen_id=5)
        self.assertEqual(citizen_1.relatives, [2, 3, 4])
        self.assertEqual(citizen_2.relatives, [1, 4])
        self.assertEqual(citizen_3.relatives, [1, 4])
        self.assertEqual(citizen_4.relatives, [1, 2, 3, 5])
        self.assertEqual(citizen_5.relatives, [4])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_relatives_400(self):
        """
            Ensure that DB data don't change with 400 response
        """
        imp_id = Import.objects.last().id
        url = reverse('patch_citizen', kwargs={'import_id': imp_id, 'citizen_id': 4})
        # change citizen.relatives from [2,3,5] to [1,2,3,5] (citizen_id=4)
        response = self.client.patch(url, data=json.dumps({"relatives": [1, 2, 3, 5, 6]}),
                                     content_type='application/json', format='json')
        citizen_1 = Citizen.objects.get(import_id=imp_id, citizen_id=1)
        citizen_2 = Citizen.objects.get(import_id=imp_id, citizen_id=2)
        citizen_3 = Citizen.objects.get(import_id=imp_id, citizen_id=3)
        citizen_4 = Citizen.objects.get(import_id=imp_id, citizen_id=4)
        citizen_5 = Citizen.objects.get(import_id=imp_id, citizen_id=5)
        self.assertEqual(citizen_1.relatives, [2, 3])
        self.assertEqual(citizen_2.relatives, [1, 4])
        self.assertEqual(citizen_3.relatives, [1, 4])
        self.assertEqual(citizen_4.relatives, [2, 3, 5])
        self.assertEqual(citizen_5.relatives, [4])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_empty_list_citizen_relatives_200(self):
        """
            Ensure we can patch single citizen.
        """
        imp_id = Import.objects.last().id
        url = reverse('patch_citizen', kwargs={'import_id': imp_id, 'citizen_id': 4})
        # change citizen.relatives from [2,3,5] to [] (citizen_id=4)
        response = self.client.patch(url, data=json.dumps({"relatives": []}),
                                     content_type='application/json', format='json')
        citizen_2 = Citizen.objects.get(import_id=imp_id, citizen_id=2)
        citizen_3 = Citizen.objects.get(import_id=imp_id, citizen_id=3)
        citizen_4 = Citizen.objects.get(import_id=imp_id, citizen_id=4)
        citizen_5 = Citizen.objects.get(import_id=imp_id, citizen_id=5)
        self.assertEqual(citizen_2.relatives, [1])
        self.assertEqual(citizen_3.relatives, [1])
        self.assertEqual(citizen_4.relatives, [])
        self.assertEqual(citizen_5.relatives, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


