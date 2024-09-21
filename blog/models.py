import uuid
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from .manager import PublishedManager
from html import unescape
from django.utils.text import slugify
import re

# Create your models here.
class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self) -> str:
        return f"Like by {self.user.get_full_name()} on {self.content_object}"
    
class Category(models.Model):
    name = models.CharField(max_length=50,unique=True, verbose_name=_("Category Name"))
    slug = models.SlugField(_('slug'), unique=True, default='default-slug', max_length=400)
    

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR',_("Draft")
        PUBLISHED = 'PB',_("Publised")
       
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    slug = models.SlugField(unique=True, max_length=200, blank=True, verbose_name=_("slug"))
    body = CKEditor5Field(verbose_name=_("Body"),config_name='default')
    publish = models.DateTimeField(default=timezone.now, verbose_name=_("Published Date"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created Date"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Modified"))
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("Author"),default=1)
    categories = models.ManyToManyField(Category, related_name='posts', verbose_name=_("Categories"))
    tags = TaggableManager()
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name=_("Status")
    )
    likes = GenericRelation(Like)
    view_count = models.PositiveIntegerField(default=0)
    saved_by = models.ManyToManyField(get_user_model(), related_name='saved_posts', through='SavedPost',verbose_name=("Saved By"), blank=True)

    objects =  models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        indexes = [
            models.Index(fields=['-publish'])
        ]
    
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_details", kwargs={"slug": self.slug})
    
    @property
    def short_description(self):
        text = re.sub(r'<[^>]*>', ' ', self.body)
        text = unescape(text)
        text = re.sub(r'\s+', ' ', text).split()
        words = text[:30]
        return ' '.join(words) + '...'
    
    @property
    def like_count(self):
        return self.likes.count()
    
    def increment_view_count(self):
        self.view_count += 1
        self.save()

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = slugify(f"{self.title}-{uuid.uuid4()}")
        super().save(*args, **kwargs)
    

class SavedPost(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f"{self.user.get_full_name()} saved {self.post.title}" 