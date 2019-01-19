from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from WebApp.models import Wspinacz, Wyjazd, UczestnikKursu


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

    class Meta:
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

        model = Wyjazd
        fields = ('data_rozpoczecia', 'data_zakonczenia', 'tytul', 'opis', 'trudnosci_drog')
        widgets = {
            'data_rozpoczecia': DateInput(),
            'data_zakonczenia': DateInput(),
            'opis': forms.Textarea(attrs={'rows': 10, 'cols': 100}),
            'trudnosci_drog': forms.SelectMultiple(choices=TRUDNOSCI_DROG)
        }

