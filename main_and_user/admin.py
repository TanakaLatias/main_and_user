from django.contrib import admin
from .models import Post, Genre, Blog, Comment, User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "song_published_at", "category", "genre", "image_01", "image_02", "image_03", "image_04")

class GenreAdmin(admin.ModelAdmin):
    list_display = ("title", "image_01", "image_02", "image_03", "image_04")

class CommentInstanceInline(admin.TabularInline):
    model = Comment
    extra = 1

class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "genre", "image_01", "image_02", "image_03", "image_04")
    inlines = [CommentInstanceInline]

admin.site.register(Post, PostAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Blog, BlogAdmin)

class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','username')

class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff' , 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'username')
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(User, MyUserAdmin)
