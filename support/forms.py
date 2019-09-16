from django import forms
from .models import Ticket, StaffProfile

class TicketForm( forms.ModelForm ):
    class Meta:
        model = Ticket
        fields = ['subject','priority','category','message']

class StaffProfileForm( forms.ModelForm ):
    class Meta:
        model = StaffProfile
        fields = ['surname','othername','telephone']