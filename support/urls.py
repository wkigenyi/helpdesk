from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('tickets',views.tickets,name='tickets'),
    path('new_ticket',views.client_create_ticket,name='new_ticket'),
    path('my_tickets',views.my_tickets,name='my_tickets'),
    path('create_staffprofile',views.create_staff_profile,name='create_staffprofile'),
    
]