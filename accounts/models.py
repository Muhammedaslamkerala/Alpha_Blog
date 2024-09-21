from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, URLValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('Email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    first_name = models.CharField(
        _('First name'),
        max_length=50,
        blank=True,
        validators=[MinLengthValidator(2)]
    )
    last_name = models.CharField(
        _('Last name'),
        max_length=50,
        blank=True,
        validators=[MinLengthValidator(2)]
    )
    profile_picture = models.ImageField(
        _('Profile picture'),
        upload_to='profile_pictures/%Y/%m/',
        blank=True,
        null=True
    )
    bio = models.TextField(_('Biography'), blank=True, null=True)
    website_url = models.URLField(
        _('Website Url'),
        max_length=255,
        blank=True,
        null=True,
        validators=[URLValidator()],
        help_text=("Provide a valid website URL.")
    )
    github_url = models.URLField(
        _('GitHub URL'),
        max_length=255,
        blank=True,
        null=True,
        validators=[URLValidator()],
        help_text=_("Provide a valid GitHub profile URL.")
    )
    linkedin_url = models.URLField(
        _('LinkedIn Url'),
        max_length=255,
        null=True,
        blank=True,
        validators=[URLValidator()],
        help_text=("Provide a valid LinkedIn profile URL.")
    )

    is_active = models.BooleanField(_('Active'), default=True)
    is_staff = models.BooleanField(_('Staff status'), default=False)
    is_superuser = models.BooleanField(_('Superuser status'), default=False)
    date_joined = models.DateTimeField(_("Date joined"), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def get_profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        else:
            return settings.STATIC_URL + "users/image/profile_pictures/default_picture.png"

    

class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    followee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followee')

    def __str__(self):
        return f'{self.follower} follows {self.followee}'