from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'memberships', views.MembershipViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
