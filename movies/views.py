from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, FormView 
from django.views.generic.detail import SingleObjectMixin 
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from .models import Movie, Comment
from .forms import CommentForm
from django.views import View 
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect


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
        comment.movie= self.object
        comment.save()
        
        return super().form_valid(form)
    def get_success_url(self):
        movie = self.get_object()
        return reverse("movie_detail", kwargs={"pk": movie.pk})
    
class CommentDeleteView(DeleteView):
    model = Comment
    template_name = "comment_delete.html"

    def get_success_url(self):
        movie_pk = self.get_object().movie.pk
        return reverse_lazy("movie_detail", kwargs={'pk': movie_pk})

class CommentUpdateView(UpdateView):
    model = Comment
    fields = (
        "comment", )
    template_name = "comment_edit.html"
    def get_success_url(self):
        movie_pk = self.get_object().movie.pk
        return reverse_lazy("movie_detail", kwargs={'pk': movie_pk})

class MovieDetailView(View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        print(view, 'view')
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
        )
    def form_valid(self, form):
        # Set the user to the current user
        form.instance.author = self.request.user
        return super().form_valid(form)
    
def LikeView(request, pk):
    movie = get_object_or_404(Movie, id=pk)
    liked = False
    if movie.likes.filter(id=request.user.id).exists():
        movie.likes.remove(request.user)
        liked = False 
    else:
        movie.likes.add(request.user )
        liked = True
    return HttpResponseRedirect(reverse("movie_detail", args=[str(pk)]))
    


