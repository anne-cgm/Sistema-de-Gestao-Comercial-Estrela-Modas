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
| **Framework Backend** | Django | Estrutura `settings.py` / `urls.py`[cite: 1] |
| **Frontend** | HTML5 / JavaScript (Vanilla) | Páginas estáticas e scripts de interface[cite: 1] |
| **Banco de Dados** | SQLite | `db.sqlite3`[cite: 1] |
| **Gerenciador de Pacotes** | npm (Node.js) | `package-lock.json` / `node_modules`[cite: 1] |
| **CI/CD & Automação** | GitHub Actions | Workflows de integração contínua (`ci.yml`)[cite: 1] |
| **Controle de Versão** | Git | —[cite: 1] |

---

## 5. Arquitetura

O sistema adota uma arquitetura em **camadas bem definidas**, garantindo o desacoplamento entre a interface de usuário, as regras de negócio e a persistência de dados. O fluxo de comunicação é síncrono e baseado no protocolo HTTP/HTTPS, onde a camada de apresentação consome uma API REST exposta pelo servidor backend.

### Camadas do Sistema

1. **Camada de Apresentação (Frontend):**
   * Desenvolvida em **HTML5 e JavaScript Vanilla**, sendo responsável por renderizar a interface e interagir com o usuário.
   * Contém telas estruturadas para fluxos específicos, tais como autenticação (`login.html`), painel principal (`dashboard.html`), gerenciamento de utilizadores (`users.html`), produtos (`products.html`), clientes (`customers.html`) e vendas (`sales.html`)[cite: 1].
   * Consome as rotas do backend através de requisições HTTP (API REST).

2. **Camada de Aplicação e Negócio (Backend):**
   * Desenvolvida em **Python** utilizando o framework **Django**[cite: 1].
   * O módulo `config` centraliza as definições do projeto (`settings.py`) e a estrutura de rotas (`urls.py`)[cite: 1].
   * Processa as requisições HTTP recebidas, executa as validações e regras de negócio do sistema e coordena a comunicação com o banco de dados.

3. **Camada de Persistência (Banco de Dados):**
   * Utiliza o banco de dados relacional **SQLite** (`db.sqlite3`)[cite: 1].
   * Armazena os dados do sistema, incluindo utilizadores, produtos, clientes e histórico de vendas.

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
│  HTML / JS (login, dashboard, etc.)     │[cite: 1]
└────────────────────┬────────────────────┘
                     │  Requisições HTTP / REST API
                     ▼
┌─────────────────────────────────────────┐
│     Aplicação & Negócio (Backend)       │
│      Django (urls.py / settings.py)     │[cite: 1]
└────────────────────┬────────────────────┘
                     │  ORM / Consultas SQL
                     ▼
┌─────────────────────────────────────────┐
│       Persistência (Banco)              │
│       SQLite3 (db.sqlite3)              │[cite: 1]
└─────────────────────────────────────────┘
**Decisões relevantes:**

- [Ex.: uso de API REST para separar cliente e servidor.]
- [Ex.: persistência relacional porque os dados possuem relacionamentos bem definidos.]

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

```text
.
├── README.md                 # Documentação principal do projeto
├── .env.example              # Modelo de variáveis de ambiente (sem segredos)
├── docs/                     # Modelagem e demais artefatos técnicos (PDF)
│   ├── README.pdf            # Índice da pasta docs/
│   └── modelagem/
│       ├── casos-de-uso/
│       │   └── especificacoes-casos-de-uso.pdf
│       ├── classes/
│       │   └── diagrama-de-classes.pdf
│       └── banco-de-dados/
│           ├── diagrama-er.pdf
│           └── modelo-logico.pdf
├── images/                   # Figuras da documentação geral (ex.: política de IA)
├── src/                      # Código-fonte da aplicação
│   ├── frontend/             # Interface com o usuário (quando houver)
│   └── backend/              # Regras de negócio, API e acesso a dados (quando houver)
├── tests/                    # Testes automatizados
└── scripts/                  # Scripts auxiliares de setup, build ou deploy
```

| Diretório / arquivo | Função |
| --- | --- |
| `README.md` | Apresentação do projeto, objetivos, tecnologias e instruções de uso |
| `.env.example` | Lista das variáveis necessárias, sem credenciais reais |
| `docs/` | Artefatos de análise e modelagem em PDF |
| `docs/modelagem/` | Casos de uso, classes e modelo de dados (diagramas embutidos nos PDFs) |
| `images/` | Figuras da documentação geral do repositório (não usar para diagramas de modelagem) |
| `src/` | Código-fonte organizado por camada ou módulo |
| `tests/` | Casos de teste e evidências de verificação |
| `scripts/` | Automação de ambiente e execução |

