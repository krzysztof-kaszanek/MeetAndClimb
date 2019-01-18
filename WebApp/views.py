from django.http import HttpResponse
from django.template import loader
from WebApp.forms import UpdateWspinacz, DodajWyjazd
from WebApp.models import Wspinacz, Wyjazd, UczestnikWyjazdu
from django.shortcuts import render, get_object_or_404, redirect


def index(request):
    template = loader.get_template('base.html')
    context = {}
    return HttpResponse(template.render(context, request))


def profil(request):
    wspinacz = Wspinacz.objects.get(user=request.user)
    instance = get_object_or_404(Wspinacz, id=wspinacz.id)
    form = UpdateWspinacz(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'profil.html', {'form': form, 'wspinacz': wspinacz})


def wyjazdy(request):
    wyjazdy_all = Wyjazd.objects.all()
    return render(request, 'wyjazdy.html', {'wyjazdy': wyjazdy_all})


def dodaj_wyjazd(request):
    wspinacz = Wspinacz.objects.get(user=request.user)
    form = DodajWyjazd(request.POST or None, request=request)
    if form.is_valid():
        print("VALID")
        form.save()
        return redirect('/wyjazdy/')
    return render(request, 'dodaj_wyjazd.html', {'form': form})


def szczegoly_wyjazdu(request, wyjazd_id):
    wyjazd = Wyjazd.objects.get(pk=wyjazd_id)
    uczestnicy = UczestnikWyjazdu.objects.all().filter(wyjazd_id=wyjazd.id)
    return render(request, 'szczegoly_wyjazdu.html', {'wyjazd': wyjazd, 'uczestnicy': uczestnicy})
