from . import views
from django.urls import path

app_name = 'video_game_data_analysis'
urlpatterns = [
    path('', views.index, name='index'),
    path('search_by_title/', views.search_by_title, name='search_by_title')
]