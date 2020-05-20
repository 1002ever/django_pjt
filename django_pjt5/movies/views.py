from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Movie
from .models import Genre
import random


def index(request):
    movie_list = Movie.objects.all()
    paginator = Paginator(movie_list, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }

    return render(request, 'movies/movie_list.html', context)

def like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        status = False
    else:
        movie.like_users.add(user)
        status = True
    context = {
        'status': status,
        'count': movie.like_users.count(),
    }
    return JsonResponse(context)

@login_required
def recommend(request):
    movies = Movie.objects.order_by("?")[:10]
    context = {
        'movies': movies,
    }

    return render(request, 'movies/recommend.html', context)