from django.shortcuts import render
from WebApp.forms import SignUpForm


def create_new_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SignUpForm
    return render(request, 'registration/signup.html', {'form': form})
