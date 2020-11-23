from django import template
from movies.models import Movie, Category

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()


#Count comes from template
@register.inclusion_tag('movies/tags/latest_movies.html')
def get_latest_movies(count=5):
    movies = Movie.objects.filter(draft=False).order_by("-id")[:count]
    return {"latest_movies":movies}
