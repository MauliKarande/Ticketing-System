from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Ticket(models.Model):

    ISSUE_TYPE_CHOICES = (
        ('SOFTWARE', 'Software Issue'),
        ('HARDWARE', 'Hardware Issue'),
        ('NETWORK', 'Network Issue'),
        ('OTHER', 'Other'),
    )

    STATUS_CHOICES = (
        ('NEW', 'Pending Admin Acceptance'),
        ('REJECTED', 'Rejected by Admin'),
        ('IN_PROGRESS', 'Admin In Progress'),
        ('ADMIN_CLOSED', 'Closed by Admin'),
        ('FINAL_CLOSED', 'Final Closed'),
    )

    APPROVAL_STATUS_CHOICES = (
        ('NOT_REQUIRED', 'Not Required'),
        ('PENDING_HOD', 'Pending HOD Approval'),
        ('PENDING_MANAGER', 'Pending Manager Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    title = models.CharField(max_length=150)
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPE_CHOICES)
    description = models.TextField()

    attachment = models.ImageField(
        upload_to='ticket_attachments/',
        null=True,
        blank=True
    )

    raised_by = models.ForeignKey(
        User,
        related_name='tickets_raised',
        on_delete=models.CASCADE
    )

    department = models.ForeignKey(
        'accounts.Department',
        on_delete=models.SET_NULL,
        null=True
    )

    assigned_to = models.ForeignKey(
        User,
        related_name='tickets_assigned',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NEW'
    )

    approval_status = models.CharField(
        max_length=30,
        choices=APPROVAL_STATUS_CHOICES,
        default='NOT_REQUIRED'
    )

    approved_by = models.ForeignKey(
        User,
        related_name='tickets_approved',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    admin_comment = models.TextField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)
    resolution_summary = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    admin_closed_at = models.DateTimeField(null=True, blank=True)
    final_closed_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.title}"
    

    #ticket comment 
class TicketComment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        related_name='comments',
        on_delete=models.CASCADE
    )
    commented_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on Ticket #{self.ticket.id}"



class TicketComment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        related_name='comments',
        on_delete=models.CASCADE
    )
    commented_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on Ticket #{self.ticket.id}"
