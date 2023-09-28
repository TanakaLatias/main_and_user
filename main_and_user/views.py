from time import timezone
import datetime
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from .models import Post, Genre, Blog, Comment
from django.views.generic.edit import FormView
from .forms import ContactForm, PostCreateForm, GenreCreateForm, BlogCreateForm, CommentCreateForm, SignUpForm, LoginFrom
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

class TopView(TemplateView):
    template_name = "main_and_user/top.html"

class AboutView(TemplateView):
    template_name = "main_and_user/about.html"

def cat(posts):
    categories=[]
    for post in posts:
        bs=post.category
        bs=bs.split("、")
        for b in bs:
            if b not in categories:
                categories.append(b)
    return categories

class PostIndexView(ListView):
    model=Post
    context_object_name='posts'
    template_name = "main_and_user/post_index.html"
    posts = Post.objects.all()
    categories=cat(posts)
    recent = timezone.now() - datetime.timedelta(days=3)
    context_vars = {'categories': categories, 'recent':recent}
    def get_context_data(self, **kwargs):
        context = super(PostIndexView, self).get_context_data(**kwargs)
        context.update(PostIndexView.context_vars)
        return context

class GenreIndexView(ListView):
    model=Genre
    context_object_name='genres'
    template_name = "main_and_user/genre_index.html"
    posts = Post.objects.all()
    recent = timezone.now() - datetime.timedelta(days=3)
    context_vars = {'posts' : posts, 'recent':recent}
    def get_context_data(self, **kwargs):
        context = super(GenreIndexView, self).get_context_data(**kwargs)
        context.update(GenreIndexView.context_vars)
        return context

class BlogIndexView(ListView):
    model = Blog
    template_name = "main_and_user/blog_index.html"
    context_object_name = 'blogs'
    paginate_by = 10
    recent = timezone.now() - datetime.timedelta(days=3)
    context_vars = {'recent':recent}
    def get_context_data(self, **kwargs):
        context = super(BlogIndexView, self).get_context_data(**kwargs)
        context.update(BlogIndexView.context_vars)
        return context

class PostDetailView(DetailView):
    model=Post
    context_object_name='post'
    template_name = "main_and_user/post_detail.html"

class GenreDetailView(DetailView):
    model=Genre
    context_object_name='genre'
    template_name = "main_and_user/genre_detail.html"
    blog_posts = Blog.objects.all()
    context_vars = {'blog_posts': blog_posts}
    def get_context_data(self, **kwargs):
        context = super(GenreDetailView, self).get_context_data(**kwargs)
        context.update(GenreDetailView.context_vars)
        return context

class BlogDetailView(DetailView):
    model=Blog
    context_object_name='blog'
    template_name = "main_and_user/blog_detail.html"

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "main_and_user/post_create.html"
    form_class = PostCreateForm
    success_url = reverse_lazy('post_index')
    login_url = '/top/'

class GenreCreateView(LoginRequiredMixin, CreateView):
    template_name = "main_and_user/genre_create.html"
    form_class = GenreCreateForm
    success_url = reverse_lazy('genre_index')
    login_url = '/top/'
    
class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = "main_and_user/blog_create.html"
    form_class = BlogCreateForm
    success_url = reverse_lazy('blog_index')
    login_url = '/top/'

class CommentCreateView(CreateView):
    model = Comment
    template_name = "main_and_user/comment_create.html"
    form_class = CommentCreateForm
    success_url = reverse_lazy('blog_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = Blog.objects.get(pk=self.kwargs['pk'])
        return context
    def form_valid(self, form):
        blog = Blog.objects.get(pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.blog = blog
        comment.save()
        return redirect('blog_detail', pk=self.kwargs['pk'])

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model=Post
    template_name = "main_and_user/post_create.html"
    form_class = PostCreateForm
    success_url = reverse_lazy('post_index')
    login_url = '/top/'
    
class GenreUpdateView(LoginRequiredMixin, UpdateView):
    model = Genre
    template_name = 'main_and_user/genre_create.html'
    form_class = GenreCreateForm
    success_url = reverse_lazy('genre_index')
    login_url = '/top/'

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'main_and_user/blog_create.html'
    form_class = BlogCreateForm
    success_url = reverse_lazy('blog_index')
    login_url = '/top/'
    
class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'main_and_user/comment_create.html'
    form_class = CommentCreateForm
    success_url = reverse_lazy('blog_index')
    login_url = '/top/'
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model=Post
    context_object_name = 'post'
    success_url=reverse_lazy('post_index')
    login_url = '/top/'

class GenreDeleteView(LoginRequiredMixin, DeleteView):
    model = Genre
    context_object_name = 'genre'
    success_url = reverse_lazy('genre_index')
    login_url = '/top/'
    
class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    context_object_name = 'blog'
    success_url = reverse_lazy('blog_index')
    login_url = '/top/'

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    context_object_name = 'comment'
    success_url = reverse_lazy('blog_index')
    login_url = '/top/'
    
class ContactView(FormView):
    template_name = 'main_and_user/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_result')
    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)

class ContactResultView(TemplateView):
    template_name = 'main_and_user/contact_result.html'

class SignupView(CreateView):
    form_class = SignUpForm
    template_name = "main_and_user/signup.html" 
    success_url = reverse_lazy("top")

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return response
    
class LoginView(BaseLoginView):
    form_class = LoginFrom
    template_name = "main_and_user/login.html"
    success_url = reverse_lazy("post_index")

class InformationView(LoginRequiredMixin, TemplateView):
    template_name = "main_and_user/information.html"

class LogoutView(LoginRequiredMixin, BaseLogoutView):
    success_url = reverse_lazy("top")




