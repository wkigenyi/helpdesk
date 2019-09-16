from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect
from .forms import UserForm
from django.contrib.auth import authenticate,login

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
            new_user = form.save()
            user = authenticate( username=new_user.email,password= request.POST['password1'] )
            login( request,user)
            return HttpResponseRedirect(reverse('support:tickets'))
    context ={'form':form}        
    return render( request,'users/register.html',context )