from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from .models import Ticket
from .forms import TicketCreateForm


# ================= ADMIN ACTIONS =================

@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return redirect('/')

    # Admin sees all active tickets (until FINAL_CLOSED)
    tickets = Ticket.objects.exclude(status='FINAL_CLOSED').order_by('-created_at')

    return render(request, 'admin_dashboard.html', {
        'tickets': tickets
    })


@login_required
def admin_accept_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.user.role != 'ADMIN':
        return redirect('/')

    ticket.status = 'IN_PROGRESS'
    ticket.assigned_to = request.user
    ticket.accepted_at = timezone.now()
    ticket.save()

    return redirect('admin_dashboard')


@login_required
def admin_reject_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.user.role != 'ADMIN':
        return redirect('/')

    if request.method == 'POST':
        ticket.status = 'REJECTED'
        ticket.rejection_reason = request.POST.get('rejection_reason')
        ticket.save()

    return redirect('admin_dashboard')


@login_required
def admin_close_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.user.role != 'ADMIN':
        return redirect('/')

    if request.method == 'POST':
        ticket.status = 'ADMIN_CLOSED'
        ticket.admin_comment = request.POST.get('admin_close_comment')
        ticket.admin_closed_at = timezone.now()
        ticket.save()

    return redirect(f'/tickets/details/{ticket.id}/')


# ================= TICKET CREATION =================

@login_required
def raise_ticket(request):
    if request.method == 'POST':
        form = TicketCreateForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.raised_by = request.user
            ticket.department = request.user.department
            ticket.status = 'NEW'

            if request.user.role == 'EMPLOYEE':
                ticket.approval_status = 'PENDING_HOD'
            else:
                ticket.approval_status = 'NOT_REQUIRED'

            ticket.save()
            return redirect('/')

    else:
        form = TicketCreateForm()

    return render(request, 'raise_ticket.html', {'form': form})


# ================= TICKET DETAILS =================

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.user.role == 'ADMIN':
        pass

    elif request.user.role == 'MANAGER':
        pass

    elif request.user.role == 'HOD':
        if ticket.department != request.user.department:
            return redirect('/')

    elif request.user.role == 'EMPLOYEE':
        if ticket.raised_by != request.user:
            return redirect('/')

    else:
        return redirect('/')

    return render(request, 'ticket_details.html', {
        'ticket': ticket
    })


# ================= HOD / MANAGER APPROVAL =================


@login_required
def approve_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.user.role not in ['HOD', 'MANAGER']:
        return redirect('/')

    if ticket.approval_status != 'PENDING_HOD':
        return redirect(f'/tickets/details/{ticket.id}/')

    ticket.approval_status = 'APPROVED'
    ticket.approved_by = request.user
    ticket.approved_at = timezone.now()   # ✅ THIS WAS MISSING
    ticket.save()

    return redirect(f'/tickets/details/{ticket.id}/')



@login_required
def reject_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.user.role not in ['HOD', 'MANAGER']:
        return redirect('/')

    if ticket.approval_status != 'PENDING_HOD':
        return redirect('/')

    if request.method == 'POST':
        ticket.approval_status = 'REJECTED'
        ticket.rejection_reason = request.POST.get('rejection_reason')
        ticket.approved_by = request.user
        ticket.save()

    return redirect(f'/tickets/details/{ticket.id}/')


# ================= FINAL CLOSE (HOD / MANAGER) =================

@login_required
def final_close_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.user.role not in ['HOD', 'MANAGER']:
        return redirect('/')

    if request.method == 'POST':
        ticket.status = 'FINAL_CLOSED'
        ticket.final_closed_by = request.user      # ✅ SAVE USER
        ticket.final_closed_at = timezone.now()    # ✅ SAVE TIME
        ticket.resolution_summary = request.POST.get('final_close_comment')
        ticket.save()

    return redirect(f'/tickets/details/{ticket.id}/')



# ================= DASHBOARDS =================

@login_required
def employee_dashboard(request):
    if request.user.role != 'EMPLOYEE':
        return redirect('/')

    tickets = Ticket.objects.filter(
        raised_by=request.user
    ).exclude(status='FINAL_CLOSED').order_by('-created_at')

    return render(request, 'employee_dashboard.html', {
        'tickets': tickets
    })


@login_required
def hod_dashboard(request):
    if request.user.role != 'HOD':
        return redirect('/')

    tickets = Ticket.objects.filter(
        department=request.user.department
    ).exclude(status='FINAL_CLOSED').order_by('-created_at')

    return render(request, 'hod_dashboard.html', {
        'tickets': tickets
    })


@login_required
def manager_dashboard(request):
    if request.user.role != 'MANAGER':
        return redirect('/')

    tickets = Ticket.objects.exclude(
        status='FINAL_CLOSED'
    ).order_by('-created_at')

    return render(request, 'manager_dashboard.html', {
        'tickets': tickets
    })


# ================= AUTH =================

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user:
            login(request, user)
            return redirect('/')

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def ticket_history(request):
    user = request.user

    if user.role == 'EMPLOYEE':
        tickets = Ticket.objects.filter(raised_by=user)

    elif user.role == 'HOD':
        tickets = Ticket.objects.filter(department=user.department)

    elif user.role in ['MANAGER', 'ADMIN']:
        tickets = Ticket.objects.all()

    else:
        tickets = Ticket.objects.none()

    return render(request, 'ticket_history.html', {
    'tickets': tickets
})

