from typing import Any
from django import forms
from .models import Post, Category
from tags.models import Tag
from django_ckeditor_5.widgets import CKEditor5Widget

class TagsWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        if value:
            tags = [tag.name for tag in value]
            value = ', '.join(tags)
        return super().render(name, value, attrs, renderer)

class PostCreationForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
               queryset = Category.objects.all(),
                widget = forms.SelectMultiple(attrs={'style':'height:100px'}),
                required = True,
            )
    tags = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter tags separated by comma'})
    )
    class Meta:
        model = Post
        fields = ('title','body','categories','tags','is_published',)
        widgets =  {
            'body': CKEditor5Widget(config_name='default'),
            
        }
    
    def clean_tags(self):
        input_tags = self.cleaned_data['tags'].split(',')
        new_tags = [Tag.objects.get_or_create(name=name.strip())[0] for name in input_tags if name.strip()]
        return new_tags

    def save(self, commit: bool = True) -> Any:
        instance = super().save(commit=False)
        instance.auhtor = self.instance.author

        if commit:
            instance.save()
            self.save_m2m()
            instance.tags.set(self.cleaned_data['tags'])

        return instance
    
class PostEditForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={'style': 'height:100px'}),
        required=True,
    )
    tags = forms.CharField(
        required=True,
        widget=TagsWidget
    )

    class Meta:
        model = Post
        fields = ('title', 'body', 'categories', 'tags', 'is_published')
        widgets = {
            'body': CKEditor5Widget(config_name='default'),
        }
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['categories'].initial = self.instance.categories.all()
            self.fields['tags'].initial = self.instance.tags.all()
    def clean_tags(self):
        input_tags = self.cleaned_data['tags'].split(',')
        new_tags = [Tag.objects.get_or_create(name=name.strip())[0] for name in input_tags if name.strip()]
        return new_tags
    
    def save(self, commit: bool = True) -> Any:
        instance = super().save(commit=False)
        

        if commit:
            instance.save()
            self.save_m2m()
            instance.tags.set(self.cleaned_data['tags'])

        return instance
