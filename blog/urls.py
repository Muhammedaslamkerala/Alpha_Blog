from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('',views.home,name='home'),
    path('search/', views.search, name='search'),
    path('post/', views.post_details, name='post_details'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/write/', views.write, name='write'),
    path('dashboard/drafts/', views.drafts, name='drafts'),
    path('dashboard/edit/', views.edit, name='edit'),
    path('dashboard/published/', views.published, name='published'),
    path('dashboard/responses', views.responses, name='responses'),
    path('search/',views.search,name='search')
   
]
