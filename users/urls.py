from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/',views.UserRegistration.as_view(),name='signup'),
    path('login/', views.UserLoginView.as_view() ,name='login'),
    path('profile/<int:id>', views.UserProfileView.as_view(), name='profile'),
    path('logout/', views.LogoutUserView.as_view(), name='logout')
    
]
