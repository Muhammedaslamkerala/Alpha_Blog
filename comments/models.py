from django.db import models
from blog.models import Post
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_("Post"))
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("Author"))
    body = models.TextField(verbose_name=_("Comment"))
    published_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Published Date"))

    def __str__(self) -> str:
         return f'{self.author.username} - {self.post.title}'