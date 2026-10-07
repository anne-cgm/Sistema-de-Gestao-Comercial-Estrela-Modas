# Planejamento de execução — Fase 1

## 1. Objetivo da Fase 1

Organizar e concluir os artefatos de análise e planejamento solicitados para a primeira fase do projeto do Sistema de Gestão Comercial Estrela Modas. A entrega deve apresentar uma visão coerente do problema da loja, dos requisitos, dos fluxos de uso, da arquitetura proposta, dos dados e da interface planejada.

Este arquivo é o mapa de execução da equipe: o `backlog.md` detalha o que precisa ser feito, enquanto o `riscos.md` registra o que pode dar errado e as respostas previstas.

## 2. Entregáveis da Fase 1

| Entregável | Evidência esperada | Situação observada no repositório |
| --- | --- | --- |
| Repositório GitHub configurado | Repositório versionado, estrutura acordada e pipeline de CI | Estrutura Django e workflow `.github/workflows/ci.yml` existem; conferir execução do CI e checklist do professor |
| README | Contexto, tecnologias, instalação, comandos e integrantes | `README.md` existe; revisar se todos os dados da loja, comandos e membros estão completos e atuais |
| Documento de visão | Problema, público, objetivos, escopo e limites do produto | Pendente de localizar/criar versão final |
| Levantamento com o cliente | Registro das necessidades, dores e validações | Pendente de localizar/documentar |
| Requisitos funcionais e não funcionais | Requisitos identificados e organizados | Pendente de localizar/documentar |
| Regras de negócio | Regras dos 10 módulos validadas com a loja | Pendente de localizar/documentar e validar |
| Casos de uso | Especificações com atores, condições, fluxos e exceções | Pendente de localizar/documentar |
| Diagrama de casos de uso | Diagrama UML alinhado às especificações | Pendente |
| Diagrama de classes inicial | Classes, atributos, operações e relações principais | Pendente de localizar/exportar |
| Documento e diagrama de arquitetura | Camadas e componentes descritos e representados | `docs/arquitetura.md` contém a descrição inicial e diagramas de fluxo; falta confirmar o diagrama UML de componentes/implantação solicitado |
| Modelo de dados / MER/DER | Arquivo editável e exportações PDF/PNG em `docs/banco-de-dados/` | Models e migration Django existem; os artefatos MER/DER e exportações não foram encontrados |
| Contrato inicial da API | Endpoints, métodos, dados, respostas e erros documentados | Pendente |
| Plano de integração de QR Code | Propósito, serviço/endpoints, dados e tratamento de indisponibilidade | `docs/integracao.md` descreve as integrações atuais; o plano específico de QR Code ainda está pendente |
| Protótipos e wireframes | Fluxos e telas essenciais no Figma/Penpot | A confirmar com a responsável; os arquivos não estão no repositório |
| Identidade visual | Marca, cores e tipografia aplicadas ao protótipo | A confirmar com a responsável |
| Backlog | Atividades, responsáveis e datas | `docs/backlog.md` existe |
| Plano de riscos | Riscos, probabilidade, impacto, respostas e responsáveis | `docs/riscos.md` existe; revisar periodicamente |
| Planejamento da Fase 1 | Sequência, responsáveis, marcos e critérios de conclusão | Este documento |

> As situações acima refletem apenas os arquivos e informações verificados no repositório. Um item marcado como pendente pode já existir em ferramenta externa, como Figma/Penpot, ou ainda precisar de validação pela equipe.

## 3. Divisão das atividades

| Atividade | Responsável principal | Apoio / dependência | Situação para a Fase 1 |
| --- | --- | --- | --- |
| Entrevista simulada, levantamento e regras de negócio | Nicolly | Responsáveis pela loja; equipe de requisitos | Pendente de evidência e validação |
| Requisitos funcionais e não funcionais | Nicolly | Equipe de requisitos | Pendente de localizar/documentar |
| Documento de visão e quadro 5W2H | Nicolly | Responsáveis pela loja | Pendente de localizar versão final |
| Wireframes e fluxo de usuário | Kamila | Requisitos e casos de uso | A confirmar no Figma/Penpot |
| Diagrama e especificação de casos de uso | Nicolly | Wireframes e requisitos validados | Pendente |
| Diagrama de classes inicial | Nicolly | Models e requisitos | Pendente de localizar/exportar |
| Identidade visual e protótipo de alta fidelidade | Kamila | Requisitos e wireframes | A confirmar no Figma |
| Repositório, estrutura Django e CI | Anne | Equipe de desenvolvimento | Django e workflow existem; revisar checklist e execução da pipeline |
| Templates base e interface | Anne | Kamila para identidade visual | Templates e arquivos estáticos existem; validar cobertura e responsividade das telas |
| Ambiente Django e conexão Neon | Anne | Sciel / responsável por banco de dados | Configuração existe; confirmar migrações e tabelas no Neon antes da entrega |
| MER/DER, exportações e conferência do schema | Sciel | Anne e equipe de desenvolvimento | Models/migration existem; artefatos do modelo e estado do Neon pendentes de confirmação |
| Documento e diagrama de arquitetura | Nicolly | Anne / desenvolvimento | Descrição inicial existe; finalizar artefato UML e revisar com a implementação |
| Contrato REST e plano de integração do QR Code | Anne | Responsável pelo módulo de produtos | Pendente |
| README e organização das pastas de documentação | Nicolly | Equipe | README existe; revisar conteúdo e completar a estrutura solicitada |
| Backlog e plano de riscos | Equipe de Projeto | Todos os responsáveis | Arquivos criados; manter atualizados |

