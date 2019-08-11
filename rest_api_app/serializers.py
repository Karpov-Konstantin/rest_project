from rest_framework import serializers
from .models import Citizen, Import


class CitizenSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(input_formats=['%d.%m.%Y'])

    class Meta:
        model = Citizen
        exclude = ['import_id']


class ImportSerializer(serializers.ModelSerializer):
    citizens = CitizenSerializer(many=True)

    class Meta:
        model = Import
        fields = ['citizens']

    def create(self, validated_data):
        citizens_data = validated_data.pop('citizens')
        imp = Import.objects.create(**validated_data)
        for citizen_data in citizens_data:
            Citizen.objects.create(import_id=imp, **citizen_data)
        return imp
