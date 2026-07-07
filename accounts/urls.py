from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_management, name='user_management'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/update-role/', views.user_update_role, name='user_update_role'),
    path('users/<int:user_id>/reset-password/', views.user_reset_password, name='user_reset_password'),
]
