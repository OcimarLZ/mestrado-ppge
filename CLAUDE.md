# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Data/analysis workspace for a master's dissertation (UFFS, Programa de Pós-Graduação em Educação) about
private/EaD expansion in teacher-training higher education in Brazil, built from INEP/CAPES census
microdata. The repo has two layers that should be kept mentally separate:

1. **The research pipeline** (root-level `bdados/`, `relats/`, `sqls/`, `utilities/`, `modelos_dados/`,
   `app/base/`) — Python scripts that build local SQLite databases from INEP/CAPES open data and produce
   the charts/tables already committed under `docs/graficos/` and `docs/tabelas/`.
2. **`web_app/`** — a FastAPI + React application that turns that research into a website. This is
   presently a *single* full-stack project (DB-backed CMS + admin UI), not yet split into the two
   deliverables the user actually wants (see "Two distinct deliverables" below).

There is no git repository initialized here yet, and no top-level test suite.

## Two distinct deliverables (important context, not yet reflected in the code layout)

- **Deliverable 1 — static landing page (urgent, this week).** A GitHub Pages–publishable site
  (static HTML/CSS/JS, no live backend; at most a bundled JSON/XML data file) to present the
  dissertation to advisors/committee members. Charts shown on this page should link back to the
  original figure in `docs/OLZ_Defesa_V_2.03.pdf` (source content also available as
  `docs/OLZ_Defesa_V_2.03.odt`) so reviewers can cross-check against the defense document.
- **Deliverable 2 — interactive data site (later).** A site with live interactive queries/dashboards
  backed by `bdados/INEP.db`. This is what `web_app/backend` is currently wired for
  (`MICRODATA_DB_URL` in `web_app/backend/database.py` points straight at `bdados/INEP.db`).

`web_app/frontend` today hardcodes `http://127.0.0.1:8000` API calls (see `src/pages/Home.tsx`,
`src/components/Layout.tsx`) and has no build-time static-export path, so it cannot be deployed to
GitHub Pages as-is — it needs a running FastAPI backend. When working on the "landing page" ask, treat
that as effectively a separate, static-only project: either a new lightweight site, or the existing
`web_app/frontend` reworked to fetch pre-exported static JSON instead of calling a live API (with the
admin/CRUD routes excluded from that build).

## Repository layout

```
bdados/          SQLite databases + DB access layer for the research pipeline
  INEP.db          Main microdata warehouse (census tables, see below)
  CAPES.db, OBSERVA.db   Other data sources
  ler_bdados_to_df.py    carregar_dataframe(sql) -> pandas DataFrame, reads config.ini [BD_INEP]
  tratar_bdados_app.py   Connection/config handling (configparser over config.ini) + save helpers
  tratar_dados_externos.py, atualizar_dados_locais.py   ETL from downloaded INEP source files

relats/          One script per report/chart, e.g. `discentes_geral.py`, `cursos_por_area.py`.
                  Pattern: build SQL -> bdados.ler_bdados_to_df.carregar_dataframe(sql) -> pandas ->
                  matplotlib/seaborn/plotly figure and/or utilities.formatar_tabela.dataframe_to_html
                  -> output written into docs/graficos/*.png (+ some *.html for interactive plotly
                  charts) and docs/tabelas/*.html.

sqls/            Ad-hoc/organized SQL queries (e.g. sqls/anped/*.sql) paired with exported .xlsx results.

utilities/       formatar_tabela.py (HTML table styling), tratar_dados.py, log.py, salvar_arq_externo.py.

modelos_dados/   SQLAlchemy models matching the CURRENT bdados/INEP.db schema: flat, prefixed table
                  names (comum_*, superior_*, basica_*) with no DB schema/namespace, since SQLite has
                  no cross-schema support. This is the authoritative model set.

app/base/        Older/experimental code. inep_models.py, capes_models.py, observa_models.py here are
                  a divergent version of the same models using Postgres-style schema-qualified table
                  names (e.g. `graduacao.ies`, table_args={'schema': 'graduacao'}) — these do NOT match
                  the current SQLite databases. gerar_grafico_*.py also has a stale hardcoded path
                  (D:/ProjetosPY/inep/INEP.db) rather than the config.ini-driven path. Treat this
                  directory as legacy/reference, not a source of truth — prefer modelos_dados/.

docs/            Output/deliverable layer.
  OLZ_Defesa_V_2.03.pdf / .odt   The dissertation defense document (source of truth for chart context).
  graficos/        Pre-generated chart images (.png) and a few interactive plotly exports (.html).
  tabelas/         Pre-generated HTML/CSV data tables.
  c4_nivel2_container.puml   C4 container diagram (PlantUML).

web_app/
  backend/   FastAPI app (main.py, models.py, schemas.py, database.py, seed_data.py). Two SQLite
             engines: `engine` -> site_cms.db (CMS content: pages, hero cards, site settings, section
             visuals) and `microdata_engine` -> bdados/INEP.db (raw analytical queries via
             PageContent.sql_query / SectionVisual.sql_query, executed with pandas.read_sql_query).
             Content model is a self-referencing tree (PageContent.parent_id) rendered as
             chapters/sections; SectionVisual attaches images/charts/SQL-driven tables to a section.
  frontend/  React 19 + TypeScript + Vite app (react-router-dom, recharts, lucide-react, axios).
             Routes: `/` (Home.tsx), `/capitulo/:slug` (GenericChapterPage.tsx, renders the
             PageContent tree), `/admin` (Admin.tsx, CRUD over the CMS). DynamicSection/VisualManager/
             VisualElement/IconPicker components render the tree + attached visuals. themes.ts holds
             site theme presets consumed by Layout.tsx.

config.ini       INI file read via configparser by bdados/tratar_bdados_app.py. `[BD_INEP]` section
                  defines SGDB/PASTA_LOCAL/DW used to build the INEP.db connection string; also holds
                  a `[Licenca]` key block (treat as sensitive, do not print/log its contents).
```