---
 
## 7. Participantes

| Nome | Matrícula | Função no projeto |
| --- | --- | --- |
| Sciel Ramos RodriguesBuitrago | [000000] | backend / testes |
| Kamila Gomes da Silva | [22503734] | frontend / documentação |
| Anna Nicolly da Silva | [000000] | backend / documentação |
| Anne Caroline Gonçalves de Mesquita | [000000] | backend / documentação / frontend |

**Professor(a) responsável:** Felippe Pires

---

## 8. Como executar

Siga as instruções abaixo para configurar e executar o projeto localmente.

### Pré-requisitos

- **Git**
- **Python 3.14+**
- **Node.js** e **npm**

---

### Instalação e execução

```bash
# 1. Clonar o repositório
git clone <URL_DO_REPOSITORIO>
cd <NOME_DA_PASTA>

# 2. Configurar o ambiente virtual do Python e instalar dependências do Backend
python -m venv venv

# No Linux/macOS:
source venv/bin/activate
# No Windows (Command Prompt):
# venv\Scripts\activate

# 3. Instalar dependências do Frontend/Node.js
npm install[cite: 1]

# 4. Executar as migrações do banco de dados (SQLite)
python backend/manage.py migrate[cite: 1]

# 5. Executar a aplicação (Servidor Django)
python backend/manage.py runserver[cite: 1]

### Pré-requisitos

- [Ex.: Git]
- [Ex.: Python 3.12+]
- [Ex.: Node.js 20+]
- [Ex.: Docker]

### Instalação e execução

```bash
# 1. Clonar o repositório
git clone [URL_DO_REPOSITORIO]
cd [NOME_DA_PASTA]

# 2. Instalar dependências
[comando de instalação]

# 3. Configurar variáveis de ambiente
cp .env.example .env
# edite o arquivo .env com as credenciais locais

# 4. Executar a aplicação
[comando de execução]
```

**Acesso local:** 

 - Backend / API: http://127.0.0.1:8000

 - Frontend: Abra os arquivos HTML da pasta frontend/ (como frontend/login.html ou frontend/dashboard.html) diretamente no navegador ou utilize uma extensão de servidor estático (como o Live Server do VS Code)

### Implantação 

- **Ambiente:** GitHub Actions / GitHub Pages 
- **URL de produção:** (https://github.com/anne-cgm/Sistema-de-Gestao-Comercial-Estrela-Modas)
- **Observações:** O projeto possui pipeline de CI/CD configurada no GitHub Actions via `.github/workflows/ci.yml`. Para ambiente de produção em nuvem (ex.: Render, Railway ou Vercel), é necessário configurar as variáveis de ambiente e ajustar as permissões de CORS no Django (`settings.py`)

## 9. Configuração

O sistema utiliza variáveis de ambiente para gerenciar as configurações do framework Django e as conexões da aplicação. As variáveis abaixo devem ser definidas em um arquivo `.env` na raiz do projeto (não versionado):

| Variável | Obrigatória | Descrição | Exemplo |
| --- | --- | --- | --- |
| `SECRET_KEY` | Sim | Chave secreta de segurança do Django | `django-insecure-chave-secreta-aqui` |
| `DEBUG` | Sim | Ativa/desativa o modo de depuração (`True` para dev, `False` para prod) | `True` |
| `ALLOWED_HOSTS` | Sim | Lista de hosts/domínios permitidos para servir a aplicação | `localhost,127.0.0.1` |
| `DATABASE_URL` | Não | String de conexão com o banco de dados (padrão local: SQLite) | `sqlite:///db.sqlite3`|
| `PORT` | Não | Porta em que o servidor web irá executar | `8000`|

*Credenciais reais e chaves secretas devem ficar apenas no arquivo `.env` local e jamais serem commitadas no repositório.*

## 10. Testes

Os testes da aplicação cobrem as validações do backend em Django e as rotas de automação configuradas na pipeline de CI/CD via GitHub Actions (`ci.yml`).

``bash
# Executar a suíte de testes unitários e de integração do Django
python backend/manage.py test

| Tipo | Ferramenta | O que verifica |
| --- | --- | --- |
| Unitários | Django Test Runner/unittest | Regras de negócio, métodos de modelos e validações isoladas do backend |
| Integração | Django Test Client | Respostas das rotas da API REST, códigos de status HTTP e persistência com o banco SQLite (db.sqlite3) |
| Automação/CI | GitHub Actions (ci.yml) | Execução automática do build e testes a cada push ou pull request na pipeline |
| Manuais | Checklist local | Fluxo de navegação e chamadas JS nas páginas estáticas em frontend/ |

**Cobertura atual:** A definir / em expansão via suíte nativa do Django.

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
