from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from .models import Movie, Comment
from .forms import CommentForm, MovieSearchForm
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from .utils import fetch_kinopoisk_data
import requests



def movie_list(request):
    movie_titles = ['Movie 1', 'Movie 2', 'Movie 3']

    for title in movie_titles:
        kinopoisk_data = fetch_kinopoisk_data(title)
        if kinopoisk_data:
            Movie.objects.create(
                title=title,
                kinopoisk_url=kinopoisk_data['url'],
            )
    movies = Movie.objects.all()
    return render(request, 'movie_kinopoisk_list.html', {'movies': movies})

class HomePageView(TemplateView):
    template_name = "home.html"


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class CommentGet(DetailView):
    model = Movie
    template_name = "movie_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):
    model = Movie
    form_class = CommentForm
    template_name = "movie_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        comment = form.save(commit=False)
        comment.movie = self.object
        comment.save()

        return super().form_valid(form)

    def get_success_url(self):
        movie = self.get_object()
        return reverse("movie_detail", kwargs={"pk": movie.pk})


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = "comment_delete.html"
    movie_detail = Movie

    def get_success_url(self):
        movie_pk = self.get_object().movie.pk
        return reverse_lazy("movie_detail", kwargs={'pk': movie_pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = self.get_object().movie
        return context
    


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ("comment",)
    template_name = "comment_edit.html"

    def get_success_url(self):
        movie_pk = self.get_object().movie.pk
        return reverse_lazy("movie_detail", kwargs={'pk': movie_pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = self.get_object().movie
        return context


class MovieDetailView(View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Movie, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id=self.user.id).exists():
            liked = True
        context['total_likes'] = total_likes
        context["liked"] = liked
        return context


class MovieListView(ListView):
    model = Movie
    template_name = "movie_list.html"
    ordering = "-date"

class ComedyMovieListView(ListView):
    model = Movie
    template_name = "comedy_movie_list.html"
    ordering = "-date"

class SportMovieListView(ListView):
    model = Movie
    template_name = "sport_movie_list.html"
    ordering = "-date"

class ActionMovieListView(ListView):
    model = Movie
    template_name = "action_movie_list.html"
    ordering = "-date"

class AnimationMovieListView(ListView):
    model = Movie
    template_name = "animation_movie_list.html"
    ordering = "-date"

class BiographyMovieListView(ListView):
    model = Movie
    template_name = "biography_movie_list.html"
    ordering = "-date"

class DocumentaryMovieListView(ListView):
    model = Movie
    template_name = "documentary_movie_list.html"
    ordering = "-date"

class DramaMovieListView(ListView):
    model = Movie
    template_name = "drama_movie_list.html"
    ordering = "-date"

class FantasyMovieListView(ListView):
    model = Movie
    template_name = "fantasy_movie_list.html"
    ordering = "-date"

class HorrorMovieListView(ListView):
    model = Movie
    template_name = "horror_movie_list.html"
    ordering = "-date"

class MusicalMovieListView(ListView):
    model = Movie
    template_name = "musical_movie_list.html"
    ordering = "-date"

class MysteryMovieListView(ListView):
    model = Movie
    template_name = "mystery_movie_list.html"
    ordering = "-date"

class ScienceFictionMovieListView(ListView):
    model = Movie
    template_name = "science_movie_list.html"
    ordering = "-date"

class ThrillerMovieListView(ListView):
    model = Movie
    template_name = "thriller_movie_list.html"
    ordering = "-date"

class RomanceMovieListView(ListView):
    model = Movie
    template_name = "romance_movie_list.html"
    ordering = "-date"

class WarMovieListView(ListView):
    model = Movie
    template_name = "war_movie_list.html"
    ordering = "-date"

class WesternMovieListView(ListView):
    model = Movie
    template_name = "western_movie_list.html"
    ordering = "-date"

class PopularMovieListView(ListView):
    model = Movie
    template_name = "popular_movie_list.html"
    ordering = "-date"

class MovieUpdateView(UpdateView):
    model = Movie
    fields = (
        "title",
        "body",
        "genre",)
    template_name = "movie_edit.html"


class MovieDeleteView(DeleteView):
    model = Movie
    template_name = "movie_delete.html"
    success_url = reverse_lazy("movie_list")


class MovieCreateView(CreateView):
    model = Movie
    template_name = "movie_new.html"
    fields = (
        "title",
        "body",
        "genre",
    )

    def form_valid(self, form):
        # Set the user to the current user
        form.instance.author = self.request.user
        return super().form_valid(form)


class MovieLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        movie = get_object_or_404(Movie, pk=pk)
        user = request.user

        if user in movie.likes.all():
            # User has already liked this movie, so unlike it
            movie.likes.remove(user)
        else:
            # User has not liked this movie yet, so like it
            movie.likes.add(user)

        # Redirect to the same page or to the detail view of the movie
        return HttpResponseRedirect(reverse('movie_detail', args=[str(pk)]))
    
class MovieSearchView(ListView):
    model = Movie
    template_name = "movie_search_results.html"
    context_object_name = "movies"
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        url = "https://movie-database-alternative.p.rapidapi.com/"
        api_url = 'https://movie-database-alternative.p.rapidapi.com/'

        querystring = {"s": query, "r": "json", "page": "1"}
        headers = {
            "X-RapidAPI-Key": "081427815mshf6c0e29b9dd7964p1709b7jsn462710f9959e",
            "X-RapidAPI-Host": "movie-database-alternative.p.rapidapi.com"
        }

        response = requests.get(api_url, headers=headers, params=querystring)
        
        movie = response.json()
        print(response.json(), 'response')
        if response:
            return movie
        else:
            return Movie.objects.filter(title__icontains=query).order_by('-date')



# def combine_html(base_path, search_path, output_path):
#     # Load the content of base.html
#     with open(base_path, 'r', encoding='utf-8') as base_file:
#         base_content = base_file.read()

#     # Load the content of movie_search.html
#     with open(search_path, 'r', encoding='utf-8') as search_file:
#         search_content = search_file.read()

#     # Parse the HTML content using Beautiful Soup
#     base_soup = BeautifulSoup(base_content, 'html.parser')
#     search_soup = BeautifulSoup(search_content, 'html.parser')

#     # Find the location in base.html where you want to insert movie_search.html content
#     content_div = base_soup.find('div', {'id': 'content'})
#     if content_div:
#         # Insert the content from movie_search.html into base.html
#         content_div.append(search_soup.body.contents)

#     # Write the combined content to the output file
#     with open(output_path, 'w', encoding='utf-8') as output_file:
#         output_file.write(str(base_soup))