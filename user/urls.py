from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('activate/', views.UserActivateAPIView.as_view(), name='activate-account'),
    
    # User roles
    path('users/<int:user_id>/roles/', views.UserRoleViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='user-roles'),
    path('users/<int:user_id>/roles/<int:pk>/', views.UserRoleViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
    }), name='user-roles'),
    
    # User departments
    path('users/<int:user_id>/departments/', views.UserDepartmentViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='user-departments'),
    path('users/<int:user_id>/departments/<int:pk>/', views.UserDepartmentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
    }), name='user-departments'),
]
