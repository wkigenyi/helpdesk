from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import TicketForm,StaffProfileForm
from django.contrib.auth.decorators import login_required
from .models import Status,Ticket,StaffProfile,ClientProfile
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from users.models import CustomUser


# Create your views here.
def index(request):
    try: 
        profile = StaffProfile.objects.get(user=request.user)
    except:
        profile = None
    finally:
        context = {'profile':profile}    
    return render(request,'support/index.html',context)
@login_required    
def client_create_ticket(request):
    """
    If the client creating the ticket 
    """
    if request.method != 'POST':
        #Client is creating a new ticket
        form = TicketForm()
    else:
        status = Status.objects.get(id=1)
        ip = get_ip_address(request)
        client = request.user
        owner = request.user
        assigned = request.user
        form = TicketForm( request.POST )
        if form.is_valid:
            new_ticket = form.save(commit=False)
            new_ticket.ip = ip
            new_ticket.status = status
            new_ticket.client = client
            new_ticket.owner = owner
            new_ticket.assigned_by = assigned
            new_ticket.save()
            send_ticket_created_email(new_ticket)
            send_ticket_recieved_email(new_ticket)
            return HttpResponseRedirect(reverse('support:my_tickets'))

        pass
    context = {'form':form,'profile':get_user_profile(request)}
    return render(request,'support/create_ticket.html',context)

@login_required    
def create_staff_profile(request):
    """
    Creating / Editing a user profile 
    """
    #If the use has a profile, we edit that one
    try:
        userprofile = StaffProfile.objects.get(user = request.user)
    
        #Profile Exists, so we edit
        
        if request.method != 'POST':
        #Client is creating a new Profile
            form = StaffProfileForm(instance=userprofile)
        else:
            user = request.user
            form = StaffProfileForm(instance=userprofile,data= request.POST )
            if form.is_valid:
                form.save()
                return HttpResponseRedirect(reverse('support:tickets'))
    except:
        #Dealing with a new profile
        if request.method != 'POST':
        #Client is creating a new Profile
            form = StaffProfileForm()
        else:
            user = request.user
            form = StaffProfileForm( request.POST )
            if form.is_valid:
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
                return HttpResponseRedirect(reverse('support:tickets'))   
    context = {'form':form,'profile':userprofile}
    return render(request,'users/create_profile.html',context)

def tickets(request):
    tickets = Ticket.objects.all()
    context = { 'tickets':tickets,'profile':get_user_profile(request) }
    return render(request,'support/tickets.html',context)

def my_tickets(request):
    tickets = Ticket.objects.filter(client=request.user)
    context = { 'tickets':tickets,'profile':get_user_profile(request) }
    return render(request,'support/tickets.html',context)





def get_ip_address(request):
    x_forwarded_for = request.META.get('X_FORWADED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def send_ticket_created_email(ticket):
    subject = 'Your ticket has been received'
    message = 'ticket details'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [ticket.client.email]
    send_mail(subject,message,email_from,recipient_list,fail_silently=True)
def send_ticket_recieved_email(ticket):
    subject = 'A Ticket has been recieved'
    message = 'Ticket ID:'+str(ticket.track_id)
    email_from = settings.EMAIL_HOST_USER
    admin = CustomUser.objects.get(id=1)
    recipient_list = [admin.email]
    send_mail(subject,message,email_from,recipient_list,fail_silently=True)

def get_user_profile( request ):
    profile = None
    try: 
        profile = StaffProfile.objects.get(user = request.user)
    except DoesNotExist:
        profile = ClientProfile.objects.get(user = request.user)
    except DoesNotExist:
        profile = None
    finally:
        return profile
