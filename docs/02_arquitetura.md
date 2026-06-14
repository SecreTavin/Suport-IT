# Documento de Arquitetura
## Sistema de Controle de Chamados Internos

### 1. Visão Arquitetural
A aplicação seguirá uma arquitetura em camadas dentro de um monolito Flask, garantindo a separação de responsabilidades (SOLID):
- **Controllers (Rotas/Views):** Lidam com requisições HTTP, renderização de templates (Jinja2) e redirecionamentos.
- **Services (Lógica de Negócio):** Contêm as regras de negócio puras (ex: distribuição automática), orquestrando chamadas aos repositórios.
- **Repositories (Acesso a Dados):** Isolam o código de banco de dados (SQL/SQLite), retornando objetos de domínio.
- **Models/Entities:** Representam as estruturas de dados e domínios da aplicação.

### 2. Estrutura de Pastas
```text
/
├── app/
│   ├── __init__.py              # Inicialização do app Flask
│   ├── models/                  # Entidades e Enums
│   │   └── domain.py
│   ├── repositories/            # Camada de abstração do Banco de Dados
│   │   ├── database.py          # Conexão com SQLite
│   │   ├── chamado_repo.py
│   │   └── responsavel_repo.py
│   ├── services/                # Regras de Negócio
│   │   └── chamado_service.py
│   ├── controllers/             # Flask Blueprints (Rotas)
│   │   └── chamado_controller.py
│   └── templates/               # Views (Jinja2 + Tailwind)
│       ├── base.html
│       ├── dashboard.html       # Lista de chamados
│       ├── chamado_form.html    # Criar/Editar
│       └── chamado_view.html    # Detalhes
├── database/
│   ├── schema.sql               # DDL para criação das tabelas
│   └── seed.sql                 # Carga inicial (Responsáveis)
├── docs/
│   ├── 01_prd.md
│   └── 02_arquitetura.md
├── requirements.txt             # Dependências (Flask, etc.)
├── README.md                    # Instruções de Setup
└── run.py                       # Ponto de entrada da aplicação
```

### 3. Modelagem e Tipagem (Domain Contracts)

```python
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

class Prioridade(str, Enum):
    BAIXA = "Baixa"
    MEDIA = "Média"
    ALTA = "Alta"

class Status(str, Enum):
    ABERTO = "Aberto"
    EM_ANDAMENTO = "Em Andamento"
    RESOLVIDO = "Resolvido"
    FECHADO = "Fechado"

@dataclass
class Responsavel:
    id: int
    nome: str

@dataclass
class Chamado:
    id: int
    titulo: str
    descricao: str
    prioridade: Prioridade
    status: Status
    responsavel_id: int
    data_abertura: datetime
```

### 4. Contratos de Serviço e Repositório (Assinaturas)

#### 4.1. Camada de Repositório (`app/repositories/`)
Responsável por encapsular o SQL e a interação com o SQLite.

```python
# app/repositories/responsavel_repo.py
def listar_todos() -> List[Responsavel]: ...
def obter_por_id(responsavel_id: int) -> Optional[Responsavel]: ...

# app/repositories/chamado_repo.py
def listar_todos(filtro_status: Optional[str] = None, filtro_prioridade: Optional[str] = None) -> List[Chamado]: ...
def obter_por_id(chamado_id: int) -> Optional[Chamado]: ...
def criar(chamado: Chamado) -> int: ...
def atualizar(chamado: Chamado) -> None: ...
def contar_chamados_pendentes_por_responsavel() -> dict[int, int]: ...
```

#### 4.2. Camada de Serviço (`app/services/`)
Responsável por aplicar as regras de negócio, especialmente a RN01 (Distribuição Automática).

```python
# app/services/chamado_service.py

@dataclass
class ChamadoCreateDTO:
    titulo: str
    descricao: str
    prioridade: Prioridade
    atribuicao_automatica: bool
    responsavel_id: Optional[int] = None

@dataclass
class ChamadoUpdateDTO:
    chamado_id: int
    prioridade: Prioridade
    status: Status
    titulo: str
    descricao: str

def criar_chamado(dados: ChamadoCreateDTO) -> Chamado: ...
def atualizar_chamado(dados: ChamadoUpdateDTO) -> Chamado: ...
def determinar_responsavel_automatico() -> int: ...
def listar_chamados(status: Optional[str] = None, prioridade: Optional[str] = None) -> List[Chamado]: ...
def obter_chamado(chamado_id: int) -> Chamado: ...
```

### 5. Plano de Rotas (Controllers / Flask Blueprints)

- **GET `/`**
  - **Controller:** Renderiza `dashboard.html`.
  - **Ação:** Chama `chamado_service.listar_chamados()` (suporta *query params* para filtros).
  
- **GET `/chamados/novo`**
  - **Controller:** Renderiza `chamado_form.html`.
  - **Ação:** Carrega a lista de responsáveis via repositório para popular o `<select>`.

- **POST `/chamados`**
  - **Controller:** Processa form de criação.
  - **Ação:** Mapeia form para `ChamadoCreateDTO`, chama `chamado_service.criar_chamado(dados)` e redireciona para `/`.

- **GET `/chamados/<int:id>`**
  - **Controller:** Renderiza `chamado_view.html`.
  - **Ação:** Chama `chamado_service.obter_chamado(id)` para exibição detalhada.

- **GET `/chamados/<int:id>/editar`**
  - **Controller:** Renderiza `chamado_form.html` (modo edição).
  - **Ação:** Carrega os dados atuais do chamado para pré-preencher o formulário.

- **POST `/chamados/<int:id>/editar`**
  - **Controller:** Processa form de edição.
  - **Ação:** Mapeia form para `ChamadoUpdateDTO`, chama `chamado_service.atualizar_chamado(dados)` e redireciona para `/chamados/<id>`.
