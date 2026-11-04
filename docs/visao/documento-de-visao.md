# Documento de Visão

## 1. Identificação do Projeto

**Projeto:** Sistema de Gestão Comercial Estrela Moda
**Instituição:** Centro Universitário de Brasília — UniCEUB
**Curso:** Ciências da Computação
**Ano:** 2026

---

## 2. Visão Geral

O projeto tem como objetivo desenvolver um sistema de gestão comercial para uma loja de roupas e acessórios, visando auxiliar no controle e na organização das principais operações internas do estabelecimento.

O sistema deverá centralizar informações relacionadas a produtos, estoque, compras, vendas, clientes, trocas, débitos, despesas e relatórios, permitindo maior organização dos dados e facilitando o acompanhamento das atividades da loja.

A solução busca reduzir a necessidade de controles manuais, facilitar a consulta das informações e fornecer à proprietária uma visão mais organizada sobre o funcionamento e o desempenho do negócio.

---

## 3. Contexto e Problema

A aplicação será desenvolvida para uma loja de roupas e acessórios cuja atividade comercial envolve a aquisição de mercadorias junto a fornecedores e posterior comercialização dos produtos aos clientes.

Atualmente, parte dos processos de controle da loja é realizada de forma manual. As informações relacionadas aos produtos, estoque, clientes com débitos e trocas são registradas em cadernos. As vendas são registradas em um caderno de caixa, no qual também são anotados os valores das vendas realizadas na modalidade fiado, sendo realizado o fechamento do caixa ao final do dia.

Também foi identificado que atualmente não existe um controle sistemático das saídas de produtos da loja. O controle das despesas é realizado por meio de planilhas eletrônicas.

Em relação aos clientes, a loja atende tanto clientes presenciais quanto clientes por meio do WhatsApp. O sistema deverá permitir o cadastro e o acompanhamento desses clientes independentemente do canal utilizado para a realização da compra.

Diante desse cenário, foi proposta a criação de um sistema de gestão comercial com o objetivo de centralizar as informações atualmente distribuídas entre cadernos e planilhas, facilitar o registro e a consulta das operações e proporcionar maior organização dos processos administrativos e comerciais da loja.

---

## 4. Justificativa

A utilização de diferentes meios de controle, como cadernos e planilhas eletrônicas, dificulta a centralização das informações e o acompanhamento das operações realizadas pela loja.

A implementação de um sistema de gestão comercial permitirá reunir essas informações em uma única solução, facilitando o registro e a consulta dos dados relacionados às operações do estabelecimento.

A solução também deverá auxiliar no acompanhamento do estoque, das vendas, dos clientes, dos débitos, das despesas e de informações consolidadas sobre a operação da loja.

---

## 5. Objetivos

### 5.1 Objetivo Geral

Desenvolver um sistema de gestão comercial destinado ao controle e à organização das principais operações internas de uma loja de roupas e acessórios.

### 5.2 Objetivos Específicos

* Centralizar as informações atualmente distribuídas entre cadernos e planilhas;
* Permitir o cadastro e gerenciamento dos produtos;
* Facilitar o acompanhamento do estoque;
* Registrar compras realizadas junto aos fornecedores;
* Registrar as vendas realizadas pela loja;
* Controlar clientes e seu histórico de compras;
* Controlar clientes que possuem débitos decorrentes de vendas a prazo;
* Registrar pagamentos relacionados aos débitos;
* Registrar e acompanhar trocas de produtos;
* Registrar e consultar despesas;
* Disponibilizar informações consolidadas por meio de dashboard e relatórios;
* Reduzir a dependência de controles manuais;
* Facilitar o acompanhamento das atividades e do desempenho da loja.

---

## 6. Público-Alvo

O sistema será destinado à utilização interna da loja de roupas e acessórios.

Os principais usuários previstos são:

* **Administradores:** responsáveis pelas atividades administrativas e de gerenciamento do sistema;
* **Funcionário:** responsável pelas atividades operacionais permitidas de acordo com suas permissões.

A solução será utilizada para apoiar as atividades de gestão e operação da loja física.

---

## 7. Stakeholders

### 7.1 Proprietária da Loja

É a principal responsável pelo negócio e participa da validação das decisões relacionadas ao sistema.

