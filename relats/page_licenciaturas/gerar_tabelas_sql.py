import argparse
import configparser
from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

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


def ler_sql(caminho_sql: Path) -> str:
    conteudo = caminho_sql.read_text(encoding="utf-8").strip()
    if not conteudo:
        raise ValueError("Arquivo SQL está vazio.")
    return conteudo


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa um arquivo .sql e exporta o resultado para Excel e HTML."
    )
    parser.add_argument(
        "sql_file",
        help="Caminho para o arquivo .sql a ser executado.",
    )
    return parser.parse_args()


def salvar_excel_com_fallback(saida: Path, tabela: pd.DataFrame) -> Path:
    try:
        with pd.ExcelWriter(saida, engine="openpyxl") as writer:
            tabela.to_excel(writer, sheet_name="dados", index=False)
        return saida
    except PermissionError:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saida_alt = saida.with_name(f"{saida.stem}_{timestamp}{saida.suffix}")
        print(f"[AVISO] O arquivo {saida.name} estava em uso. Salvando como: {saida_alt.name}")
        with pd.ExcelWriter(saida_alt, engine="openpyxl") as writer:
            tabela.to_excel(writer, sheet_name="dados", index=False)
        return saida_alt


def salvar_html_com_fallback(saida: Path, tabela: pd.DataFrame) -> Path:
    html_content = tabela.to_html(index=False, classes='tabela-dados')
    html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <title>Exportação de Dados - {saida.stem}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            color: #333;
        }}
        h2 {{
            color: #444;
        }}
        .tabela-dados {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }}
        .tabela-dados th, .tabela-dados td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        .tabela-dados th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        .tabela-dados tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .tabela-dados tr:hover {{
            background-color: #f1f1f1;
        }}
    </style>
</head>
<body>
    <h2>Resultados do Arquivo: {saida.stem}.sql</h2>
    {html_content}
</body>
</html>"""
    
    try:
        saida.write_text(html_template, encoding="utf-8")
        return saida
    except PermissionError:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saida_alt = saida.with_name(f"{saida.stem}_{timestamp}{saida.suffix}")
        saida_alt.write_text(html_template, encoding="utf-8")
        return saida_alt


def main():
    args = parse_args()
    caminho_sql = Path(args.sql_file).resolve()

    if not caminho_sql.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_sql}")
    if caminho_sql.suffix.lower() != ".sql":
        raise ValueError("O parâmetro deve apontar para um arquivo com extensão .sql")

    sql = ler_sql(caminho_sql)
    engine = carregar_engine()

    print(f"Executando a consulta: {caminho_sql.name}...")
    df = pd.read_sql(text(sql), engine)
    
    if df.empty:
        print("A consulta não retornou dados. Nenhum arquivo foi gerado.")
        return

    saida_excel = caminho_sql.with_suffix(".xlsx")
    saida_html = caminho_sql.with_suffix(".html")

    saida_excel_real = salvar_excel_com_fallback(saida_excel, df)
    saida_html_real = salvar_html_com_fallback(saida_html, df)

    print("\nArquivos gerados com sucesso:")
    print(f"Excel : {saida_excel_real}")
    print(f"HTML  : {saida_html_real}")


if __name__ == "__main__":
    main()
