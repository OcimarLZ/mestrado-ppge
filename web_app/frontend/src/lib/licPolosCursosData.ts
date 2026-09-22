// Acesso ao detalhamento por curso dentro de cada polo/campus (2014 x 2024), gerado por
// web_app/content_export/export_lic_polos_cursos.py a partir de sqls/cap5/lic_polos_cursos.sql.
// Usado para expandir uma linha de DataTablePolos e mostrar os cursos ofertados naquele
// polo, cada um com sua própria matrícula.
//
// Este JSON tem ~2 MB (6.7 mil linhas) -- import() dinamico em vez de import estatico, para
// nao inflar o bundle inicial de TODAS as paginas do site so por causa desta unica tela de
// detalhamento (o restante do app nao usa code-splitting por rota).
import type { AnoCenso } from './licIesData';
import type { TipoPolo } from './licPolosData';

export interface LicPoloCursoRegistro {
  ies_nome: string;
  sigla: string;
  ies_uf: string;
  ano_censo: AnoCenso;
  municipio: string;
  municipio_uf: string;
  tipo_polo: TipoPolo;
  curso: string;
  matriculas: number;
}

interface LicPolosCursosPayload {
  gerado_em: string;
  fonte: string;
  anos: AnoCenso[];
  registros: LicPoloCursoRegistro[];
}

const chave = (sigla: string, ano: AnoCenso, municipio: string, tipo: TipoPolo) => `${sigla}|${ano}|${municipio}|${tipo}`;

let indicePromise: Promise<Map<string, LicPoloCursoRegistro[]>> | null = null;

function carregarIndice(): Promise<Map<string, LicPoloCursoRegistro[]>> {
  if (!indicePromise) {
    indicePromise = import('../data/lic_polos_cursos.json').then((mod) => {
      const data = mod.default as LicPolosCursosPayload;
      const indice = new Map<string, LicPoloCursoRegistro[]>();
      for (const r of data.registros) {
        const k = chave(r.sigla, r.ano_censo, r.municipio, r.tipo_polo);
        const lista = indice.get(k) ?? [];
        lista.push(r);
        indice.set(k, lista);
      }
      for (const lista of indice.values()) {
        lista.sort((a, b) => b.matriculas - a.matriculas);
      }
      return indice;
    });
  }
  return indicePromise;
}

export async function getCursosDoPolo(sigla: string, ano: AnoCenso, municipio: string, tipo: TipoPolo): Promise<LicPoloCursoRegistro[]> {
  const indice = await carregarIndice();
  return indice.get(chave(sigla, ano, municipio, tipo)) ?? [];
}
