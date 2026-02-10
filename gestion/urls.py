from django import views
from django.urls import path
from .views import  get_page, detail_actualite
from . import views


app_name = 'gestion'
urlpatterns = [
    path('',get_page, {'slug': 'accueil'}, name='accueil'),
    path('<str:slug>.html', get_page, name='get_page'),
    path('actualite/<int:id>/', detail_actualite, name='detail_actualites'),
]
