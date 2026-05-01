from django import views
from django.urls import path
from .views import  get_page, detail_actualite
from . import views


app_name = 'gestion'
urlpatterns = [
    path('',get_page, {'slug': 'index'}, name='index'),
    path('<str:slug>.html', get_page, name='get_page'),
    path('actualite/<int:id>/', detail_actualite, name='detail_actualites'),
    path('admin-mairie/', views.dashboard_mairie, name='dashboard_mairie'),
    path('ajax-changer-statut/', views.ajax_changer_statut_acte, name='ajax_changer_statut'),
    path('ajax-changer-statut-legalisation/', views.ajax_changer_statut_legalisation, name='ajax_changer_statut_legalisation'),
]