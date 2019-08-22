from django.urls import path
from .views import *

urlpatterns = [

    path('imports', ImportCreateView.as_view(), name='imports'),  # POST
    path('imports/<int:import_id>/citizens', ImportReadView.as_view(), name='citizens'),  # GET
    path('imports/<int:import_id>/citizens/<int:citizen_id>', CitizenUpdateView.as_view(),
         name='patch_citizen'),  # PATCH
    path('imports/<int:import_id>/citizens/birthdays', ListBirthdays.as_view(), name='birthdays'),  # GET
    path('imports/<int:import_id>/towns/stat/percentile/age', ListPercentiles.as_view(), name='percentile'),  # GET

]