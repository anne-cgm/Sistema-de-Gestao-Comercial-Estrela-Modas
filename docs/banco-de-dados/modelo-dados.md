# Documentação do Modelo de Dados (EER)

Esta documentação descreve a modelagem de dados do sistema, detalhando suas entidades, atributos, chaves primárias/estrangeiras e relacionamentos de cardinalidade.

---

## 1. Visão Geral das Entidades

O sistema está estruturado nos seguintes módulos principais:
* **Cadastros Base:** `usuario`, `cliente`, `categoria`, `produto`, `variacao_produto`.
* **Estoque:** `estoque`, `movimentacao_estoque`.
* **Vendas e Trocas:** `venda`, `item_venda`, `troca`, `item_troca`.
* **Compras:** `compra`, `item_compra`.
* **Financeiro:** `debito`, `pagamento`, `despesa`.

---

## 2. Dicionário de Dados

### 2.1. Usuários e Clientes

#### `usuario`
Armazena os usuários/operadores do sistema.
* **`id`** (`INT`, PK, Auto-increment) - Identificador único do usuário.
* **`nome`** (`VARCHAR(255)`) - Nome completo do usuário.
* **`senha`** (`VARCHAR(255)`) - Hash da senha de acesso.
* **`login`** (`VARCHAR(100)`) - Login de acesso ao sistema.
* **`ativo`** (`TINYINT(1)`) - Indica se o usuário está ativo (1) ou inativo (0).

#### `cliente`
Armazena as informações dos clientes.
* **`id`** (`INT`, PK, Auto-increment) - Identificador único do cliente.
* **`nome`** (`VARCHAR(255)`) - Nome completo do cliente.
* **`telefone`** (`VARCHAR(20)`) - Telefone de contato.

---

### 2.2. Produtos, Variações e Categorias

#### `categoria`
Agrupa produtos em categorias.
* **`id`** (`INT`, PK, Auto-increment) - Identificador da categoria.
* **`nome`** (`VARCHAR(100)`) - Nome da categoria.
* **`descricao`** (`TEXT`) - Descrição detalhada da categoria.

#### `produto`
Representa os produtos cadastrados.
* **`id`** (`INT`, PK, Auto-increment) - Identificador único do produto.
* **`sku_pai`** (`VARCHAR(50)`) - Código SKU pai para agrupamento.
* **`nome`** (`VARCHAR(255)`) - Nome do produto.
* **`descricao`** (`TEXT`) - Descrição do produto.
* **`material`** (`VARCHAR(100)`) - Composição do material.
* **`estampa`** (`VARCHAR(100)`) - Padrão de estampa.
* **`composicao`** (`VARCHAR(100)`) - Detalhes adicionais de composição.
* **`preco_custo`** (`DECIMAL(10,2)`) - Valor de custo do produto.
* **`preco_venda`** (`DECIMAL(10,2)`) - Valor padrão de venda.
* **`status`** (`TINYINT(1)`) - Status de disponibilidade.
* **`categoria_id`** (`INT`, FK) - Referência à tabela `categoria`.

#### `variacao_produto`
Gerencia variações de tamanho, cor e SKU de um produto pai.
* **`id`** (`INT`, PK, Auto-increment) - Identificador da variação.
* **`sku`** (`VARCHAR(50)`) - SKU específico da variação.
* **`tamanho`** (`VARCHAR(20)`) - Tamanho do produto (ex: P, M, G, 40).
* **`cor`** (`VARCHAR(50)`) - Cor da variação.
* **`codigo_qr`** (`VARCHAR(255)`) - Código QR / código de barras impresso na etiqueta.
* **`produto_id`** (`INT`, FK) - Referência à tabela `produto`.

---

### 2.3. Estoque e Movimentação

#### `estoque`
Controla a quantidade disponível e mínima por variação de produto.
* **`id`** (`INT`, PK, Auto-increment) - Identificador do registro de estoque.
* **`quantidade`** (`INT`) - Quantidade física disponível.
* **`minimo`** (`INT`) - Estoque mínimo para alerta de reposição.
* **`variacao_produto_id`** (`INT`, FK) - Referência à tabela `variacao_produto`.

