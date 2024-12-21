from django.urls import path

from . import views
from . import search

urlpatterns = [
    path('', views.index, name="index"),
    path('projects/search/', search.search_project_by_name,name = 'search'),
    path('header/', views.header, name="header"),
    path('projects/supertictactoe/', views.supertictactoe, name="supertictactoe"),
    path('projects/polyptoton/', views.polyptoton, name="polyptoton"),
    path('projects/photo1/', views.photo1, name="photo1"),
    path('projects/trigonomis/', views.trigonomis, name="trigonomis"),
    path('projects/invective/', views.invective, name="invective"),
    path('projects/isocolon/', views.isocolon, name="isocolon"),
    path('projects/about/', views.about, name="about"),
    path('projects/school/', views.school, name="school"),
    path('projects/powerschool/', views.powerschool, name="powerschool"),
    path('projects/run_crawltest/', views.run_crawltest, name="run_crawltest"),
    path('politics/', views.politics, name="politics"),
    path('politics/instructions/', views.instructions, name="instructions"),
    path('politics/quiz/', views.quiz, name="quiz"),
    path('politics/results/', views.results, name="results"),
]
