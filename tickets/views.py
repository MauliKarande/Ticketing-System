from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Ticket
from .forms import TicketCreateForm



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
