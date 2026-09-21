import configparser
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


UF_SIGLAS = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT",
    "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO",
    "RR", "SC", "SP", "SE", "TO",
]


def carregar_engine() -> object:
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
            sqlite_path = Path(pasta_local.strip("/")) / arquivo
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
    bloco = []
    comentarios = []
    titulo_atual = ""

    for linha in linhas:
        strip = linha.strip()

        if strip.startswith("#"):
            comentarios.append(strip.lstrip("#").strip())
            continue

        if re.match(r"^\s*SELECT\b", linha, flags=re.IGNORECASE):
            if bloco:
                consultas.append({"titulo": titulo_atual, "sql": "\n".join(bloco).strip()})
                bloco = []

            titulo_atual = " | ".join([c for c in comentarios if c])
            if not titulo_atual:
                titulo_atual = f"consulta_{len(consultas) + 1:02d}"
            comentarios = []
            bloco.append(linha)
            continue

        if bloco:
            bloco.append(linha)

    if bloco:
        consultas.append({"titulo": titulo_atual, "sql": "\n".join(bloco).strip()})

    for i, q in enumerate(consultas, start=1):
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
        return f"{sql}\nWHERE cc.estado = :uf", {"uf": uf}

    return sql, {}


def detectar_tipo_agregacao(sql: str) -> str:
    tem_count = bool(re.search(r"\bcount\s*\(", sql, flags=re.IGNORECASE))
    tem_sum = bool(re.search(r"\bsum\s*\(", sql, flags=re.IGNORECASE))

    if tem_count and tem_sum:
        return "count_sum"
    if tem_count:
        return "count"
    if tem_sum:
        return "sum"
    return "agg"


def limpar_nome(valor: str, max_len: int = 80) -> str:
    txt = valor.lower().strip()
    txt = re.sub(r"[^a-z0-9_]+", "_", txt)
    txt = re.sub(r"_+", "_", txt).strip("_")
    if not txt:
        txt = "sem_nome"
    return txt[:max_len]


def transformar_para_planilha(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    if "ano_censo" not in df.columns:
        return df

    base = df.copy()
    base["ano_censo"] = pd.to_numeric(base["ano_censo"], errors="coerce")
    base = base.dropna(subset=["ano_censo"])
    if base.empty:
        return base

    base["ano_censo"] = base["ano_censo"].astype(int)

    colunas_numericas = [
        c for c in base.columns
        if c != "ano_censo" and pd.api.types.is_numeric_dtype(base[c])
    ]

    colunas_agrupamento = [
        c for c in base.columns
        if c not in ["ano_censo"] + colunas_numericas
    ]

    if not colunas_numericas:
        return base

    if len(colunas_numericas) == 1:
        valor_col = colunas_numericas[0]
        indice = colunas_agrupamento if colunas_agrupamento else ["agrupamento"]
        if not colunas_agrupamento:
            base["agrupamento"] = valor_col
        piv = base.pivot_table(
            index=indice,
            columns="ano_censo",
            values=valor_col,
            aggfunc="sum",
            fill_value=0,
        ).reset_index()
    else:
        longo = base.melt(
            id_vars=["ano_censo"] + colunas_agrupamento,
            value_vars=colunas_numericas,
            var_name="agrupamento",
            value_name="valor",
        )
        indice = ["agrupamento"] + colunas_agrupamento
        piv = longo.pivot_table(
            index=indice,
            columns="ano_censo",
            values="valor",
            aggfunc="sum",
            fill_value=0,
        ).reset_index()

    colunas_anos = sorted([c for c in piv.columns if isinstance(c, int)])
    colunas_nao_anos = [c for c in piv.columns if c not in colunas_anos]
    return piv[colunas_nao_anos + colunas_anos]


def escolher_uf() -> str:
    print("\nEscolha o filtro de UF:")
    print("0 - TODOS")
    for i, uf in enumerate(UF_SIGLAS, start=1):
        print(f"{i:02d} - {uf}")

    while True:
        entrada = input("Digite a opção (número) ou a sigla da UF: ").strip().upper()
        if entrada == "0" or entrada == "TODOS":
            return "TODOS"

        if entrada in UF_SIGLAS:
            return entrada

        if entrada.isdigit():
            idx = int(entrada)
            if 1 <= idx <= len(UF_SIGLAS):
                return UF_SIGLAS[idx - 1]

        print("Opção inválida. Tente novamente.")


def main():
    base_dir = Path(__file__).resolve().parent
    sql_path = base_dir / "scripts.sql"
    consultas = parse_sqls(sql_path)
    uf = escolher_uf()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = base_dir / f"saida_planilhas_{uf.lower()}_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    engine = carregar_engine()

    print(f"\nTotal de SQLs detectados: {len(consultas)}")
    print(f"Filtro de UF aplicado: {uf}")
    print(f"Pasta de saída: {output_dir}\n")

    for consulta in consultas:
        sql_exec, params = aplicar_filtro_uf(consulta["sql"], uf)
        try:
            df = pd.read_sql(text(sql_exec), engine, params=params)
            tabela = transformar_para_planilha(df)
        except Exception as exc:
            erro_path = output_dir / f"erro_sql_{consulta['id']:02d}.txt"
            erro_path.write_text(
                f"Título: {consulta['titulo']}\n\nErro: {exc}\n\nSQL:\n{sql_exec}\n",
                encoding="utf-8",
            )
            print(f"[ERRO] SQL {consulta['id']:02d} -> {erro_path.name}")
            continue

        tipos_agg = detectar_tipo_agregacao(consulta["sql"])
        colunas_grupo = [
            c for c in tabela.columns
            if c != "ano_censo" and not (isinstance(c, int) or str(c).isdigit())
        ]
        if colunas_grupo:
            nome_grupo = "_".join([limpar_nome(c, 20) for c in colunas_grupo[:3]])
        else:
            nome_grupo = "geral"

        nome_arquivo = (
            f"sql_{consulta['id']:02d}_{nome_grupo}_{tipos_agg}.xlsx"
        )
        xlsx_path = output_dir / limpar_nome(nome_arquivo, 120)
        if not str(xlsx_path).lower().endswith(".xlsx"):
            xlsx_path = xlsx_path.with_suffix(".xlsx")

        with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
            tabela.to_excel(writer, index=False, sheet_name="dados")

        print(f"[OK] SQL {consulta['id']:02d} -> {xlsx_path.name}")

    print("\nProcesso finalizado.")


if __name__ == "__main__":
    main()
