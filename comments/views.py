from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, slug=self.kwargs.get('slug'))
        comment = form.save(commit=False)
        comment.post = post
        comment.author = self.request.user
        comment.save()
        redirect('blog:post_details', slug=post.slug)

    def form_invalid(self, form):
        post = get_object_or_404(Post, slug=self.kwargs.get('slug'))
        return redirect('blog:post_details', slug=post.slug)
    