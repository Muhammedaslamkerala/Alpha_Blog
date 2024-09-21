from typing import Any

from django.db.models.query import QuerySet
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView,  ListView, DeleteView, CreateView, TemplateView, View
from django.views.generic.edit import UpdateView
from django.utils.http import urlencode
from . models import Post, Category, SavedPost
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCreationForm, PostEditForm


class EntryHomeView(TemplateView):
    template_name = 'blog/entry_home_page.html'

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/logged_user_home_page.html'
    context_object_name = 'post_list'
    
        
    def get_queryset(self):
        category_slug = self.request.GET.get('category')
        if category_slug:
           category = get_object_or_404(Category, slug=category_slug)
           return Post.published.filter(categories=category)
        return Post.published.all()
    

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_details_page.html'
    context_object_name = 'post'
    
    def get_object(self):
        return get_object_or_404(Post, slug=self.kwargs.get('slug'))
    
    def get_success_url(self):
        return reverse('blog:post_details', kwargs={'slug': self.object.slug})
    
    

def saved(request):
    return render(request, 'blog/posts_saved_lists_page.html')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_write_page.html'
    form_class = PostCreationForm
    success_url = reverse_lazy('blog:post_list')
   
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.get_absolute_url()
    
    

class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'blog/post_edit_page.html'
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.get_absolute_url()

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_nameb = 'blog/post_confirm_delete.html'
    
    def get_object(self):
        slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=slug, author=self.request.user)
        return post

    def get_success_url(self):
        params = urlencode({'deleted':True})

        return reverse_lazy('blog:post_list') + '?' + params
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)
    
class DraftAndPublishedPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/publihsed_draft_posts_list_page.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        tab = self.request.GET.get('tab','published')

        if tab == 'published':
            return queryset.filter(status=Post.Status.PUBLISHED)
        elif tab == 'draft':
            return queryset.filter(status=Post.Status.DRAFT)
        else:
            return queryset
        

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['selected_tab'] = self.request.GET.get('tab','published')
        return context
    

class PostSaveView(LoginRequiredMixin,View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        user = request.user

        saved_post, created = SavedPost.objects.get_or_create(user=user, post=post)
        if not created:
            saved_post.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    

class PostSavedListView(LoginRequiredMixin ,ListView):
    model = SavedPost
    template_name = 'blog/posts_saved_lists_page.html'

    def get_queryset(self) -> QuerySet[Any]:
        return SavedPost.objects.filter(user=self.request.user) 
    

class UnifiedSearchView(View):
    ...

   
    

