from datetime import date
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Ctegories"""
    name = models.CharField("Category", max_length=100)
    description = models.TextField("Description")
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class ActorDirector(models.Model):
    """Actors and directors"""
    name = models.CharField("Name", max_length=100)
    age = models.PositiveSmallIntegerField("Age", default=0)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="actors/")

    def get_absolute_url(self):
        return reverse("actor_director_detail", kwargs={"slug": self.name})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Actors and directors"
        verbose_name_plural = "Actors and directors"


class Genre(models.Model):
    """Geners"""
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Movie(models.Model):
    """Movies"""
    title = models.CharField("Title", max_length=100)
    tagline = models.CharField("Tagline", max_length=100, default="")
    description = models.TextField("Description")
    poster = models.ImageField("Poster", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Release Date", default=2020)
    country = models.CharField("Country", max_length=30)
    directors = models.ManyToManyField(ActorDirector, verbose_name="Directors", related_name="film_directors")
    actors = models.ManyToManyField(ActorDirector, verbose_name="Actors", related_name="film_actors")
    genre = models.ManyToManyField(Genre, verbose_name="Genres")
    world_premiere = models.DateField("World premiere", default=date.today)
    budget = models.PositiveIntegerField("Budget", default=0, help_text="Enter sum in eur")
    fees = models.PositiveIntegerField("Fees in the world", default=0, help_text="Enter sum in eur")
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=100, unique=True)
    draft = models.BooleanField("Draft", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Get absolute URL for each movie"""
        return reverse("movie_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"


class Review(models.Model):
    """Reviews"""
    #email = models.EmailField()
    name = models.CharField("Name", max_length=100)
    text = models.TextField("Message", max_length=5000)
    movie = models.ForeignKey(Movie, verbose_name="Movie", on_delete=models.CASCADE)
    date_time = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        #sort reviews: newer reviews first
        ordering = ['-id']
