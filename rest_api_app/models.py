from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

GENDER_FIELDS = (('male', 'male'), ('female', 'female'))


class Import(models.Model):
    def __str__(self):
        return self.id


class Citizen(models.Model):
    import_id = models.ForeignKey(Import, related_name='citizens', on_delete=models.CASCADE)
    citizen_id = models.IntegerField()

    # address
    town = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    building = models.CharField(max_length=255)
    apartment = models.IntegerField()

    # personal data
    name = models.CharField(max_length=100)
    birth_date = models.DateField()  # Проверить, что дата является валидной можно с помощью datetime.date
    gender = models.CharField(max_length=6, choices=GENDER_FIELDS)
    relatives = ArrayField(models.IntegerField(), null=True, blank=True)

    def __str__(self):
        return self.name + ' with citizen_id ' + str(self.citizen_id)

