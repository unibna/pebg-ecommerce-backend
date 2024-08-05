from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'users/roles', views.UserRoleViewSet)
router.register(r'users/departments', views.UserDepartmentViewSet)
router.register(r'users/memberships', views.UserMembershipViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    
    path('me/', views.MeAPIView.as_view(), name='me'),
    path('activate/', views.UserActivateAPIView.as_view(), name='activate-account'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
]
