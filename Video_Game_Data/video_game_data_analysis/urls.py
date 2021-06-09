from . import views
from django.urls import path

app_name = 'video_game_data_analysis'
urlpatterns = [
    path('', views.index, name='index')
]