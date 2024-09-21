from django.urls import path
from blog import views
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from .feeds import LatestPostsFeed

app_name = 'blog'

sitemaps = {
    'posts':PostSitemap,
}


urlpatterns = [
    path('home/',views.EntryHomeView.as_view(), name='home'),
    path('',views.PostListView.as_view(),name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_details'),
    path('new-story', views.PostCreateView.as_view(), name='post_write'),
    path('post/<slug:slug>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete', views.PostDeleteView.as_view(), name='post-delete'),
    path('me/saved-posts/', views.saved, name='saved_posts'),
    path('me/stories/',views.DraftAndPublishedPostListView.as_view(),name='stories'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('sitemap.xml',sitemap,
         {'sitemaps': sitemaps}, 
         name='django.contrib.sitemaps.views.sitemap'),
    path('logout/', auth_views.LogoutView.as_view(next_page='blog:home'), name='logout')
]
