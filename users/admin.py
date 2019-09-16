from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField 
from .models import CustomUser
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

class UserCreationForm( forms.Form ):
    password1 = forms.CharField(label='Password',widget = forms.PasswordInput())
    password2 = forms.CharField(label='Password Confirmation',widget = forms.PasswordInput())
    class Meta:
        model=CustomUser
        fields = ('email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.FormValidationError('Passwords Don\'t Match')
        return password2
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm( forms.Form ):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = CustomUser
        fields = ('email','password','is_admin','is_staff')
    def clean_password(self):
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ( 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(CustomUser)


