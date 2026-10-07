# Contrato Inicial da API

## 1. Objetivo

Este documento apresenta o contrato inicial das APIs previstas para o Sistema de Gestão Comercial da loja.

Nesta fase, está prevista a utilização da **QR Server API** para a geração dos QR Codes utilizados na identificação interna dos produtos.

A API será utilizada para gerar a imagem do QR Code a partir de uma URL ou identificador definido pelo sistema. A leitura do QR Code e o controle de acesso à ficha do produto serão realizados pela própria aplicação.

---

## 2. API externa — QR Server

### 2.1 Finalidade

A QR Server API será utilizada para gerar os QR Codes associados às variações dos produtos cadastrados no sistema.

Cada QR Code deverá conter um identificador ou URL capaz de direcionar o usuário para a ficha correspondente ao produto.

A API disponibiliza um endpoint de geração de QR Code que utiliza requisição HTTP e recebe o conteúdo a ser armazenado no código por meio do parâmetro `data`.

### 2.2 Documentação oficial

Documentação da API:

https://goqr.me/api/doc/create-qr-code/

Endpoint utilizado:

```text
https://api.qrserver.com/v1/create-qr-code/
```

---

## 3. Endpoint de geração de QR Code

### Endpoint

```http
GET https://api.qrserver.com/v1/create-qr-code/
```

### Parâmetros

| Parâmetro | Obrigatório | Descrição                               |
| --------- | ----------- | --------------------------------------- |
| `data`    | Sim         | Conteúdo que será armazenado no QR Code |
| `size`    | Não         | Dimensão da imagem gerada               |
| `format`  | Não         | Formato da imagem, como PNG ou SVG      |

O parâmetro `data` será utilizado para armazenar a URL ou identificador utilizado pelo sistema para localizar a variação do produto.

A API permite a geração da imagem do QR Code por meio de uma requisição HTTP GET.

### Exemplo de requisição

```http
GET https://api.qrserver.com/v1/create-qr-code/?data=https%3A%2F%2Fsistema.exemplo%2Fproduto%2F123&size=200x200
```

### Exemplo de utilização no sistema

Para uma variação de produto identificada internamente pelo código `123`, o sistema poderá gerar um QR Code contendo uma URL semelhante a:

```text
https://sistema.exemplo/produto/123
```

A URL será codificada no QR Code pela API.

---

## 4. Fluxo de utilização

O fluxo previsto para utilização dos QR Codes é:

```text
Cadastro do produto
        ↓
Criação da variação do produto
        ↓
Geração do identificador da variação
        ↓
Sistema solicita geração do QR Code
        ↓
QR Server API gera a imagem
        ↓
QR Code é associado à variação do produto
        ↓
QR Code é disponibilizado para identificação interna
        ↓
Usuário realiza a leitura do QR Code
        ↓
Sistema identifica o produto
        ↓
Sistema verifica autenticação
        ↓
Ficha do produto é apresentada
        ↓
Usuário autorizado pode adicionar o produto ao carrinho
```

---

## 5. Controle de acesso

A QR Server API não será responsável pelo controle de acesso aos produtos.

O QR Code apenas direcionará o usuário para o recurso correspondente dentro da aplicação.

Ao acessar a ficha do produto, o sistema deverá verificar se o usuário está autenticado.

Somente usuários autenticados e com permissão para utilizar o sistema poderão visualizar a ficha destinada ao uso interno e adicionar o produto ao carrinho do PDV.

Usuários não autenticados deverão ser direcionados para a tela de autenticação.

O controle de permissões será realizado pelo backend da aplicação.

---

## 6. Leitura do QR Code

A leitura do QR Code não será realizada pela QR Server API.

A API será utilizada para **gerar a imagem do QR Code**. A leitura será realizada pelo dispositivo utilizado pelo funcionário ou administrador, utilizando recurso compatível de leitura de QR Code.

Após a leitura, o dispositivo deverá acessar a URL ou identificador armazenado no código e encaminhar a solicitação para a aplicação.

---

## 7. Dados envolvidos

O QR Code deverá armazenar somente o identificador necessário para localizar a variação do produto ou uma URL que contenha esse identificador.

Exemplo:

```text
https://sistema.exemplo/produto/123
```

As informações completas do produto não deverão ser armazenadas diretamente no QR Code.

As informações apresentadas na ficha serão recuperadas pelo sistema a partir do identificador correspondente no banco de dados.

---

## 8. Resposta da API externa

A QR Server API retorna uma imagem correspondente ao QR Code solicitado.

Exemplo conceitual:

```text
Requisição
    ↓
QR Server API
    ↓
Imagem do QR Code
```

O formato padrão da imagem gerada é PNG, podendo outros formatos, como SVG, ser especificados quando necessário.

---

## 9. Tratamento de indisponibilidade

Caso a API externa esteja indisponível no momento da geração do QR Code, o sistema deverá informar a falha ao usuário responsável pela operação.

A indisponibilidade da API não deverá comprometer os dados já cadastrados no sistema.

O produto e sua respectiva variação deverão permanecer registrados normalmente no banco de dados, mesmo que a geração do QR Code precise ser realizada posteriormente.

O comportamento definitivo para novas tentativas de geração deverá ser definido durante a implementação.

---

## 10. Segurança

O QR Code não deverá conter informações sensíveis do estabelecimento ou dos clientes.

O acesso às funcionalidades internas dependerá da autenticação realizada pela própria aplicação.

A URL ou identificador presente no QR Code não deverá ser considerado, por si só, como mecanismo de autenticação ou autorização.

A autorização para visualizar informações internas e utilizar o PDV deverá ser realizada pelo sistema.

---

## 11. API interna da aplicação

Além da integração com a QR Server API, o sistema deverá possuir uma API própria para comunicação entre o frontend e o backend.

Os endpoints internos serão definidos de acordo com os módulos e funcionalidades implementados.

Entre os recursos previstos estão:

* autenticação de usuários;
* produtos;
* variações de produtos;
* estoque;
* clientes;
* clientes com débitos;
* vendas;
* trocas;
* despesas;
* relatórios.

Os endpoints específicos, métodos HTTP, parâmetros e formatos JSON serão detalhados conforme a implementação da aplicação e a definição do backlog.

---

## 12. Status da definição

A integração com a QR Server API está definida para a geração dos QR Codes dos produtos.

Os seguintes pontos permanecem sujeitos à definição durante a implementação:

* formato definitivo do identificador armazenado no QR Code;
* estrutura da URL utilizada para acesso à ficha do produto;
* mecanismo de leitura do QR Code utilizado no frontend;
* endpoint interno responsável pela consulta da ficha do produto;
* comportamento em caso de falha na geração do QR Code;
* definição dos endpoints completos da API interna.
