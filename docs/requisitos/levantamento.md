# Levantamento de Requisitos

## 1. Identificação

**Projeto:** Sistema de Gestão Comercial Estrela Moda
**Instituição:** Centro Universitário de Brasília — UniCEUB
**Curso:** Ciências da Computação
**Ano:** 2026

---

## 2. Objetivo do Levantamento

O levantamento de requisitos tem como objetivo identificar e compreender as necessidades da loja em relação ao controle de suas operações internas, servindo como base para a definição dos requisitos do sistema.

Foram analisados os processos atualmente realizados pela loja, os controles utilizados, as necessidades identificadas pelas responsáveis e as regras de negócio informadas durante as etapas de levantamento.

---

## 3. Metodologia de Elicitação

A elicitação de requisitos é realizada de forma incremental, tendo como ponto de partida o escopo inicial elaborado pela equipe do projeto.

A principal técnica utilizada é a **entrevista**, realizada com as responsáveis pela loja. A sócia participa diretamente do levantamento por possuir conhecimento sobre os processos relacionados ao funcionamento do estabelecimento, enquanto a proprietária participa das etapas de levantamento e validação conforme a necessidade.

As informações obtidas durante as entrevistas são analisadas e utilizadas para detalhar os requisitos do sistema. Decisões tomadas durante o levantamento são registradas na documentação, enquanto pontos que ainda dependem de esclarecimento permanecem identificados como pendentes.

Após a especificação, os requisitos deverão ser submetidos à validação das responsáveis pela loja.

---

## 4. Entrevista Realizada

### 4.1 Informações da Entrevista

| Informação                    | Registro                                                                                                                                                       |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Data**                      | 09/09/2026                                                                                                                                                     |
| **Participantes**             | Sócia da loja e Engenheira de Requisitos                                                                                                                       |
| **Técnica**                   | Entrevista                                                                                                                                                     |
| **Responsável pelo registro** | Engenheira de Requisitos                                                                                                                                       |
| **Objetivo**                  | Levantar e esclarecer informações sobre os processos atualmente realizados pela loja, identificar necessidades do negócio e detalhar os requisitos do sistema. |

---

## 5. Situação Atual

Durante o levantamento, foram identificadas as seguintes formas de controle utilizadas atualmente pela loja:

* produtos registrados em caderno;
* controle de estoque realizado em caderno;
* informações de clientes com débitos registradas em caderno;
* trocas registradas em caderno;
* vendas registradas em caderno de caixa;
* vendas realizadas na modalidade fiado registradas no controle de caixa;
* fechamento do caixa realizado ao final do dia;
* ausência de controle sistemático das saídas de produtos;
* despesas controladas por meio de planilhas eletrônicas.

Também foi identificado que a loja atende clientes presencialmente e por meio do WhatsApp.

---

## 6. Informações Identificadas

### 6.1 Produtos

Durante o levantamento, foram identificadas necessidades relacionadas ao cadastro e à identificação dos produtos comercializados pela loja.

Foram consideradas informações como:

* nome do produto;
* categoria;
* tamanho;
* cor;
* preço;
* quantidade;
* identificação dos produtos por códigos;
* possibilidade de utilização de código para identificação e consulta.

As informações mais detalhadas sobre a estrutura dos produtos deverão ser consolidadas nos requisitos e no modelo de dados, conforme forem validadas.

### 6.2 Estoque

Foi identificada a necessidade de controlar as quantidades disponíveis dos produtos.

A loja considera **1 unidade como estoque mínimo** para fins de identificação de estoque baixo.

Também foi identificada a necessidade de registrar as movimentações relacionadas à entrada e saída de produtos.

### 6.3 Compras

Foi identificada a necessidade de registrar as compras de mercadorias realizadas junto aos fornecedores.

O registro deverá considerar, no mínimo:

* produtos adquiridos;
* quantidades;
* valor da compra.

### 6.4 Vendas

Foi identificada a necessidade de registrar as vendas realizadas pela loja.

As operações devem considerar:

* produtos vendidos;
* quantidades;
* valores;
* desconto, quando aplicável;
* forma de pagamento.

As formas de pagamento identificadas são:

* dinheiro;
* Pix;
* cartão de débito;
* cartão de crédito;
* fiado.

As vendas realizadas na modalidade fiado devem estar associadas ao respectivo cliente.

### 6.5 Clientes

Foi identificada a necessidade de manter informações cadastrais dos clientes e possibilitar a consulta de seu histórico de compras.

O cadastro deverá permitir o acompanhamento dos clientes independentemente do canal utilizado para a realização da compra.

### 6.6 Clientes com Débitos

