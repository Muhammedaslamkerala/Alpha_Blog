from django.shortcuts import render, redirect ,get_object_or_404
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView,LogoutView
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib import sessions
# Create your views here.

class UserRegistration(CreateView):
     template_name = 'users/registraion.html'
     form_class = RegistrationForm
     success_url = reverse_lazy('users:login')
     
class UserLoginView(View):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("blog:home")
    
    def get(self,request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                if remember_me:
                   request.session.set_expiry(timezone.now() + timezone.timedelta(weeks=1))
                else:
                   request.session.set_expiry(0)
                return redirect(self.success_url)
        return render(request, 'users/login.html',{'form':form})
    
class LogoutUserView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse_lazy('blog:home'))
        
                
class UserProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        author = get_object_or_404(get_user_model(), id=user_id)
        return render(request, self.template_name, {'author': author})