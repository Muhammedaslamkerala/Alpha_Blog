from django.db import models
from blog.models import Post, Like
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_("Post"))
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("Author"))
    body = models.CharField(max_length=200,verbose_name=_("Comment"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created Date"))
    likes = GenericRelation(Like)

    def __str__(self) -> str:
        if self.author:
            return f"Comment by {self.author.get_full_name()} on {self.post.title}"
        return f"No Author : {self.body[:30]}"
    
    @property
    def like_count(self):
        return self.likes.count()

class Replay(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='replies')
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    body = models.CharField(max_length=200,verbose_name=_("Replay"))
    created_at = models.DateField(auto_now_add=True, verbose_name=_("Created Date"))
    likes = GenericRelation(Like)

    def __str__(self):
        if self.author:
            return f"Replay by {self.author.get_full_name()} to {self.parent_comment}"
        return f"No Author : {self.body[:30]}"
    
    @property
    def like_count(self):
        return self.likes.count()
    
        
   