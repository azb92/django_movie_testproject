from django.contrib import admin
from django.utils.html import mark_safe
from .models import Category, Genre, Movie, ActorDirector, Review


#admin.site.register(Category, CategoryAdmin)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name", )


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year", )
    search_fields = ("title", "category__name", )
    save_on_top = True
    actions = ["unpublish", "publish"]
    #save_as = True
    list_editable = ("draft", )
    readonly_fields = ("get_image", )
    #fields = (("actors", "directors", "genre"), )
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"), )
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
        }),
        (None, {
            "fields": (("country", "year", "world_premiere"), )
        }),
        ("Actors, directors, genres, category", {
            "classes": ("collapse", ),
            "fields": (("actors", "directors", "genre", "category"), )
        }),
        (None, {
            "fields": (("budget", "fees"), )
        }),
        (None, {
            "fields": (("url", "draft"), )
        }),
    )

    def unpublish(self, request, queryset):
        """ Unpublisch movies """
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message = "1 movie have been updated"
        else:
            message = f"{row_update} movies have been updated"
        self.message_user(request, message)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="150" height="200">')

    def publish(self, request, queryset):
        """ Publisch movies """
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message = "1 movie have been updated"
        else:
            message = f"{row_update} movies have been updated"
        self.message_user(request, message)

    get_image.short_description = "Image"

    unpublish.short_descriptions = "Unpublish"
    unpublish.allowed_permissions = ('change', )

    publish.short_descriptions = "Publish"
    publish.allowed_permissions = ('change', )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "movie")
    list_filter = ("movie", )
    readonly_fields = ("name", )


@admin.register(ActorDirector)
class ActorDirectorwAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="60" height="70">')

    get_image.short_description = "Image"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name", )


admin.site.site_title = "Django movie project"
admin.site.site_header = "Django movie project"
