from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import RegistrarForm

class Entrar(View):
    template_name = "contas/entrar.html"
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user:
            login(request, user)
            return redirect("/contas/usuario/")
        return render(request, self.template_name, {"erro": "Credenciais inválidas."})

class Registrar(View):
    template_name = "contas/registrar.html"
    def get(self, request):
        return render(request, self.template_name, {"form": RegistrarForm()})
    def post(self, request):
        form = RegistrarForm(request.POST)
        if form.is_valid():
            u = form.save(commit=False)
            u.set_password(form.cleaned_data["password"])
            u.save()
            login(request, u)
            return redirect("/contas/usuario/")
        return render(request, self.template_name, {"form": form})

@login_required
def perfil(request):
    return render(request, "contas/perfil.html")

def sair(request):
    logout(request)
    return redirect("/")
