from rest_framework import generics, exceptions
from rest_framework.views import APIView
from .models import Citizen, Import
from .serializers import CitizenSerializer, ImportSerializer, CitizenUpdateSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db import transaction
from collections import defaultdict
from datetime import date
import numpy as np


class ImportCreateView(generics.CreateAPIView):
    serializer_class = ImportSerializer

    def create(self, request, *args, **kwargs):
        response = super(ImportCreateView, self).create(request, *args, **kwargs)
        response.data = {
            'data': {
                'import_id': Import.objects.last().id
            }
        }
        return response


class ImportReadView(generics.RetrieveAPIView):
    queryset = Import.objects.all().order_by('citizens__citizen_id')
    serializer_class = ImportSerializer
    lookup_url_kwarg = 'import_id'

    def retrieve(self, request, *args, **kwargs):
        response = super(ImportReadView, self).retrieve(request, *args, **kwargs)
        response.data = {
            'data': response.data.get('citizens')
        }
        return response


class CitizenUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Citizen.objects.all()
    serializer_class = CitizenUpdateSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, import_id=self.kwargs['import_id'], citizen_id=self.kwargs['citizen_id'])
        self.check_object_permissions(self.request, obj)
        return obj

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        input_relatives = serializer.validated_data.get('relatives')
        if isinstance(input_relatives, list):  # also check empty list
            ids_to_delete = set(instance.relatives) - set(input_relatives)
            ids_to_add = set(input_relatives) - set(instance.relatives)
            with transaction.atomic():
                for citizen_id in ids_to_add:
                    citizen = Citizen.objects.get(import_id=instance.import_id, citizen_id=citizen_id)
                    citizen.relatives.append(instance.citizen_id)
                    citizen.save()

                for citizen_id in ids_to_delete:
                    citizen = Citizen.objects.get(import_id=instance.import_id, citizen_id=citizen_id)
                    citizen.relatives.remove(instance.citizen_id)
                    citizen.save()
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        obj_full_data = CitizenSerializer(instance).data
        response = Response({
            'data': obj_full_data
        })

        return response

    def put(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(request.method)


class ListBirthdays(APIView):
    @staticmethod
    def get(request, import_id):
        result = dict()
        for key in range(1, 13):
            result[str(key)] = list()

        get_object_or_404(Import, pk=import_id)  # Raise 404 if it doesn't exist
        citizens = Citizen.objects.filter(import_id=import_id)
        for citizen in citizens:
            citizen_result = defaultdict(int)
            for rel_id in citizen.relatives:
                relative = Citizen.objects.get(import_id=import_id, citizen_id=rel_id)
                birthday_month = str(relative.birth_date.month)
                citizen_result[birthday_month] += 1
            for month, presents in citizen_result.items():
                result[month].append({
                    'citizen_id': citizen.citizen_id,
                    'presents': presents
                })
        return Response({'data': result})


class ListPercentiles(APIView):
    @staticmethod
    def get(request, import_id):
        result = list()
        date_dict = defaultdict(list)
        get_object_or_404(Import, pk=import_id)  # Raise 404 if it doesn't exist
        citizens = list(Citizen.objects.filter(import_id=import_id).values_list('birth_date', 'town'))
        for citizen in citizens:
            town, birth_date = citizen[1], citizen[0]
            age = calculate_age(birth_date)
            date_dict[town].append(age)
        for town, date_list in date_dict.items():
            result.append({
                'town': town,
                'p50': np.percentile([date_list], 50),
                'p75': np.percentile([date_list], 75),
                'p99': np.percentile([date_list], 99),
            })
        return Response({'data': result})


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
