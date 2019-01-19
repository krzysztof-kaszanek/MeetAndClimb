from WebApp.models import Wiadomosc, Wspinacz


def my_context_processor(request):
    wspinacz = Wspinacz.objects.get(user=request.user)
    wiadomosci = Wiadomosc.objects.all().filter(odbiorca=wspinacz, przeczytana=False)
    liczba_wiadomosci = len(wiadomosci)
    return {'liczba_wiadomosci': liczba_wiadomosci}
