# Eng-de-Software-UFRN

Repositório de exemplo para as atividades da disciplina de Engenharia de Software da UFRN.

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Como clonar ou baixar](#como-clonar-ou-baixar)  
- [Estrutura do Projeto](#estrutura-do-projeto)  
- [Diagramas](#diagramas)
- [Licença](#licença)  

## Sobre o Projeto

### Título
Sistema para pesquisa e recomendação de filmes

### Descrição
O projeto consiste em um catálogo de filmes, de modo que o usuário consiga procurar, registrar e avaliar filmes. Além disso, o sistema irá recomendar filmes de acordo com as preferências e histórico do usuário.

### Componentes
- Alan César Rebouças de Araújo Carvalho
- Francisco Micarlos Teixeira Pinto

## Como clonar ou baixar

Você pode obter este repositório de três formas:

### Clonar via HTTPS
```bash
git clone https://github.com/Alan-CRA/Trabalho_Eng_Software.git
```

### Clonar via SSH
```bash
git clone git@github.com:Alan-CRA/Trabalho_Eng_Software.git
```

### Baixar como ZIP
1. Acesse a página do repositório no GitHub:
   https://github.com/Alan-CRA/Trabalho_Eng_Software
2. Clique no botão **Code** (verde).
3. Selecione **Download ZIP**.
4. Extraia o arquivo ZIP para o local desejado em seu computador.

## Rodando localmente
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate  # Windows

pip install -r requirements.txt
cp .env.example .env
# edite .env e coloque seu TMDB_READ_ACCESS_TOKEN

python manage.py migrate
python manage.py runserver
# http://127.0.0.1:8000
```

## Notas
- Tailwind via CDN no `templates/base.html`.
- Integração TMDB com cache local em `filmes/`.

## Funcionalidades Implementadas

### US1 - Pesquisa de Filmes
- Busca de filmes por título usando API TMDB
- Exibição de resultados com poster, nota e data de lançamento
- Cache local dos filmes buscados

### US2 - Detalhamento do Filme
- Página completa com título, sinopse, elenco, gêneros
- Informações de duração e nota média do TMDB
- Links para plataformas de streaming disponíveis

### US3 - Autenticação de Usuários
- Cadastro com validação de senha forte
- Login com mensagens de feedback
- Página de perfil com estatísticas do usuário
- Logout com confirmação

### US4 - Avaliação de Filmes ⭐
- Sistema de avaliação com notas de 1 a 10 estrelas
- Comentários opcionais nas avaliações
- Edição e exclusão de avaliações
- Média das avaliações dos usuários exibida no filme
- Histórico de avaliações no perfil do usuário

### US5 - Recomendação de Filmes 💡 (NOVA)
- Sistema de recomendação baseado nas avaliações do usuário
- Análise dos gêneros preferidos (filmes com nota >= 7)
- Busca de filmes populares dos gêneros identificados
- Filtra filmes já avaliados ou favoritados
- Página dedicada com até 12 recomendações personalizadas
- Mensagem indicando os gêneros que geraram as sugestões

## Estrutura do Projeto

```
Eng-de-Software-UFRN/
├── LICENSE
├── README.md
├── User_Stories.md
├── Diagramas.md
├── PrincipiosProjeto.md
└── docs/
    └── ... diagramas/
        ├── diagrama_comportamental.png
        └── diagrama_classes.png
├── config/
    └── ...
├── contas/
    └── ...
├── filmes/
    └── ...
├── pages/
    └── ...
├── scripts/
    └── ...
├── static/
    └── ...
├── templates/
    └── ...
├── .env
├── manage.py
└── requirements.txt
    
```

- LICENSE: termos da licença do projeto (MIT).
- README.md: arquivo de apresentação do projeto.
- User_Stories.md: histórias de usuários.
- Diagramas.md: explicação textual e justificativa dos diagramas.
- PrincipiosProjeto.md: Princípios de projetos que serão utilizados no projeto.
- docs/diagramas: contém as imagens dos diagramas gerados.


## Diagramas

O projeto inclui dois tipos de diagramas principais:

- **Diagrama Comportamental (UC-01, UC-02, UC-03, UC-04):** mostra o fluxo de atividades nos casos de uso de pesquisa de filmes, detalhamento do filme, autenticação de usuários e avaliação de filmes.  
- **Diagrama Estrutural (Classes):** representa a estrutura estática do sistema, incluindo entidades, atributos, relacionamentos e serviços.

As descrições e justificativas estão documentadas no arquivo [`Diagramas.md`](Diagramas.md).

## Licença

Este projeto está licenciado sob a **Licença MIT**. Veja o arquivo `LICENSE` para mais detalhes.

---
