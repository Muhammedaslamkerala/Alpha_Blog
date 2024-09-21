from django.contrib.syndication.views import Feed
from django.db.models.base import Model
from django.urls import reverse_lazy
from django.utils.safestring import SafeText
from .models import Post

class LatestPostsFeed(Feed):
    title = 'My Blog'
    link = reverse_lazy('blog:post_list')
    description = "Latest posts from my blog."

    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item: Model) -> SafeText:
        return item.title 
    
    def item_description(self, item: Model) -> str:
        return item.short_description
    
    def item_pubdate(self, item: Model):
        return item.publish