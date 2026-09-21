import configparser
import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from sqlalchemy import create_engine, text


UF_SIGLAS = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT",
    "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO",
    "RR", "SC", "SP", "SE", "TO",
]


def carregar_engine() -> object:
    db_url = None
    try:
        db_url = st.secrets.get("INEP_DB_URL") if hasattr(st, "secrets") else None
    except Exception:
        db_url = None

    if db_url:
        return create_engine(db_url)

    root = Path(__file__).resolve().parents[2]
    config_path = root / "config.ini"
    default_sqlite = root / "INEP.db"

    if not config_path.exists():
        return create_engine(f"sqlite:///{default_sqlite.as_posix()}")

    parser = configparser.ConfigParser()
    parser.read(config_path, encoding="utf-8")

    if "BD_INEP" not in parser:
        return create_engine(f"sqlite:///{default_sqlite.as_posix()}")

    bd = parser["BD_INEP"]
    sgdb = bd.get("SGDB", "sqlite").strip().lower()

    if sgdb == "sqlite":
        pasta_local = bd.get("PASTA_LOCAL", "").replace("\\", "/")
        arquivo = bd.get("DW", "INEP.db").strip()

        if pasta_local:
            pasta_limpa = pasta_local.strip("/")
            sqlite_path = Path(pasta_limpa) / arquivo
        else:
            sqlite_path = default_sqlite

        if not sqlite_path.exists():
            sqlite_path = default_sqlite

        return create_engine(f"sqlite:///{sqlite_path.as_posix()}")

    return create_engine(f"sqlite:///{default_sqlite.as_posix()}")


def parse_sqls(caminho_sql: Path) -> list[dict]:
    conteudo = caminho_sql.read_text(encoding="utf-8")
    linhas = conteudo.splitlines()

    consultas = []
    bloco_atual = []
    comentarios = []
    titulo_atual = ""

    for linha in linhas:
        strip = linha.strip()

        if strip.startswith("#"):
            comentarios.append(strip.lstrip("#").strip())
            continue

        if re.match(r"^\s*SELECT\b", linha, flags=re.IGNORECASE):
            if bloco_atual:
                consultas.append({"titulo": titulo_atual, "sql": "\n".join(bloco_atual).strip()})
                bloco_atual = []

            titulo_atual = " | ".join([c for c in comentarios if c])
            if not titulo_atual:
                titulo_atual = f"Consulta {len(consultas) + 1}"
            comentarios = []

            bloco_atual.append(linha)
            continue

        if bloco_atual:
            bloco_atual.append(linha)

    if bloco_atual:
        consultas.append({"titulo": titulo_atual, "sql": "\n".join(bloco_atual).strip()})

    for i, q in enumerate(consultas, start=1):
        if not q["titulo"]:
            q["titulo"] = f"Consulta {i}"
        q["id"] = i

    return consultas


def aplicar_filtro_uf(sql: str, uf: str) -> tuple[str, dict]:
    if uf == "TODOS":
        return sql, {}

    if re.search(r"\bwhere\b", sql, flags=re.IGNORECASE):
        sql_filtrado = re.sub(
            r"\bwhere\b",
            "WHERE cc.estado = :uf AND ",
            sql,
            count=1,
            flags=re.IGNORECASE,
        )
        return sql_filtrado, {"uf": uf}

    if re.search(r"\bfrom\s+curso_censo\s+cc\b", sql, flags=re.IGNORECASE):
        sql_filtrado = f"{sql}\nWHERE cc.estado = :uf"
        return sql_filtrado, {"uf": uf}

    return sql, {}


@st.cache_data(show_spinner=False)
def executar_consulta(sql: str, uf: str) -> tuple[pd.DataFrame, str | None]:
    engine = carregar_engine()
    sql_exec, params = aplicar_filtro_uf(sql, uf)

    try:
        df = pd.read_sql(text(sql_exec), engine, params=params)
        return df, None
    except Exception as exc:
        return pd.DataFrame(), str(exc)


