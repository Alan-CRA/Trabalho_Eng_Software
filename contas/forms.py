from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class RegistrarForm(forms.ModelForm):
    """Formulário para registro de novos usuários."""
    
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Senha",
        help_text="Mínimo de 8 caracteres."
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirme a senha"
    )

    class Meta:
        model = User
        fields = ("username", "email")
        
    def clean_email(self):
        """Valida se o email já está em uso."""
        email = self.cleaned_data.get("email", "").strip().lower()
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    def clean_password(self):
        """Valida a força da senha usando os validadores do Django."""
        password = self.cleaned_data.get("password")
        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                raise forms.ValidationError(list(e.messages))
        return password

    def clean(self):
        """Valida se as senhas conferem."""
        data = super().clean()
        password = data.get("password")
        password2 = data.get("password2")
        
        if password and password2 and password != password2:
            raise forms.ValidationError("As senhas não conferem.")
        return data

