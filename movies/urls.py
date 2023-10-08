from django.urls import path
from .views import (MovieListView, 
                    MovieDetailView, 
                    MovieUpdateView,
                    MovieDeleteView, 
                    MovieCreateView,
                    )
urlpatterns = [
    path("<int:pk>/", MovieDetailView.as_view(),
        name="movie_detail"), 
    path("<int:pk>/edit/", MovieUpdateView.as_view(),
        name="movie_edit"),
    path("<int:pk>/delete/", MovieDeleteView.as_view(),
        name="movie_delete"), 
    path("new/", MovieCreateView.as_view(), name="movie_new"),
    path("", MovieListView.as_view(),
        name="movie_list"),
 ]