def montar_grafico_linhas(df: pd.DataFrame, titulo: str):
    if "ano_censo" not in df.columns:
        return None, "Sem coluna ano_censo para montar série temporal."

    temp = df.copy()
    temp["ano_censo"] = pd.to_numeric(temp["ano_censo"], errors="coerce")
    temp = temp.dropna(subset=["ano_censo"])

    colunas_numericas = [
        c for c in temp.columns
        if c != "ano_censo" and pd.api.types.is_numeric_dtype(temp[c])
    ]

    if not colunas_numericas:
        return None, "Não há colunas numéricas para gráfico de linhas."

    agregado = temp.groupby("ano_censo", as_index=False)[colunas_numericas].sum()

    if len(colunas_numericas) <= 6:
        series = colunas_numericas
        mensagem = None
    else:
        series = colunas_numericas[:6]
        mensagem = "Mais de 6 colunas numéricas detectadas: exibindo as 6 primeiras séries."

    longo = agregado.melt(
        id_vars=["ano_censo"],
        value_vars=series,
        var_name="serie",
        value_name="valor",
    )

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 4.2))
    sns.lineplot(data=longo, x="ano_censo", y="valor", hue="serie", marker="o", ax=ax)
    ax.set_title(titulo, fontsize=12, weight="bold")
    ax.set_xlabel("Ano do Censo")
    ax.set_ylabel("Valor")
    ax.ticklabel_format(style="plain", axis="x")
    ax.legend(title="Série", fontsize=8, title_fontsize=9, loc="best")
    fig.tight_layout()

    return fig, mensagem


def injetar_css():
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
}

.stApp {
    background:
      radial-gradient(circle at 5% 10%, #dbeafe 0%, transparent 40%),
      radial-gradient(circle at 90% 5%, #fae8ff 0%, transparent 35%),
      linear-gradient(130deg, #f8fafc 0%, #eef2ff 100%);
}

.hero {
    background: linear-gradient(120deg, #0f172a 0%, #1d4ed8 45%, #0ea5e9 100%);
    border-radius: 18px;
    padding: 1.5rem;
    color: white;
    box-shadow: 0 20px 50px rgba(15, 23, 42, 0.25);
    margin-bottom: 1rem;
}

.hero h1 {
    margin: 0;
    font-size: 1.9rem;
    letter-spacing: 0.3px;
}

.hero p {
    margin: 0.5rem 0 0 0;
    opacity: 0.92;
}

.card {
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 16px;
    padding: 1rem;
    box-shadow: 0 8px 20px rgba(30, 41, 59, 0.08);
}
</style>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(
        page_title="Landing Licenciaturas",
        page_icon="📈",
        layout="wide",
    )
    injetar_css()

    st.markdown(
        """
<div class="hero">
  <h1>Licenciaturas no Brasil</h1>
  <p>Painel analítico com consultas SQL, tabelas dinâmicas e gráficos de linhas por ano do censo.</p>
</div>
        """,
        unsafe_allow_html=True,
    )

    base_dir = Path(__file__).resolve().parent
    caminho_sql = base_dir / "scripts.sql"
    consultas = parse_sqls(caminho_sql)

    col_filtro, col_info = st.columns([1, 2])
    with col_filtro:
        uf = st.selectbox(
            "Filtrar por UF",
            options=["TODOS"] + UF_SIGLAS,
            index=0,
            help="Aplica o filtro de unidade da federação nas consultas da tabela curso_censo.",
        )

    with col_info:
        st.markdown(
            f"<div class='card'><b>Total de SQLs detectados:</b> {len(consultas)}<br/><b>Filtro atual:</b> {uf}</div>",
            unsafe_allow_html=True,
        )

    st.write("")

    for consulta in consultas:
        titulo = consulta["titulo"]
        sql = consulta["sql"]

        with st.container(border=True):
            st.subheader(f"{consulta['id']:02d}. {titulo}")

            with st.expander("Ver SQL desta consulta"):
                st.code(sql, language="sql")

            df, erro = executar_consulta(sql, uf)

            if erro:
                st.error(f"Erro ao executar SQL: {erro}")
                continue

            col1, col2, col3 = st.columns(3)
            col1.metric("Registros", len(df))

            if "ano_censo" in df.columns and not df.empty:
                anos = pd.to_numeric(df["ano_censo"], errors="coerce").dropna()
                if anos.empty:
                    col2.metric("Ano inicial", "-")
                    col3.metric("Ano final", "-")
                else:
                    col2.metric("Ano inicial", int(anos.min()))
                    col3.metric("Ano final", int(anos.max()))
            else:
                col2.metric("Ano inicial", "-")
                col3.metric("Ano final", "-")

            fig, aviso = montar_grafico_linhas(df, titulo)
            if aviso:
                st.info(aviso)
            if fig is not None:
                st.pyplot(fig, width="stretch")

            st.markdown("**Tabela de dados**")
            st.dataframe(df, width="stretch", height=320)


if __name__ == "__main__":
    import sys
    if "streamlit" not in sys.modules:
        print(
            "\nEste arquivo deve ser executado via Streamlit:\n"
            "  streamlit run relats/page_licenciaturas/landing_licenciaturas.py\n"
        )
        sys.exit(0)
    main()
