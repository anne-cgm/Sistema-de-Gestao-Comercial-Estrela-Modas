# Requisitos Não Funcionais

## 1. Identificação

**Projeto:** Sistema de Gestão Comercial Estrela Moda
**Instituição:** Centro Universitário de Brasília — UniCEUB
**Curso:** Ciências da Computação
**Ano:** 2026

---

## 2. Objetivo

Este documento apresenta os requisitos não funcionais identificados para o Sistema de Gestão Comercial Estrela Moda.

Os requisitos não funcionais definem características relacionadas à qualidade, segurança, desempenho, usabilidade, disponibilidade e manutenção do sistema.

As especificações que ainda dependem de definição ou validação permanecem identificadas como pendentes.

---

## 3. Requisitos Não Funcionais

### RNF01 — Controle de acesso

O sistema deverá controlar o acesso às funcionalidades de acordo com o perfil e as permissões atribuídas a cada usuário.

### RNF02 — Autenticação

O sistema deverá exigir autenticação dos usuários para acesso às funcionalidades que necessitem de controle de acesso.

### RNF03 — Autorização

O sistema deverá verificar as permissões do usuário antes de permitir a execução de operações restritas.

### RNF04 — Integridade dos dados

O sistema deverá manter a integridade dos dados registrados, evitando operações que resultem em informações inconsistentes.

### RNF05 — Persistência dos dados

Os dados registrados no sistema deverão ser armazenados de forma persistente, permitindo sua consulta posteriormente.

### RNF06 — Usabilidade

A interface deverá apresentar as informações e funcionalidades de forma clara e organizada, facilitando a utilização pelos usuários da loja.

### RNF07 — Consistência das informações

As informações apresentadas em diferentes módulos deverão permanecer consistentes entre si, especialmente nos dados relacionados a produtos, estoque, vendas, clientes e débitos.

### RNF08 — Rastreabilidade das operações

O sistema deverá manter os registros necessários para permitir o acompanhamento das operações realizadas.

### RNF09 — Manutenção

A aplicação deverá ser estruturada de forma a facilitar a manutenção e a evolução das funcionalidades ao longo do desenvolvimento.

### RNF10 — Desempenho

O sistema deverá apresentar tempo de resposta adequado para as operações realizadas pelos usuários.

O tempo máximo de resposta para operações críticas ainda deverá ser definido e validado.

### RNF11 — Disponibilidade

O sistema deverá estar disponível para utilização durante os períodos de operação da loja, considerando a infraestrutura definida para a solução.

Os requisitos específicos de disponibilidade ainda deverão ser definidos.

### RNF12 — Segurança

O sistema deverá proteger os dados armazenados e restringir o acesso às informações conforme as permissões dos usuários.

### RNF13 — Compatibilidade

A aplicação deverá ser desenvolvida considerando o ambiente tecnológico definido para o projeto e os dispositivos utilizados para acesso ao sistema.

Os requisitos específicos de compatibilidade ainda deverão ser detalhados conforme a definição da arquitetura.

---

## 4. Pontos Pendentes

Os seguintes aspectos ainda dependem de definição ou validação:

* tempo máximo de resposta para operações críticas;
* requisitos específicos de disponibilidade;
* infraestrutura e hospedagem;
* requisitos específicos de compatibilidade;
* demais critérios de desempenho que sejam considerados necessários.

---

## 5. Rastreabilidade

Os requisitos não funcionais deverão ser considerados na definição da arquitetura, das tecnologias, do modelo de implantação e da implementação do sistema.

Os requisitos relacionados à segurança e ao controle de acesso também deverão ser relacionados aos casos de uso e à matriz de permissões.
