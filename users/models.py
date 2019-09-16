from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


# Create your models here.
class CustomUserManager( BaseUserManager ):
    def create_user( self,email,password=None ):
        """
        Creates and saves user with the provided email address 
        """
        if not email:
            raise ValueError(  'A proper email address is required' )
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser( self,email,password ):
        """
        Creates a superuser with a provide username and password
        """
        user = self.create_user(email,password)
        user.is_admin = True
        user.save( using = self._db )
        return user

class CustomUser( AbstractBaseUser ):
    email = models.EmailField(unique=True,max_length=255,verbose_name='Email Address')
    is_active = models.BooleanField(default = True )
    is_staff = models.BooleanField( default = False )
    is_admin = models.BooleanField( default = False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email' #Users will login with emails
    REQUIRED_FIELDS = []    #Email is required since it is the username field, and pass is always required

    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff( self ):
        return self.is_admin

    



