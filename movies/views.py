from django.views.generic import View, ListView, DetailView
from django.shortcuts import redirect
from django.db.models import Q
from .models import Movie, ActorDirector, Genre
from .forms import ReviewForm


class GenreYear:
    """Return genrs and years for sidebar"""
    def get_genres(self):
        return Genre.objects.all().order_by("name")

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year").order_by("-year")


class MovieListView(GenreYear, ListView):
    """List of movies"""
    model = Movie
    queryset = Movie.objects.filter(draft=False).order_by("-id")
    paginate_by = 2
#    def get_context_data(self, *args, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context["categories"] = Category.objects.all()
#        return context


class CategoryListView(GenreYear, ListView):
    """List of categories"""
    model = Movie
    paginate_by = 1
    #url -> /category/slug
    def get_queryset(self):
        slug = self.kwargs['slug']
        queryset = Movie.objects.filter(category__url=slug, draft=False).order_by("-id") #movie.category -> category.url
        return queryset
    #url -> ?category=pk
#    def get(self, request, pk):
#        movies = Movie.objects.filter(category=pk)
#        return render(request, "movies/movie_list.html", {"movie_list":movies})


class MovieDetailView(GenreYear, DetailView):
    """Full movie description"""
    model = Movie
    slug_field = "url"


class AddReview(View):
    """Adding rewiews"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            #form.movie_id = pk #movie_id is presented in DB - movie_reviews
            form.movie = movie #Django will automaticaly find connections
            form.save()
        return redirect(movie.get_absolute_url())


class ActorDirectorView(GenreYear, DetailView):
    """Actor/director page"""
    model = ActorDirector
    template_name = 'movies/actor_director_detail.html'
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    """Filtered movie list"""
    paginate_by = 1

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genre__in=self.request.GET.getlist("genre")),
            #Q(category__in=self.request.GET.getlist("category")), # for adding category to the filter url
            draft=False
        ).distinct()
        return queryset

    #For pagination. Generate list with all needed ?year=_&?genre=_
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class SearchView(GenreYear, ListView):
    """Search"""
    paginate_by = 1
    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"), draft=False)

    #For pagination. Generate list with ?q=_&
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context
