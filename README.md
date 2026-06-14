# Sistema de Controle de Chamados Internos

Sistema monolítico para digitalizar, centralizar e organizar pedidos de suporte interno, com distribuição automática de tarefas.

## Justificativa Tecnológica
Optou-se por uma arquitetura monolítica utilizando Python e Flask, banco de dados embutido SQLite e frontend renderizado no servidor via Jinja2 + Tailwind CSS (via CDN). Essa abordagem reduz atritos entre front e backend, facilita o desenvolvimento local sem processos de build complexos de JS e atende aos requisitos de código limpo (SOLID e DRY) mantendo a simplicidade de manutenção por equipes pequenas.

## Pré-requisitos
- Python 3.10 ou superior.

## Como Executar Localmente

1. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie a aplicação:**
   ```bash
   python run.py
   ```
   > **Nota:** O banco de dados (`database/app.db`) e os dados de exemplo (Seed de Responsáveis) serão inicializados automaticamente no primeiro uso.

4. **Acesse no navegador:**
   [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Considerações para Produção

Esta aplicação foi desenvolvida com foco em simplicidade e prototipagem rápida. Para um ambiente de produção real, as seguintes melhorias são recomendadas:

- **Servidor WSGI:** Utilizar um servidor de produção como Gunicorn ou uWSGI em vez do servidor de desenvolvimento do Flask.
- **Banco de Dados:** Para cenários de alta concorrência, migrar o SQLite para um SGBD mais robusto como PostgreSQL ou MySQL.
- **Variáveis de Ambiente:** Garantir que `FLASK_DEBUG` esteja configurado como `False` no arquivo `.env` do ambiente de produção.
- **Autenticação:** O sistema atual não possui controle de acesso. O próximo passo crucial para um ambiente real seria implementar um sistema de login para proteger o acesso aos dados e funcionalidades.