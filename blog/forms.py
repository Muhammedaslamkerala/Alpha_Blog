from typing import Any
from django import forms
from .models import Post, Category
from taggit.forms import TagField
from django_ckeditor_5.widgets import CKEditor5Widget

class BasePostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
               queryset = Category.objects.all(),
                widget = forms.SelectMultiple(attrs={'style':'height:100px'}),
                required = True,
            )
    tags = TagField()
    class Meta:
        model = Post
        fields = ('title','body','categories','tags','status',)
        widgets =  {
            'body': CKEditor5Widget(config_name='default'),
        
        }
    def save(self, commit: bool = True) -> Any:
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance
    
class PostCreationForm(BasePostForm):
    
    def save(self, commit: bool = True) -> Any:
        instance = super().save(commit=False)
        instance.author = self.instance.author
        return super().save(commit=commit)
    
class PostEditForm(BasePostForm):
    pass