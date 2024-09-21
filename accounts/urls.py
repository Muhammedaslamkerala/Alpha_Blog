from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
#     path('signup/',views.RegistrationView.as_view(),name='signup'),
#    
    path('profile/<int:pk>', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/', views.UserProfileEdit.as_view(), name='profile_edit'),
    path('login/', views.CustomLoginView.as_view() ,name='login'),
    # change password urls
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

    # reset password urls
    path('password-reset/',views.CustomPasswordResetView.as_view(),name='password_reset'),
    path('password-reset/done',views.CustomPasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-rest/<uidb64>/<token>/',views.CustomPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-rest/complete/',views.CustomPasswordResetCompleteView.as_view(),name='password_reset_complete'),

    
]
