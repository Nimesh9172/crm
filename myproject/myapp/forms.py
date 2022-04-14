from enum import unique
from django import forms
from .models import Customer
from django.contrib.auth.forms import UserCreationForm
from .models import User,ListUpload

class CustomerForm(forms.ModelForm):
    name = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    phone = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    productid = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    price = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    city = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    remarks = forms.CharField(max_length=200,widget=forms.Textarea(attrs={'class':'form-control','rows':'1'}))
    
    class Meta:
        model = Customer
        fields = '__all__'

class CreateUserform(UserCreationForm):
    username = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=200,widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2','is_user','is_admin']

class ListUploadForm(forms.ModelForm):
    listid = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    listname = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    files = forms.FileField(max_length=200,widget=forms.FileInput(attrs={'class':'form-control'}))

    class Meta:
        model = ListUpload
        fields = '__all__'