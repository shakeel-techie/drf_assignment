from django.urls import path, include
from rest_framework import routers

from document import views


router = routers.DefaultRouter()
router.register(r'document', views.DocumentViewSet, basename="doc")

urlpatterns = [
    path('', include(router.urls)),
]