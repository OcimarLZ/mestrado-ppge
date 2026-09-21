import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Lê uma pasta, lista arquivos .sql e permite escolher qual consulta executar "
            "na rotina de geração de planilha."
        )
    )
    parser.add_argument(
        "sql_folder",
        help="Pasta onde estão os arquivos .sql.",
    )
    parser.add_argument(
        "--recursivo",
        action="store_true",
        help="Se informado, busca .sql também em subpastas.",
    )
    return parser.parse_args()


def localizar_sqls(pasta: Path, recursivo: bool) -> list[Path]:
    if recursivo:
        arquivos = [p for p in pasta.rglob("*.sql") if p.is_file()]
    else:
        arquivos = [p for p in pasta.glob("*.sql") if p.is_file()]
    return sorted(arquivos, key=lambda x: str(x).lower())


def escolher_arquivo_sql(arquivos: list[Path], pasta_base: Path) -> Path | None:
    if not arquivos:
        return None

    print("\nArquivos SQL encontrados:")
    for i, arquivo in enumerate(arquivos, start=1):
        try:
            exibicao = arquivo.relative_to(pasta_base)
        except ValueError:
            exibicao = arquivo
        print(f"{i:02d} - {exibicao}")

    print("00 - Cancelar")

    while True:
        entrada = input("\nEscolha o número do SQL que deseja executar: ").strip()
        if not entrada:
            print("Entrada vazia. Informe um número.")
            continue

        if entrada == "00" or entrada == "0":
            return None

        if entrada.isdigit():
            idx = int(entrada)
            if 1 <= idx <= len(arquivos):
                return arquivos[idx - 1]

        print("Opção inválida. Tente novamente.")


def executar_rotina_sql_unico(arquivo_sql: Path) -> int:
    script_base = Path(__file__).resolve().parent / "gerar_planilha_sql_unico.py"
    if not script_base.exists():
        print(f"[ERRO] Rotina base não encontrada: {script_base}")
        return 1

    cmd = [sys.executable, str(script_base), str(arquivo_sql)]
    print("\nExecutando rotina de planilha para:")
    print(f"{arquivo_sql}\n")

    proc = subprocess.run(cmd)
    return proc.returncode


def main():
    args = parse_args()
    pasta_sql = Path(args.sql_folder).resolve()

    if not pasta_sql.exists() or not pasta_sql.is_dir():
        raise FileNotFoundError(f"Pasta inválida: {pasta_sql}")

    arquivos = localizar_sqls(pasta_sql, recursivo=args.recursivo)
    if not arquivos:
        print("Nenhum arquivo .sql encontrado na pasta informada.")
        return

    escolhido = escolher_arquivo_sql(arquivos, pasta_sql)
    if escolhido is None:
        print("Operação cancelada.")
        return

    codigo = executar_rotina_sql_unico(escolhido)
    if codigo == 0:
        print("\nFinalizado com sucesso.")
    else:
        print(f"\nFinalizado com erro. Código de saída: {codigo}")


if __name__ == "__main__":
    main()
