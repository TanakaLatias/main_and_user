from django.urls import path
from .views import TopView, AboutView, PostIndexView, BlogIndexView, PostDetailView, BlogDetailView, GenreIndexView, GenreDetailView, PostCreateView, GenreCreateView, BlogCreateView, CommentCreateView, PostUpdateView, GenreUpdateView, BlogUpdateView, CommentUpdateView, PostDeleteView, GenreDeleteView, BlogDeleteView, CommentDeleteView, ContactView, ContactResultView, SignupView, LoginView, InformationView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("top/", TopView.as_view(), name="top"),
    path("about/", AboutView.as_view(), name="about"),
    path("post/index/", PostIndexView.as_view(), name="post_index"),
    path("genre/index/", GenreIndexView.as_view(), name="genre_index"),
    path("blog/index/", BlogIndexView.as_view(), name="blog_index"),
    path("post/detail/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("genre/detail/<int:pk>/", GenreDetailView.as_view(), name="genre_detail"),
    path("blog/detail/<int:pk>/", BlogDetailView.as_view(), name="blog_detail"),
    path("post/create/", PostCreateView.as_view(), name="post_create"),
    path("genre/create/", GenreCreateView.as_view(), name="genre_create"),
    path("blog/create/", BlogCreateView.as_view(), name="blog_create"),
    path("comment/create/<int:pk>/", CommentCreateView.as_view(), name="comment_create"),
    path("post/update/<int:pk>/", PostUpdateView.as_view(), name="post_update"),
    path("genre/update/<int:pk>/", GenreUpdateView.as_view(), name="genre_update"),
    path("blog/update/<int:pk>/", BlogUpdateView.as_view(), name="blog_update"),
    path("comment/update/<int:pk>/", CommentUpdateView.as_view(), name="comment_update"),
    path("post/delete/<int:pk>/", PostDeleteView.as_view(), name="post_delete"),
    path("genre/delete/<int:pk>/", GenreDeleteView.as_view(), name="genre_delete"),
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(),name='blog_delete'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(),name='comment_delete'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/result/', ContactResultView.as_view(), name='contact_result'),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('information/', InformationView.as_view(), name="information"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
