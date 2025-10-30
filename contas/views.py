from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegistroForm, LoginForm
# Create your views here.
def user(request):
    return render(request,'contas/user.html')


def registrar(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "Conta criada com sucesso!")
            return redirect('pages:home')
    else:
        form = RegistroForm()
    return render(request, "contas/register.html", {"form": form})

def entrar(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, f"Bem-vindo, {usuario.username}!")
            return redirect('pages:home')
    else:
        form = LoginForm()
    return render(request, "contas/login.html", {"form": form})

def sair(request):
    logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect('pages:home')