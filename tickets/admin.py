from django.contrib import admin
from .models import Ticket, TicketComment


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'status',
        'approval_status',
        'department',
        'raised_by',
        'created_at',
    )
    list_filter = ('status', 'approval_status', 'department')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = (
        'ticket',
        'commented_by',
        'created_at',
    )
    search_fields = ('comment',)
    ordering = ('-created_at',)