Foi identificada a necessidade de controlar clientes que possuem valores pendentes decorrentes de vendas realizadas na modalidade fiado.

O controle deverá permitir consultar:

* valor da venda;
* valor pago;
* valor pendente;
* pagamentos realizados.

Foi informado que os débitos não possuem prazo de vencimento definido.

### 6.7 Trocas

Foi identificada a necessidade de registrar as trocas realizadas pela loja e atualizar as informações relacionadas ao estoque.

As regras informadas para realização de trocas são:

* prazo de até 30 dias;
* apresentação da etiqueta do produto;
* produto não pode estar manchado;
* produto não pode ter sido lavado.

Também foi informado que, caso um produto adquirido no fiado seja danificado pelo cliente, o valor correspondente deverá ser pago pelo cliente.

### 6.8 Despesas

Foi identificada a necessidade de registrar e acompanhar as despesas relacionadas à operação da loja.

Atualmente, esse controle é realizado por meio de planilhas eletrônicas.

As categorias de despesas ainda não foram definidas.

### 6.9 Dashboard e Relatórios

Foi identificada a necessidade de disponibilizar informações consolidadas para auxiliar o acompanhamento da loja.

Entre as informações inicialmente identificadas estão:

* histórico diário de vendas;
* lucro mensal;
* produtos mais vendidos no mês;
* produtos com estoque baixo;
* relatórios relacionados às operações da loja.

As fórmulas e indicadores financeiros ainda dependem de definição e validação.

---

## 7. Regras e Decisões Identificadas

Durante o levantamento, foram identificadas as seguintes regras e decisões:

1. O estoque mínimo considerado pela loja é de 1 unidade.
2. As formas de pagamento são dinheiro, Pix, cartão de débito, cartão de crédito e fiado.
3. Vendas realizadas na modalidade fiado devem estar associadas ao respectivo cliente.
4. Os débitos permanecem pendentes até sua quitação.
5. Os débitos não possuem prazo de vencimento definido.
6. Os pagamentos realizados devem atualizar o valor pendente.
7. As vendas não podem ser canceladas.
8. Eventuais correções ou devoluções devem ser tratadas por meio do processo de troca.
9. O desconto praticado pela loja é de 5% quando solicitado pelo cliente.
10. A autorização para aplicação do desconto ainda depende de validação.
11. Trocas somente são realizadas dentro do prazo de 30 dias.
12. Não são permitidas trocas sem a etiqueta do produto.
13. Não são permitidas trocas de produtos manchados ou lavados.
14. Caso um produto adquirido no fiado seja danificado pelo cliente, o valor correspondente deverá ser pago pelo cliente.

---

## 8. Usuários e Permissões

Foram identificados dois perfis de usuário:

* Administrador;
* Funcionário.

Inicialmente estão previstas:

* três contas de administrador;
* uma conta de funcionário.

As permissões foram definidas preliminarmente durante o levantamento e deverão ser validadas pelas responsáveis pela loja.

### 8.1 Permissões dos Administradores

| Funcionalidade       | Permissão |
| -------------------- | --------- |
| Produtos             | CRUD      |
| Estoque              | RU        |
| Vendas               | CR        |
| Clientes             | CRUD      |
| Clientes com Débitos | CRU       |
| Trocas               | CRUD      |

### 8.2 Permissões do Funcionário

| Funcionalidade       | Permissão |
| -------------------- | --------- |
| Produtos             | R         |
| Estoque              | R         |
| Vendas               | CR        |
| Clientes             | CRU       |
| Clientes com Débitos | CRU       |
| Trocas               | CRU       |

**Legenda:** C — Create; R — Read; U — Update; D — Delete.

---

## 9. Pontos Pendentes de Validação

Os seguintes pontos ainda dependem de esclarecimento ou validação com as responsáveis pela loja:

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
* validação das permissões dos administradores e do funcionário;
* demais especificações elaboradas a partir do levantamento que ainda não foram formalmente validadas.

---

## 10. Observações

O levantamento de requisitos possui caráter incremental. Dessa forma, novas informações obtidas durante as próximas etapas poderão complementar ou alterar os requisitos atualmente documentados.

As alterações deverão ser registradas na documentação e consideradas nos artefatos relacionados ao projeto, mantendo a rastreabilidade entre levantamento, requisitos, casos de uso, arquitetura, modelo de dados e API.

---

## 11. Histórico

| Data       | Alteração                                                                             |
| ---------- | ------------------------------------------------------------------------------------- |
| 09/09/2026 | Realização da entrevista inicial e levantamento das necessidades e processos da loja. |
| 2026       | Consolidação das informações levantadas na documentação do projeto.                   |
