"""
from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from backend.models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput
                               )
    password2 = forms.CharField(label='Password confirmation',
                               widget=forms.PasswordInput
                               )
    is_admin = forms.BooleanField(label="is_admin",
                                 widget=forms.CheckboxInput)
    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self,commit=True):
        user = super(UserCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('password','is_active','is_admin')

    def clean_password(self):
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_user_password_template = None

    list_display = ('email','is_admin','is_active','last_login')
    list_filter = ('is_admin',)
    fieldsets = (
        (('基础信息'),{'fields':("email",'password')}),
        (('用户权限'),{'fields':('is_admin','is_active',)}),
    )
    add_fieldsets = (
        (("用户信息"),{
            "classes":('wide',),
            "fields":('email','password1','password2')
        }),
        (("用户权限"),{
            "fields":("is_admin","is_active")
        })
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
# Register your models here.
admin.site.register(User,UserAdmin)
admin.site.unregister(Group)
"""
