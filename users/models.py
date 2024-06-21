from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True, default='profile_pictures/default_picture.png')
    bio = models.TextField(blank=True, null=True, verbose_name=_('biography'))
    date_of_birth = models.DateField(null=True, verbose_name=_('date of birth'))
    
    def __str__(self) -> str:
        return self.username