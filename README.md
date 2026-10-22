# Pecunia AgroTech · versão 2

Aplicação local para o Tema 3 do Hackathon UFJF 2026: análise econômica e financeira da pecuária leiteira. Interface em português brasileiro, código e contratos em inglês. Frontend Next.js/React/TypeScript e backend Python 3.12+/FastAPI/Pydantic v2/SQLite. Não utiliza serviços externos durante a operação.

## Executar neste computador

1. Encerre a versão anterior com **Ctrl+C no terminal em que ela foi iniciada**. O iniciador não encerra processos existentes nas portas 3000 e 8000.
2. Abra o Terminal e entre na pasta do projeto:

```bash
cd "/Users/lucasrocha/Documents/Codex/2026-10-20/role-atue-como-um-desenvolvedor-senior/outputs/pecunia-agrotech"
./START.command
```

3. Aguarde a mensagem de inicialização e abra **http://localhost:3000**. A API fica em **http://localhost:8000/api/v1/health**.
4. Use Ctrl+C para encerrar os dois servidores.

Também é possível dar dois cliques em `START.command` no Finder. Esta versão não usa Streamlit nem o caminho antigo `work/.venv/bin/streamlit`.

## Preparar em outro computador

Instale Python 3.12+ e Node.js 20.9+; Node 24 foi usado na validação. A instalação inicial requer internet. Na pasta do projeto:

```bash
chmod +x setup.sh START.command
./setup.sh
./START.command
```

O script prepara o ambiente com `uv sync --locked`, instala o frontend por `npm ci`, verifica contratos e gera o build. Depois disso, a execução normal é offline. As versões reproduzíveis estão em `backend/uv.lock` e `frontend/package-lock.json`.

Para desenvolvimento, em terminais separados:

```bash
cd backend
uv sync --locked
uv run uvicorn main:app --reload --port 8000
```

```bash
cd frontend
npm ci
npm run dev
```

O frontend usa `NEXT_PUBLIC_API_URL=http://localhost:8000`, configurável em `frontend/.env.local` a partir de `.env.example`. Alterar essa variável exige novo build. Para desenvolvimento em outra porta local, configure `PECUNIA_FRONTEND_ORIGIN` no backend com uma origem HTTP de loopback. Não exponha estes servidores sem autenticação à rede pública.

## Usar o produto

- **Lançamentos:** registre receitas e despesas; venda de leite exige litros positivos. O caixa do dia utiliza o rateio real daquele mês.
- **Calendário financeiro:** selecione um dia, consulte os movimentos, edite ou exclua mediante confirmação. Alterações retroativas atualizam o fechamento correspondente.
- **Fechamento & DRE:** consulte receitas, variáveis, fixos, resultado, custo por litro, evolução diária e distribuição de gastos. Exporte CSV ou relatório executivo Markdown.
- **Análises & diagnósticos:** consulte indicadores, regras R01–R07, evidências e explicações COMO/PORQUE.
- **Simulações:** crie um cenário vazio ou copie somente o mês selecionado do contexto de origem. Altere seus registros e configurações independentemente do histórico real.
- **Configurações:** informe custos fixos, vacas em lactação e preço do insumo. Salve por mês e contexto. Valores digitados não afetam o resultado antes da confirmação do banco.

O seletor de contexto distingue **Histórico real**, **Demonstração** e **Cenário hipotético**. Os resultados nunca somam esses contextos. Campos sem informação aparecem como indisponíveis; não são convertidos em zero.

## Banco, migração e backup

O novo banco é `backend/data/farm.db`, com esquema em inglês e versão 2. `PECUNIA_DB_PATH` pode apontar para um banco de teste separado. Não há acesso direto do navegador ao SQLite.

Na primeira inicialização padrão, se existir `backend/data/fazenda.db` da versão anterior, o backend faz backup e importa os registros para `farm.db`, preservando IDs, centavos, versões, descrições e identificação de simulação. O arquivo anterior permanece intacto. A migração nesta entrega foi testada sobre uma cópia de 74 registros; o banco ativo não foi migrado enquanto o servidor anterior continuava em execução. Veja `docs/migration-validation.json`.

Custos legados de meses com contextos mistos recebem sinalização para revisão. Número de vacas e preço do insumo desconhecidos não são inventados. Vendas antigas sem volume continuam preservadas e precisam ser corrigidas antes dos indicadores dependentes de litros.

Sem banco anterior, o contexto real começa vazio e a demonstração recebe 30 dias de dados persistidos. Reiniciar não duplica o seed. Para restaurar somente a demonstração, abra Simulações, confirme a operação e digite **RESTAURAR DEMONSTRAÇÃO**. A operação gera backup e preserva o histórico real e os demais cenários.

Backup manual consistente, inclusive com SQLite em WAL:

```bash
backend/.venv/bin/python backup_database.py
```

Os backups ficam em `backups/`. Para recuperar, encerre os servidores, guarde o banco atual e seus arquivos WAL/SHM, restaure a cópia no caminho configurado e reinicie. Não substitua um banco aberto. O ZIP de código não contém bancos privados, backups ou dependências.

## Verificações

```bash
cd backend
uv run pytest -q
uv run ruff check .
uv run mypy src main.py
```

```bash
cd frontend
npm run typecheck
npm run lint
npm test
npm run contracts:check
npm run build
```

Para regenerar contratos após mudar DTOs: `npm run contracts`. Para E2E, inicie os dois servidores, prepare o Chromium com `npx playwright install chromium` e execute `npm run test:e2e`. Use exclusivamente um banco descartável para esses testes: o roteiro cria e remove registros.

Resultado desta entrega: **46 testes de backend e 19 de frontend aprovados**; tipos, lint, contratos e build aprovados. Os 2 roteiros Playwright não chegaram a executar: o macOS bloqueou a criação do processo Chromium com `MachPortRendezvousServer: Permission denied`. A verificação visual complementar ocorreu no navegador integrado. Responsividade automatizada e navegação integral por teclado permanecem sem aprovação E2E neste ambiente; não são declaradas validadas.

## Documentação

- `docs/architecture.md`: arquitetura, fórmulas e decisões provisórias.
- `docs/requirements.md`: rastreabilidade RF01–RF10.
- `docs/verification.md`: evidências e limites da validação.
- `backend/openapi.json`: contrato completo; disponível também em `/openapi.json` com a API iniciada.
- `docs/dashboard.png` e `docs/calendar.png`: capturas da interface integrada.

Escopo: análise gerencial por data de lançamento, sem integração bancária, tributação, autenticação multiusuário ou previsão biológica. O antigo protótipo Streamlit continua separado desta aplicação.
