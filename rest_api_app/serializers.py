from rest_framework import serializers, exceptions
from .models import Citizen, Import
from collections import defaultdict


class CitizenSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(format='%d.%m.%Y', input_formats=['%d.%m.%Y'])
    relatives = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Citizen
        # exclude = ['import_id', 'id']
        fields = ['citizen_id', 'town', 'street', 'building', 'apartment', 'name', 'birth_date', 'gender', 'relatives']
        ordering = ['citizen_id']


class CitizenUpdateSerializer(CitizenSerializer):
    class Meta:
        model = Citizen
        exclude = ['import_id', 'id', 'citizen_id']
        # fields = ['name', 'town', 'street', 'building', 'apartment', 'relatives']

    def validate_relatives(self, attrs):
        validated_data = super(CitizenUpdateSerializer, self).validate(attrs)
        all_citizens = Citizen.objects.filter(import_id=self.instance.import_id).values_list('citizen_id', flat=True)
        if not set(validated_data).issubset(set(all_citizens)):
            raise exceptions.ValidationError('Incorrect relatives')
        if self.instance.citizen_id in validated_data:
            raise exceptions.ValidationError('Сan\'t be related to himself')
        return validated_data

    def validate(self, attrs):
        validated_data = super(CitizenUpdateSerializer, self).validate(attrs)
        if len(validated_data.keys()) < 1:
            raise exceptions.ValidationError(
                {'valid_quantity': 'at least 1 field is required'}
            )
        return validated_data


class ImportSerializer(serializers.ModelSerializer):
    citizens = CitizenSerializer(many=True)

    class Meta:
        model = Import
        fields = ['citizens']

    def validate(self, attrs):
        validated_data = super(ImportSerializer, self).validate(attrs)
        citizens_data = validated_data.get('citizens')
        input_rel = defaultdict(set)
        output_rel = defaultdict(set)

        for citizen_data in citizens_data:
            citizen_relatives = citizen_data.get('relatives')
            citizen_id = citizen_data.get('citizen_id')
            if len(citizen_relatives) > 0:
                input_rel.update({citizen_id: set(citizen_relatives)})
            for rel_id in citizen_relatives:
                output_rel[rel_id].add(citizen_id)

        if input_rel != output_rel:
            raise exceptions.ValidationError(
                {'valid_relatives': 'relatives do not match'}
            )
        return validated_data

    def create(self, validated_data):
        citizens_data = validated_data.pop('citizens')
        imp = Import.objects.create(**validated_data)
        for citizen_data in citizens_data:
            Citizen.objects.create(import_id=imp, **citizen_data)
        return imp
