from typing import Any
from django import forms
from django.contrib.auth import get_user_model


class RegistrationForm(forms.ModelForm):
    
       password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password', 'style': 'width:95%;'}))
       
       password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'conform password', 'style': 'width:95%;'}))
       
       
       class Meta:
              model = get_user_model()
              fields = ['first_name', 'last_name', 'username', 'email']
              widgets = {
              'first_name':forms.TextInput(attrs={'placeholder':'First name', 'style': 'width:95%;'}),
              'last_name':forms.TextInput(attrs={'placeholder':'Last name', 'style': 'width:95%;'}),
              'username':forms.TextInput(attrs={'placeholder':'Username', 'style': 'width:95%;'}),
                 'email': forms.EmailInput(attrs={'placeholder': 'Email', 'style': 'width:95%;'}),
              }

       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              for field in self.fields.values():
                     field.label = " "
                     field.label_suffix = " "
       
       def clean_password2(self):
              password1 = self.cleaned_data.get("password1")
              password2 = self.cleaned_data.get("password2")
              if password1 and password2 and password1 != password2:
                     raise forms.ValidationError("Passwords don't match")
              return password2
       
       def clean_username(self):
              username = self.cleaned_data.get('username')
              if CustomUser.objects.filter(username=username).exists():
                     raise forms.ValidationError("Username is already taken")
              return username
       
       def clean_email(self):
              email = self.cleaned_data.get('email')
              if CustomUser.objects.filter(email=email).exists():
                     raise forms.ValidationError("Email is already taken")
              return email
       
       
       def save(self, commit=True):
              user= super().save(commit=False)
              user.set_password(self.cleaned_data['password1'])
              if commit:
                    user.save()
              return user
       

class LoginForm(forms.Form):

       username = forms.CharField(
              widget=forms.TextInput(attrs={'placeholder':'Username', 'class':'form-control'}),
              label='')
       
       password = forms.CharField(
              widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control'}),
              label='')
       
       remember_me = forms.BooleanField(
              required=False,
              widget=forms.CheckboxInput(attrs={'class':'form-control-checkbox'}),
              label="Remember me"
       )



       