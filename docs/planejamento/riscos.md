# Plano de riscos do sistema

## 1. Objetivo

Este documento registra riscos que podem afetar o desenvolvimento, a segurança, os dados e a operação do Sistema de Gestão Comercial Estrela Modas. Ele parte do plano de riscos de requisitos fornecido pela equipe e acrescenta riscos técnicos relacionados à arquitetura atual (Django, PostgreSQL no Neon e interface renderizada pelo servidor).

As avaliações são iniciais. A equipe deve revisá-las com as responsáveis pela loja e atualizá-las conforme os requisitos e a implantação forem definidos.

## 2. Critérios de avaliação

- **Probabilidade:** chance de o risco ocorrer.
- **Impacto:** consequência para os dados, usuários, operação da loja, prazo ou qualidade do sistema caso ocorra.
- **Classificação:** baixa, média ou alta.
- **Status:** aberto, mitigado, encerrado ou ocorrido.

## 3. Matriz de riscos

| ID | Risco | Probabilidade | Impacto | Resposta / prevenção | Responsável | Status |
| --- | --- | --- | --- | --- | --- | --- |
| R01 | Requisitos ainda pendentes de validação pelas responsáveis pela loja | Média | Alto | Validar os requisitos antes de concluir as funcionalidades correspondentes e registrar mudanças na documentação e no backlog. | Equipe de Requisitos | Aberto |
| R02 | Regras financeiras e critérios dos indicadores ainda não estão completamente definidos | Média | Alto | Definir e validar fórmulas de lucro, totais, saldos e indicadores antes de fechar dashboard e relatórios. | Requisitos e Desenvolvimento | Aberto |
| R03 | Permissões dos perfis de acesso ainda não foram validadas | Média | Alto | Confirmar com a loja o que cada perfil pode consultar, criar, alterar e excluir; configurar e revisar as permissões no Django. | Requisitos e Desenvolvimento | Aberto |
| R04 | Regras de troca ainda têm pontos pendentes | Média | Alto | Validar estoque, diferenças de valores, motivo, crédito gerado e tratamento de vendas fiado antes de concluir o fluxo. | Requisitos e Desenvolvimento | Aberto |
| R05 | Categorias de despesas ainda não foram definidas | Média | Médio | Levantar e validar as categorias com a loja antes de consolidar cadastros e relatórios de despesas. | Requisitos | Aberto |
| R06 | Alterações de requisitos durante o desenvolvimento podem gerar retrabalho ou inconsistência entre documentação e sistema | Média | Médio | Registrar cada alteração, avaliar seu impacto em telas, regras, models, migrações, documentação e backlog, e aprová-la com a equipe. | Equipe de Projeto | Aberto |
| R07 | Dados incorretos inseridos pelos usuários podem causar cadastros, saldos ou relatórios incorretos | Média | Alto | Validar os campos no servidor, limitar valores e quantidades, apresentar mensagens claras e orientar os usuários. | Desenvolvimento | Aberto |
| R08 | Hospedagem, disponibilidade e procedimentos de operação ainda não estão definidos | Média | Médio | Definir ambiente de produção, disponibilidade esperada, responsáveis pela operação e procedimento de recuperação antes da implantação. | Equipe de Projeto | Aberto |
| R09 | Testes e validações podem revelar problemas que exijam ajustes antes da entrega | Média | Médio | Registrar problemas, priorizar por impacto e corrigir antes de liberar cada funcionalidade. | Desenvolvimento | Aberto |
| R10 | Histórico de migrações do banco e tabelas existentes no Neon podem divergir | Alta | Alto | Conferir projeto, branch, banco e schema usados por `DATABASE_URL`; comparar `django_migrations` com as tabelas reais; corrigir o esquema sem apagar dados sem cópia e aprovação. | Desenvolvimento / Banco de Dados | Ocorrido — divergência observada no ambiente local |
| R11 | Atualizações concorrentes de estoque em compras, vendas e trocas podem gerar quantidades incorretas | Média | Alto | Executar operações relacionadas em transações atômicas, validar disponibilidade no servidor e manter registro das movimentações para conferência. | Desenvolvimento | Aberto |
| R12 | Exposição de credenciais do Neon ou da chave secreta do Django pode permitir acesso indevido | Média | Alto | Manter segredos fora do Git, restringir acesso aos arquivos de ambiente, usar variáveis protegidas na hospedagem e trocar credenciais que tenham sido expostas. | Toda a equipe / Desenvolvimento | Aberto |
| R13 | Configurações de desenvolvimento podem ser usadas inadvertidamente em produção | Média | Alto | Antes da implantação, configurar `DEBUG=False`, hosts permitidos, HTTPS, segredo forte e os demais controles da checklist de implantação do Django. | Desenvolvimento / Infraestrutura | Aberto |
| R14 | Falta de cópias de segurança ou de validação da restauração pode causar perda de dados | Média | Alto | Definir frequência e retenção de backups do PostgreSQL, responsáveis e procedimento de restauração; verificar periodicamente que a restauração funciona. | Banco de Dados / Infraestrutura | Aberto |
| R15 | Funcionalidades previstas com QR Code ou API externa podem depender de decisões e serviços ainda não definidos | Média | Médio | Definir se o QR Code será gerado e lido localmente ou dependerá de serviço externo; documentar dados, disponibilidade, falhas e alternativa manual. | Requisitos e Desenvolvimento | Aberto |

