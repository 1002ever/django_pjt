from django.urls import path
from . import views

app_name='community'

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('create/',views.create, name='create'),
    path('<int:detail_pk>/detail/',views.detail, name='detail'),
    path('<int:detail_pk>/update/', views.update, name='update'),
    path('<int:detail_pk>/delete/', views.delete, name='delete'),
    path('<int:detail_pk>/comment/', views.comment_create, name='comment_create'),
    path('<int:detail_pk>/comment_delete/<int:comment_pk>/', views.comment_delete, name ='comment_delete'),
]