#### `movimentacao_estoque`
Registra todo o histórico de entradas, saídas ou ajustes.
* **`id`** (`INT`, PK, Auto-increment) - Identificador da movimentação.
* **`tipo`** (`VARCHAR(50)`) - Tipo de movimentação (ex: Entrada, Saída, Ajuste).
* **`quantidade`** (`INT`) - Quantidade movimentada.
* **`data_hora`** (`DATETIME`) - Registro de data e hora do evento.
* **`estoque_id`** (`INT`, FK) - Referência à tabela `estoque`.

---

### 2.4. Compras (Entrada de Mercadoria)

#### `compra`
Registra os pedidos/notas de compra de estoque.
* **`id`** (`INT`, PK, Auto-increment) - Identificador da compra.
* **`data`** (`DATE`) - Data em que a compra foi realizada.
* **`valorTotal`** (`DECIMAL(10,2)`) - Valor total da ordem de compra.
* **`usuario_id`** (`INT`, FK) - Usuário responsável por registrar a compra.

#### `item_compra`
Itens vinculados a uma compra.
* **`id`** (`INT`, PK, Auto-increment) - Identificador do item da compra.
* **`quantidade`** (`INT`) - Quantidade comprada.
* **`valor_unitario`** (`DECIMAL(10,2)`) - Preço pago por unidade.
* **`subtotal`** (`DECIMAL(10,2)`) - Subtotal (`quantidade * valor_unitario`).
* **`compra_id`** (`INT`, FK) - Referência à tabela `compra`.
* **`variacao_produto_id`** (`INT`, FK) - Referência à tabela `variacao_produto`.

---

### 2.5. Vendas e Trocas

#### `venda`
Registra as operações de venda do sistema.
* **`id`** (`INT`, PK, Auto-increment) - Identificador único da venda.
* **`data_hora`** (`DATETIME`) - Data e hora de conclusão da venda.
* **`subtotal`** (`DECIMAL(10,2)`) - Soma dos valores dos itens antes do desconto.
* **`desconto`** (`DECIMAL(10,2)`) - Valor total de desconto aplicado.
* **`valor_total`** (`DECIMAL(10,2)`) - Valor final cobrado.
* **`forma_pagamento`** (`VARCHAR(50)`) - Forma de pagamento utilizada.
* **`usuario_id`** (`INT`, FK) - Operador/Usuário que realizou a venda.
* **`cliente_id`** (`INT`, FK, Nullable) - Cliente associado à venda.

#### `item_venda`
Itens vendidos na transação.
* **`id`** (`INT`, PK, Auto-increment) - Identificador do item da venda.
* **`quantidade`** (`INT`) - Quantidade vendida.
* **`preco_unitario`** (`DECIMAL(10,2)`) - Valor cobrado por unidade.
* **`subtotal`** (`DECIMAL(10,2)`) - Subtotal do item.
* **`tipo`** (`VARCHAR(50)`) - Classificação do item no contexto da venda.
* **`venda_id`** (`INT`, FK) - Referência à tabela `venda`.
* **`variacao_produto_id`** (`INT`, FK) - Referência à tabela `variacao_produto`.

#### `troca`
Registra a solicitação de troca de itens de uma venda.
* **`id`** (`INT`, PK, Auto-increment) - Identificador da troca.
* **`data`** (`DATE`) - Data da solicitação de troca.
* **`diferenca_preco`** (`DECIMAL(10,2)`) - Valor de diferença a pagar ou devolver.
* **`possui_etiqueta`** (`TINYINT(1)`) - Se o produto trocado possui etiqueta intacta.
* **`esta_manchado_ou_lavado`** (`TINYINT(1)`) - Validação de integridade do item retornado.
* **`venda_id`** (`INT`, FK) - Venda original associada.

