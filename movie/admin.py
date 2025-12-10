from django.contrib import admin
# Register your models here.
# movie/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.templatetags.static import static
from .models import (
    Genre,
    Movie,
    Movie_similarity,
    User as MovieUser,     # 为了避免和 auth.User 重名，这里起个别名
    Movie_rating,
    Movie_hot,
)
from .models import Announcement

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'poster_preview', 'name', 'imdb_id', 'release_time')
    list_filter = ('genre',)
    search_fields = ('name', 'imdb_id', 'director', 'actors')
    filter_horizontal = ('genre',)

    def poster_preview(self, obj):
        """
        Use imdb_id to build the poster path under movie/static/movie/poster.
        Static URL will be: /static/movie/poster/<imdb_id>.jpg
        """
        url = static(f'movie/poster/{obj.imdb_id}.jpg')  # 如果你实际是 .png 就改成 .png
        return format_html(
            '<img src="{}" style="height:60px;border-radius:6px;'
            'object-fit:cover;box-shadow:0 6px 18px rgba(0,0,0,0.5);" />',
            url
        )

    poster_preview.short_description = "Poster"



@admin.register(Movie_similarity)
class MovieSimilarityAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_source', 'movie_target', 'similarity')
    list_filter = ('movie_source',)
    search_fields = ('movie_source__name', 'movie_target__name')


@admin.register(MovieUser)
class MovieUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')


@admin.register(Movie_rating)
class MovieRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'movie', 'score')
    list_filter = ('score',)
    search_fields = ('user__name', 'movie__name')


@admin.register(Movie_hot)
class MovieHotAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'rating_number')
    list_filter = ('rating_number',)
    search_fields = ('movie__name',)

# movie/admin.py
admin.site.site_header = "🎬 Movie Recommendation Admin"
admin.site.site_title = "Movie Admin"
admin.site.index_title = "Welcome to the Movie Management Dashboard"


# movie/admin.py
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content')
#    date_hierarchy = 'created_at'
