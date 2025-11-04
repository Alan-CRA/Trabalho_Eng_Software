# Padrões de Projeto

# 1. Fachada
Nesse projeto, o padrão de Fachada é utilizado no arquivo tmdb.py (dentro do app filmes), pois ele esconde toda a lógica de uso da API. Isso evita que o usuário (ou outras partes do código) utilize diretamente essa classe, permitindo que a comunicação ocorra apenas através de uma fachada que gerencia o acesso.

# 2. Template Method
Template Method também é utilizado no arquivo views.py dentro do app pages, onde as classes Home e About se utilizam do template TemplateView implementado pelo próprio Django, adicionando apenas as informações necessárias, sem mudar o fluxo do código.