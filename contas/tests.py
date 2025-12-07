from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class AutenticacaoTest(TestCase):
    """Testes para o sistema de autenticação."""

    def setUp(self):
        """Configura o ambiente de teste."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123!"
        )

    def test_pagina_login_carrega(self):
        """Testa se a página de login carrega corretamente."""
        response = self.client.get(reverse("contas:entrar"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bem-vindo de volta")

    def test_pagina_registro_carrega(self):
        """Testa se a página de registro carrega corretamente."""
        response = self.client.get(reverse("contas:registrar"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Crie sua conta")

    def test_login_sucesso(self):
        """Testa login com credenciais válidas."""
        response = self.client.post(reverse("contas:entrar"), {
            "username": "testuser",
            "password": "TestPass123!"
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_falha_credenciais_invalidas(self):
        """Testa login com credenciais inválidas."""
        response = self.client.post(reverse("contas:entrar"), {
            "username": "testuser",
            "password": "senhaerrada"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usuário ou senha incorretos")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_campos_vazios(self):
        """Testa login com campos vazios."""
        response = self.client.post(reverse("contas:entrar"), {
            "username": "",
            "password": ""
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Por favor, preencha todos os campos")

    def test_registro_sucesso(self):
        """Testa registro com dados válidos."""
        response = self.client.post(reverse("contas:registrar"), {
            "username": "novousuario",
            "email": "novo@example.com",
            "password": "SenhaForte123!",
            "password2": "SenhaForte123!"
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="novousuario").exists())

    def test_registro_senhas_diferentes(self):
        """Testa registro com senhas que não conferem."""
        response = self.client.post(reverse("contas:registrar"), {
            "username": "novousuario",
            "email": "novo@example.com",
            "password": "SenhaForte123!",
            "password2": "OutraSenha456!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "As senhas não conferem")
        self.assertFalse(User.objects.filter(username="novousuario").exists())

    def test_registro_senha_fraca(self):
        """Testa registro com senha fraca."""
        response = self.client.post(reverse("contas:registrar"), {
            "username": "novousuario",
            "email": "novo@example.com",
            "password": "123",
            "password2": "123"
        })
        self.assertEqual(response.status_code, 200)
        # Deve conter alguma mensagem de erro de validação de senha
        self.assertFalse(User.objects.filter(username="novousuario").exists())

    def test_registro_email_duplicado(self):
        """Testa registro com email já existente."""
        response = self.client.post(reverse("contas:registrar"), {
            "username": "outrousuario",
            "email": "test@example.com",  # Email já existe
            "password": "SenhaForte123!",
            "password2": "SenhaForte123!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Este e-mail já está cadastrado")

    def test_logout(self):
        """Testa logout do usuário."""
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get(reverse("contas:sair"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_perfil_requer_login(self):
        """Testa que a página de perfil requer autenticação."""
        response = self.client.get(reverse("contas:perfil"))
        self.assertEqual(response.status_code, 302)  # Redireciona para login
        self.assertIn("entrar", response.url)

    def test_perfil_logado(self):
        """Testa acesso à página de perfil quando logado."""
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get(reverse("contas:perfil"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")

    def test_login_redireciona_se_autenticado(self):
        """Testa que usuário já logado é redirecionado do login."""
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get(reverse("contas:entrar"))
        self.assertEqual(response.status_code, 302)  # Redireciona para perfil

    def test_registro_redireciona_se_autenticado(self):
        """Testa que usuário já logado é redirecionado do registro."""
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get(reverse("contas:registrar"))
        self.assertEqual(response.status_code, 302)  # Redireciona para perfil


class RegistrarFormTest(TestCase):
    """Testes para o formulário de registro."""

    def test_form_campos_obrigatorios(self):
        """Testa que username e senhas são campos obrigatórios."""
        from contas.forms import RegistrarForm
        form = RegistrarForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password", form.errors)
        self.assertIn("password2", form.errors)

    def test_form_valido(self):
        """Testa formulário com dados válidos."""
        from contas.forms import RegistrarForm
        form = RegistrarForm(data={
            "username": "validuser",
            "email": "valid@example.com",
            "password": "ValidPass123!",
            "password2": "ValidPass123!"
        })
        self.assertTrue(form.is_valid())
