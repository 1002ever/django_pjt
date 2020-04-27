from django.urls import path
from . import views


app_name = 'polls'

urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('<int:poll_pk>/comment_create/', views.comment_create, name="comment_create"),
]