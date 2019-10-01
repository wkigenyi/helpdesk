from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect
from .forms import UserForm
from .models import CustomUser
from support.forms import ClientProfileForm
from django.contrib.auth import authenticate,login
from helpdesk.helpers import get_user_profile

# Create your views here.
def my_tickets( request ):
    if( request.user.is_admin ):
        return HttpResponseRedirect(reverse('support:tickets'))
    else:
        return HttpResponseRedirect(reverse('support:my_tickets'))
def register( request ):
    """
    Create a new user
    """
    if request.method != 'POST':
        form = UserForm()
    else:
        form = UserForm( data=request.POST )
        if form.is_valid:
            try:
                new_user = form.save()
                user = authenticate( username=new_user.email,password= request.POST['password1'] )
                login( request,user)
                return HttpResponseRedirect(reverse('support:my_tickets'))
            except ValueError:
                return HttpResponseRedirect(reverse('support:index'))
    context ={'form':form}        
    return render( request,'users/register.html',context )
def users (request):
    users = CustomUser.objects.all()
    profile = get_user_profile( request.user )
    context = { 'users':users, 'profile':profile }
    
    return render( request,'users/users.html',context)

def user_profile(request,id):
    someone = CustomUser.objects.get(id=id )
    userprofile = get_user_profile( someone )
    profile = get_user_profile( request.user )
    #We shall either create or edit a profile
    #We shall only create profiles clients, staff will create their profiles
    if userprofile:
        if request.method != 'POST':
        #Client is creating a new Profile
            form = ClientProfileForm(instance=userprofile)
        else:
            
            form = ClientProfileForm(instance=userprofile,data= request.POST )
            if form.is_valid:
                form.save()
                return HttpResponseRedirect(reverse('users:users'))
    else:
        #Dealing with a new profile
        if request.method != 'POST':
        #Client is creating a new Profile
            form = ClientProfileForm()
        else:
            
            form = ClientProfileForm( request.POST )
            if form.is_valid:
                userprofile = form.save(commit=False)
                userprofile.user = user
                userprofile.save()
                return HttpResponseRedirect(reverse('users:users'))
           
    context = {'form':form,'userprofile':userprofile,'someone':someone,'profile':profile}
    return render(request,'users/create_client_profile.html',context)

    

    
        