Suas principais necessidades estão relacionadas à organização da loja, acompanhamento das operações e obtenção de informações que auxiliem na gestão do negócio.

### 7.2 Sócia da Loja

Atua como stakeholder e representante da loja durante o levantamento de requisitos.

Participa das reuniões de levantamento, contribuindo com informações sobre os processos e necessidades do estabelecimento. Também poderá atuar como principal interlocutora da equipe de desenvolvimento durante determinadas etapas do projeto.

Entre seus principais interesses estão:

* melhorar a organização da loja;
* acompanhar o estoque;
* controlar vendas e compras;
* acompanhar despesas;
* obter informações para auxiliar na gestão;
* reduzir controles manuais.

### 7.3 Funcionários da Loja

São usuários potenciais do sistema e utilizarão as funcionalidades operacionais de acordo com as permissões definidas.

Entre suas necessidades estão:

* facilidade de uso;
* rapidez no registro das operações;
* consulta de produtos e estoque;
* redução de tarefas manuais.

### 7.4 Equipe de Desenvolvimento

É responsável pela análise, projeto, desenvolvimento, testes, documentação e entrega do sistema.

A equipe deverá transformar os requisitos levantados e validados junto às responsáveis pela loja em uma solução funcional, mantendo a documentação atualizada durante o desenvolvimento.

---

## 8. Escopo

A primeira versão do sistema será destinada ao gerenciamento interno das operações da loja física.

O escopo inicial contempla os seguintes módulos:

### 8.1 Produtos

Permitir o cadastro e gerenciamento das peças e acessórios comercializados pela loja, incluindo informações como nome, categoria, tamanho, cor, preço e quantidade.

### 8.2 Estoque

Permitir o acompanhamento das quantidades disponíveis, registrando entradas e saídas de produtos e sinalizando situações de estoque baixo.

### 8.3 Registro de Compras

Permitir o registro das compras de mercadorias realizadas junto aos fornecedores para abastecimento da loja, incluindo produtos adquiridos, quantidades e valores.

### 8.4 Vendas

Permitir o registro das vendas realizadas, incluindo produtos, quantidades, descontos e formas de pagamento, realizando a atualização correspondente do estoque.

O módulo também deverá permitir o registro de vendas realizadas a prazo, possibilitando identificar o cliente, o valor total da venda, o valor já pago e o valor pendente.

### 8.5 Dashboard

Apresentar um resumo das principais informações da loja, incluindo informações relacionadas às vendas, produtos em estoque, produtos com estoque baixo e demais indicadores definidos para o sistema.

### 8.6 Clientes

Permitir o cadastro básico de clientes e a consulta de seu histórico de compras.

### 8.7 Clientes com Débitos

Permitir o controle de clientes que realizam compras a prazo, possibilitando consultar as vendas realizadas, os valores pagos, os valores pendentes e o histórico de pagamentos.

### 8.8 Trocas

Permitir o registro de trocas de produtos e a realização das respectivas atualizações no estoque.

### 8.9 Controle de Despesas

Permitir o registro e acompanhamento dos gastos relacionados à operação e manutenção da loja que não correspondem à aquisição de mercadorias para revenda.

### 8.10 Relatórios

Permitir a visualização de informações consolidadas para auxiliar no acompanhamento da loja, como produtos mais vendidos, vendas realizadas, estoque baixo e informações financeiras estimadas.

---

## 9. Fora do Escopo

A primeira versão do sistema não contemplará:

* loja virtual para realização de vendas pela internet;
* funcionalidades de e-commerce;
* demais funcionalidades externas que não façam parte do gerenciamento interno da loja.

O sistema será inicialmente destinado ao gerenciamento das operações da loja física.

---

## 10. Principais Funcionalidades

As principais funcionalidades previstas para o sistema são:

* cadastro, consulta e gerenciamento de produtos;
* organização dos produtos por categorias e variações;
* identificação dos produtos por códigos;
* consulta e controle de estoque;
* registro de entradas e saídas de produtos;
* registro de compras;
* registro de vendas;
* aplicação de descontos conforme as regras da loja;
* registro das formas de pagamento;
* registro de vendas a prazo;
* cadastro e consulta de clientes;
* consulta do histórico de compras;
* consulta de clientes com débitos;
* consulta de valores pendentes;
* registro de pagamentos de débitos;
* consulta do histórico de pagamentos;
* registro de trocas;
* atualização do estoque após as operações correspondentes;
* registro e consulta de despesas;
* dashboard com informações gerenciais;
* emissão de relatórios.

