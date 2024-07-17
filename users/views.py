from pyexpat.errors import messages
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from .forms import RegistrationForm, LoginForm, ProfileEditForm
from django.contrib.auth import  login, logout
from django.urls import reverse_lazy , reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib import sessions
# Create your views here.

class RegistrationView(FormView):
     template_name = 'users/registraion.html'
     form_class = RegistrationForm
     success_url = reverse_lazy('users:login')

     def form_valid(self, form):
         form.save()
         return super().form_valid(form)
class LoginView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("blog:home")
    
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)
    
    
class LogoutUserView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse_lazy('blog:home'))
        
                
class UserProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'users/profile.html'
    context_object_name = 'user'
    
    def get_object(self, queryset= None):
        return get_object_or_404(self.model, id=self.request.user.id)
    
class UserProfileEdit(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileEditForm
    template_name = 'users/edit_profile.html'
    success_url = 'users:profile'

    def get_object(self, queryset= None):
        return self.request.user
        
    
    def get_success_url(self):
        return reverse(self.success_url, kwargs={'pk':self.request.user.pk})
    
    def form_valid(self, form):
        if 'profile_picture-clear' in self.request.POST:
            # User wants to remove the profile picture
            self.object.profile_picture.delete(save=False)
            self.object.profile_picture = None
    
        return super().form_valid(form)
    