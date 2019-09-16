from django.db import models
from phone_field import PhoneField
from users.models import CustomUser
import uuid


# Create your models here.
class Category( models.Model ):
    category_name = models.CharField(max_length = 50)
    def __str__(self):
        return self.category_name
    
class Priority ( models.Model ):
    priority = models.CharField(max_length = 50)
    def __str__(self):
        return self.priority
class Status ( models.Model ):
    status = models.CharField(max_length = 50)
    def __str__(self):
        return self.status

class Ticket ( models.Model ):
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length = 500)
    track_id = models.UUIDField(unique=True,default=uuid.uuid4)
    dt = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    client = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='client')
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='owner')
    assigned_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='assigned_by')

class Reply ( models.Model ):
    ticket = models.ForeignKey( Ticket,on_delete=models.CASCADE )
    message = models.TextField( max_length=500 )
    replier = models.ForeignKey( CustomUser,on_delete=models.CASCADE )
    dt = models.DateTimeField( auto_now_add=True )
class Company ( models.Model ):
    full_name = models.CharField( max_length=200 )
    short_name = models.CharField( max_length=50 )

class StaffProfile (models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    surname = models.CharField(max_length=50)
    othername = models.CharField(max_length=50)
    telephone = PhoneField(help_text='Your Mobile Phone Number')
    def __str__(self):
        return self.surname+' '+self.othername
    

class ClientProfile (models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    surname = models.CharField(max_length=50)
    other_name = models.CharField(max_length=50)
    telephone = PhoneField()
    company = models.ForeignKey( Company,on_delete=models.CASCADE )
