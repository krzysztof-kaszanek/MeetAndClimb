from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from WebApp.models import Wspinacz, Wyjazd, UczestnikKursu
from WebApp.stale import RODZAJE_SPRZETU, TRUDNOSCI_DROG


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=32, label='Imię')
    last_name = forms.CharField(max_length=32, label='Nazwisko')
    email = forms.EmailField(max_length=64, label='Email')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Konto o podanym adresie email już istnieje!")
        return email


class WyslijPotwierdzeniePrzelewu(forms.ModelForm):
    class Meta:
        model = UczestnikKursu
        fields = ('potwierdzenie_wplaty',)


class WyslijUbezpieczenie(forms.ModelForm):
    class Meta:
        model = Wspinacz
        fields = ('ubezpieczenie',)


class UpdateWspinacz(forms.ModelForm):
    nazwa_sprzetu = forms.ChoiceField(choices=RODZAJE_SPRZETU, label='Nazwa sprzętu', help_text='Dodaj sprzęt do profilu')
    ilosc_sprzetu = forms.IntegerField(min_value=1, label='Ilość sprzętu')

    class Meta:
        model = Wspinacz
        fields = ('opis_umiejetnosci', 'ubezpieczenie')
        labels = {
            'opis_umiejetnosci': 'Opis umiejętności'
        }
        widgets = {
            'opis_umiejetnosci': forms.Textarea(attrs={'rows': 4, 'cols': 100}),
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class DodajWyjazd(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(DodajWyjazd, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(DodajWyjazd, self).save(*args, **kwargs)
        if self.request:
            wspinacz = Wspinacz.objects.get(user=self.request.user)
            obj.organizator = wspinacz
        obj.save()
        return obj

    def clean(self):
        data_rozpoczecia = self.cleaned_data['data_rozpoczecia']
        data_zakonczenia = self.cleaned_data['data_zakonczenia']
        if data_zakonczenia < data_rozpoczecia:
            raise forms.ValidationError("Data rozpoczęcia musi poprzedzać datę zakończenia wyjazdu")

    class Meta:
        model = Wyjazd
        fields = ('data_rozpoczecia', 'data_zakonczenia', 'tytul', 'opis', 'trudnosci_drog')
        widgets = {
            'data_rozpoczecia': DateInput(),
            'data_zakonczenia': DateInput(),
            'opis': forms.Textarea(attrs={'rows': 10, 'cols': 100}),
            'trudnosci_drog': forms.SelectMultiple(choices=TRUDNOSCI_DROG)
        }
