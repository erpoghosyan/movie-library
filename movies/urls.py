from django.urls import path
from .views import (HomePageView,
                    SignUpView,
                    MovieListView, 
                    MovieDetailView, 
                    MovieUpdateView,
                    MovieDeleteView, 
                    MovieCreateView,
                    CommentDeleteView,
                    CommentUpdateView,
                    LikeView,
                    )
urlpatterns = [
    path("home/", HomePageView.as_view(), name="home"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("<int:pk>/", MovieDetailView.as_view(),
        name="movie_detail"), 
    path("<int:pk>/edit/", MovieUpdateView.as_view(),
        name="movie_edit"),
    path("<int:pk>/delete/", MovieDeleteView.as_view(),
        name="movie_delete"), 
    path("new/", MovieCreateView.as_view(), name="movie_new"),
    path("", MovieListView.as_view(),
        name="movie_list"),
    path('like/<int:pk>/', LikeView, name='like_movie'),
    path("<int:pk>/delete/comment/", CommentDeleteView.as_view(),
        name="comment_delete"),
    path("<int:pk>/edit/comment/", CommentUpdateView.as_view(),
        name="comment_edit")
 ]

