from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('tickets',views.tickets,name='tickets'),
    path('view_ticket/<int:id>',views.view_ticket,name='view_ticket'),
    path('change_ticket_status/<int:id>',views.change_ticket_status,name='change_ticket_status'),
    path('change_ticket_category/<int:id>',views.change_ticket_category,name='change_ticket_category'),
    path('change_ticket_priority/<int:id>',views.change_ticket_priority,name='change_ticket_priority'),
    path('change_ticket_owner/<int:id>',views.change_ticket_owner,name='change_ticket_owner'),
    path('add_ticket_reply/<int:id>',views.add_ticket_reply,name='add_ticket_reply'),
    path('category',views.category,name='category'),
    path('priority',views.priority,name='priority'),
    path('status',views.status,name='status'),
    path('new_category',views.new_category,name='new_category'),
    path('new_priority',views.new_priority,name='new_priority'),
    path('new_status',views.new_status,name='new_status'),
    path('edit_category/<int:id>',views.edit_category,name='edit_category'),
    path('edit_priority/<int:id>',views.edit_priority,name='edit_priority'),
    path('edit_status/<int:id>',views.edit_status,name='edit_status'),
    path('new_ticket',views.client_create_ticket,name='new_ticket'),
    path('new_company',views.new_company,name='new_company'),
    path('my_tickets',views.my_tickets,name='my_tickets'),
    path('create_staffprofile',views.create_staff_profile,name='create_staffprofile'),
    path('new_profile/',views.create_client_profile,name='new_profile2'),
    path('new_profile/<int:id>/',views.create_client_profile,name='new_profile'),
    path('client_companies',views.client_companies,name='client_companies'),
    
]