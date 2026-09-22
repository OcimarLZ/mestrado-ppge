// Acesso ao detalhamento por campus/polo das licenciaturas das IES federais (2014 x 2024),
// gerado por web_app/content_export/export_lic_polos_detalhe.py a partir de
// sqls/cap5/lic_polos_detalhe.sql. Mesmo motivo de licIesData.ts para congelar em JSON
// (bdados/INEP.db nao existe no runner do GitHub Actions).
import raw from '../data/lic_polos_detalhe.json';
import type { AnoCenso } from './licIesData';

export type TipoPolo = 'Presencial' | 'EaD próprio' | 'UAB';

export interface LicPoloRegistro {
  ies_nome: string;
  sigla: string;
  ies_uf: string;
  ano_censo: AnoCenso;
  municipio: string;
  municipio_uf: string;
  tipo_polo: TipoPolo;
  num_cursos: number;
  matriculas: number;
}

interface LicPolosPayload {
  gerado_em: string;
  fonte: string;
  nota_metodologica: string;
  anos: AnoCenso[];
  registros: LicPoloRegistro[];
}

const data = raw as LicPolosPayload;

export function getLicPolosRegistros(): LicPoloRegistro[] {
  return data.registros;
}

export function getLicPolosAnos(): AnoCenso[] {
  return data.anos;
}

export function getLicPolosFonte(): string {
  return data.fonte;
}

export function getLicPolosNotaMetodologica(): string {
  return data.nota_metodologica;
}

export function getLicPolosGeradoEm(): string {
  return data.gerado_em;
}
