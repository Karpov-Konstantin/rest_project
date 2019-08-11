from rest_framework import generics
from .models import Citizen, Import
from .serializers import CitizenSerializer, ImportSerializer
# Create your views here.


class ImportCreateView(generics.CreateAPIView):
    serializer_class = ImportSerializer


class ImportReadView(generics.ListAPIView):
    queryset = Import.objects.all()
    serializer_class = ImportSerializer

    def get_queryset(self):
        import_id = self.kwargs['import_id']
        return Import.objects.filter(id=import_id)


class CitizenUpdateView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Citizen.objects.all()
    serializer_class = CitizenSerializer

    def get_queryset(self):
        import_id = self.kwargs['import_id']
        citizen_id = self.kwargs['citizen_id']
        return Citizen.objects.filter(citizen_id=citizen_id, import_id=import_id)