> **R10:** durante a configuração, o comando de criação do usuário administrativo encontrou a tabela `auth_user` ausente, enquanto o Django indicou que as migrações de autenticação já estavam aplicadas. A divergência foi observada; a causa e a correção precisam ser confirmadas no banco/schema efetivamente usado pela aplicação.

## 4. Estratégias de resposta

### 4.1 Requisitos e regras de negócio

As regras de negócio pendentes devem ser confirmadas pelas responsáveis pela loja antes da implementação definitiva. Mudanças devem ser registradas e avaliadas quanto ao efeito sobre os casos de uso, protótipos, banco, telas e backlog.

### 4.2 Integridade dos dados e estoque

As operações devem validar os dados no backend, mesmo quando a interface também valida campos. Operações que alterem saldos ou estoque devem ser tratadas de forma consistente no banco. As movimentações precisam permitir conferência entre entradas, saídas e quantidade disponível.

### 4.3 Banco de dados e migrações

Antes de aplicar mudanças no banco, a equipe deve confirmar o destino configurado, consultar o estado das migrações e preservar os dados existentes. Correções de esquema devem ser planejadas; apagar tabelas ou o histórico de migrações não deve ser usado como tentativa inicial de solução.

### 4.4 Acesso e segredos

Os perfis e permissões devem refletir decisões validadas pela loja. Credenciais e chaves devem ser fornecidas por variáveis de ambiente e não podem ser incluídas em commits, capturas ou mensagens compartilhadas.

### 4.5 Implantação e continuidade

Antes de disponibilizar o sistema aos usuários, devem ser definidos hospedagem, configurações de produção, política de backup e procedimento de restauração. As medidas precisam ser verificadas no ambiente de implantação.

## 5. Acompanhamento

Os riscos devem ser revistos nas etapas de planejamento, desenvolvimento, validação e implantação, e também quando uma regra ou decisão técnica mudar. Ao revisar um risco, atualizar probabilidade, impacto, resposta, responsável e status. Novos riscos devem receber um identificador sequencial.

### Status possíveis

- **Aberto:** identificado e ainda sujeito a acompanhamento.
- **Mitigado:** medidas de redução foram aplicadas; o risco residual ainda pode ser acompanhado.
- **Encerrado:** não apresenta impacto relevante ou deixou de se aplicar.
- **Ocorrido:** o evento aconteceu e está sendo tratado como problema do projeto ou do sistema.

## 6. Histórico de alterações

| Data | Alteração | Responsável |
| --- | --- | --- |
| 06/10/2026 | Criação inicial do plano de riscos do sistema, com base no plano de riscos de requisitos e na arquitetura atual do projeto. | Equipe de Projeto |
