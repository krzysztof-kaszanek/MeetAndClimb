from WebApp.models import Wiadomosc, Wspinacz


def my_context_processor(request):
    if request.user.is_active:
        wspinacz = Wspinacz.objects.get(user=request.user)
        wiadomosci = Wiadomosc.objects.all().filter(odbiorca=wspinacz, przeczytana=False)
        liczba_wiadomosci = len(wiadomosci)
        return {'liczba_wiadomosci': liczba_wiadomosci}
    else:
        return {'liczba_wiadomosci': 0}
