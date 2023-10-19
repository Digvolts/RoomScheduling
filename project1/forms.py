from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Ruangan
from .models import PemesananRuangan

class CustomUserCreationForm(UserCreationForm):
    # Menggunakan TextInput untuk menghilangkan help text
    # username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))



class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-dark'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-dark'}))


class RuanganForm(forms.ModelForm):
    class Meta:
        model = Ruangan
        fields = ['nama_ruangan', 'deskripsi', 'gambar']


class PemesananRuanganForm(forms.ModelForm):
    class Meta:
        model = PemesananRuangan
        fields = ['nama_ruangan', 'waktu_peminjaman', 'tanggal_pakai', 'alasan']

