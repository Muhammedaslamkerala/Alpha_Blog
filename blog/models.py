
from django.db import models
from users.models import Author
from tags.models import Tag
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self) -> str:
        return self.name
    

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='c_posts')
    tags = models.ManyToManyField(Tag, related_name='t_posts')
    is_published = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
    
    