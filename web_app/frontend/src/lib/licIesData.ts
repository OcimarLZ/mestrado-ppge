// Acesso ao panorama de IES federais x licenciatura (matriculas, cursos, campus e polos
// EaD/UAB, 2014 x 2024), gerado por web_app/content_export/export_lic_ies_geral.py a partir
// de sqls/cap5/lic_ies_geral.sql. Congelado em JSON pelo mesmo motivo do site-content.json:
// bdados/INEP.db (2,8 GB) nao existe no runner do GitHub Actions.
import raw from '../data/lic_ies_geral.json';

export type AnoCenso = 2014 | 2024;

export interface LicIesRegistro {
  ies_nome: string;
  sigla: string;
  estado: string;
  ano_censo: AnoCenso;
  total_matriculas: number;
  total_matriculas_lic: number;
  num_cursos_lic: number;
  num_campus_presencial: number;
  num_polos_ead_proprio: number;
  num_polos_uab: number;
  mat_lic_presencial: number;
  mat_lic_ead_proprio: number;
  mat_lic_uab: number;
  perc_licenciatura: number;
  perc_lic_uab: number;
  perc_lic_ead_proprio: number;
}

interface LicIesPayload {
  gerado_em: string;
  fonte: string;
  anos: AnoCenso[];
  colunas: Record<string, string>;
  registros: LicIesRegistro[];
}

const data = raw as LicIesPayload;

export function getLicIesRegistros(): LicIesRegistro[] {
  return data.registros;
}

export function getLicIesAnos(): AnoCenso[] {
  return data.anos;
}

export function getLicIesFonte(): string {
  return data.fonte;
}

export function getLicIesGeradoEm(): string {
  return data.gerado_em;
}
