from django import forms
from .models import Ticket


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'issue_type', 'description', 'attachment']
