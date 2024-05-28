from django.db import models
from blog.models import Post
from users.models import Author
# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    body = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.author.user.username} - {self.post.title}'