from WebApp.models import Wiadomosc, Wspinacz, Instruktor


def my_context_processor(request):
    if request.user.is_active:
        wspinacz = Wspinacz.objects.get(user=request.user)
        wiadomosci = Wiadomosc.objects.all().filter(odbiorca=wspinacz, przeczytana=False)
        liczba_wiadomosci = len(wiadomosci)
        instruktor = Instruktor.objects.filter(wspinacz_ptr=wspinacz)
        if instruktor.count() > 0:
            uzytkownik_instruktorem = True
        else:
            uzytkownik_instruktorem = False
        return {'liczba_wiadomosci': liczba_wiadomosci, 'uzytkownik_instruktorem': uzytkownik_instruktorem}
    else:
        return {'liczba_wiadomosci': 0, 'uzytkownik_instruktorem': False}
