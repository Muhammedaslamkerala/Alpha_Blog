from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Tag Name"))

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['name']
    
    def __str__(self) -> str:
        return self.name