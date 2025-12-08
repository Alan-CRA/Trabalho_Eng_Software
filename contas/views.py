from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from .forms import RegistrarForm


class Entrar(View):
    """View para login de usuários."""
    template_name = "contas/entrar.html"

    def get(self, request):
        # Redireciona se já estiver logado
        if request.user.is_authenticated:
            messages.info(request, "Você já está logado.")
            return redirect("contas:perfil")
        return render(request, self.template_name)

    def post(self, request):
        # Redireciona se já estiver logado
        if request.user.is_authenticated:
            return redirect("contas:perfil")

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            return render(request, self.template_name, {
                "erro": "Por favor, preencha todos os campos."
            })

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bem-vindo de volta, {user.username}!")
            # Redireciona para a página solicitada ou perfil
            next_url = request.GET.get("next") or request.POST.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("pages:home")
        
        return render(request, self.template_name, {
            "erro": "Usuário ou senha incorretos. Verifique suas credenciais."
        })


class Registrar(View):
    """View para registro de novos usuários."""
    template_name = "contas/registrar.html"

    def get(self, request):
        # Redireciona se já estiver logado
        if request.user.is_authenticated:
            messages.info(request, "Você já possui uma conta e está logado.")
            return redirect("contas:perfil")
        return render(request, self.template_name, {"form": RegistrarForm()})

    def post(self, request):
        # Redireciona se já estiver logado
        if request.user.is_authenticated:
            return redirect("contas:perfil")

        form = RegistrarForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            messages.success(
                request,
                f"Conta criada com sucesso! Bem-vindo ao CineRecomenda, {user.username}!"
            )
            return redirect("pages:home")
        return render(request, self.template_name, {"form": form})


@login_required(login_url="contas:entrar")
def perfil(request):
    """View do perfil do usuário logado."""
    from filmes.models import Avaliacao, Favorito
    
    # Avaliações do usuário
    avaliacoes = Avaliacao.objects.filter(
        user=request.user
    ).select_related('filme').order_by('-criado_em')
    
    # Favoritos do usuário
    favoritos = Favorito.objects.filter(user=request.user)
    
    total_avaliacoes = avaliacoes.count()
    total_favoritos = favoritos.count()
    
    context = {
        "avaliacoes": avaliacoes[:5],  # Últimas 5 avaliações no perfil
        "total_avaliacoes": total_avaliacoes,
        "total_favoritos": total_favoritos,
        "filmes_vistos": total_avaliacoes,
    }
    return render(request, "contas/perfil.html", context)


@login_required(login_url="contas:entrar")
def minhas_avaliacoes(request):
    """View para listar todas as avaliações do usuário."""
    from filmes.models import Avaliacao
    
    avaliacoes = Avaliacao.objects.filter(
        user=request.user
    ).select_related('filme').order_by('-criado_em')
    
    context = {
        "avaliacoes": avaliacoes,
        "total": avaliacoes.count(),
    }
    return render(request, "contas/minhas_avaliacoes.html", context)


@login_required(login_url="contas:entrar")
def meus_favoritos(request):
    """View para listar todos os filmes favoritos do usuário."""
    from filmes.models import Favorito
    
    favoritos = Favorito.objects.filter(
        user=request.user
    ).select_related('filme').order_by('-criado_em')
    
    context = {
        "favoritos": favoritos,
        "total": favoritos.count(),
    }
    return render(request, "contas/meus_favoritos.html", context)


def sair(request):
    """View para logout de usuários."""
    if request.user.is_authenticated:
        messages.success(request, "Você saiu da sua conta. Até logo!")
    logout(request)
    return redirect("pages:home")

