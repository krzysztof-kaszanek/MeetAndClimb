from django.test import TestCase
from WebApp.forms import DodajWyjazd, UpdateWspinacz, SignUpForm
from WebApp.models import User


class TestyFormularzy(TestCase):
    def test_dodaj_wyjazd_data_rozp_data_zak_prawidlowe1(self):
        data = {'data_rozpoczecia': '2019-01-02', 'data_zakonczenia': '2019-01-02', 'tytul': 'wyjazd',
                'opis': 'jakis opis', 'trudnosci_drog': ['5a', '5b']}
        form = DodajWyjazd(data=data)
        self.assertTrue(form.is_valid())

    def test_dodaj_wyjazd_data_rozp_data_zak_prawidlowe2(self):
        data = {'data_rozpoczecia': '2019-01-02', 'data_zakonczenia': '2019-01-13', 'tytul': 'wyjazd',
                'opis': 'jakis opis', 'trudnosci_drog': ['5a', '5b']}
        form = DodajWyjazd(data=data)
        self.assertTrue(form.is_valid())

    def test_dodaj_wyjazd_data_rozp_data_zak_nieprawidlowe(self):
        data = {'data_rozpoczecia': '2019-01-14', 'data_zakonczenia': '2019-01-13', 'tytul': 'wyjazd',
                'opis': 'jakis opis', 'trudnosci_drog': ['5a', '5b']}
        form = DodajWyjazd(data=data)
        self.assertFalse(form.is_valid())

    def test_update_wspinacz_ilosc_sprzetu_ujemna(self):
        data = {'opis_umiejetnosci': 'opis', 'ubezpieczenie': '', 'nazwa_sprzetu': 'sr lodowa',
                'ilosc_sprzetu': -2}
        form = UpdateWspinacz(data=data)
        self.assertFalse(form.is_valid())

    def test_update_wspinacz_ilosc_brak_opisu(self):
        data = {'opis_umiejetnosci': None, 'ubezpieczenie': '', 'nazwa_sprzetu': 'sr lodowa',
                'ilosc_sprzetu': 2}
        form = UpdateWspinacz(data=data)
        self.assertFalse(form.is_valid())

    def test_rejestracja_email_powtorzony(self):
        data = {'username': 'user12', 'first_name': 'adam',
                 'last_name': 'adamowski', 'email': 'user123@gmail.com',
                 'password1': 'verystrongpassword', 'password2': 'verystrongpassword'}
        User.objects.create(username='user1', first_name='adam', last_name='adamski', email='user123@gmail.com', password='silnehaslo')
        form = SignUpForm(data=data)
        self.assertFalse(form.is_valid())
