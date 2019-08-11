from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
# Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register(r'snippets', views.SnippetViewSet)
# router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),

    path('imports/', ImportCreateView.as_view()),  # POST
    path('imports/<int:import_id>/citizens/', ImportReadView.as_view()),  # GET
    path('imports/<int:import_id>/citizens/<int:citizen_id>/', CitizenUpdateView.as_view()),  # PATCH
    # path('imports/<int:import_id>/citizens/birthdays', CitizenView.as_view()),  # GET
    # path('imports/<int:import_id>/towns/stat/percentile/age/', CitizenView.as_view()),  # GET

    path('imports/<int:citizen_id>/citizens/', CitizenUpdateView.as_view()),  # GET

]