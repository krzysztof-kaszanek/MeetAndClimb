from django.shortcuts import render, redirect
from WebApp.forms import SignUpForm
from WebApp.models import Wspinacz


def create_new_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            nowy_uzytkownik = form.save()
            Wspinacz.objects.create(opis_umiejetnosci="", user_id=nowy_uzytkownik.pk)
            return redirect('index')
    else:
        form = SignUpForm
    return render(request, 'registration/signup.html', {'form': form})
