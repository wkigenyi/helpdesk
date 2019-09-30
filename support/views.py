from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import TicketForm,StaffProfileForm,CompanyForm,ClientProfileForm,CategoryForm
from .forms import StatusForm,PriorityForm,TicketStatusForm,TicketCategoryForm,TicketOwnerForm
from .forms import TicketPriorityForm,ReplyForm
from django.contrib.auth.decorators import login_required
from .models import Status,Ticket,StaffProfile,ClientProfile,Company,Category, Priority,Status,Reply
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from users.models import CustomUser
from helpdesk.helpers import get_user_profile


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
def change_ticket_status(request,id):
    #method will always be post
    ticket = Ticket.objects.get(id=id)
    form = TicketStatusForm(instance=ticket,data=request.POST)
    if form.is_valid:
        form.save()
        return HttpResponseRedirect(reverse('support:view_ticket',args=[id]))
@login_required
def change_ticket(request,id):
    #method will always be post
    ticket = Ticket.objects.get(id=id)
    form = TicketCategoryForm(instance=ticket,data=request.POST)
    if form.is_valid:
        form.save()
        return HttpResponseRedirect(reverse('support:view_ticket',args=[id]))
@login_required
def change_ticket_priority(request,id):
    #method will always be post
    ticket = Ticket.objects.get(id=id)
    form = TicketPriorityForm(instance=ticket,data=request.POST)
    if form.is_valid:
        form.save()
        return HttpResponseRedirect(reverse('support:view_ticket',args=[id]))
@login_required
def change_ticket_owner(request,id):
    #method will always be post
    ticket = Ticket.objects.get(id=id)
    form = TicketOwnerForm(instance=ticket,data=request.POST)
    if form.is_valid:
        form.save()
        return HttpResponseRedirect(reverse('support:view_ticket',args=[id]))
@login_required
def add_ticket_reply(request,id):
    #method will always be post
    ticket = Ticket.objects.get(id=id)
    form = ReplyForm(data=request.POST)
    if form.is_valid:
        reply=form.save(commit=False)
        reply.ticket = ticket
        reply.replier = request.user
        reply.save()
        return HttpResponseRedirect(reverse('support:view_ticket',args=[id]))
@login_required
def change_ticket_category(request,id):
    #method will always be post
    ticket = Ticket.objects.get(id=id)
    form = TicketCategoryForm(instance=ticket,data=request.POST)
    if form.is_valid:
        form.save()
        return HttpResponseRedirect(reverse('support:view_ticket',args=[id]))


@login_required    
def create_staff_profile(request):
    """
    Creating / Editing a user profile 
    """
    #If the use has a profile, we edit that one
    profile = get_user_profile(request.user)
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
                userprofile = form.save(commit=False)
                userprofile.user = user
                userprofile.save()
                return HttpResponseRedirect(reverse('support:tickets'))   
    context = {'form':form,'profile':profile}
    return render(request,'users/create_profile.html',context)

@login_required    
def create_client_profile(request,id):
    """
    Creating / Editing a user profile 
    """
    user = CustomUser.objects.get(id = id)
    userprofile = None
    #If the use has a profile, we edit that one
    try:
        userprofile = ClientProfile.objects.get(user = user)
    
        #Profile Exists, so we edit
        
        if request.method != 'POST':
        #Client is creating a new Profile
            form = ClientProfileForm(instance=userprofile)
        else:
            
            form = ClientProfileForm(instance=userprofile,data= request.POST )
            if form.is_valid:
                form.save()
                return HttpResponseRedirect(reverse('support:tickets'))
    except:
        #Dealing with a new profile
        if request.method != 'POST':
        #Client is creating a new Profile
            form = ClientProfileForm()
        else:
            
            form = ClientProfileForm( request.POST )
            if form.is_valid:
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
                return HttpResponseRedirect(reverse('users:users'))   
    context = {'form':form,'profile':userprofile,'someone':user}
    return render(request,'users/create_client_profile.html',context)

@login_required
def tickets(request):
    tickets = Ticket.objects.all()
    context = { 'tickets':tickets,'profile':get_user_profile(request.user) }
    return render(request,'support/tickets.html',context)
