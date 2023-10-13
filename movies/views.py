from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, FormView 
from django.views.generic.detail import SingleObjectMixin 
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from .models import Movie
from .forms import CommentForm
from django.views import View 
from django.views.generic import TemplateView

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
        comment = form.save(commit=False) 
        comment.movie= self.object
        comment.save()
        return super().form_valid(form)
    def get_success_url(self):
        movie = self.get_object()
        return reverse("movie_detail", kwargs={"pk": movie.pk})


class MovieDetailView(LoginRequiredMixin, View): 
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)
    def post(self, request, *args, **kwargs): 
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class MovieListView(ListView): 
    model = Movie
    template_name = "movie_list.html"

class MovieDetailView(DetailView):
    model = Movie
    template_name = "movie_detail.html"
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context['form'] = CommentForm()
        return context

class MovieUpdateView(UpdateView): 
    model = Movie
    fields = (
        "title",
        "body", )
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
        "author",
)


