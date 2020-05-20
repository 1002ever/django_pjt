from django.urls import path
from . import views


app_name = 'movies'

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:movie_pk>/like/', views.like, name="like"),
    path('recommend/', views.recommend, name="recommend"),
]