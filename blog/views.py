from typing import Any

from django.db.models import Q
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView,  ListView, TemplateView, DeleteView, CreateView
from django.views import View
from django.views.generic.edit import UpdateView, FormMixin
from . models import Post, Category
from django.contrib.auth import get_user_model
from tags.models import Tag
from .forms import PostCreationForm, PostEditForm
from comments.forms import CommentForm
# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'post_list'
    
    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by("-published_date")
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class CategoryPostListView(ListView):  
     model = Post
     template_name = 'blog/category.html'
     context_object_name = 'post_list'

     def get_queryset(self):
        category = Post.objects.filter(categories__id=self.kwargs.get('pk'))
        return category
    
     def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all() 
        return context
    
    

class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    template_name = 'blog/post_details.html'
    context_object_name = 'post'
    form_class = CommentForm
    
    def get_object(self):
        return get_object_or_404(Post, id=self.kwargs.get('pk'))
    
    def get_success_url(self):
        return reverse('blog:post_details', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return super().get_context_data(**kwargs)
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.prefetch_related('comment_set').order_by('-comment_set__published_date') # When you want to sort or filter objects based on fields of related models, you use the double underscore (__) syntax to navigate across relationships. 
    #     return queryset   not working

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["comments"] =  post.comments.all().order_by('-published_date')
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_valid(form)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

             
class SearchListView(ListView):
    model = Post
    template_name = 'blog/search.html'
    context_object_name = 'search_post_list'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | 
                Q(tags__name__icontains=query) | 
                Q(categories__name__icontains=query)
            ).distinct()
         

class TagPostListview(ListView):
    model = Post
    template_name = 'blog/tags.html'
    context_object_name = 'post_list'

    def get_queryset(self) -> QuerySet[Any]:
        tag = get_object_or_404(Tag, id=self.kwargs.get('pk'))
        tag_by_post = Post.objects.filter(tags=tag)
        return tag_by_post
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["tag"] = get_object_or_404(Tag, id=self.kwargs.get('pk'))
        return context
    
    
    
     
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = 'dashbord/post_write.html'
    form_class = PostCreationForm
    success_url = reverse_lazy('blog:home')
   
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
   

class PostEditView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'dashbord/post_edit.html'
    success_url = reverse_lazy('blog:home')

    
class PostDelete(LoginRequiredMixin,View):

    def get(self,request,pk):
        post = get_object_or_404(Post,id=pk)
        post.delete()
        return redirect(request.META.get('HTTP_REFERER'))

# class PostDelete(LoginRequiredMixin, DeleteView):
#     model = Post
#     template_name = 

class DashbordView(LoginRequiredMixin,TemplateView):
    template_name = 'dashbord/dashbord.html'

class PostPublishedListView(LoginRequiredMixin,ListView):
    model = Post 
    template_name = 'dashbord/post_published.html'
    context_object_name ='post_list'

    def get_queryset(self) -> QuerySet[Any]:
        return Post.objects.filter(is_published=True, author=self.request.user).order_by("-published_date")

class DraftListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'dashbord/post_draft.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(is_published=False, author=self.request.user ).order_by('-published_date')
    


