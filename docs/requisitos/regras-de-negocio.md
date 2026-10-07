# Regras de Negócio

## 1. Identificação

**Projeto:** Sistema de Gestão Comercial Estrela Moda
**Instituição:** Centro Universitário de Brasília — UniCEUB
**Curso:** Ciências da Computação
**Ano:** 2026

---

## 2. Objetivo

Este documento apresenta as regras de negócio identificadas durante o levantamento de requisitos.

As regras representam condições e comportamentos que deverão ser respeitados pelo sistema de acordo com as necessidades e os processos da loja.

As regras que ainda dependem de validação estão identificadas nas seções correspondentes.

---

## 3. Regras de Negócio

### RN01 — Estoque mínimo

O estoque mínimo considerado pela loja é de **1 unidade**.

### RN02 — Formas de pagamento

As formas de pagamento utilizadas pela loja são:

* dinheiro;
* Pix;
* cartão de débito;
* cartão de crédito;
* fiado.

### RN03 — Associação da venda fiado ao cliente

Toda venda realizada na modalidade fiado deverá estar associada ao respectivo cliente.

### RN04 — Pendência do débito

O valor decorrente de uma venda realizada no fiado deverá permanecer pendente até que seja realizado o pagamento correspondente.

### RN05 — Ausência de prazo de vencimento

Os débitos registrados na modalidade fiado não possuem prazo de vencimento definido.

### RN06 — Atualização do débito

O valor pendente deverá ser atualizado após o registro de um pagamento.

### RN07 — Quitação do débito

Um débito deverá deixar de apresentar valor pendente quando seu valor integral for quitado.

### RN08 — Desconto de 5%

A loja pratica desconto de **5% quando solicitado pelo cliente**, observadas as regras de autorização definidas pela loja.

**Situação:** pendente de validação quanto à autorização para aplicação do desconto.

### RN09 — Prazo para troca

As trocas somente poderão ser realizadas dentro do prazo de **30 dias**.

### RN10 — Etiqueta para troca

Não será permitida a troca de um produto sem a respectiva etiqueta.

### RN11 — Condições do produto para troca

Não será permitida a troca de produtos que estejam:

* manchados;
* lavados.

### RN12 — Produto fiado danificado pelo cliente

Caso um produto adquirido na modalidade fiado seja danificado pelo cliente, o valor correspondente deverá ser pago pelo cliente.

### RN13 — Movimentação do estoque

As movimentações de estoque decorrentes das operações do sistema deverão ser registradas.

### RN14 — Produtos disponíveis para venda

Somente produtos cadastrados e disponíveis para venda poderão ser utilizados em operações de venda.

### RN15 — Cancelamento de vendas

As vendas realizadas não poderão ser canceladas.

### RN16 — Correção de vendas

Eventuais correções ou devoluções deverão ser tratadas por meio do processo de troca.

### RN17 — Preservação dos registros

Os registros históricos das operações deverão ser preservados para consulta posterior.

### RN18 — Controle de acesso

As operações disponíveis no sistema deverão respeitar as permissões associadas ao perfil do usuário.

---

## 4. Regras Pendentes de Definição

As seguintes regras ainda dependem de esclarecimento ou validação:

### RN19 — Atualização do estoque em trocas

Deverá ser definido como os produtos envolvidos em uma troca serão movimentados no estoque.

### RN20 — Diferença de preço em trocas

Deverá ser definido como o sistema deverá tratar diferenças de preço quando o produto recebido na troca possuir valor diferente do produto devolvido.

### RN21 — Troca por produto de categoria diferente

Deverá ser definido se será permitida a troca por produto pertencente a uma categoria diferente.

### RN22 — Registro do motivo da troca

Deverá ser definido se o motivo da troca deverá ser obrigatoriamente registrado.

### RN23 — Tratamento do fiado em trocas

Deverá ser definido como o valor de uma venda realizada no fiado deverá ser tratado quando ocorrer uma troca.

### RN24 — Categorias de despesas

Deverão ser definidas e validadas as categorias utilizadas para classificação das despesas.

### RN25 — Indicadores financeiros

Deverão ser definidos e validados os critérios e fórmulas utilizados para cálculo dos indicadores financeiros do sistema.

---

## 5. Observações

As regras pendentes deverão ser atualizadas neste documento após as próximas etapas de levantamento e validação.

As regras de negócio deverão ser consideradas na especificação dos requisitos funcionais, casos de uso, modelo de dados e implementação do sistema.
