from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User
from .forms import AdminUserCreateForm, AdminUserRoleForm, AdminPasswordResetForm


def _is_admin(request):
    return request.user.is_authenticated and request.user.role == 'ADMIN'


@login_required
def user_management(request):
    if not _is_admin(request):
        return redirect('/')

    users = User.objects.all().order_by('username')

    return render(request, 'user_management.html', {
        'users': users,
    })


@login_required
def user_create(request):
    if not _is_admin(request):
        return redirect('/')

    if request.method == 'POST':
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            return redirect('user_management')
    else:
        form = AdminUserCreateForm()

    return render(request, 'user_create.html', {
        'form': form,
    })


@login_required
def user_detail(request, user_id):
    if not _is_admin(request):
        return redirect('/')

    user_obj = get_object_or_404(User, id=user_id)
    role_form = AdminUserRoleForm(instance=user_obj)
    password_form = AdminPasswordResetForm()

    return render(request, 'user_detail.html', {
        'user_obj': user_obj,
        'role_form': role_form,
        'password_form': password_form,
    })


@login_required
def user_update_role(request, user_id):
    if not _is_admin(request):
        return redirect('/')

    user_obj = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = AdminUserRoleForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'{user_obj.username} updated successfully.')
        else:
            messages.error(request, 'Could not update user. Please check the form.')

    return redirect('user_detail', user_id=user_obj.id)


@login_required
def user_reset_password(request, user_id):
    if not _is_admin(request):
        return redirect('/')

    user_obj = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = AdminPasswordResetForm(request.POST)
        if form.is_valid():
            user_obj.set_password(form.cleaned_data['new_password'])
            user_obj.save()
            messages.success(request, f'Password reset for {user_obj.username}.')
        else:
            messages.error(request, 'Could not reset password. Please check the form.')

    return redirect('user_detail', user_id=user_obj.id)
