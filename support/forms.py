from django import forms
from .models import Ticket, StaffProfile,Company,ClientProfile,Category,Status,Priority,Reply

class TicketForm( forms.ModelForm ):
    class Meta:
        model = Ticket
        fields = ['subject','priority','category','message']

class StaffProfileForm( forms.ModelForm ):
    class Meta:
        model = StaffProfile
        fields = ['surname','other_name','telephone']
class ClientProfileForm( forms.ModelForm ):
    class Meta:
        model = ClientProfile
        fields = ['surname','other_name','telephone','company']
class CompanyForm( forms.ModelForm ):
    class Meta:
        model = Company 
        fields = '__all__'
class StatusForm( forms.ModelForm ):
    class Meta:
        model = Status 
        fields = '__all__'
class CategoryForm( forms.ModelForm ):
    class Meta:
        model = Category 
        fields = '__all__'
class PriorityForm( forms.ModelForm ):
    class Meta:
        model = Priority 
        fields = '__all__'
class TicketStatusForm( forms.ModelForm ):
    class Meta:
        model = Ticket 
        fields = ['status']
        labels = {'status':'Change Status To:'}
class TicketCategoryForm( forms.ModelForm ):
    class Meta:
        model = Ticket 
        fields = ['category']
        labels = {'category':'Move To Category:'}
class TicketPriorityForm( forms.ModelForm ):
    class Meta:
        model = Ticket 
        fields = ['priority']
        labels = {'priority':'Change Priority To:'}
class TicketOwnerForm( forms.ModelForm ):
    class Meta:
        model = Ticket 
        fields = ['owner']
        labels = {'owner':'Assign To:'}

class ReplyForm( forms.ModelForm ):
    class Meta:
        model = Reply 
        fields = ['message']
        labels = {'message':'Add A Reply'}