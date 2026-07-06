from django import forms
from .models import Ticket, TicketStage


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'title',
            'issue_type',
            'description',
            'attachment',
        ]


class TicketStageForm(forms.ModelForm):
    class Meta:
        model = TicketStage
        fields = [
            'title',
            'description',
        ]
