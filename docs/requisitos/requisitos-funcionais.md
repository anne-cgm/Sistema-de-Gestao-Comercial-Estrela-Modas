# Requisitos Funcionais

## 1. Identificação

**Projeto:** Sistema de Gestão Comercial Estrela Moda
**Instituição:** Centro Universitário de Brasília — UniCEUB
**Curso:** Ciências da Computação
**Ano:** 2026

---

## 2. Objetivo

Este documento apresenta os requisitos funcionais identificados para o Sistema de Gestão Comercial Estrela Moda.

Os requisitos descrevem as funcionalidades que o sistema deverá disponibilizar para apoiar o gerenciamento interno da loja.

Os requisitos ainda sujeitos a validação deverão ser ajustados conforme novas definições forem obtidas durante o levantamento.

---

## 3. Requisitos Funcionais

### 3.1 Produtos

**RF01 — Cadastrar produto**
O sistema deverá permitir ao usuário autorizado cadastrar produtos, informando seus dados de identificação e demais informações necessárias.

**RF02 — Classificar produto**
O sistema deverá permitir classificar os produtos por categoria, subcategoria e tipo.

**RF03 — Registrar características do produto**
O sistema deverá permitir registrar características dos produtos, como material e estilo, além de outras informações técnicas definidas para o cadastro.

**RF04 — Registrar preços do produto**
O sistema deverá permitir registrar o preço de custo e o preço de venda dos produtos e calcular automaticamente a margem ou MVA, conforme a fórmula definida para o sistema.

**RF05 — Cadastrar variações do produto**
O sistema deverá permitir cadastrar variações de um produto, considerando informações como tamanho e cor.

**RF06 — Identificar variação por SKU**
O sistema deverá permitir associar um código SKU específico a cada variação de produto.

**RF07 — Consultar produtos**
O sistema deverá permitir pesquisar e consultar produtos cadastrados.

**RF08 — Identificar produto por QR Code**
O sistema deverá permitir identificar um produto ou variação por meio da leitura de seu QR Code.

**RF09 — Consultar informações do produto**
O sistema deverá apresentar as informações cadastradas do produto e de suas respectivas variações.

**RF10 — Consultar produto por QR Code**
O sistema deverá permitir acessar as informações do produto a partir da leitura de seu QR Code.

**RF11 — Alterar dados do produto**
O sistema deverá permitir que usuários com permissão alterem os dados dos produtos cadastrados.

**RF12 — Controlar disponibilidade do produto**
O sistema deverá permitir controlar a disponibilidade dos produtos para utilização nas operações de venda.

**RF13 — Adicionar produto ao PDV por meio do QR Code**
O sistema deverá permitir que usuários autenticados e autorizados adicionem um produto ao PDV a partir de sua ficha identificada por QR Code.

---

### 3.2 Estoque

**RF14 — Consultar estoque**
O sistema deverá permitir consultar as quantidades disponíveis dos produtos.

**RF15 — Registrar entrada de estoque**
O sistema deverá permitir registrar entradas de produtos no estoque.

**RF16 — Registrar saída de estoque**
O sistema deverá permitir registrar saídas de produtos do estoque.

**RF17 — Atualizar estoque**
O sistema deverá atualizar as quantidades disponíveis de acordo com as operações que movimentarem o estoque.

**RF18 — Identificar estoque baixo**
O sistema deverá identificar produtos cuja quantidade disponível seja igual ou inferior ao estoque mínimo definido pela loja, considerando inicialmente 1 unidade.

---

### 3.3 Registro de Compras

**RF19 — Registrar compra**
O sistema deverá permitir registrar compras de mercadorias realizadas junto aos fornecedores.

**RF20 — Registrar produtos adquiridos**
O sistema deverá permitir registrar os produtos e as respectivas quantidades adquiridas em uma compra.

**RF21 — Registrar valor da compra**
O sistema deverá permitir registrar o valor total da compra realizada.

**RF22 — Atualizar estoque após compra**
O sistema deverá atualizar o estoque após o registro de uma compra de mercadorias.

---

### 3.4 Vendas

**RF23 — Registrar venda**
O sistema deverá permitir registrar uma venda realizada pela loja.

**RF24 — Registrar itens da venda**
O sistema deverá permitir registrar os produtos e as respectivas quantidades presentes em uma venda.

**RF25 — Aplicar desconto**
O sistema deverá permitir aplicar desconto de 5% quando solicitado pelo cliente, observadas as regras de autorização definidas pela loja.

**RF26 — Registrar forma de pagamento**
O sistema deverá permitir registrar a forma de pagamento utilizada na venda.

