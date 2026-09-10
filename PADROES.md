# Padrões do Projeto e Guia de Contribuição

Este documento define as convenções de código, nomes de variáveis, estrutura de banco de dados e organização de branches para o desenvolvimento do sistema de gestão da loja de roupas.

---

## Convenções Gerais de Nomenclatura

* **Python / Django:** Use `snake_case` (ex: `cliente_id`, `data_venda`).
* **JavaScript (Front-end):** Use `camelCase` (ex: `clienteId`, `dataVenda`).
* **Banco de Dados (PostgreSQL / Neon):** Nomes de tabelas no plural e colunas em `snake_case` e minúsculo (ex: tabela `produtos`, coluna `preco_venda`).
* **API REST (JSON):** Chaves em `snake_case` (ex: `{"preco_venda": 89.90}`).

---

## Dicionário de Variáveis Padronizadas

Todos os integrantes devem utilizar **exatamente** os nomes abaixo para garantir a integração entre HTML/JS, Django e Banco Neon.

### 1. Produtos, Estoque e QR Code
* `produto_id`: Identificador único do produto.
* `nome_produto`: Nome da peça de roupa.
* `codigo_barras`: Código impresso ou escaneado.
* `qr_code_data`: Dados retornados pela leitura da API de QR Code.
* `categoria`: Categoria da peça (ex: Feminino, Masculino, Infantil).
* `tamanho`: Tamanho da peça (P, M, G, GG, etc.).
* `cor`: Cor da peça.
* `preco_custo`: Valor de compra do fornecedor.
* `preco_venda`: Preço de venda ao consumidor.
* `quantidade_estoque`: Quantidade disponível no estoque.
* `estoque_minimo`: Limite para alerta de reposição.

### 2. Vendas, Trocas e PDV
* `venda_id`: Identificador da transação.
* `data_venda`: Data e hora da compra.
* `valor_total`: Valor final cobrado no carrinho.
* `desconto_aplicado`: Valor ou porcentagem de abatimento.
* `forma_pagamento`: Forma de pagamento (Dinheiro, Pix, Cartão, Fiado).
* `itens_venda`: Lista/array com os produtos do carrinho.
* `troca_id`: Identificador do registro de troca.
* `motivo_troca`: Descrição da motivação da devolução.
* `cupom_credito`: Valor liberado para o cliente usar em novas compras.

### 3. Clientes e Débitos (Fiado)
* `cliente_id`: Identificador único do cliente.
* `nome_cliente`: Nome completo.
* `cpf_cliente`: CPF (somente números).
* `telefone`: Telefone de contato com DDD.
* `endereco_completo`: Endereço informado.
* `saldo_devedor`: Valor total pendente no fiado.
* `limite_credito`: Valor máximo permitido para compras a prazo.
* `historico_pagamentos`: Registro de amortizações do débito.

### 4. Compras, Abastecimento e Despesas
* `compra_id`: Identificador do lote/abastecimento de entrada.
* `fornecedor_nome`: Nome do fornecedor ou fábrica.
* `numero_nota_fiscal`: Número da nota fiscal de entrada.
* `data_chegada`: Data de recebimento das peças.
* `despesa_id`: Identificador do gasto registrado.
* `descricao_despesa`: Detalhe da despesa (ex: Aluguel, Viagem SP).
* `categoria_despesa`: Tipo da conta (Viagem, Loja, Impostos, etc.).
* `valor_despesa`: Valor do gasto efetuado.

---

## Estrutura e Nomenclatura de Branches

Utilizamos o padrão `categoria/nome-da-tarefa` para manter o versionamento organizado. Abaixo estão exemplos/sugestões de branchs:

### Branches Principais
* `main`: Código estável e entregas oficiais aprovadas.
* `develop`: Branch de integração diária do time.

### Branches de Documentação e Modelagem
* `docs/requisitos-5w2h`
* `docs/diagramas-uml`
* `docs/modelo-banco-neon`
* `docs/api-contrato`

### Branches de Infraestrutura e Interface Base
* `infra/setup-django-neon`
* `infra/ci-github-actions`
* `front/layout-base-html-css`
* `design/prototipos-figma`

### Branches de Módulos (Funcionalidades)
* `feature/modulo-produtos-estoque`
* `feature/modulo-trocas-qrcode`
* `feature/modulo-vendas-pdv`
* `feature/modulo-despesas-relatorios`
* `feature/modulo-clientes-debitos`
* `feature/modulo-compras-dashboard`

---

## 3. Padronização de Commits (Conventional Commits)

Todas as mensagens de commit devem iniciar com um dos numerais/prefixos abaixo, seguido de descrição clara no imperativo:

* **`feat:`** Criação de nova funcionalidade no sistema.
  * *Exemplo:* `feat: adiciona leitura de qr code na tela de vendas`
* **`fix:`** Correção de bugs ou erros no código.
  * *Exemplo:* `fix: corrige calculo de desconto no carrinho de compras`
* **`doc:`** Alterações ou adições na documentação (`/docs`, `README.md`, diagramas, etc.).
  * *Exemplo:* `doc: adiciona diagrama de casos de uso e especificacao textual`
* **`style:`** Modificações puramente estéticas sem alterar regra de negócio (CSS, formatação HTML).
  * *Exemplo:* `style: ajusta paleta de cores e espaçamento dos botoes`
* **`refactor:`** Refatoração de código sem alterar funcionamento ou corrigir bugs.
  * *Exemplo:* `refactor: otimiza consulta de clientes no banco neon`
* **`test:`** Adição ou correção de testes automatizados.
  * *Exemplo:* `test: inclui teste unitario para cadastro de produtos`
