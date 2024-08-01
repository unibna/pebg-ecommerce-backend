from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    
    path('activate/', views.UserActivateAPIView.as_view(), name='activate-account'),
    path('users/<int:user_id>/roles/', views.UserRoleViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update', 
        'delete': 'destroy'
    }), name='user-roles'),
]
