from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    if not request.user.is_authenticated:
        return redirect('/admin/login/')

    if request.user.role == 'ADMIN':
        return redirect('/tickets/admin/dashboard/')
    elif request.user.role == 'EMPLOYEE':
        return redirect('/tickets/employee/dashboard/')
    elif request.user.role == 'HOD':
        return redirect('/tickets/hod/dashboard/')
    elif request.user.role == 'MANAGER':
        return redirect('/tickets/manager/dashboard/')

    return redirect('/admin/login/')


urlpatterns = [
    path('', home),   # 👈 THIS FIXES 404
    path('admin/', admin.site.urls),
    path('tickets/', include('tickets.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
