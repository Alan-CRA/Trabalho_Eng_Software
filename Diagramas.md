# Documentação de Diagramas

## 1. Diagrama Comportamental

### Descrição
O diagrama comportamental desenvolvido representa o **fluxo de ações e decisões do sistema** nos casos de uso identificados no projeto:

- **UC-01 — Pesquisa de filmes:** o usuário pesquisa títulos disponíveis, aplicando filtros (gênero, duração, disponibilidade).  
- **UC-02 — Detalhamento do filme:** o usuário acessa uma página de informações do filme, contendo sinopse, elenco, gênero e links para streaming.  
- **UC-03 — Autenticação de usuários:** o usuário pode criar uma conta, realizar login e recuperar senha em caso de esquecimento.

### Justificativa
A escolha por um **diagrama comportamental** (Diagrama de Atividades) foi feita porque ele:

- Permite **visualizar o comportamento dinâmico do sistema**, mostrando como os processos se encadeiam em cada caso de uso.  
- Ajuda a identificar **condições de decisão** (ex.: filme encontrado) e ramificações de fluxo.  
- Facilita o entendimento das **interações entre usuário e sistema**, servindo como ponte entre os requisitos funcionais (user stories) e a futura implementação.

---

## 2. Diagrama Estrutural

### Justificativa

Para o diagrama estrutural foi escolhido o diagrama de classes, pois ele é o mais descritivo dos vistos em sala.

### Explicação
No diagrama existem as seguintes classes:

- Filme
- Avaliacao
- Genero
- Pessoa
- Usuario
- Ator
- FiltroPesquisa
- Streaming
- Autenticacao

Onde Usuario e Ator herdam atributos da classe Pessoa.

### Padrões Criados
Para deixar o diagrama mais limpo, em todas as classes foram colocados os metodos setters() e getters() que abrangem todo os metodos sets e gets necessários em cada classe. 