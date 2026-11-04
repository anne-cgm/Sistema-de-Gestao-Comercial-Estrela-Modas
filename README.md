# Sistema de Gestão Comercial - Estrela Modas

[![Status](https://img.shields.io/badge/status-[em_desenvolvimento]-yellow)]()
[![Versão](https://img.shields.io/badge/versão-[0.1.0]-blue)]()
[![Licença](https://img.shields.io/badge/licença-[acadêmica]-lightgrey)]()

<img width="200" height="200" alt="estrela_modas_logo" src="https://github.com/user-attachments/assets/1c297274-0078-473c-830e-ee045a1bdb99" />

**Instituição:** UniCEUB 
**Curso:** Ciência da Computação
**Disciplina:** Desenvolvimento Web
**Turma / Semestre:** Turma A e Turma B
**Professor(a):** Felippe Pires 
**Status do projeto:** MVP

---

## Sumário

- [1. Descrição do projeto](#1-descrição-do-projeto)
- [2. Funcionalidades](#2-funcionalidades)
- [3. Demonstração](#3-demonstração)
- [4. Tecnologias utilizadas](#4-tecnologias-utilizadas)
- [5. Arquitetura](#5-arquitetura)
- [6. Organização dos diretórios](#6-organização-dos-diretórios)
- [7. Participantes](#7-participantes)
- [8. Como executar](#8-como-executar)
- [9. Configuração](#9-configuração)
- [10. Testes](#10-testes)
- [11. Uso de inteligência artificial](#11-uso-de-inteligência-artificial)
- [12. Contribuição e fluxo de trabalho](#12-contribuição-e-fluxo-de-trabalho)
- [13. Histórico de versões](#13-histórico-de-versões)
- [14. Limitações e próximos passos](#14-limitações-e-próximos-passos)
- [15. Licença, referências e contato](#15-licença-referências-e-contato)

---

## 1. Descrição do projeto

O sistema foi desenvolvido a partir do levantamento e da análise das necessidades de uma loja de roupas e acessórios.

A solução contempla, inicialmente, funcionalidades relacionadas ao cadastro de produtos, controle de estoque, registro de compras e vendas, gerenciamento de clientes, controle de débitos, trocas, despesas, dashboard e relatórios.

O projeto está sendo desenvolvido seguindo uma abordagem de desenvolvimento ágil, com levantamento e validação contínua dos requisitos junto às responsáveis pelo negócio.

### Objetivos

- **Objetivo geral:** Desenvolver uma aplicação mobile para um sistema de gestão comercial de uma loja de roupas.
  
- **Objetivos específicos:**
  - Centralizar as informações da loja em um único sistema;
  - Facilitar o controle de produtos e estoque;
  - Registrar vendas e compras de mercadorias;
  - Auxiliar no acompanhamento de clientes e débitos;
  - Registrar trocas e despesas;
  - Disponibilizar informações gerenciais para acompanhamento do negócio;
  -  Reduzir a dependência de controles realizados manualmente.

### Público-alvo

- Donos/gerentes da loja — controlam vendas, estoque, despesas e funcionários.
- Funcionários/vendedores — realizam vendas, consultam produtos e atualizam informações.
- Responsáveis pelo estoque — controlam entrada, saída e quantidade de peças.
- Responsáveis pelo financeiro — acompanham vendas, despesas e faturamento.
- Administradores — gerenciam usuários, funcionários e configurações do sistema.

---

## 2. Funcionalidades

| Funcionalidade | Descrição | Status |
|---|---|---|
| **Produtos** | Cadastro e gerenciamento de produtos, categorias, características, variações, preços, SKU, QR Code e pesquisa. | Em andamento |
| **Estoque** | Consulta de quantidades, entradas e saídas, atualização automática e alerta de estoque baixo. | Planejada |
| **Registro de compras** | Registro de compras, produtos, quantidades e valores, com atualização do estoque após o recebimento. | Em andamento |
| **Vendas** | Registro de vendas, produtos, quantidades, descontos, formas de pagamento, estoque e vendas fiadas. | Em andamento |
| **Dashboard** | Visualização de vendas, estoque, produtos com estoque baixo e informações gerenciais. | Planejada |
| **Clientes** | Cadastro, consulta de dados e histórico de compras. | Em andamento |
| **Clientes com débitos** | Consulta de débitos, registro de pagamentos, atualização dos valores pendentes e histórico de pagamentos. | Em andamento |
| **Trocas** | Registro de trocas, atualização do estoque e aplicação das regras de troca. | Planejada |
| **Controle de despesas** | Registro, consulta e classificação das despesas da loja. | Planejada |
| **Relatórios** | Relatórios de vendas, produtos mais vendidos, estoque baixo e indicadores financeiros. | Em andamento |

### Requisitos não funcionais

| Requisito | Descrição | Status |
|---|---|---|
| **Desempenho** | As principais operações do sistema devem apresentar tempo de resposta adequado, evitando atrasos perceptíveis durante o uso. | Planejada |
| **Segurança** | O sistema deve proteger as informações dos usuários e utilizar autenticação para controlar o acesso às funcionalidades. | Planejada |
| **Controle de acesso** | O sistema deve permitir diferentes níveis de acesso de acordo com o perfil do usuário. | Planejada |
| **Usabilidade** | A interface deve ser simples, intuitiva e facilitar a utilização por funcionários e responsáveis pela loja. | Em andamento |
| **Responsividade** | A interface deve se adaptar a diferentes tamanhos de tela, principalmente computadores, notebooks e dispositivos móveis. | Planejada |
| **Disponibilidade** | O sistema deve estar disponível durante o período de funcionamento e utilização da loja, conforme o ambiente de implantação. | Planejada |
| **Integridade dos dados** | As operações realizadas no sistema devem manter os dados consistentes, evitando registros incompletos ou incompatíveis. | Planejada |
| **Manutenibilidade** | O código deve ser organizado de forma a facilitar futuras correções, alterações e inclusão de novas funcionalidades. | Em andamento |
| **Escalabilidade** | A estrutura do sistema deve permitir a inclusão de novos produtos, usuários, clientes e registros sem comprometer seu funcionamento. | Planejada |
| **Backup** | Os dados importantes do sistema devem possuir mecanismos de backup e recuperação conforme a infraestrutura utilizada. | Planejada |

---

---

## 3. Demonstração

*Inclua capturas de tela, GIF ou link para vídeo. Coloque as imagens em `images/`.*

## Login
<img width="1463" height="837" alt="image" src="https://github.com/user-attachments/assets/c7123331-f0a6-4e85-8719-21dda8b08038" />

## Relatórios
<img width="1451" height="843" alt="Captura de tela 2026-10-07 023022" src="https://github.com/user-attachments/assets/70270a0f-06a7-44e7-bac2-b09beb2ac6f7" />

## Clientes com Débitos
<img width="1448" height="852" alt="Captura de tela 2026-10-07 023001" src="https://github.com/user-attachments/assets/1cf59bde-4967-435a-844e-d6550ec2a423" />

## Novo Produto
<img width="1448" height="847" alt="Captura de tela 2026-10-07 022925" src="https://github.com/user-attachments/assets/9f2d7553-85ee-4d06-8ed8-39861846cf5f" />

## Registrar Compra
<img width="1450" height="852" alt="Captura de tela 2026-10-07 022915" src="https://github.com/user-attachments/assets/cbfea8c5-6e9a-4ccb-9c75-f2f36f931ee1" />

## Mais
<img width="1452" height="852" alt="Captura de tela 2026-10-07 022838" src="https://github.com/user-attachments/assets/f206c274-1b8b-44eb-823e-dcef887c514f" />

## Nova Venda
<img width="1452" height="852" alt="Captura de tela 2026-10-07 022825" src="https://github.com/user-attachments/assets/d7dab467-1d04-406e-a47e-bc4b11292eca" />

## Clientes
<img width="1465" height="836" alt="Captura de tela 2026-10-07 022650" src="https://github.com/user-attachments/assets/939e76d5-43f2-477e-b498-d53b92eac5a6" />

## Produtos
<img width="1460" height="832" alt="Captura de tela 2026-10-07 022632" src="https://github.com/user-attachments/assets/90f9f0fa-8859-41b1-a532-7cad564c83d5" />

## Painel
<img width="1462" height="830" alt="Captura de tela 2026-10-07 022621" src="https://github.com/user-attachments/assets/e3434fbb-231c-4fda-917f-15c53f8fc92e" />


| Tela | Descrição |
| --- | --- |
| Login | Acesso ao sistema com e-mail e senha |
| Relatórios | Vendas, estoque e financeiro |
| Clientes com Débitos | Acompanhar valores fiados e pagamentos |
| Novo Produto | Cadastra novo produto |
| Registrar Compra | Registrar mercadorias e entradas |
| Mais | Acesso aos módulos administrativos |
| Nova Venda | Registre produtos, desconto e pagamento |
| Clientes | Cadastros e histórico de compras |
| Produtos | Catálogo e variações |
| Painel | Acompanhe o movimento da loja. |

**Vídeo / protótipo:** https://youtu.be/5MNjWmEUNYE

---

## 4. Tecnologias utilizadas

| Camada | Tecnologia | Versão / Observação |
| --- | --- | --- |
| **Linguagem Backend** | Python | 3.14 (identificado via `.pyc`)[cite: 1] |
| **Framework Backend** | Django | Estrutura `settings.py` / `urls.py` (Versão 6.1.3) [cite: 1] |
| **Frontend** | HTML5/CSS3/JavaScript (Vanilla) | Páginas e scripts de interface[cite: 1] |
| **Banco de Dados** | PostgreSQL | Hospedado na plataforma Neon [cite: 1] |
| **Acesso ao Banco** | psycopg | Driver de conexão com PostgreSQL [cite: 1] |
| **Configuração do Banco** | dj-database-url | Leitura da URL de conexão[cite: 1] |
| **Gerenciador de Pacotes** | npm (Node.js) | `package-lock.json` / `node_modules`[cite: 1] |
| **Gerenciador de Dependências Python** | pip | `requirements.txt` [cite: 1] |
| **Containerização** | Docker | Criação e execução de contêineres para a aplicação [cite: 1] |
| **Orquestração de Contêineres** | Docker Compose | Configuração e gerenciamento dos serviços da aplicação [cite: 1] |
| **CI/CD & Automação** | GitHub Actions | Workflows de integração contínua (`ci.yml`)[cite: 1] |
| **Controle de Versão** | Git | — [cite: 1] |

---

## 5. Arquitetura

O sistema adota uma arquitetura em **camadas bem definidas**, garantindo o desacoplamento entre a interface de usuário, as regras de negócio e a persistência de dados. O fluxo de comunicação é síncrono e baseado no protocolo HTTP/HTTPS, onde a camada de apresentação consome uma API REST exposta pelo servidor backend.

O backend é executado em um container Docker, gerenciado pelo Docker Compose, enquanto o banco de dados PostgreSQL permanece hospedado externamente na plataforma Neon. Essa configuração permite organizar e padronizar o ambiente de execução da aplicação.

### Camadas do Sistema

1. **Camada de Apresentação (Frontend):**
   * Desenvolvida em **HTML5, CSS3 e JavaScript Vanilla**, sendo responsável por renderizar a interface e interagir com o usuário.
   * Contém telas estruturadas para fluxos específicos, tais como autenticação (`login.html`), painel principal (`dashboard.html`), gerenciamento de utilizadores (`users.html`), produtos (`products.html`), clientes (`customers.html`) e vendas (`sales.html`)[cite: 1].
   * Consome as rotas do backend através de requisições HTTP (API REST).

2. **Camada de Aplicação e Negócio (Backend):**
   * Desenvolvida em **Python** utilizando o framework **Django**[cite: 1].
   * O módulo `config` centraliza as definições do projeto (`settings.py`) e a estrutura de rotas (`urls.py`)[cite: 1].
   * Processa as requisições HTTP recebidas, executa as validações e regras de negócio do sistema e coordena a comunicação com o banco de dados.
   * Executada em um container Docker, cuja configuração é definida pelo (`Dockerfile`) e gerenciada pelo Docker Compose. 

3. **Camada de Persistência (Banco de Dados):**
   * Utiliza o banco de dados relacional **PostgreSQL**, hospedado na plataforma Neon.
   * Armazena os dados do sistema, incluindo utilizadores, produtos, clientes e histórico de vendas.
   * A conexão com o banco é realizada pelo backend por meio da variável de ambiente (`DATABASE_URL`)

---

### Diagrama de Arquitetura

O diagrama detalhado da arquitetura e o modelo de entidades encontram-se disponíveis no diretório `docs/` do repositório.

#### Fluxo de Dados:

  ```text
[ Utilizador ]
      │
      ▼
┌─────────────────────────────────────────┐
│       Apresentação (Frontend)           │
│       HTML / CSS / JavaScript           |
|       (login, dashboard, etc.)          │[cite: 1]
└────────────────────┬────────────────────┘
                     │  Requisições HTTP / REST API
                     ▼
┌─────────────────────────────────────────┐
│            Container Docker             |
|                                         |
|     Aplicação & Negócio (Backend)       │
│      Django (urls.py / settings.py)     │[cite: 1]
└────────────────────┬────────────────────┘
                     │  ORM / Consultas SQL
                     |  Conexão via DATABASE_URL
                     ▼
┌─────────────────────────────────────────┐
│       Persistência (Banco)              │
│       PostgreSQL - Neon                 |
|       (Hospedagem externa)              |
└─────────────────────────────────────────┘

**Decisões relevantes:**

- Uso de uma arquitetura em camadas para separar a interface, o processamento das regras de negócio e a persistência dos dados.

- Utilização de banco de dados relacional PostgreSQL, considerando os relacionamentos entre os dados do sistema.

- Hospedagem do banco de dados na plataforma Neon, mantendo a persistência separada do ambiente de execução da aplicação.

- Utilização de Docker para padronizar o ambiente de execução do backend.

- Utilização de Docker Compose para configurar e iniciar o container da aplicação, incluindo as variáveis de ambiente e o mapeamento de portas.


### Endpoints principais (quando houver API)

| Método | Rota | Descrição |
| --- | --- | --- |
| `POST` | `/api/[recurso]` | [Ex.: criar um registro] |
| `GET` | `/api/[recurso]` | [Ex.: listar registros] |
| `GET` | `/api/[recurso]/{id}` | [Ex.: obter um registro] |
| `PUT` | `/api/[recurso]/{id}` | [Ex.: atualizar um registro] |
| `DELETE` | `/api/[recurso]/{id}` | [Ex.: remover um registro] |

Documentação completa da API: docs/api.md

---
```

## 6. Organização dos diretórios

A estrutura do projeto está organizada em diretórios que separam as configurações do Django, a aplicação, a interface, os testes, a documentação e os arquivos de infraestrutura. Essa organização facilita a manutenção e o desenvolvimento do sistema.

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── backend/
│   └── db.sqlite3
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docs/
│   ├── api/
│   │   └── contrato-api.md
│   ├── arquitetura/
│   │   ├── arquitetura.drawio
│   │   ├── arquitetura.drawio.png
│   │   ├── arquitetura.md
│   │   ├── integracao.md
│   │   └── integracoes.md
│   ├── banco-de-dados/
│   │   ├── image.png
│   │   ├── modelo-dados.md
│   │   └── modelo-er.mwb
│   ├── casos-de-uso/
│   │   ├── Diagrama Caso Uso Loja.asta
│   │   ├── diagrama-casos-de-uso.png
│   │   └── especificacao-do-caso-de-uso
│   ├── planejamento/
│   │   ├── backlog.md
│   │   ├── planejamento-fase-1.md
│   │   └── riscos.md
│   ├── requisitos/
│   │   ├── levantamento.md
│   │   ├── regras-de-negocio.md
│   │   ├── requisitos-funcionais.md
│   │   ├── requisitos-nao-funcionais.md
│   │   └── retricoes.md
│   ├── visao/
│   │   └── documento-de-visao.md
│   └── PADROES.md
├── estrela_modas/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── frontend/
│   ├── static/
│   │   └── estrela_modas/
│   │       ├── cadastro_produto.js
│   │       ├── clientes.js
│   │       ├── compras.js
│   │       ├── dashboard.js
│   │       ├── debitos.js
│   │       ├── estoque.js
│   │       ├── login.js
│   │       ├── mais_opcoes.js
│   │       ├── nova_venda.js
│   │       ├── produtos.js
│   │       ├── relatorios.js
│   │       └── shared.js
│   └── templates/
│       └── estrela_modas/
│           ├── cadastro_produto.html
│           ├── clientes.html
│           ├── compras.html
│           ├── dashboard.html
│           ├── debitos.html
│           ├── estoque.html
│           ├── index.html
│           ├── login.html
│           ├── mais_opcoes.html
│           ├── nova_venda.html
│           ├── produtos.html
│           ├── registro.html
│           └── relatorios.html
├── tests/
│   ├── build.js
│   └── script.test.js
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── package.json
├── package-lock.json
├── README.md
└── requirements.txt
```

| Diretório / arquivo | Função |
| --- | --- |
| `.github/workflows/` | Armazena os workflows de automação do GitHub Actions. |
| `backend/` | Contém arquivos relacionados ao ambiente do backend e o banco SQLite local (`db.sqlite3`). |
| `config/` | Reúne as configurações centrais do Django, incluindo configurações gerais, rotas e interfaces WSGI e ASGI. |
| `docs/` | Armazena a documentação técnica e os artefatos de desenvolvimento do projeto. |
| `docs/api/` | Contém o contrato e a documentação da API. |
| `docs/arquitetura/` | Reúne diagramas, documentos de arquitetura e especificações de integração. |
| `docs/banco-de-dados/` | Armazena modelos e diagramas relacionados à estrutura do banco de dados. |
| `docs/casos-de-uso/` | Contém diagramas e especificações dos casos de uso do sistema. |
| `docs/planejamento/` | Reúne o backlog, o planejamento das fases e o registro de riscos do projeto. |
| `docs/requisitos/` | Armazena os documentos de levantamento, regras de negócio e requisitos funcionais e não funcionais. |
| `docs/visao/` | Contém o documento de visão do projeto. |
| `estrela_modas/` | Contém a aplicação Django, incluindo modelos, formulários, visualizações, rotas, testes e configurações administrativas. |
| `estrela_modas/migrations/` | Armazena as migrações responsáveis por registrar alterações na estrutura do banco de dados. |
| `frontend/static/estrela_modas/` | Contém os arquivos JavaScript responsáveis pelas funcionalidades e interações da interface. |
| `frontend/templates/estrela_modas/` | Armazena os templates HTML das telas do sistema. |
| `tests/` | Reúne arquivos de testes e verificações relacionadas ao projeto. |
| `.dockerignore` | Define os arquivos e diretórios que não devem ser enviados para a construção da imagem Docker. |
| `.gitignore` | Define os arquivos e diretórios que não devem ser versionados pelo Git. |
| `Dockerfile` | Define as instruções para construir a imagem Docker da aplicação. |
| `docker-compose.yml` | Configura e gerencia a inicialização do ambiente da aplicação. |
| `manage.py` | Permite executar comandos administrativos do Django. |
| `package.json` | Contém as informações e configurações das dependências Node.js. |
| `package-lock.json` | Registra as versões das dependências Node.js instaladas. |
| `requirements.txt` | Lista as dependências Python necessárias para a aplicação. |
| `README.md` | Apresenta o projeto, suas tecnologias e instruções de utilização. |
---
 
## 7. Participantes

| Nome | Matrícula | Função no projeto |
| --- | --- | --- |
| Sciel Ramos RodriguesBuitrago | [22510054] | backend / frontend / Engenheiro de Dados |
| Kamila Gomes da Silva | [22503734] | backend / frontend / Designer UI/UX |
| Anna Nicolly da Silva | [22500860] | backend / frontend / documentação |
| Anne Caroline Gonçalves de Mesquita | [22500825] | backend / frontend / testes / Gerenciadora de Projetos |

**Professor(a) responsável:** Felippe Pires

---

## 8. Como executar

### 8.1. Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

- Git;
- Python 3.14 ou superior;
- Docker Desktop com Docker Compose (para execução com contêineres).

Também é necessário possuir o arquivo `backend/.env`, configurado com as variáveis de ambiente exigidas pela aplicação.

### 8.2. Execução com Docker Compose (recomendada)

O Docker Compose permite configurar e executar a aplicação em um ambiente padronizado, utilizando as configurações definidas no `Dockerfile` e no `docker-compose.yml`.

**1. Clone o repositório:**

```bash
git clone <https://github.com/anne-cgm/Sistema-de-Gestao-Comercial-Estrela-Modas.git>
cd <Sistema-de-Gestao-Comercial-Estrela-Modas>
```

**2. Verifique se o arquivo `backend/.env` está configurado.**

Esse arquivo contém as variáveis necessárias para a execução da aplicação e a conexão com o banco de dados PostgreSQL hospedado na Neon.

**3. Construa a imagem e inicie o contêiner:**

```bash
docker compose up --build -d
```

**4. Execute as migrações do banco de dados:**

```bash
docker compose exec web python manage.py migrate
```

**5. Verifique se o contêiner está em execução:**

```bash
docker compose ps
```

**6. Acesse a aplicação pelo navegador:**

```text
http://localhost:8000
```

#### Comandos úteis do Docker Compose

| Comando | Descrição |
|---|---|
| `docker compose up -d` | Inicia os contêineres em segundo plano |
| `docker compose up --build -d` | Reconstrói a imagem e inicia os contêineres |
| `docker compose ps` | Lista os contêineres em execução |
| `docker compose logs -f web` | Exibe os logs da aplicação em tempo real |
| `docker compose down` | Para e remove os contêineres |
| `docker compose build` | Constrói a imagem da aplicação |

### 8.3. Execução sem Docker (alternativa)

Também é possível executar a aplicação diretamente no ambiente local, utilizando Python e Django, sem a necessidade de Docker.

**1. Clone o repositório:**

```bash
git clone <https://github.com/anne-cgm/Sistema-de-Gestao-Comercial-Estrela-Modas.git>
cd <Sistema-de-Gestao-Comercial-Estrela-Modas>
```

**2. Crie um ambiente virtual Python:**

```bash
python -m venv venv
```

**3. Ative o ambiente virtual:**

No Windows (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
source venv/bin/activate
```

**4. Instale as dependências do projeto:**

```bash
pip install -r requirements.txt
```

**5. Verifique se o arquivo `backend/.env` está configurado.**

As variáveis `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` e `DATABASE_URL` são necessárias para a configuração da aplicação e conexão com o banco de dados.

**6. Execute as migrações:**

```bash
python manage.py migrate
```

**7. Inicie o servidor de desenvolvimento:**

```bash
python manage.py runserver
```

**8. Acesse a aplicação pelo navegador:**

```text
http://127.0.0.1:8000
```

> **Observação:** Nas duas formas de execução, a aplicação utiliza o PostgreSQL hospedado na Neon. Portanto, é necessário ter o arquivo `backend/.env` corretamente configurado e acesso à internet para estabelecer a conexão com o banco de dados.

## 9. Configuração

O sistema utiliza variáveis de ambiente para gerenciar as configurações do framework Django e a conexão com o banco de dados PostgreSQL hospedado na plataforma Neon.

As variáveis devem ser definidas no arquivo `backend/.env`, que é utilizado pelo Docker Compose durante a inicialização da aplicação. Esse arquivo não deve ser versionado no repositório, pois contém informações sensíveis.

| Variável | Obrigatória | Descrição | Exemplo |
| --- | --- | --- | --- |
| `SECRET_KEY` | Sim | Chave secreta utilizada pelo Django para funções de segurança. | `django-insecure-chave-secreta-aqui` |
| `DEBUG` | Sim | Ativa ou desativa o modo de depuração do Django (`True` para desenvolvimento e `False` para produção). | `True` |
| `ALLOWED_HOSTS` | Sim | Lista de hosts e domínios permitidos para acessar a aplicação. | `localhost,127.0.0.1` |
| `DATABASE_URL` | Sim | String de conexão com o banco de dados PostgreSQL hospedado no Neon. | `postgresql://usuario:senha@host/banco?sslmode=require` |

### Exemplo de configuração

O arquivo `backend/.env` deve seguir o formato abaixo, substituindo os valores de exemplo pelas configurações correspondentes ao ambiente:

```env
SECRET_KEY=django-insecure-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://usuario:senha@host/banco?sslmode=require
```

**Importante:** as credenciais reais do banco de dados e a chave secreta do Django devem permanecer apenas no arquivo `.env` local. Nunca compartilhe ou versione esse arquivo no GitHub. Para ambientes de produção, utilize variáveis de ambiente configuradas diretamente na plataforma de hospedagem.

## 10. Testes

Os testes do projeto verificam funcionalidades do backend desenvolvido em Django e os scripts de teste do frontend. A execução dos testes do backend pode ser realizada por meio do container Docker, enquanto os testes do frontend utilizam as ferramentas configuradas no projeto.

### Execução dos testes

```bash
# Executar a suíte de testes do Django
docker compose exec web python manage.py test

# Executar os testes do frontend, caso o script esteja configurado no package.json
npm test
```

### Tipos de testes

| Tipo | Ferramenta | O que verifica |
| --- | --- | --- |
| Backend | Django Test Runner / unittest | Testes das funcionalidades, regras de negócio e validações implementadas no backend. |
| Frontend | Scripts de teste em JavaScript | Verificações relacionadas aos scripts e funcionalidades do frontend. |
| Automação/CI | GitHub Actions (`ci.yml`) | Execução automática das etapas de integração contínua configuradas no workflow. |
| Manuais | Verificação local | Funcionamento da aplicação, navegação entre páginas e interação com as funcionalidades do sistema. |

**Cobertura atual:** A cobertura de testes está em desenvolvimento e pode ser ampliada conforme novas funcionalidades e testes forem implementados.

---

## 11. Uso de inteligência artificial

Este repositório segue a política de uso de IA da disciplina (semáforo pedagógico):

![Política de uso de IA — semáforo](images/semaforo.png)

| Situação | Significado |
| --- | --- |
| **Vermelho — uso proibido** | Atividades de autonomia intelectual (ex.: provas presenciais sem consulta). |
| **Amarelo — uso limitado** | IA pode ser ferramenta auxiliar, desde que haja declaração de uso. |
| **Verde — uso permitido** | Uso livre ao longo da atividade acadêmica. |

### Declaração de uso

*Preencha de forma honesta. Se não houve uso de IA, declare explicitamente.*

- **Houve uso de IA neste projeto?** Sim
- **Ferramentas utilizadas:** ChatGPT, GitHub Copilot, Gemini
- **Finalidade:** revisão de texto, geração de esboço de testes, esclarecimento de dúvidas de sintaxe
- **O que NÃO foi delegado à IA:** definição do problema, modelagem, implementação das regras de negócio, testes finais

---

## 12. Contribuição e fluxo de trabalho

Para manter a organização do código e o alinhamento entre os membros da equipe no repositório **Sistema-de-Gestao-Comercial-Estrela-Modas**, adotamos o seguinte fluxo de ramificação baseação no estado atual do projeto:

### Branches

- `main` — Branch principal e estável do projeto (default).
- `docs/[nome]` — Alterações relativas à documentação do sistema (ex.: `docs/fase-concepcao`).
- `feature/[nome]` — Desenvolvimento de novas funcionalidades ou scripts (ex.: `feature/Script-BD`).
- `backend/[nome]` — Configurações, rotas e módulos do servidor (ex.: `backend/configuracao-django`).
- `front/[nome]` — Ajustes de interface e telas (ex.: `front/ajustes-telas-compras`).
- `infra/[nome]` — Definições de infraestrutura, banco de dados e ambiente (ex.: `infra/setup-django-neon`).

---

### Commits

As mensagens de commit devem ser curtas, diretas e no imperativo (seguindo a convenção *Conventional Commits*):

- `feat: adiciona controle de estoque no backend`
- `fix: ajusta exibição de tabela nas telas de compras`
- `docs: adiciona diagrama de arquitetura e README`
- `infra: configura banco PostgreSQL/Neon`

---

### Passos para contribuição

1. Crie uma nova branch a partir da `main` utilizando o prefixo correspondente:
   ```bash
   git checkout -b feature/nome-da-sua-feature

2. Realize as alterações e valide o comportamento localmente.

3. Adicione os arquivos modificados e crie o commit:

   ```bash
    git add .
    git commit -m "feat: descrição objetiva da alteração"
   
4. Envie a branch para o repositório remoto:

    ```bash
    git push origin feature/nome-da-sua-feature
    Abra um Pull Request (PR) direcionado à branch main no GitHub para revisão dos demais integrantes antes de realizar o merge.
    
## 13. Histórico de versões

| Versão | Data | Descrição |
| --- | --- | --- |
| `0.2.0` | 2026-05-10 | Estruturação do backend em Django, integração com banco de dados e ajuste das telas de compras e frontend. |
| `0.1.0` | 2026-01-10 | MVP inicial com telas estáticas em HTML/JS (login, dashboard, clientes, produtos e vendas) e pipeline de CI via GitHub Actions. |
| `0.0.1` | 2026-23-09 | Configuração inicial da estrutura do repositório e ambiente de desenvolvimento. |

---

## 14. Limitações e próximos passos

### Problemas conhecidos

- A comunicação entre os formulários do frontend estático e as rotas da API Django ainda necessita de ajustes finos para tratamento de erros em tempo real.
- Layout responsivo pendente de ajustes em telas com largura inferior a 360 px.
- Fluxo de recuperação e redefinição de senha ainda não envia e-mails automáticos.

### Roadmap

- [ ] Finalizar a integração completa de todas as rotas do Django com os scripts de frontend (`frontend/*.js`).
- [ ] Implementar autenticação via JWT/Sessão completa para proteção das páginas do painel.
- [ ] Adicionar suporte à exportação de relatórios de vendas e estoque nos formatos PDF e CSV.
- [ ] Concluir o deploy definitivo da aplicação e banco de dados em ambiente de nuvem (ex.: Render/Railway + Neon/PostgreSQL).

## 15. Licença, referências e contato

**Licença:** Este projeto está sob a licença **MIT**.

### Documentação complementar

- Índice da pasta `docs/`: [`docs/README.pdf`](docs/README.pdf)
- Casos de uso (diagrama + especificações): [`docs/modelagem/casos-de-uso/especificacoes-casos-de-uso.pdf`](docs/modelagem/casos-de-uso/especificacoes-casos-de-uso.pdf)
- Diagrama de classes: [`docs/modelagem/classes/diagrama-de-classes.pdf`](docs/modelagem/classes/diagrama-de-classes.pdf)
- Modelo conceitual (ER): [`docs/modelagem/banco-de-dados/diagrama-er.pdf`](docs/modelagem/banco-de-dados/diagrama-er.pdf)
- Modelo lógico: [`docs/modelagem/banco-de-dados/modelo-logico.pdf`](docs/modelagem/banco-de-dados/modelo-logico.pdf)
- Apresentação: [`docs/apresentacao.pdf`](docs/)

### Referências

- **Django Software Foundation.** Documentação Oficial do Django (v5.x). Disponível em: <https://docs.djangoproject.com/>.
- **Python Software Foundation.** Documentação Oficial da Linguagem Python. Disponível em: <https://docs.python.org/3/>.
- **MDN Web Docs.** HTML, CSS e JavaScript para Desenvolvedores Web. Mozilla Foundation. Disponível em: <https://developer.mozilla.org/>.
- **SQLite Development Team.** SQLite Documentation. Disponível em: <https://www.sqlite.org/docs.html>.
- **GitHub.** GitHub Actions Documentation: Continuous Integration & Deployment. Disponível em: <https://docs.github.com/en/actions>.

### Contato

Dúvidas sobre o projeto: kamila.gs@sempreceub.com

**Agradecimentos:** Professor Felippe Pires e materiais da disciplina.
