from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

from tickets.views import login_view, logout_view



def home(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.user.role == 'ADMIN':
        return redirect('/tickets/admin/dashboard/')
    elif request.user.role == 'EMPLOYEE':
        return redirect('/tickets/employee/dashboard/')
    elif request.user.role == 'HOD':
        return redirect('/tickets/hod/dashboard/')
    elif request.user.role == 'MANAGER':
        return redirect('/tickets/manager/dashboard/')

    return redirect('/login/')



urlpatterns = [
    path('', home),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('tickets/', include('tickets.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
