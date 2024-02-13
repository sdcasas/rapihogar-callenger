from django.urls import path, include
from rest_framework import routers

from core.models import Company

from .views import CompanyViewSet


router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')


urlpatterns = [
    path('', include(router.urls)),
]
