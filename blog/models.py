
from django.db import models
from tags.models import Tag
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50,unique=True, verbose_name=_("Category Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']

    def __str__(self) -> str:
        return self.name
    

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    body = CKEditor5Field(verbose_name=_("Body"),config_name='default')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Published Date"))
    last_modified = models.DateTimeField(auto_now=True, verbose_name=_("Last Modified"))
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("Author"), null=True)
    categories = models.ManyToManyField(Category, related_name='posts', verbose_name=_("Categories"))
    tags = models.ManyToManyField(Tag, related_name='posts',verbose_name=_("Tags"))
    is_published = models.BooleanField(default=False, verbose_name=_("Is Publised"))

    def __str__(self) -> str:
        return self.title
    
    