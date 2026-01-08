from django.urls import path
from . import views

urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/accept/<int:ticket_id>/', views.admin_accept_ticket, name='admin_accept_ticket'),
    path('admin/reject/<int:ticket_id>/', views.admin_reject_ticket, name='admin_reject_ticket'),
    path('raise/', views.raise_ticket, name='raise_ticket'),
]