@login_required
def view_ticket(request,id):
    ticket = Ticket.objects.get(id=id)
    profile = get_user_profile(request.user)
    clientprofile = get_user_profile(ticket.client)
    replyform = ReplyForm()
    replies = []
    statusform = TicketStatusForm(instance=ticket)
    categoryform = TicketCategoryForm(instance=ticket)
    ownerform = TicketOwnerForm(instance=ticket)
    priorityform = TicketPriorityForm(instance=ticket)

    try:
        reply = Reply.objects.filter(ticket=id)
        replies.extend(reply)
    except Reply.DoesNotExist:
        pass
            
    context = {
        'ticket':ticket,
        'profile':profile,
        'replies':replies,
        'userprofile':clientprofile,
        'statusform':statusform,
        'categoryform':categoryform,
        'ownerform':ownerform,
        'priorityform':priorityform,
        'replyform':replyform
        }
    return render(request,'support/view_ticket.html',context)

@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(client=request.user)
    context = { 'tickets':tickets,'profile':get_user_profile(request.user) }
    return render(request,'support/tickets.html',context)
@login_required
def category(request):
    categories = Category.objects.all()
    context = { 'categories':categories,'profile':get_user_profile(request.user) }
    return render(request,'support/category.html',context)
@login_required    
def new_category(request):
    """
    If the client creating the ticket 
    """
    if request.method != 'POST':
        #Client is creating a new ticket
        form = CategoryForm()
    else:
        
        form = CategoryForm( request.POST )
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('support:category'))

        pass
    context = {'form':form,'profile':get_user_profile(request)}
    return render(request,'support/new_category.html',context)

@login_required    
def edit_category(request,id):
    """
    If the client is editing a category 
    """
    category = Category.objects.get(id=id)

    if request.method != 'POST':
        #Client is creating a new ticket
        form = CategoryForm(instance=category)
    else:
        
        form = CategoryForm(instance=category, data=request.POST )
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('support:category'))

        pass
    context = {'form':form,'profile':get_user_profile(request),'category':category}
    return render(request,'support/edit_category.html',context)

@login_required    
def edit_status(request,id):
    """
    If the client is editing a Status 
    """
    status = Status.objects.get(id=id)

    if request.method != 'POST':
        #Client is creating a new ticket
        form = StatusForm(instance=status)
    else:
        
        form = StatusForm(instance=status, data=request.POST )
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('support:status'))

        pass
    context = {'form':form,'profile':get_user_profile(request.user),'status':status}
    return render(request,'support/edit_status.html',context)
@login_required    
def edit_priority(request,id):
    """
    If the client is editing a priority 
    """
    priority = Priority.objects.get(id=id)

    if request.method != 'POST':
        #Client is creating a new ticket
        form = PriorityForm(instance=priority)
    else:
        
        form = PriorityForm(instance=priority, data=request.POST )
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('support:priority'))

        pass
    context = {'form':form,'profile':get_user_profile(request.user),'priority':priority}
    return render(request,'support/edit_priority.html',context)



@login_required
def status(request):
    statuses = Status.objects.all()
    context = { 'statuses':statuses,'profile':get_user_profile(request.user) }
    return render(request,'support/status.html',context)
@login_required    
def new_status(request):
    """
    If the client creating the ticket 
    """
    if request.method != 'POST':
        #Client is creating a new ticket
        form = StatusForm()
    else:
        
        form = StatusForm( request.POST )
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('support:status'))

        pass
    context = {'form':form,'profile':get_user_profile(request.user)}
    return render(request,'support/new_status.html',context)


@login_required
def priority(request):
    priorities = Priority.objects.all()
    context = { 'priorities':priorities,'profile':get_user_profile(request.user) }
    return render(request,'support/priority.html',context)
@login_required    
def new_priority(request):
    """
    If the client creating the ticket 
    """
    if request.method != 'POST':
        #Client is creating a new ticket
        form = PriorityForm()
    else:
        
        form = PriorityForm( request.POST )
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('support:priority'))

        pass
    context = {'form':form,'profile':get_user_profile(request.user)}
    return render(request,'support/new_priority.html',context)


@login_required
def client_companies(request):
    companies = Company.objects.all()
    context = { 'companies':companies }
    return render(request,'support/companies.html',context)

@login_required
def new_company(request):
    """
    For the user to create a new company 
    """
    if request.method != 'POST':
        #Client is creating a new company
        form = CompanyForm()
    else:

        form = CompanyForm( request.POST ) 
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('support:client_companies'))
    context = {'form':form }
    return render(request,'support/create-company.html',context)



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

