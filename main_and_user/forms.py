from django import forms
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from .models import Post, Genre, Blog, Comment, User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm 

class PostCreateForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=["title", "text", "song_published_at", "category", "genre", "image_01", "image_02", "image_03", "image_04",]
        labels = {"title": "", "text": "", "song_published_at": "", "category": "", "genre": ""}
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "Title", 'class': 'form_css'}),
            'text': forms.Textarea(attrs={'placeholder': "Texe", 'class': 'form_css_text'}),
            'song_published_at': forms.NumberInput(attrs={"type": "date", 'placeholder': "SongPublishedDate", 'class': 'form_css'}),
            'category': forms.TextInput(attrs={'placeholder': "Category", 'class': 'form_css'}),
            'genre': forms.TextInput(attrs={'placeholder': "Genre", 'class': 'form_css'}),
        }

class GenreCreateForm(forms.ModelForm):
    class Meta:
        model=Genre
        fields=["title", "text", "image_01", "image_02", "image_03", "image_04"]
        labels = {"title": "", "text": "",}
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "Title", 'class': 'form_css'}),
            'text': forms.Textarea(attrs={'placeholder': "Text", 'class': 'form_css_text'}),
        }

class BlogCreateForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields=["title", "text", "genre", "image_01", "image_02", "image_03", "image_04",]
        labels = {"title": "", "text": "", "genre": ""}
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "Title", 'class': 'form_css'}),
            'text': forms.Textarea(attrs={'placeholder': "Text", 'class': 'form_css_text'}),
            'genre': forms.TextInput(attrs={'placeholder': "Genre", 'class': 'form_css'}),
        }

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["name", "title", "text"]
        labels = {"title": "", "text": ""}
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "Name", 'class': 'form_css'}),
            'title': forms.TextInput(attrs={'placeholder': "Title", 'class': 'form_css'}),
            'text': forms.Textarea(attrs={'placeholder': "Text", 'class': 'form_css_text'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': "Name", 'class': 'form_css'}),
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'placeholder': "Email", 'class': 'form_css'}),
    )
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'placeholder': "Message", 'class': 'form_css_text'}),
    )

    def send_email(self):
        subject = "MusicMemoMessage"
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        from_email = '{name} <{email}>'.format(name=name, email=email)
        recipient_list = [settings.EMAIL_HOST_USER]
        try:
            send_mail(subject, message, from_email, recipient_list)
        except BadHeaderError:
            return HttpResponse("Error(s) occurred.")

class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {'username': '', 'email': ''}
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "Username", 'class': 'form_css'}),
            'email': forms.EmailInput(attrs={'placeholder': "Email", 'class': 'form_css'}),
        }

class LoginFrom(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {'username': '', 'email': ''}
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "Username", 'class': 'form_css'}),
            'email': forms.EmailInput(attrs={'placeholder': "Email", 'class': 'form_css'}),
        }
