from typing import Any

from django.db.models import Q
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect 
from django.views.generic import DetailView,  ListView, TemplateView, DeleteView, CreateView
from django.views import View
from django.views.generic.edit import UpdateView
from . models import Post, Category
from django.contrib.auth import get_user_model
from tags.models import Tag
from .forms import PostCreationForm, PostEditForm
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
    
    

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_details.html'
    context_object_name = 'post'
    
    def get_object(self):
        return get_object_or_404(Post, id=self.kwargs.get('pk'))
    
class SearchListView(ListView):
    model = Post
    template_name = 'blog/search.html'
    context_object_name = 'search_post_list'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
             return Post.objects.filter(Q(title__icontains=query) | 
                                        Q(tags__name__icontains=query) | 
                                        Q(categories__name__icontains=query) ).distinct()
         

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
    
    
    
     
class PostCreateView(CreateView):
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
   

class PostEditView(UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'dashbord/post_edit.html'
    success_url = reverse_lazy('blog:home')

    
class PostDelete(View):

    def get(self,request,pk):
        post = get_object_or_404(Post,id=pk)
        post.delete()
        return redirect(request.META.get('HTTP_REFERER'))

        

class DashbordView(TemplateView):
    template_name = 'dashbord/dashbord.html'

class PostPublishedListView(ListView):
    model = Post 
    template_name = 'dashbord/post_published.html'
    context_object_name ='post_list'

    def get_queryset(self) -> QuerySet[Any]:
        return Post.objects.filter(is_published=True).order_by("-published_date")

class DraftListView(ListView):
    model = Post
    template_name = 'dashbord/post_draft.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(is_published=False).order_by('-published_date')
    

    


def responses(request):
    return render(request, 'dashbord/responses.html')

