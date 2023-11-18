from django.conf import settings 
from django.db import models 
from django.urls import reverse
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    genre = models.CharField(max_length=255, default="null")
    kinopoisk_url = models.URLField(default='https://example.com')
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    likes = models.ManyToManyField(User, related_name='liked_movies')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse("movie_list")
