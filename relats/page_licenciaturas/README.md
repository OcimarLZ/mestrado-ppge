# Landing Page de Licenciaturas

Esta página gera, para cada SQL de [scripts.sql](scripts.sql):

- um card com indicadores principais;
- um gráfico de linhas em Seaborn com `ano_censo` como eixo temporal;
- uma tabela com os dados retornados.

Também inclui filtro por UF com todas as unidades federativas do Brasil.

## Como executar

Na raiz do projeto:

```powershell
streamlit run relats/page_licenciaturas/landing_licenciaturas.py
```

## Banco de dados

A página tenta conectar nesta ordem:

1. segredo/configuração `INEP_DB_URL` do Streamlit;
2. configuração `BD_INEP` de `config.ini` (SQLite);
3. fallback para `INEP.db` na raiz do projeto.
