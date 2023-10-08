from django.contrib import admin 
from .models import Movie, Comment

class CommentInline(admin.TabularInline): 
     model = Comment

class MovieAdmin(admin.ModelAdmin): 
     inlines = [
        CommentInline,
    ]
admin.site.register(Movie, MovieAdmin)
admin.site.register(Comment)

