from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/',views.RegistrationView.as_view(),name='signup'),
    path('login/', views.LoginView.as_view() ,name='login'),
    path('profile/<int:pk>', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/', views.UserProfileEdit.as_view(), name='profile_edit'),
    path('logout/', views.LogoutUserView.as_view(), name='logout')
    
]
