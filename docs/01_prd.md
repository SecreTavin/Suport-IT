# Product Requirements Document (PRD)
## Sistema de Controle de Chamados Internos

### 1. Visão Geral
O "Sistema de Controle de Chamados Internos" visa digitalizar, centralizar e organizar os pedidos de suporte da empresa (ex: problemas de hardware, dúvidas de software). O objetivo é substituir os canais informais, muitas vezes caóticos (como WhatsApp e e-mail), por uma plataforma estruturada que garanta uma distribuição justa de tarefas entre a equipe de suporte e facilite o acompanhamento do ciclo de vida dos tickets.

### 2. Stack Tecnológica
- **Backend:** Python com o framework Flask.
- **Banco de Dados:** SQLite (banco embutido, dispensando setup complexo e facilitando testes locais).
- **Frontend:** Templates HTML renderizados no lado do servidor via Jinja2, utilizando o Tailwind CSS via CDN para uma estilização ágil, responsiva e sem necessidade de processos de *build*.
- **Arquitetura:** Monolítica, priorizando a produtividade de equipes pequenas e a redução de atrito entre camadas de desenvolvimento.

### 3. Entidades Principais (Modelagem)
#### 3.1. Responsável (Atendente)
- **Definição:** Membro da equipe de suporte que atuará na resolução dos chamados.
- **Atributos Básicos:** ID, Nome.
- **Regras:** Não haverá tela de cadastro, edição ou deleção (sem CRUD) para Responsáveis nesta primeira versão. O banco de dados deverá ser preenchido inicialmente (através de um processo de *seed*) com pelo menos 3 (três) opções de responsáveis disponíveis para o sistema.

#### 3.2. Chamado (Ticket)
- **Definição:** Registro do pedido de suporte.
- **Atributos Básicos:** ID, Título, Descrição, Prioridade, Status, ID do Responsável, Data/Hora de Abertura.
- **Domínios de Valores:**
  - **Prioridade:** Baixa, Média, Alta.
  - **Status:** Aberto, Em Andamento, Resolvido, Fechado.

### 4. Funcionalidades (Épicos e User Stories)

#### Épico 1: Gestão de Chamados (CRUD de Tickets)
- **US 1.1 - Abertura de Chamados:** O sistema deve possuir um formulário para criação de novos chamados, solicitando Título, Descrição e Prioridade. A data/hora de abertura deve ser gerada automaticamente pelo sistema.
- **US 1.2 - Atribuição de Responsabilidade:** No momento de criação de um chamado, o usuário deve ser capaz de selecionar um Responsável específico ou marcar uma opção de "Distribuição Automática".
- **US 1.3 - Visualização e Edição:** O usuário ou atendente deve poder acessar uma tela de detalhe de um chamado existente para atualizar a sua Prioridade, Status ou modificar os dados inseridos (Título, Descrição).

#### Épico 2: Dashboard e Acompanhamento
- **US 2.1 - Listagem (Tela Principal):** Ao acessar o sistema, deve ser exibida uma tela inicial ou *dashboard* contendo uma tabela ou lista de todos os chamados registrados.
- **US 2.2 - Filtros Básicos:** Na tela de listagem, devem existir controles que permitam ao usuário filtrar rapidamente a visualização (ex: ver apenas chamados de Prioridade "Alta" ou ocultar chamados já "Fechados" e "Resolvidos").

### 5. Regras de Negócio (Business Rules)
- **RN01 - Distribuição Automática:** Quando um chamado for criado utilizando a opção de "atribuição automática", o sistema deve identificar qual dos Responsáveis possui o MENOR número de chamados pendentes sob sua responsabilidade e atribuir a nova tarefa a ele.
  - *Critério de pendência:* São considerados chamados pendentes apenas aqueles que estiverem com o Status igual a `Aberto` ou `Em Andamento`.
  - *Critério de desempate:* Caso dois ou mais responsáveis tenham o mesmo número de chamados pendentes (ex: todos têm 0), o sistema pode escolher qualquer um deles de forma arbitrária (ex: o primeiro da lista retornada pelo banco).

### 6. Diretrizes Técnicas e Critérios de Aceite
- **Código e Qualidade (SOLID/DRY):** A lógica de negócio (especialmente a de distribuição automática) deve estar bem separada da lógica de roteamento e *views*. Espera-se funções bem nomeadas, modulares, e evitar repetição de código.
- **Usabilidade (UI/UX):** A interface construída com Tailwind CSS deve ser limpa, intuitiva e plenamente funcional. As ações (botões, formulários e links) devem ter espaçamento adequado e feedback visual consistente, mesmo que o design geral seja simples.
- **Documentação e Setup (README):** É requisito fundamental garantir que o sistema possa ser executado por qualquer pessoa localmente com o mínimo de fricção.
  - Deve existir um `README.md` orientando sobre: pré-requisitos, passo a passo para criar o ambiente virtual (ex: `venv`), instalação de pacotes, instrução para rodar o *seed* do banco de dados e o comando para iniciar a aplicação localmente.
  - O README também deve documentar um breve parágrafo justificando as escolhas de tecnologia e arquitetura adotadas no projeto.