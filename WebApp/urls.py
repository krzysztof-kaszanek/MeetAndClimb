from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wyloguj/', views.wyloguj, name='wyloguj'),
    path('profil/', views.profil, name='profil'),
    path('wyjazdy/', views.wyjazdy, name='wyjazdy'),
    path('wyjazdy/<int:wyjazd_id>/', views.szczegoly_wyjazdu, name='szczegoly_wyjazdu'),
    path('wyjazdy/dodaj/', views.dodaj_wyjazd, name='dodaj_wyjazd'),
    path('zglos/<int:wyjazd_id>/', views.zglos_na_wyjazd, name='zglos_na_wyjazd'),
    path('zgloszenia/', views.przegladaj_zgloszenia, name='przegladaj_zgloszenia'),
    path('zgloszenia/zaakceptuj/<int:zgloszenie_id>/', views.zaakceptuj_zgloszenie, name='zaakceptuj_zgloszenie'),
    path('zgloszenia/odrzuc/<int:zgloszenie_id>/', views.odrzuc_zgloszenie, name='odrzuc_zgloszenie'),
    path('wiadomosci/', views.przegladaj_wiadomosci, name='przegladaj_wiadomosci'),
    path('wiadomosci/<int:wiadomosc_id>', views.czytaj_wiadomosc, name='czytaj_wiadomosc'),
]