---

## 11. Usuários e Controle de Acesso

O sistema deverá contemplar os perfis de:

* **Administrador**
* **Funcionário**

Inicialmente estão previstas três contas de administrador e uma conta de funcionário.

O acesso às funcionalidades deverá respeitar as permissões atribuídas ao perfil do usuário.

As permissões são dadas de acordo com a seguinte legenda:
* C — Create 
* R — Read 
* U — Update  
* D — Delete

### Perfis e Permissões:


| Funcionalidade       | Permissão dos Administradores |
| -------------------- | ------------------------ |
| Produtos             | CRUD                      |
| Estoque              |         RU          |
| Vendas               | CR             |
| Clientes             | CRUD             |
| Clientes com Débitos | CRU             |
| Trocas               | CRUD          |
<br>

| Funcionalidade       | Permissão do Funcionário |
| -------------------- | ------------------------ |
| Produtos             | R                       |
| Estoque              | R                       |
| Vendas               | CR           |
| Clientes             | CRU             |
| Clientes com Débitos | CRU            |
| Trocas               | CRU            |
<br>

As permissões ainda permanecem pendentes de validação.

---

## 12. Principais Regras de Negócio

Entre as regras de negócio identificadas durante o levantamento estão:

* O estoque mínimo considerado pela loja é de 1 unidade.
* As formas de pagamento utilizadas são dinheiro, Pix, cartão de débito, cartão de crédito e em débito(fiado).
* Vendas realizadas na modalidade fiado devem estar associadas ao respectivo cliente.
* Os débitos permanecem pendentes até sua quitação e não possuem prazo de vencimento definido.
* Os pagamentos realizados devem atualizar o valor pendente do débito.
* As vendas não podem ser canceladas.
* Eventuais correções ou devoluções devem ser tratadas por meio do processo de troca.
* O desconto praticado pela loja é de 5% quando solicitado pelo cliente, observadas as regras de autorização que ainda deverão ser validadas.
* Trocas somente são realizadas dentro do prazo de 30 dias.
* Não são permitidas trocas sem a etiqueta do produto.
* Não são permitidas trocas de produtos manchados ou lavados.
* Caso um produto adquirido no fiado seja danificado pelo cliente, o valor correspondente deverá ser pago pelo cliente.
* As movimentações de estoque deverão ser registradas.
* Os registros históricos das operações deverão ser preservados.
* O acesso às funcionalidades deverá respeitar as permissões associadas ao perfil do usuário.

---

## 13. Restrições

### RT01 — Escopo inicial

A primeira versão do sistema será destinada ao gerenciamento interno das operações da loja física.

### RT02 — Escopo comercial

A primeira versão do sistema não contemplará uma loja virtual para realização de vendas pela internet.

### RT03 — Dados de operação

O funcionamento dos módulos dependerá do registro correto das informações pelos usuários responsáveis.

### RT04 — Controle de acesso

O acesso às funcionalidades será condicionado ao perfil e às permissões atribuídas ao usuário.

A solução deverá contemplar três contas de administrador e uma conta de funcionário.

### RT05 — Infraestrutura

A infraestrutura necessária para hospedagem, armazenamento e execução do sistema deverá ser definida de acordo com a arquitetura e as necessidades identificadas durante o desenvolvimento.

---

## 14. Premissas

Com base no levantamento realizado, são consideradas premissas iniciais do projeto:

* O sistema será utilizado para gerenciamento interno da loja física.
* As informações utilizadas pelo sistema deverão ser registradas pelos usuários responsáveis.
* Os produtos e suas respectivas informações deverão estar cadastrados para que possam ser utilizados nas operações correspondentes.
* As regras de negócio levantadas deverão ser validadas pelas responsáveis pela loja antes da implementação definitiva.
* As permissões de acesso deverão ser definidas de acordo com os perfis de usuário.
* As especificações ainda pendentes poderão ser refinadas durante as próximas etapas do levantamento e validação.

