from django.test import TestCase
from WebApp.models import Wyjazd, Wspinacz, User, Wiadomosc
from django.urls import reverse


class TestyWidokow(TestCase):

    def test_strona_glowna_dostepna(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_szczegoly_wyjazdu_dostepne(self):
        user = User.objects.create(username='user1', password='haslosilne')
        wspinacz = Wspinacz.objects.create(user=user, opis_umiejetnosci='opis', ubezpieczenie='ubezpieczenie.pdf')
        Wyjazd.objects.create(id=1, data_rozpoczecia='2019-01-01', data_zakonczenia='2019-02-01', tytul='aaa', opis='aaa',
                              trudnosci_drog=['5a', '5b'], organizator=wspinacz)
        self.client.login(username='user1', password='haslosilne')
        resp = self.client.get('/wyjazdy/1', follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_szczegoly_wyjazdu_dostepne_przez_reverse(self):
        user = User.objects.create(username='user1', password='haslosilne')
        wspinacz = Wspinacz.objects.create(user=user, opis_umiejetnosci='opis', ubezpieczenie='ubezpieczenie.pdf')
        Wyjazd.objects.create(id=1, data_rozpoczecia='2019-01-01', data_zakonczenia='2019-02-01', tytul='aaa',
                              opis='aaa', trudnosci_drog=['5a', '5b'], organizator=wspinacz)
        self.client.login(username='user1', password='haslosilne')
        resp = self.client.get(reverse('szczegoly_wyjazdu', kwargs={'wyjazd_id': 1}), follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_wiadomosc_dostepna_przez_reverse(self):
        user = User.objects.create(username='user1', password='haslosilne')
        wspinacz = Wspinacz.objects.create(user=user, opis_umiejetnosci='opis', ubezpieczenie='ubezpieczenie.pdf')
        Wyjazd.objects.create(id=1, data_rozpoczecia='2019-01-01', data_zakonczenia='2019-02-01', tytul='aaa',
                              opis='aaa',
                              trudnosci_drog=['5a', '5b'], organizator=wspinacz)
        Wiadomosc.objects.create(id=1, nadawca=wspinacz, odbiorca=wspinacz, tytul='tytul', wiadomosc='tekst',
                                 przeczytana=False, data_wyslania='2019-01-01')
        self.client.login(username='user1', password='haslosilne')
        resp = self.client.get(reverse('czytaj_wiadomosc', kwargs={'wiadomosc_id': 1}), follow=True)
        self.assertEqual(resp.status_code, 200)




