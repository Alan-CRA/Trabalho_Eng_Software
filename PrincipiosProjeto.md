# Principios de Projeto

## Princípio da Responsabilidade Única (SRP):

- A classe Autenticacao deve gerenciar apenas as lógicas de login, cadastro e recuperação de senha.

- A classe Filme deve conter apenas os dados do filme, enquanto a classe FiltroPesquisa deve ser responsável pela lógica de busca.

## Princípio Aberto/Fechado (OCP):

- A funcionalidade de pesquisa de filmes (US1) deve permitir a adição de novos filtros (por ator, prêmios, etc.) sem precisar alterar o código de busca já existente, apenas adicionando novas classes de filtro.

## Princípio da Substituição de Liskov (LSP):

- Onde o sistema espera um objeto do tipo Pessoa, ele deve funcionar perfeitamente se receber um Usuario ou um Ator, garantindo que a herança seja consistente.


## Prefira Composição a Herança:

- A relação entre Filme e Genero ou Elenco é um bom exemplo. Um filme "possui um" gênero, em vez de "ser um" tipo de gênero. O uso de composição (associando esses objetos) torna o sistema mais flexível do que criar subclasses como FilmeDeAcao ou FilmeDeComedia.

## Alta Coesão:

- A classe Filme demonstra alta coesão, pois todos os seus atributos (título, sinopse, elenco) e métodos servem ao propósito único de representar e gerenciar as informações de um filme. Da mesma forma, a classe Avaliacao deve ser coesa, contendo apenas o que é estritamente necessário para representar uma avaliação.