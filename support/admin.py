from django.contrib import admin
from .models import Priority,Category,Ticket,Status,StaffProfile

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Priority)
admin.site.register(Category)
admin.site.register(Status)
admin.site.register(StaffProfile)

