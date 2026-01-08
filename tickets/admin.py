from django.contrib import admin
from .models import Ticket, TicketComment


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'issue_type',
        'status',
        'approval_status',
        'raised_by',
        'department',
        'created_at',
    )
    list_filter = ('status', 'approval_status', 'issue_type', 'department')
    search_fields = ('title', 'description')


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'commented_by', 'created_at')
