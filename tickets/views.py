from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Ticket
from .forms import TicketCreateForm

from django.contrib.auth import authenticate, login, logout



@login_required
def admin_accept_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Only Admin can accept
    if request.user.role != 'ADMIN':
        return redirect('admin_dashboard')

    ticket.status = 'IN_PROGRESS'
    ticket.assigned_to = request.user
    ticket.accepted_at = timezone.now()
    ticket.admin_comment = "Accepted by admin"
    ticket.save()

    return redirect('admin_dashboard')


@login_required
def admin_reject_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.user.role != 'ADMIN':
        return redirect('admin_dashboard')

    if request.method == 'POST':
        reason = request.POST.get('rejection_reason')

        if reason:
            ticket.status = 'REJECTED'
            ticket.rejection_reason = reason
            ticket.save()

    return redirect('admin_dashboard')


#temporary

from django.shortcuts import render


@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return redirect('/')

    tickets = Ticket.objects.filter(status='NEW')

    return render(request, 'admin_dashboard.html', {
        'tickets': tickets
    })


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
            return redirect('/tickets/admin/dashboard/')
    else:
        form = TicketCreateForm()

    return render(request, 'raise_ticket.html', {'form': form})


@login_required
def ticket_details(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Only Admin can view full ticket details for now
    if request.user.role != 'ADMIN':
        return redirect('/')

    return render(request, 'ticket_details.html', {
        'ticket': ticket
    })
@login_required
def approve_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Only HOD or Manager can approve
    if request.user.role not in ['HOD', 'MANAGER']:
        return redirect('/')

    # Approval only if pending
    if ticket.approval_status != 'PENDING_HOD':
        return redirect('/')

    ticket.approval_status = 'APPROVED'
    ticket.approved_by = request.user
    ticket.save()

    return redirect(f'/tickets/details/{ticket.id}/')


@login_required
def reject_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Only HOD or Manager can reject
    if request.user.role not in ['HOD', 'MANAGER']:
        return redirect('/')

    if ticket.approval_status != 'PENDING_HOD':
        return redirect('/')

    if request.method == 'POST':
        ticket.approval_status = 'REJECTED'
        ticket.approved_by = request.user
        ticket.save()

    return redirect(f'/tickets/details/{ticket.id}/')

@login_required
def employee_dashboard(request):
    if request.user.role != 'EMPLOYEE':
        return redirect('/')

    tickets = Ticket.objects.filter(raised_by=request.user).order_by('-created_at')

    return render(request, 'employee_dashboard.html', {
        'tickets': tickets
    })

@login_required
def hod_dashboard(request):
    if request.user.role != 'HOD':
        return redirect('/')

    tickets = Ticket.objects.filter(
        department=request.user.department
    ).order_by('-created_at')

    return render(request, 'hod_dashboard.html', {
        'tickets': tickets
    })

@login_required
def manager_dashboard(request):
    if request.user.role != 'MANAGER':
        return redirect('/')

    tickets = Ticket.objects.all().order_by('-created_at')

    return render(request, 'manager_dashboard.html', {
        'tickets': tickets
    })





def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')

    
@login_required
def logout_view(request):
    logout(request)
    return redirect('/login/')