## Running things

### Research pipeline (root-level Python)

No requirements.txt exists at the repo root; `app/base/requirements.txt` (UTF-16 encoded) lists the
closest approximation: pandas, matplotlib, seaborn, plotly, SQLAlchemy, openpyxl, Flask. A `venv/`
already exists at the repo root — prefer activating it over creating a new environment.

Reports are run as standalone scripts from the repo root (they import `bdados.*` and `utilities.*` as
packages), e.g.:

```bash
python relats/discentes_geral.py
```

This regenerates the corresponding file(s) under `docs/tabelas/` and/or `docs/graficos/`.

### web_app backend (FastAPI)

```bash
cd web_app/backend
# .venv already present; activate it (Windows: .venv\Scripts\Activate.ps1)
uvicorn main:app --reload
```

`web_app/backend/requirements.txt` is currently **empty** — if setting up a fresh environment, install
at minimum: fastapi, uvicorn, sqlalchemy, pandas, python-dotenv, pydantic (check `.venv` for exact
pinned versions if unsure). `.env` in `web_app/backend/` may hold `CMS_DB_URL` / `MICRODATA_DB_URL`
overrides (see `database.py`) — do not print its contents.

On startup the app auto-creates CMS tables and seeds `DashboardSummary`, `SiteSettings`, and
`HomeCard` if empty (`seed_database()` in `main.py`, plus `seed_data.seed_all()`).

### web_app frontend (Vite/React)

```bash
cd web_app/frontend
npm install     # first time
npm run dev     # dev server (expects backend at http://127.0.0.1:8000)
npm run build   # tsc -b && vite build -> dist/
npm run lint    # oxlint
```

No test runner is configured in either the frontend or backend.

## Working conventions specific to this repo

- Prose, UI copy, commit-worthy comments, and variable/domain names throughout the codebase are in
  Portuguese (pt-BR) — match that when adding content, labels, or docstrings meant for the dissertation
  site.
- When adding a new report script under `relats/`, follow the existing pattern: SQL string ->
  `bdados.ler_bdados_to_df.carregar_dataframe` -> pandas transform -> `utilities.formatar_tabela` for
  HTML tables and/or matplotlib/seaborn/plotly for `docs/graficos/`. Don't invent a new data-access
  path — reuse `carregar_dataframe`.
- When touching database models, cross-check the target file's table names against the actual SQLite
  schema (`sqlite3 bdados/INEP.db ".tables"` or equivalent) before trusting `app/base/*_models.py` —
  it's known to be stale relative to `modelos_dados/*_models.py`.
- Any static/GitHub-Pages-facing work must not assume a reachable backend at request time; data needed
  client-side has to be baked in at build time (static JSON/XML) rather than fetched from FastAPI.
