from django import forms
from .models import Avaliacao


class AvaliacaoForm(forms.ModelForm):
    """Formulário para avaliação de filmes."""
    
    nota = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'hidden',
            'id': 'nota-input'
        })
    )
    comentario = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Escreva sua opinião sobre o filme (opcional)...',
            'rows': 3,
            'class': 'w-full rounded-xl bg-white/5 border border-white/10 px-4 py-3 text-base text-zinc-100 placeholder:text-zinc-500 focus:outline-none focus:ring-2 focus:ring-rose-400/40 resize-none'
        })
    )

    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario']
