from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('',views.PostListView.as_view(),name='home'),
    path('category/<int:pk>', views.CategoryListView.as_view(), name='category'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_details'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('dashboard/', views.DashbordView.as_view(), name='dashboard'),
    path('dashboard/post/write/', views.PostCreateView.as_view(), name='write'),
    path('dashboard/post/<int:pk>/delete', views.PostDelete.as_view(),name='post_delete'),
    path('dashboard/post/drafts/', views.DraftListView.as_view(), name='post_draft'),
    path('dashboard/post/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('dashboard/published/', views.PostPublishedListView.as_view(), name='published'),
    path('dashboard/responses', views.responses, name='responses'),
   
]
