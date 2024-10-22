from django.urls import path

from . import views
from . import search

urlpatterns = [
    path('', views.index, name="index"),
    path('projects/search/', search.search_project_by_name,name = 'search'),
    path('header/', views.header, name="header"),
    path('projects/supertictactoe/', views.supertictactoe, name="supertictactoe"),
    path('projects/photo1/', views.photo, name="photo1"),
]
