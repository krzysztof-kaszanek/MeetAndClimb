from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from WebApp.stale import STOPNIE_INSTRUKTORSKIE, TRUDNOSCI_DROG, RODZAJE_SPRZETU, RODZAJE_KURSU, STATUS


class Wspinacz(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    opis_umiejetnosci = models.CharField(max_length=255)
    ubezpieczenie = models.FileField(upload_to='uploads', null=True, blank=True)


class Instruktor(Wspinacz):
    stopien_instruktorski = models.CharField(max_length=255, choices=STOPNIE_INSTRUKTORSKIE)


class Wyjazd(models.Model):
    organizator = models.ForeignKey(Wspinacz, on_delete=models.CASCADE)
    data_rozpoczecia = models.DateField()
    data_zakonczenia = models.DateField()
    tytul = models.CharField(max_length=255)
    opis = models.CharField(max_length=255)
    trudnosci_drog = ArrayField(models.CharField(max_length=255, choices=TRUDNOSCI_DROG))


class Kurs(models.Model):
    instruktor = models.ForeignKey(Instruktor, on_delete=models.CASCADE)
    data_rozpoczecia = models.DateField()
    data_zakonczenia = models.DateField()
    opis = models.CharField(max_length=255)
    cena = models.FloatField()
    limit_osob = models.PositiveIntegerField()
    rodzaj_kursu = models.CharField(max_length=255, choices=RODZAJE_KURSU)


class PosiadaSprzet(models.Model):
    wspinacz = models.ForeignKey(Wspinacz, on_delete=models.CASCADE)
    nazwa_sprzetu = models.CharField(max_length=255, choices=RODZAJE_SPRZETU)
    ilosc_sprzetu = models.IntegerField()


class UczestnikWyjazdu(models.Model):
    wspinacz = models.ForeignKey(Wspinacz, on_delete=models.CASCADE)
    wyjazd = models.ForeignKey(Wyjazd, on_delete=models.CASCADE)
    status_zgloszenia = models.CharField(max_length=255, choices=STATUS)


class UczestnikKursu(models.Model):
    wspinacz = models.ForeignKey(Wspinacz, on_delete=models.CASCADE)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE)
    potwierdzenie_wplaty = models.FileField(upload_to='uploads')
    status_zapisu = models.CharField(max_length=255, choices=STATUS, default='oczek')


class Wiadomosc(models.Model):
    nadawca = models.ForeignKey(Wspinacz, on_delete=models.CASCADE, related_name='nadawca')
    odbiorca = models.ForeignKey(Wspinacz, on_delete=models.CASCADE, related_name='odbiorca')
    tytul = models.CharField(max_length=255)
    wiadomosc = models.CharField(max_length=255)
    przeczytana = models.BooleanField(default=False)
    data_wyslania = models.DateTimeField(auto_now_add=True)
