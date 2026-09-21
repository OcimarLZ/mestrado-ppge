
import argparse
import configparser
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

def carregar_engine() -> object:
    # Assumindo que o script esteja em d:\ProjetosPY\inep\sqls\cap5\
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


def main():
    parser = argparse.ArgumentParser(description="Gera uma planilha Excel a partir de um arquivo SQL.")
    parser.add_argument("sql_file", help="Caminho para o arquivo SQL")
    parser.add_argument("-o", "--output", help="Caminho para o arquivo Excel de saída (opcional)")
    args = parser.parse_args()

    sql_path = Path(args.sql_file)
    
    if not sql_path.exists():
        print(f"Arquivo SQL não encontrado: {sql_path}")
        return

    with open(sql_path, "r", encoding="utf-8") as f:
        sql = f.read()

    engine = carregar_engine()
    print(f"Executando consulta de {sql_path} no banco {engine.url}...")
    
    df = pd.read_sql(text(sql), engine)
    
    if df.empty:
        print("Nenhum dado encontrado.")
        return

    print(f"Processados {len(df)} linhas.")
    
    if args.output:
        arquivo_saida = Path(args.output)
    else:
        arquivo_saida = sql_path.parent / f"{sql_path.stem}.xlsx"
        
    # Gerar o Excel
    with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados')
        worksheet = writer.sheets['Dados']
        for col in worksheet.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 100)
            worksheet.column_dimensions[column].width = adjusted_width

    print(f"Planilha gerada com sucesso: {arquivo_saida}")


if __name__ == "__main__":
    main()