#### `item_troca`
Lista os itens devolvidos/substituídos durante a troca.
* **`id`** (`INT`, PK, Auto-increment) - Identificador do item trocado.
* **`quantidade`** (`INT`) - Quantidade devolvida/trocada.
* **`troca_id`** (`INT`, FK) - Referência à tabela `troca`.
* **`variacao_produto_id`** (`INT`, FK) - Referência à variação do produto devolvido.

---

### 2.6. Módulo Financeiro

#### `debito`
Registra pendências financeiras e fiados de clientes gerados por vendas.
* **`id`** (`INT`, PK, Auto-increment) - Identificador do débito.
* **`valor`** (`DECIMAL(10,2)`) - Valor original da dívida.
* **`status`** (`VARCHAR(50)`) - Status da dívida (ex: Pendente, Quitado, Parcial).
* **`saldo_pendente`** (`DECIMAL(10,2)`) - Valor restante a ser pago.
* **`venda_id`** (`INT`, FK) - Referência à tabela `venda`.
* **`cliente_id`** (`INT`, FK) - Referência à tabela `cliente`.

#### `pagamento`
Registra o abatimento/quitação dos débitos do cliente.
* **`id`** (`INT`, PK, Auto-increment) - Identificador do pagamento.
* **`valor`** (`DECIMAL(10,2)`) - Valor pago.
* **`data_hora`** (`DATETIME`) - Data e hora do pagamento.
* **`debito_id`** (`INT`, FK) - Referência ao registro de `debito`.

#### `despesa`
Registra custos e despesas operacionais registradas pelos usuários.
* **`id`** (`INT`, PK, Auto-increment) - Identificador da despesa.
* **`descricao`** (`VARCHAR(255)`) - Descrição da despesa.
* **`valor`** (`DECIMAL(10,2)`) - Valor total da despesa.
* **`data`** (`DATE`) - Data do vencimento/pagamento.
* **`categoria`** (`VARCHAR(100)`) - Categoria da despesa (ex: Aluguel, Luz, Fornecedores).
* **`usuario_id`** (`INT`, FK) - Usuário que lançou a despesa.

---

## 3. Relacionamentos e Cardinalidade

| Tabela Origem | Tabela Destino | Cardinalidade | Descrição |
| :--- | :--- | :---: | :--- |
| `categoria` | `produto` | 1 : N | Uma categoria engloba múltiplos produtos. |
| `produto` | `variacao_produto` | 1 : N | Um produto pode ter várias variações (ex: tamanhos e cores). |
| `variacao_produto` | `estoque` | 1 : 1 | Cada variação possui um controle único de estoque. |
| `estoque` | `movimentacao_estoque` | 1 : N | Um estoque pode registrar diversas movimentações ao longo do tempo. |
| `usuario` | `venda` | 1 : N | Um usuário pode realizar várias vendas. |
| `cliente` | `venda` | 1 : N | Um cliente pode realizar várias vendas (opcional). |
| `venda` | `item_venda` | 1 : N | Uma venda é composta por um ou mais itens. |
| `variacao_produto` | `item_venda` | 1 : N | Uma variação de produto pode estar presente em vários itens de venda. |
| `venda` | `troca` | 1 : N | Uma venda pode gerar uma ou mais solicitações de troca. |
| `troca` | `item_troca` | 1 : N | Uma troca é composta por um ou mais itens trocados. |
| `variacao_produto` | `item_troca` | 1 : N | Uma variação de produto pode constar em múltiplos itens de troca. |
| `usuario` | `compra` | 1 : N | Um usuário pode registrar várias compras de fornecedores. |
| `compra` | `item_compra` | 1 : N | Uma compra possui diversos itens comprados. |
| `variacao_produto` | `item_compra` | 1 : N | Uma variação pode ser comprada em diferentes pedidos de compra. |
| `cliente` | `debito` | 1 : N | Um cliente pode ter múltiplos débitos associados. |
| `venda` | `debito` | 1 : N | Uma venda pode gerar um ou mais lançamentos de débito. |
| `debito` | `pagamento` | 1 : N | Um débito pode ser pago de forma parcelada em múltiplos pagamentos. |
| `usuario` | `despesa` | 1 : N | Um usuário registra várias despesas no sistema. |
