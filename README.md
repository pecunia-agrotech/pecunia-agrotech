# Pecunia AgroTech

> **Hackathon UFJF 2026 — Tema 3: Análise Econômica e Financeira da Pecuária Leiteira**

Aplicação local e 100% offline para gestão, planejamento financeiro e diagnóstico especialista da pecuária leiteira. Possui interface em português brasileiro, com bases de código e contratos distribuídos nos repositórios do [**Frontend**](https://github.com/pecunia-agrotech/pecunia-frontend), [**Backend**](https://github.com/pecunia-agrotech/pecunia-backend) e [**Documentação/ADRs**](https://github.com/pecunia-agrotech/pecunia-docs).

---

## 🗺️ Repositórios e Navegação

Acesse diretamente os repositórios oficiais da organização no GitHub:

| Módulo / Repositório | Descrição | Link do Repositório | Links Locais |
| ----- | ----- | ----- | ----- |
| 🐍 **Backend Engine** | API REST em FastAPI, Pydantic v2, SQLite e Motor de Inferência (Regras R01–R07). | [**pecunia-backend**](https://github.com/pecunia-agrotech/pecunia-backend) | [`backend/`](./backend/) • [`tests/`](./backend/tests/) • [`openapi.json`](./backend/openapi.json) |
| ⚛️ **Frontend Application** | Interface gráfica em Next.js (App Router), React, Tailwind CSS e Shadcn UI. | [**pecunia-frontend**](https://github.com/pecunia-agrotech/pecunia-frontend) | [`frontend/`](./frontend/) • [`src/`](./frontend/src/) • [`tests/`](./frontend/tests/) |
| 📚 **Documentação & ADRs** | Especificações de arquitetura, decisões técnicas (ADRs), requisitos e relatórios. | [**pecunia-docs**](https://github.com/pecunia-agrotech/pecunia-docs) | [`docs/`](./docs/) • [`architecture.md`](./docs/architecture.md) • [`requirements.md`](./docs/requirements.md) |
| 🛠️ **Scripts & Automação** | Utilitários de verificação de contratos OpenAPI/TypeScript e geração de DTOs. | — | [`scripts/`](./scripts/) |

### Estrutura Geral do Projeto

| Arquivo / Pasta | Finalidade |
| ----- | ----- |
| 📁 [`backend/`](./backend/) | Módulo do Backend ([Repositório GitHub](https://github.com/pecunia-agrotech/pecunia-backend)). |
| 📁 [`frontend/`](./frontend/) | Módulo do Frontend ([Repositório GitHub](https://github.com/pecunia-agrotech/pecunia-frontend)). |
| 📁 [`docs/`](./docs/) | Documentação e ADRs ([Repositório GitHub](https://github.com/pecunia-agrotech/pecunia-docs)). |
| 📁 [`scripts/`](./scripts/) | Scripts de checagem e sincronização de contratos API/TypeScript. |
| 📄 [`.gitignore`](./.gitignore) | Regras para ignorar arquivos temporários, caches de build (`.next`, `__pycache__`) e banco local. |
| 📄 [`README.md`](./README.md) | Documentação principal com guia de instalação, arquitetura, testes e escopo. |
| 📄 [`SHADCN-LICENSE.md`](./SHADCN-LICENSE.md) | Licença de reutilização dos componentes visuais do Shadcn UI. |
| 📄 [`START.command`](./START.command) / [`START.ps1`](./START.ps1) | Scripts de execução automática da aplicação para macOS/Linux e Windows. |
| 📄 [`setup.sh`](./setup.sh) / [`setup.ps1`](./setup.ps1) | Scripts de preparação inicial de dependências do ambiente. |
| 📄 [`package.json`](./package.json) / [`package-lock.json`](./package-lock.json) | Gerenciamento de versões no ambiente Node.js na raiz. |
| 📄 [`run_local.py`](./run_local.py) | Script orquestrador em Python para inicialização simultânea dos servidores. |
| 📄 [`backup_database.py`](./backup_database.py) | Utilitário para backup seguro do banco de dados SQLite em modo WAL. |

---

## 🚀 Como Rodar a Aplicação

### Pré-requisitos

* **Python 3.12+** (gerenciamento via `uv`)
* **Node.js 20.9+** (Node 24 utilizado na validação)
* Gerenciador de dependências `uv` (`pip install uv`)

> *Nota:* A instalação inicial de dependências requer conexão com a internet. Após a configuração, a aplicação opera 100% offline.

### Execução Automática

#### 🐧 Linux / 🍎 macOS
```bash
chmod +x setup.sh START.command
./setup.sh
./START.command
```

#### 🪟 Windows (PowerShell)
```powershell
.\setup.ps1
.\START.ps1
```

O script realiza o alinhamento de dependências via `uv sync --locked` no [**Backend**](https://github.com/pecunia-agrotech/pecunia-backend), instala os pacotes do [**Frontend**](https://github.com/pecunia-agrotech/pecunia-frontend) via `npm ci`, valida os contratos de API e gera o build final.

> **Pontos de Acesso:**
> - **Interface Web (Frontend):** [http://localhost:3000](http://localhost:3000)
> - **API Healthcheck (Backend):** [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)
> - **Especificação OpenAPI (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs) ou no arquivo [`backend/openapi.json`](./backend/openapi.json)

---

### Módulo de Desenvolvimento (Modo Dev)

Para executar os serviços em terminais separados com suporte a *hot-reload*:

#### 1. Backend ([`pecunia-backend`](https://github.com/pecunia-agrotech/pecunia-backend))
```bash
cd backend
uv sync --locked
uv run uvicorn main:app --reload --port 8000
```

#### 2. Frontend ([`pecunia-frontend`](https://github.com/pecunia-agrotech/pecunia-frontend))
```bash
cd frontend
npm ci
npm run dev
```

> **Variáveis de Ambiente:**  
> O frontend utiliza `NEXT_PUBLIC_API_URL=http://localhost:8000`, configurável em [`frontend/.env.local`](./frontend/.env.example). Alterar essa variável exige um novo build. Para portas customizadas, ajuste `PECUNIA_FRONTEND_ORIGIN` no backend.

---

## 💻 Módulos do Produto e Uso

* **Lançamentos:** Registre receitas e despesas com validações específicas (venda de leite exige volume positivo em litros). O caixa diário utiliza o rateio real daquele mês.
* **Calendário Financeiro:** Seleção diária com histórico detalhado de movimentos, permitindo edições e exclusões com recálculo automático retroativo.
* **Fechamento & DRE:** Painel gerencial com receitas, despesas variáveis/fixas, margens, custo por litro de leite e exportação em CSV ou relatório executivo em Markdown.
* **Análises & Diagnósticos:** Motor de inferência especialista baseado nas Regras R01–R07, com evidências e explicações no formato *COMO* / *PORQUE*.
* **Simulações:** Criação de cenários hipotéticos independentes a partir do histórico real ou do zero para projeções financeiras.
* **Configurações:** Definição mensal e por contexto de custos fixos, vacas em lactação e preço de insumos.

> **Isolamento de Contextos:** O seletor de contexto separa explicitamente **Histórico Real**, **Demonstração** e **Cenário Hipotético**. Os dados de diferentes contextos jamais são somados ou mesclados.

---

## 🗄️ Banco de Dados, Migração e Backup

* **Banco de Dados Principal:** [`backend/data/farm.db`](./backend/data/) (esquema em inglês, versão 2). O caminho pode ser alterado via variável `PECUNIA_DB_PATH`.
* **Migração Automática:** Se existir um banco legado (`backend/data/fazenda.db`), a aplicação realiza backup e migra automaticamente os registros para o `farm.db`. Veja os detalhes de validação da migração em [`docs/migration-validation.json`](./docs/migration-validation.json).
* **Restauração de Demonstração:** No menu *Simulações*, é possível resetar a base de demonstração digitando `RESTAURAR DEMONSTRAÇÃO`, gerando backup preventivo sem afetar o histórico real.

### Backup Manual

Para gerar uma cópia de segurança consistente (com suporte ao modo SQLite WAL):

**Linux / macOS:**
```bash
backend/.venv/bin/python backup_database.py
```

**Windows (PowerShell):**
```powershell
backend\.venv\Scripts\python.exe backup_database.py
```

*Os arquivos de backup são salvos no diretório `/backups`.*

---

## 🧪 Verificação e Qualidade de Código

### Backend ([`pecunia-backend`](https://github.com/pecunia-agrotech/pecunia-backend))
```bash
cd backend
uv run pytest -q
uv run ruff check .
uv run mypy src main.py
```
*Testes localizados em [`backend/tests/`](./backend/tests/).*

### Frontend ([`pecunia-frontend`](https://github.com/pecunia-agrotech/pecunia-frontend))
```bash
cd frontend
npm run typecheck
npm run lint
npm test
npm run contracts:check
npm run build
```
*Testes localizados em [`frontend/tests/`](./frontend/tests/).*

* **Regeneração de Contratos TypeScript:** `npm run contracts` (no diretório frontend via script em [`scripts/`](./scripts/)).
* **Testes E2E (Playwright):** `npx playwright install chromium` e `npm run test:e2e` (utilizar banco descartável).

> **Resultado da Validação:** **46 testes de backend** e **19 testes de frontend** aprovados com 100% de sucesso em checagens de tipos, linting, validação de contratos OpenAPI e build final. Detalhes completos em [`docs/verification.md`](./docs/verification.md).

---

## 📚 Documentação Técnica Detalhada

Acesse a documentação técnica completa localizada no repositório [**pecunia-docs**](https://github.com/pecunia-agrotech/pecunia-docs):

* 📐 [**`docs/architecture.md`**](./docs/architecture.md) — Arquitetura de Software (Clean Architecture), decisões de design (ADRs) e fórmulas financeiras/zootécnicas.
* 📋 [**`docs/requirements.md`**](./docs/requirements.md) — Matriz de Rastreabilidade dos Requisitos Funcionais (RF01–RF10).
* 🔍 [**`docs/verification.md`**](./docs/verification.md) — Evidências, logs e relatórios de validação dos testes unitários, de integração e E2E.
* 📄 [**docs/openapi.json`**](./backend/openapi.json) — Especificação técnica OpenAPI 3.0 completa da API REST.
* 🖼️ Capturas de Tela: [**Dashboard**](./docs/dashboard.png) e [**Calendário Financeiro**](./docs/calendar.png).

---

## 🎯 Escopo da Entrega

**Incluído:** Análise gerencial local por data de lançamento, DRE gerencial completo, fluxo de caixa, simulação de cenários, motor de inferência especialista com explicações e operação offline.

**Fora do Escopo:** Integração bancária automatizada, módulos tributários/fiscais, autenticação multiusuário na nuvem ou modelos de previsão biológica. O protótipo legado em Streamlit permanece arquivado separadamente.
