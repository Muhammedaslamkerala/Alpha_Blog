from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings


class RegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name','email']

    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus':True}))
    def __init__(self, *args, **kwargs):
         super().__init__(*args,**kwargs)
         for field in self.fields.values():
              field.widget.attrs['class'] = 'form-control'
       

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'bio',]
        
    
    
          