As formas identificadas são:

* dinheiro;
* Pix;
* cartão de débito;
* cartão de crédito;
* fiado.

**RF27 — Atualizar estoque após venda**
O sistema deverá atualizar as quantidades disponíveis dos produtos após o registro de uma venda.

**RF28 — Registrar venda fiado**
O sistema deverá permitir registrar uma venda na modalidade fiado e associá-la ao respectivo cliente.

---

### 3.5 Dashboard

**RF29 — Consultar histórico diário de vendas**
O sistema deverá apresentar o histórico das vendas realizadas por dia.

**RF30 — Consultar lucro mensal**
O sistema deverá apresentar o lucro mensal conforme os critérios e fórmulas financeiras definidos e validados para o sistema.

**RF31 — Consultar produtos mais vendidos**
O sistema deverá apresentar os produtos mais vendidos no período mensal.

**RF32 — Consultar produtos com estoque baixo**
O sistema deverá apresentar os produtos identificados com estoque baixo.

---

### 3.6 Clientes

**RF33 — Cadastrar cliente**
O sistema deverá permitir cadastrar clientes.

**RF34 — Consultar dados do cliente**
O sistema deverá permitir consultar os dados cadastrais dos clientes.

**RF35 — Consultar histórico de compras do cliente**
O sistema deverá permitir consultar o histórico de compras associado a um cliente.

---

### 3.7 Clientes com Débitos

**RF36 — Consultar clientes com débitos**
O sistema deverá permitir consultar os clientes que possuem valores pendentes decorrentes de vendas realizadas na modalidade fiado.

**RF37 — Consultar débito do cliente**
O sistema deverá permitir consultar os valores relacionados aos débitos de um cliente, incluindo valores pagos e valores pendentes.

**RF38 — Registrar pagamento de débito**
O sistema deverá permitir registrar pagamentos realizados pelo cliente para quitação de valores pendentes.

**RF39 — Atualizar valor pendente**
O sistema deverá atualizar o valor pendente do débito após o registro de um pagamento.

**RF40 — Consultar histórico de pagamentos**
O sistema deverá permitir consultar o histórico de pagamentos realizados pelo cliente para seus débitos.

---

### 3.8 Trocas

**RF41 — Registrar troca**
O sistema deverá permitir registrar uma troca de produto, respeitando as regras definidas pela loja.

**RF42 — Atualizar estoque após troca**
O sistema deverá atualizar as quantidades em estoque de acordo com os produtos envolvidos na troca.

---

### 3.9 Controle de Despesas

**RF43 — Registrar despesa**
O sistema deverá permitir registrar despesas relacionadas à operação e manutenção da loja.

**RF44 — Consultar despesas**
O sistema deverá permitir consultar as despesas registradas.

**RF45 — Classificar despesa**
O sistema deverá permitir classificar as despesas de acordo com as categorias definidas pela loja.

---

### 3.10 Relatórios

**RF46 — Gerar relatório de vendas**
O sistema deverá permitir consultar informações consolidadas sobre as vendas realizadas.

**RF47 — Gerar relatório de produtos mais vendidos**
O sistema deverá permitir consultar os produtos mais vendidos em determinado período.

**RF48 — Gerar relatório de estoque baixo**
O sistema deverá permitir consultar os produtos identificados com estoque baixo.

**RF49 — Gerar relatório financeiro estimado**
O sistema deverá permitir apresentar informações financeiras estimadas conforme os critérios e fórmulas definidos e validados para o sistema.

---

## 4. Observações sobre Validação

Os requisitos relacionados a cálculos financeiros, autorização de descontos, comportamento do estoque durante trocas, tratamento financeiro de trocas envolvendo vendas fiado e categorias de despesas dependem de definições adicionais da loja.

Essas definições deverão ser incorporadas aos requisitos correspondentes após validação.

Os requisitos relacionados às permissões dos usuários também deverão ser confrontados com a matriz de permissões validada pelas responsáveis pela loja.

---

## 5. Rastreabilidade Inicial

Os requisitos funcionais deverão ser utilizados como base para a elaboração dos demais artefatos do projeto:

* **Casos de uso:** relacionar funcionalidades aos atores do sistema;
* **Arquitetura:** identificar componentes responsáveis pela implementação das funcionalidades;
* **Modelo de dados:** identificar informações necessárias para atender aos requisitos;
* **API:** definir os recursos e operações necessários;
* **Protótipos:** representar as principais funcionalidades nas interfaces;
* **Backlog:** decompor os requisitos em tarefas de desenvolvimento.
