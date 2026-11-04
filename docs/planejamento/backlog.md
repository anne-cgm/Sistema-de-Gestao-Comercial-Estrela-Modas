# Backlog do projeto

Este documento reúne os itens de trabalho informados pela equipe. Os prazos foram mantidos no formato `DD/MM`, pois o ano não foi especificado. O status de cada item também não foi informado e, por isso, não foi presumido.

> **Observação:** a numeração recebida vai do item 09 diretamente para o item 11. O item 10 não foi incluído porque não houve descrição dele.

## Itens de planejamento e documentação

### 01 — Mapeamento inicial e entrevista com o cliente

- **Responsável:** Nicolly
- **Objetivo:** conduzir e simular o levantamento de requisitos com a loja de roupas para entender as dores do cliente.
- **Entregas:**
  - Mapear as regras de negócio dos 10 módulos: Produtos, Estoque, Abastecimento, Vendas, Dashboard, Clientes, Débitos, Trocas, Despesas/Viagens e Relatórios.
  - Listar os requisitos funcionais e não funcionais do sistema.
- **Data limite:** 14/09

### 02 — Rascunho do fluxo de usuário (wireframes)

- **Responsável:** Kamila
- **Objetivo:** criar os esboços/wireframes iniciais das telas no Figma ou Penpot.
- **Entregas:**
  - Mapear a navegação principal, incluindo o menu e as telas dos 10 módulos.
  - Usar os wireframes como insumo visual para a elaboração dos casos de uso.
- **Data limite:** 12/09

### 03 — Elaboração do quadro 5W2H

- **Responsável:** Nicolly
- **Objetivo:** elaborar a síntese do projeto no formato 5W2H (What, Why, Where, When, Who, How e How much).
- **Entregas:** contextualizar o problema do cliente e a proposta da aplicação web para a loja de roupas.
- **Data limite:** 14/09

### 04 — Diagrama e especificação dos casos de uso

- **Responsável:** Nicolly
- **Entregas:**
  - Construir o diagrama de casos de uso em notação UML, cobrindo os atores e as interações do sistema.
  - Elaborar a documentação textual detalhada dos casos de uso: atores, pré-condições, pós-condições, fluxo principal, fluxos alternativos e exceções.
- **Data limite:** 14/09

### 05 — Diagrama de classes inicial

- **Responsável:** Nicolly
- **Entregas:**
  - Modelar em UML as classes do sistema, representando os 10 módulos.
  - Definir atributos, métodos e relacionamentos para dar suporte ao banco de dados e às views do Django.
- **Data limite:** 14/09

### 06 — Protótipo de alta fidelidade e identidade visual

- **Responsável:** Kamila
- **Entregas:**
  - Criar a marca/logotipo e definir a paleta de cores e a tipografia da aplicação.
  - Finalizar, no Figma, o protótipo navegável de alta fidelidade de todas as telas essenciais.
- **Data limite:** 15/09

### 07 — Configuração do repositório e pipeline de CI

- **Responsável:** Anne
- **Entregas:**
  - Criar o repositório a partir do template do professor, incluindo a estrutura `/docs`, `/docs/diagramas` e demais pastas solicitadas.
  - Configurar a estrutura inicial do projeto Django.
  - Configurar o GitHub Actions para automatizar testes e linters em cada Pull Request.
- **Data limite:** 16/09

### 08 — Estruturação dos templates HTML/CSS/JS base

- **Responsável:** Anne
- **Entregas:**
  - Criar o layout base dos templates Django usando HTML5, CSS3 e JavaScript.
  - Estruturar a navegação lateral (sidebar), o cabeçalho e a área de conteúdo responsiva para os 10 módulos.
  - Aplicar os estilos da identidade visual.
  - Preparar scripts JavaScript para manipulação do DOM e requisições assíncronas com Fetch API.
- **Data limite:** 16/09

### 09 — Configuração dos ambientes Django, Neon PostgreSQL e CI

- **Responsável:** Anne
- **Entregas:**
  - Configurar o projeto Django com conexão ao Neon PostgreSQL por variáveis de ambiente (`.env`).
  - Configurar o GitHub Actions para automatizar testes e linters em cada Pull Request.
