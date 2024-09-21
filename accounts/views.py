from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, UpdateView
from django.contrib.auth import views as auth_views
from django.views.generic.edit import FormView
from .forms import RegistrationForm, LoginForm, ProfileEditForm
from django.contrib.auth import  login
from django.urls import reverse_lazy , reverse
from django.contrib.auth import get_user_model
# Create your views here.

class RegistrationView(FormView):
     template_name = 'accounts/registraion.html'
     form_class = RegistrationForm
     success_url = reverse_lazy('accounts:login')

     def form_valid(self, form):
         form.save()
         return super().form_valid(form)
     
class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("blog:home")
    
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)
    
class CustomPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'accounts/password_change_form_page.html'
    success_url = reverse_lazy('accounts:password_change_done')

class CustomPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'accounts/password_change_done_page.html'

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_rest_form_page.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_rest_done_page.html'

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_rest_complete_page.html'


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm_page.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
                
class UserProfileView(DetailView):
    model = get_user_model()
    template_name = 'accounts/user_profile_page.html'
    context_object_name = 'user'
    
    def get_object(self, queryset= None):
        return get_object_or_404(self.model, id=self.request.user.pk)
    
class UserProfileEdit(UpdateView):
    model = get_user_model()
    form_class = ProfileEditForm
    template_name = 'accounts/user_profile_edit_page.html'
    success_url = 'accounts:profile'

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
    
def pro(request):
    return render(request, 'accounts/registration.html')
