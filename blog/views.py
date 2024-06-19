from typing import Any

from django.db.models import Q
from django.db.models.query import QuerySet
from django.urls import reverse_lazy,reverse
from django.shortcuts import render, get_object_or_404, redirect 
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.generic import DetailView,  ListView, TemplateView, DeleteView
from django.views import View
from . models import Post, Category
from users.models import Author
from tags.models import Tag
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

class CategoryListView(ListView):  
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
         
class PostCreateView(View):
    template_name = 'dashbord/post_write.html'
    success_url = reverse_lazy('blog:home')

    

    def get(self, request):
        categories = Category.objects.all()
        return render(request, self.template_name,{'categories': categories})

    def post(self, request):
        title = request.POST.get('title')
        body = request.POST.get('body')
        tags_input = request.POST.get('tags')
        category_input = request.POST.get('category')
        is_published = request.POST.get('is_published') == 'on'

        if title and body:
           user_instance = User.objects.get(username=request.user)
           user = Author.objects.get(user=user_instance)
           post = Post(title=title, body=body,author= user,is_published=is_published)
           post.save()
           
        if tags_input:
           tags = [tag.strip() for tag in tags_input.split(',')]
           for tag_name in tags:
               tag, created = Tag.objects.get_or_create(name=tag_name)
               post.tags.add(tag)

        if category_input:
           category = Category.objects.get(id=category_input)
           post.categories.add(category)       

        return redirect(self.success_url)
     
class PostEditView(View):
    template_name = 'dashbord/post_edit.html' 
    success_url = reverse_lazy('blog:home')     

    def get(self, request,pk):
        post = get_object_or_404(Post, pk=pk)
        categories = Category.objects.all()
        return render(request, self.template_name,{'post':post,'categories':categories})
    
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        title = request.POST.get('title')
        body = request.POST.get('body')
        tags_input = request.POST.get('tags')
        category_input = request.POST.get('category')
        is_published = request.POST.get('is_published') == 'on'

        if title and body:
            post.title = title
            post.body = body
            post.is_published =is_published
            post.save()

        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(',')]
            post.tags.clear()
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)
        
        if category_input:
            post.categories.clear()
            category = Category.objects.get(id=category_input)
            post.categories.add(category)

        return redirect(self.success_url)
    
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

