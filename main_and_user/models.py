from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=300)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    song_published_at = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=500)
    genre = models.CharField(max_length=500)
    image_01 = models.ImageField(null=True, blank=True, upload_to="media/main_and_user/post/")
    image_02 = models.ImageField(null=True, blank=True, upload_to="media/main_and_user/post/")
    image_03 = models.ImageField(null=True, blank=True, upload_to="media/main_and_user/post/")
    image_04 = models.ImageField(null=True, blank=True, upload_to="media/main_and_user/post/")
    def __str__(self):
        return self.title
    class Meta:
        ordering = ('created_at',)
    
class Genre(models.Model):
    title = models.CharField(max_length=300)
    text = models.TextField()
    image_01 = models.ImageField(null=True, blank=True, upload_to="media/main_and_user/genre/")
    image_02 = models.ImageField(null=True, blank=True, upload_to="media/main_and_user/genre/")
    image_03 = models.ImageField(null=True, blank=True, upload_to="media/main_and_user/genre/")
    image_04 = models.ImageField(null=True, blank=True, upload_to="media/main_and_user/genre/")
    def __str__(self):
        return self.title
    class Meta:
        ordering = ('id',)
        
class Blog(models.Model):
    title = models.CharField(max_length=300)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    genre = models.CharField(max_length=500, blank=True, null=True)
    image_01 = models.ImageField(null=True, blank=True, upload_to="media/main_and_user/blog/")
    image_02 = models.ImageField(null=True, blank=True, upload_to="media/main_and_user/blog/")
    image_03 = models.ImageField(null=True, blank=True, upload_to="media/main_and_user/blog/")
    image_04 = models.ImageField(null=True, blank=True, upload_to="media/main_and_user/blog/")
    def __str__(self):
        return self.title
    class Meta:
        ordering = ('created_at',)
    
class Comment(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ('id',)

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff must be True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must be True.')
        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_("username"), max_length=100, validators=[username_validator])
    email = models.EmailField(_("email_address"), unique=True)
    is_superuser = models.BooleanField(_("superuser status"), default=False)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)