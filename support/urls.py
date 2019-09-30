from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('tickets',views.tickets,name='tickets'),
    path('category',views.category,name='category'),
    path('priority',views.priority,name='priority'),
    path('status',views.status,name='status'),
    path('new_category',views.new_category,name='new_category'),
    path('new_priority',views.new_priority,name='new_priority'),
    path('new_status',views.new_status,name='new_status'),
    #path('edit_category',views.edit_category,name='edit_category'),
    #path('edit_priority',views.edit_priority,name='edit_priority'),
    #path('edit_status',views.edit_status,name='edit_status'),
    path('new_ticket',views.client_create_ticket,name='new_ticket'),
    path('new_company',views.new_company,name='new_company'),
    path('my_tickets',views.my_tickets,name='my_tickets'),
    path('create_staffprofile',views.create_staff_profile,name='create_staffprofile'),
    path('new_profile/',views.create_client_profile,name='new_profile2'),
    path('new_profile/<int:id>/',views.create_client_profile,name='new_profile'),
    path('client_companies',views.client_companies,name='client_companies'),
    
]