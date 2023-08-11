from django.urls import path, include
from rest_framework import routers

from .views import ImapItemViewSet

router = routers.DefaultRouter()
router.register(r'', ImapItemViewSet)

urlpatterns = [
  path('', include(router.urls)),
]
