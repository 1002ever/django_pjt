from django.urls import path
from . import views


app_name = 'articles'

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:movie_pk>/reviews/', views.review_index, name="review_index"),
    path('<int:movie_pk>/create/', views.create, name="create"),
    path('<int:review_pk>/', views.detail, name="detail"),
    path('<int:review_pk>/like/', views.like, name="like"),
    path('<int:review_pk>/update', views.update, name="update"),
    path('<int:review_pk>/delete', views.delete, name="delete"),
    path('<int:review_pk>/comment_create', views.comment_create, name="comment_create"),
    path('<int:review_pk>/comment_delete/<int:comment_pk>/', views.comment_delete, name="comment_delete")
]