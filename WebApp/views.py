from django.http import HttpResponse
from django.template import loader
from WebApp.forms import UpdateWspinacz, DodajWyjazd
from WebApp.models import Wspinacz, Wyjazd, UczestnikWyjazdu, PosiadaSprzet
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout


def index(request):
    template = loader.get_template('base.html')
    context = {}
    return HttpResponse(template.render(context, request))


def profil(request):
    wspinacz = Wspinacz.objects.get(user=request.user)
    instance = get_object_or_404(Wspinacz, id=wspinacz.id)
    sprzet = PosiadaSprzet.objects.all().filter(wspinacz=wspinacz)
    form = UpdateWspinacz(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'profil.html', {'form': form, 'wspinacz': wspinacz, 'sprzet': sprzet})


def wyjazdy(request):
    wyjazdy_all = Wyjazd.objects.all()
    return render(request, 'wyjazdy.html', {'wyjazdy': wyjazdy_all})


def dodaj_wyjazd(request):
    form = DodajWyjazd(request.POST or None, request=request)
    if form.is_valid():
        form.save()
        return redirect('/wyjazdy/')
    return render(request, 'dodaj_wyjazd.html', {'form': form})


def szczegoly_wyjazdu(request, wyjazd_id):
    wyjazd = Wyjazd.objects.get(pk=wyjazd_id)
    uczestnicy = UczestnikWyjazdu.objects.all().filter(wyjazd_id=wyjazd.id)
    return render(request, 'szczegoly_wyjazdu.html', {'wyjazd': wyjazd, 'uczestnicy': uczestnicy})


def wyloguj(request):
    logout(request)
    return redirect('index')


def zglos_na_wyjazd(request, wyjazd_id):
    wspinacz = Wspinacz.objects.get(user=request.user)
    UczestnikWyjazdu.objects.create(wspinacz=wspinacz, wyjazd_id=wyjazd_id, status_zgloszenia='oczek')
    return render(request, 'zgloszenie_wyslane.html', {})


def przegladaj_zgloszenia(request):
    wspinacz = Wspinacz.objects.get(user=request.user)
    zgloszenia = UczestnikWyjazdu.objects.all().filter(status_zgloszenia='oczek', wyjazd__organizator=wspinacz)
    return render(request, 'zgloszenia.html', {'zgloszenia': zgloszenia})


def zaakceptuj_zgloszenie(request, zgloszenie_id):
    zgloszenie = UczestnikWyjazdu.objects.get(pk=zgloszenie_id)
    zgloszenie.status_zgloszenia = 'zaakc'
    zgloszenie.save()
    return redirect('przegladaj_zgloszenia')


def odrzuc_zgloszenie(request, zgloszenie_id):
    zgloszenie = UczestnikWyjazdu.objects.get(pk=zgloszenie_id)
    zgloszenie.status_zgloszenia = 'odrz'
    zgloszenie.save()
    return redirect('przegladaj_zgloszenia')