---

## 15. Riscos Iniciais

Os seguintes pontos foram identificados como riscos ou fatores que podem impactar o desenvolvimento do sistema:

| Risco                                                          | Possível impacto                                                 |
| -------------------------------------------------------------- | ---------------------------------------------------------------- |
| Requisitos ainda pendentes de validação                        | Alterações nas funcionalidades e no desenvolvimento              |
| Regras financeiras ainda não definidas                         | Alterações no dashboard e nos relatórios                         |
| Permissões dos administradores e funcionários ainda pendentes de validação            | Alterações no controle de acesso                                 |
| Categorias de despesas ainda não definidas                     | Alterações no módulo de despesas                              |
| Regras detalhadas de trocas ainda pendentes                          | Alterações no módulo de trocas e no controle de estoque                              |
| Tempo máximo de resposta ainda não definido                    | Dificuldade para estabelecer critérios específicos de desempenho |
| Dependência do registro correto das informações pelos usuários | Possibilidade de dados inconsistentes ou incompletos             |

---

## 16. Critérios de Sucesso

O sistema será considerado adequado aos objetivos iniciais quando:

* centralizar as principais informações relacionadas às operações da loja;
* permitir o registro e a consulta das operações contempladas no escopo;
* permitir o acompanhamento dos produtos e do estoque;
* permitir o registro e acompanhamento das vendas;
* permitir o cadastro e consulta dos clientes;
* permitir o acompanhamento dos clientes com débitos;
* permitir o registro e consulta dos pagamentos de débitos;
* permitir o registro das trocas conforme as regras definidas;
* permitir o registro e acompanhamento das despesas;
* disponibilizar informações consolidadas para auxiliar o acompanhamento da loja;
* respeitar os perfis e permissões de acesso definidos;
* reduzir a dependência dos controles manuais atualmente utilizados pela loja.

Os critérios poderão ser refinados conforme os requisitos forem validados e o sistema for desenvolvido.

---

## 17. Situação Atual e Pontos a Validar

O levantamento de requisitos é realizado de forma incremental. Algumas definições ainda dependem de validação com as responsáveis pela loja.

Entre os principais pontos pendentes estão:

* requisitos de infraestrutura, hospedagem e disponibilidade;
* tempo máximo de resposta para operações críticas;
* indicadores financeiros e respectivas fórmulas de cálculo;
* categorias de despesas;
* autorização para aplicação do desconto de 5%;
* comportamento do estoque após trocas;
* tratamento de diferenças de preço em trocas;
* registro do motivo da troca;
* possibilidade de troca por produto de categoria diferente;
* tratamento de vendas realizadas no fiado quando ocorre uma troca;
* demais especificações elaboradas a partir do levantamento que ainda não foram formalmente validadas.

Esses pontos deverão ser analisados e incorporados à documentação conforme forem definidos e validados.

---

## 18. Rastreabilidade da Documentação

Este Documento de Visão serve como referência para os demais artefatos do projeto.

A partir dele deverão ser detalhados:

* **Requisitos:** funcionalidades e regras necessárias ao sistema;
* **Casos de uso:** interações entre os usuários e o sistema;
* **Arquitetura:** organização dos componentes e tecnologias utilizadas;
* **Modelo de dados:** estrutura das informações armazenadas;
* **API:** recursos e operações disponibilizados pelo sistema;
* **Protótipos:** representação das principais interfaces;
* **Planejamento:** tarefas, responsáveis, riscos e evolução do projeto.

Os artefatos deverão permanecer alinhados às definições validadas durante o levantamento de requisitos.

---

## 19. Histórico de Validação

As informações deste documento são baseadas no escopo inicial do projeto e no levantamento de requisitos realizado com as responsáveis pela loja.

**Entrevista registrada:**

* **Data:** 09/09/2026
* **Participantes:** Sócia da loja e Engenheira de Requisitos
* **Técnica:** Entrevista
* **Objetivo:** Levantar e esclarecer informações sobre os processos atualmente realizados pela loja, identificar necessidades do negócio e detalhar os requisitos do sistema.

As informações que ainda não foram validadas estão identificadas neste documento como pontos pendentes e deverão ser atualizadas conforme novas decisões forem tomadas.
