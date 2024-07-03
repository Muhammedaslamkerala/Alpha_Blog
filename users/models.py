from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email address'), unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(_('Profile_picture'), upload_to='profile_pictures', blank=True, null=True)
    bio = models.TextField(_('Biography'), blank=True, null=True)

    is_active = models.BooleanField(_('Activate'), default=True)
    is_staff = models.BooleanField(_('Staff status'), default=False)
    is_superuser = models.BooleanField(_('SuperUser status'),default=False)
    date_joined = models.DateTimeField(_("Date joined"), default=timezone.now)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_by_natural_key(self, email):
        return self.objects.get(email=email)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        return self.email
    
    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip() 
    