## 4. Cronograma e marcos

As datas abaixo foram transcritas do backlog no formato `DD/MM`. O ano e a data formal da entrega da Fase 1 não foram informados; a equipe deve confirmá-los antes de usar este cronograma como calendário definitivo.

| Marco | Atividades relacionadas | Responsável(is) | Data limite informada |
| --- | --- | --- | --- |
| 1. Desenhar os fluxos iniciais | Wireframes e navegação principal | Kamila | 12/09 |
| 2. Entender e especificar o problema | Entrevista/levantamento, requisitos, regras de negócio, 5W2H, casos de uso e diagrama de classes | Nicolly | 14/09 |
| 3. Validar a direção visual | Identidade visual e protótipo de alta fidelidade | Kamila | 15/09 |
| 4. Preparar base técnica e repositório | Django, templates base, Neon, estrutura do repositório e CI | Anne | 16/09 |
| 5. Fechar modelo de dados | MER/DER, modelos Django, exportações e migrações | Sciel | 20/09 |
| 6. Integrar os módulos do MVP | Produtos/Estoque/Trocas; Vendas/Despesas/Relatórios | Mila e Sciel | 24/09 |
| 7. Completar módulos relacionados | Compras/Abastecimento e Dashboard | Anne | 28/09 |
| 8. Consolidar arquitetura | Documento de visão e diagrama de arquitetura | Nicolly | 02/10 |
| 9. Documentar integrações | Contrato inicial da API REST e plano da API de QR Code | Anne | 03/10 |
| 10. Revisar documentação e repositório | README e organização final das pastas | Nicolly | 05/10 |
| 11. Completar módulo de clientes | Clientes e clientes com débito | Nicolly | 08/10 |

Os itens de desenvolvimento dos marcos 7, 8 e 12 estão no backlog geral do MVP. A equipe deve confirmar com o professor se todos fazem parte do critério de entrega da Fase 1 ou se são uma trilha de implementação paralela à entrega documental.

### Sequência de execução

```text
Levantamento
    → análise dos requisitos e regras de negócio
    → especificação dos casos de uso
    → validação com a loja
    → modelagem de classes, dados e arquitetura
    → wireframes e protótipos visuais
    → contrato da API e plano de integrações
    → revisão cruzada dos artefatos
    → organização do repositório e entrega da Fase 1
```

As atividades podem avançar em paralelo quando não dependerem de decisões ainda pendentes. Por exemplo, o protótipo pode evoluir enquanto os requisitos são refinados, mas deve ser revisto depois da validação das regras e dos fluxos.

## 5. Estratégia de execução

1. Manter tarefas, responsáveis e prazos no `docs/backlog.md`; atualizar o status quando a equipe confirmar o andamento.
2. Cada responsável produz ou atualiza os artefatos de sua atividade e informa dependências ou decisões pendentes.
3. Manter documentos e código no GitHub, organizados conforme o checklist do professor. Arquivos do Figma/Penpot devem ter seus links registrados na documentação, se não puderem ser versionados no repositório.
4. Versionar alterações por commits claros e revisar mudanças antes de integrá-las à branch principal.
5. Validar requisitos e regras pendentes com as responsáveis pela loja; registrar decisões e atualizar os documentos afetados.
6. Manter documentação, modelos de dados, protótipos e implementação compatíveis entre si.
7. Acompanhar riscos pelo `docs/riscos.md`, atualizando a matriz quando probabilidade, impacto ou status mudar.
8. Antes da entrega, revisar links, nomes, diagramas, exportações, estrutura de pastas e consistência entre artefatos.

## 6. Critérios de conclusão da Fase 1

A Fase 1 será considerada concluída quando:

- todos os entregáveis definidos pelo professor estiverem presentes ou tiverem link para o local aprovado onde estão armazenados;
- requisitos, regras de negócio e casos de uso tiverem sido revisados e validados;
- diagramas, models, contrato da API, protótipos e arquitetura forem coerentes entre si;
- README e estrutura do repositório estiverem atualizados e organizados conforme o checklist;
- arquivos editáveis e exportações solicitadas (PDF/PNG) estiverem incluídos nas pastas corretas;
- backlog e riscos refletirem o estado real do projeto;
- a equipe fizer uma revisão final conjunta e confirmar a versão que será entregue.

## 7. Pendências para confirmar com a equipe

- Ano das datas do backlog e data oficial de entrega da Fase 1.
- Se os itens de desenvolvimento dos módulos fazem parte da avaliação da Fase 1 ou são uma etapa posterior.
- Situação real dos wireframes e protótipo no Figma/Penpot.
- Localização/estado dos documentos de visão, requisitos, regras de negócio, casos de uso, diagramas e MER/DER.
- Responsáveis de apoio e revisores para cada artefato.
- Situação da conexão, das migrações e das tabelas no Neon.

## 8. Histórico de alterações

| Data | Alteração | Responsável |
| --- | --- | --- |
| 06/10/2026 | Criação do planejamento inicial da Fase 1 com base no backlog informado e nos artefatos encontrados no repositório. | Equipe de Projeto |
