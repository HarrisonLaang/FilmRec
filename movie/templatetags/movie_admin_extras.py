# movie/templatetags/movie_admin_extras.py
from django import template
from movie.models import Movie, User as MovieUser, Movie_rating,Genre
from django.db.models import Count, Avg
import json
import re

register = template.Library()


@register.simple_tag
def total_movies():
    return Movie.objects.count()


@register.simple_tag
def total_front_users():
    return MovieUser.objects.count()


@register.simple_tag
def total_ratings():
    return Movie_rating.objects.count()

@register.simple_tag
def rating_score_stats():
    """
    Return JSON: {labels: [...], counts: [...]}
    labels: distinct scores, e.g. ["1.0","2.0",...]
    counts: number of ratings for each score.
    """
    qs = (Movie_rating.objects
          .values('score')
          .annotate(count=Count('id'))
          .order_by('score'))

    labels = [str(row['score']) for row in qs]
    counts = [row['count'] for row in qs]

    return json.dumps({"labels": labels, "counts": counts})

@register.simple_tag
def genre_movie_stats(limit=8):
    """
    Return JSON for top N genres by movie count:
    {labels: [...genre names...], counts: [...]}
    """
    qs = (Genre.objects
          .annotate(movie_count=Count('movie'))
          .order_by('-movie_count')[:limit])

    labels = [g.name for g in qs]
    counts = [g.movie_count for g in qs]

    return json.dumps({"labels": labels, "counts": counts})

@register.simple_tag
def movies_by_year_stats():
    """
    使用 Movie.release_time 中出现的 4 位数字作为年份，
    统计每一年对应的电影数量。
    返回 JSON: {labels: [...years...], counts: [...]}
    """
    year_counts = {}

    # 取出所有 release_time（排除空的）
    for r in Movie.objects.exclude(release_time="").values_list('release_time', flat=True):
        text = r or ""
        m = re.search(r'\d{4}', text)  # 找到第一个 4 位数字当作年份
        if m:
            year = m.group(0)
            year_counts[year] = year_counts.get(year, 0) + 1

    if not year_counts:
        return json.dumps({"labels": [], "counts": []})

    # 按年份升序排序
    years_sorted = sorted(year_counts.keys())
    labels = years_sorted
    counts = [year_counts[y] for y in years_sorted]

    return json.dumps({"labels": labels, "counts": counts})

@register.simple_tag
def genre_avg_rating_stats(limit=6):
    """
    选电影数量最多的前 limit 个类型，
    计算每个类型的平均评分。
    返回 JSON: {labels: [...genre names...], counts: [...avg scores...]}
    """
    qs = (Genre.objects
          .annotate(
              movie_count=Count('movie'),
              avg_score=Avg('movie__movie_rating__score')
          )
          .filter(movie_count__gt=0, avg_score__isnull=False)
          .order_by('-movie_count')[:limit])

    labels = [g.name for g in qs]
    counts = [round(g.avg_score or 0, 2) for g in qs]

    return json.dumps({"labels": labels, "counts": counts})
