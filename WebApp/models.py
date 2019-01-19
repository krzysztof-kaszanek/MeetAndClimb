from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Wspinacz(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    opis_umiejetnosci = models.CharField(max_length=255)
    ubezpieczenie = models.FileField(upload_to='uploads', null=True, blank=True)


class Instruktor(Wspinacz):
    STOPNIE_INSTRUKTORSKIE = (
        ('wsp_skalnej', 'Instruktor wspinaczki skalnej'),
        ('tater', 'Instruktor taternictwa'),
        ('alp', 'Instruktor alpinizmu')
    )

    stopien_instruktorski = models.CharField(max_length=255, choices=STOPNIE_INSTRUKTORSKIE)


class Wyjazd(models.Model):
    TRUDNOSCI_DROG = (
        ('3', '3'),
        ('4', '4'),
        ('5a', '5a'),
        ('5b', '5b'),
        ('5c', '5c'),
        ('6a', '6a'),
        ('6b', '6b'),
        ('6c', '6c'),
        ('7a', '7a'),
        ('7b', '7b'),
        ('7c', '7c'),
        ('8a', '8a'),
        ('8b', '8b'),
        ('8c', '8c'),
        ('9a', '9a'),
        ('9b', '9b'),
        ('9c', '9c'),
    )

    organizator = models.ForeignKey(Wspinacz, on_delete=models.CASCADE)
    data_rozpoczecia = models.DateField()
    data_zakonczenia = models.DateField()
    tytul = models.CharField(max_length=255)
    opis = models.CharField(max_length=255)
    trudnosci_drog = ArrayField(models.CharField(max_length=255, choices=TRUDNOSCI_DROG))


class Kurs(models.Model):
    RODZAJE_KURSU = (
        ('skal', 'Kurs skałkowy'),
        ('tater', 'Kurs taternicki'),
        ('law', 'Kurs lawinowy')
    )

    instruktor = models.ForeignKey(Instruktor, on_delete=models.CASCADE)
    data_rozpoczecia = models.DateField()
    data_zakonczenia = models.DateField()
    opis = models.CharField(max_length=255)
    cena = models.FloatField()
    limit_osob = models.PositiveIntegerField()
    rodzaj_kursu = models.CharField(max_length=255, choices=RODZAJE_KURSU)


class PosiadaSprzet(models.Model):
    RODZAJE_SPRZETU = (
        ('lina_poj', 'Lina pojedyncza'),
        ('lina pol', 'Lina połówkowa'),
        ('lina bliz', 'Lina bliźniacza'),
        ('hms', 'Karabinek HMS'),
        ('ekspres', 'Ekspres'),
        ('ekspres gor', 'Eskpres górski'),
        ('zestaw kosci', 'Zestaw kości'),
        ('zestaw kosci mech', 'Zestaw kości mechanicznych'),
        ('sr lodowa', 'Śruba lodowa'),
    )

    wspinacz = models.ForeignKey(Wspinacz, on_delete=models.CASCADE)
    nazwa_sprzetu = models.CharField(max_length=255, choices=RODZAJE_SPRZETU)
    ilosc_sprzetu = models.IntegerField()


class UczestnikWyjazdu(models.Model):
    STATUS = (
        ('oczek', 'Oczekujące'),
        ('odrz', 'Odrzucone'),
        ('zaakc', 'Zaakceptowane')
    )

    wspinacz = models.ForeignKey(Wspinacz, on_delete=models.CASCADE)
    wyjazd = models.ForeignKey(Wyjazd, on_delete=models.CASCADE)
    status_zgloszenia = models.CharField(max_length=255, choices=STATUS)


class UczestnikKursu(models.Model):
    wspinacz = models.ForeignKey(Wspinacz, on_delete=models.CASCADE)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE)
    potwierdzenie_wplaty = models.FileField(upload_to='uploads')


class Wiadomosc(models.Model):
    nadawca = models.ForeignKey(Wspinacz, on_delete=models.CASCADE, related_name='nadawca')
    odbiorca = models.ForeignKey(Wspinacz, on_delete=models.CASCADE, related_name='odbiorca')
    tytul = models.CharField(max_length=255)
    wiadomosc = models.CharField(max_length=255)
    przeczytana = models.BooleanField(default=False)
    data_wyslania = models.DateTimeField(auto_now_add=True)
