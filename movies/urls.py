from django.urls import path
from . import views


urlpatterns = [
    path("", views.MovieListView.as_view(), name="home"),
    path("filter/", views.FilterMoviesView.as_view(), name="filter"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("<slug:slug>/", views.CategoryListView.as_view(), name="category_detail"),
    path("movie/<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", views.ActorDirectorView.as_view(), name="actor_director_detail")
    #<path:url> #will handle lots on agruments in url /agrumetn/argument/argumet etc
]
