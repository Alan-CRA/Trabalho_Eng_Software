from django import forms
from django.contrib.auth.models import User

class RegistrarForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirme a senha")

    class Meta:
        model = User
        fields = ("username", "email")

    def clean(self):
        data = super().clean()
        if data.get("password") != data.get("password2"):
            raise forms.ValidationError("As senhas não conferem.")
        return data