- **Data limite:** 16/09

### 11 — Modelagem MER/DER e criação do banco de dados (Django + Neon)

- **Responsável:** Sciel
- **Entregas:**
  - Criar o modelo conceitual/lógico do banco de dados (MER/DER), cobrindo as tabelas e os relacionamentos dos 10 módulos.
  - Exportar o arquivo editável e as versões PDF/PNG para `docs/banco-de-dados/`.
  - Criar os `models.py` no Django refletindo o MER/DER e os padrões de nomes definidos (por exemplo, `nome_produto` e `cpf_cliente`).
  - Executar as migrations para criar as tabelas no PostgreSQL hospedado no Neon.
- **Data limite:** 20/09

## Itens de desenvolvimento

### 12 — [Dev] Módulos Produtos, Estoque e Trocas

- **Responsável:** Mila
- **Escopo:** desenvolver frontend (HTML/CSS/JS) e backend (Python/Django + Neon DB) para:
  1. **Produtos:** cadastro com geração e leitura de QR Code, catálogo e listagem com filtros.
  2. **Estoque:** controle de entradas/saídas e alertas de nível mínimo.
  3. **Trocas:** registro de devoluções, emissão de cupons de crédito e consulta de peças via QR Code.
- **Data limite:** 24/09

### 13 — [Dev] Módulos Vendas, Despesas/Viagens e Relatórios

- **Responsável:** Sciel
- **Escopo:** desenvolver frontend (HTML/CSS/JS) e backend (Python/Django + Neon DB) para:
  1. **Vendas:** PDV com leitor de QR Code para adicionar roupas rapidamente ao carrinho e dar baixa no estoque.
  2. **Despesas/Viagens:** registro e categorização dos custos operacionais da loja.
  3. **Relatórios:** telas com dados consolidados e opção de impressão/exportação.
- **Data limite:** 24/09

### 14 — [Dev] Módulos Clientes e Clientes com Débito

- **Responsável:** Nicolly
- **Escopo:** desenvolver frontend (HTML/CSS/JS) e backend (Python/Django + Neon DB) para:
  1. **Clientes:** formulário de cadastro e busca de clientes.
  2. **Clientes com Débito:** controle de saldo devedor/fiado e histórico de pagamentos.
- **Data limite:** 08/10

### 15 — [Dev] Módulos Compras/Abastecimento e Dashboard

- **Responsável:** Anne
- **Escopo:** desenvolver frontend (HTML/CSS/JS) e backend (Python/Django + Neon DB) para:
  1. **Compras/Abastecimento:** entrada de novas compras e registro de lote/QR Code.
  2. **Dashboard:** painel principal com gráficos e indicadores em JavaScript.
- **Data limite:** 28/09

## Itens de arquitetura e organização

### 16 — Documento de visão e arquitetura do sistema

- **Responsável:** Nicolly
- **Entregas:**
  - Redigir a versão final do Documento de Visão.
  - Criar o diagrama de arquitetura da aplicação em UML (componentes/implantação).
  - Explicar as camadas: HTML/CSS/JS no frontend, Python/Django no backend e PostgreSQL no Neon.
- **Data limite:** 02/10

### 17 — Contrato inicial da API REST e plano da API de QR Code

- **Responsável:** Anne
- **Entregas:**
  - Documentar os endpoints da API REST própria em JSON.
  - Elaborar o plano de integração da API externa de QR Code, incluindo propósito, endpoints consumidos, exibição das informações das roupas e tratamento de indisponibilidade.
- **Data limite:** 03/10

### 18 — Estruturação dos arquivos e README.md no GitHub

- **Responsável:** Nicolly
- **Entregas:**
  - Atualizar o `README.md` com detalhes da loja, tecnologias (HTML/CSS/JS, Python/Django e Neon), comandos para execução e integrantes.
  - Organizar as pastas conforme o checklist do professor: `/docs/visao`, `/docs/casos-de-uso`, `/docs/arquitetura`, `/docs/banco-de-dados`, `/docs/api` e `/docs/prototipos`.
- **Data limite:** 05/10
