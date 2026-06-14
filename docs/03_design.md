# Design System & UI/UX Guidelines
## Sistema de Controle de Chamados Internos

Este documento define as diretrizes visuais e os padrões de componentes para o frontend da aplicação, utilizando **Tailwind CSS**. Como o Tailwind será importado via CDN, usaremos as classes utilitárias padrão do framework, mantendo a padronização sem a necessidade de um arquivo `tailwind.config.js` complexo.

---

### 1. Paleta de Cores (Cores Semânticas e Neutras)

A paleta foi escolhida para transmitir profissionalismo, clareza e facilitar a identificação rápida do estado dos chamados.

*   **Fundo da Aplicação (Background):** `bg-gray-50` (Um cinza bem claro para destacar os "cards" brancos).
*   **Superfícies (Cards, Modais, Tabelas):** `bg-white` com bordas suaves `border-gray-200` e sombras leves `shadow-sm`.
*   **Textos Principais:** `text-gray-900` (Títulos e dados importantes).
*   **Textos Secundários:** `text-gray-500` ou `text-gray-600` (Descrições, placeholders, datas).
*   **Cor Primária (Ações principais, links, botões):** `bg-blue-600` (Hover: `bg-blue-700`).

#### 1.1 Cores de Status e Prioridade (Badges)
Para permitir que o usuário bata o olho e entenda a urgência/situação, usaremos os seguintes padrões de *Badges*:

*   **Prioridade Alta / Status Aberto:** Vermelho (`bg-red-100 text-red-800 border-red-200`)
*   **Prioridade Média / Status Em Andamento:** Amarelo/Laranja (`bg-yellow-100 text-yellow-800 border-yellow-200`)
*   **Prioridade Baixa / Status Resolvido:** Verde (`bg-green-100 text-green-800 border-green-200`)
*   **Status Fechado:** Cinza Escuro (`bg-gray-100 text-gray-800 border-gray-200`)

---

### 2. Tipografia

Aproveitaremos a fonte sem serifa padrão do sistema fornecida pelo Tailwind (`font-sans`), que se adapta bem (ex: San Francisco no Mac, Segoe UI no Windows, Roboto no Android).

*   **Títulos de Página (H1):** `text-2xl font-bold text-gray-900 tracking-tight`
*   **Títulos de Seção/Cards (H2):** `text-lg font-semibold text-gray-800`
*   **Texto Base (Parágrafos, Dados de Tabela):** `text-sm text-gray-600` ou `text-base text-gray-700`

---

### 3. Layout e Espaçamento

*   **Container Principal:** O conteúdo central será contido em um invólucro para não esticar demais em monitores grandes.
    *   *Classes:* `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8`
*   **Navegação (Header):** Simples e fixa no topo.
    *   *Classes:* `bg-white border-b border-gray-200 py-4 px-6 flex justify-between items-center`
*   **Espaçamento Interno de Cards:** `p-6` para um respiro confortável ao redor do conteúdo.

---

### 4. Padrões de Componentes (Snippets)

#### 4.1. Botões
*   **Primário (Salvar, Criar Chamado):**
    `inline-flex justify-center rounded-md border border-transparent bg-blue-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors`
*   **Secundário / Voltar:**
    `inline-flex justify-center rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors`

#### 4.2. Formulários (Inputs e Selects)
*   **Label:** `block text-sm font-medium text-gray-700 mb-1`
*   **Input / Select / Textarea:**
    `block w-full rounded-md border-gray-300 bg-gray-50 border px-3 py-2 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm`

#### 4.3. Badges (Etiquetas)
Usados nas listagens e na visualização detalhada.
*   *Estrutura Base:* `inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium`

#### 4.4. Tabelas (Dashboard)
A lista de chamados deve ser limpa, com divisórias sutis.
*   **Container da Tabela:** `overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg bg-white`
*   **Cabeçalho (TH):** `bg-gray-50 px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-gray-200`
*   **Linha (TR):** `hover:bg-gray-50 transition-colors`
*   **Célula (TD):** `whitespace-nowrap px-6 py-4 text-sm text-gray-900 border-b border-gray-200`

---

### 5. Considerações de UX
*   **Prevenção de Erros:** O formulário de criação deve marcar os campos obrigatórios (*) e o botão de submit deve fornecer clareza na ação (ex: "Abrir Chamado" em vez de apenas "Enviar").
*   **Acessibilidade:** Os contrastes de cor propostos atendem aos requisitos básicos de leitura. Todos os inputs de formulário devem estar devidamente associados às suas labels no HTML.
*   **Feedback Visual:** Elementos interativos (links, botões, linhas da tabela) terão `hover` para indicar que são clicáveis.