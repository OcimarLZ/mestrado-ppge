// Acesso aos indicadores por IES em 2024 (Apêndice C da dissertação), gerado por
// web_app/content_export/export_apendices_c_d_e.py a partir de
// planilhas/Apêndice C - Indicadores dos cursos licenciaturas_federais em 2024.xlsx.
// Congelado em JSON pelo mesmo motivo do site-content.json: a planilha não roda em CI.
import raw from '../data/apendice_c_indicadores_2024.json';

export interface ApendiceCRegistro {
  sigla: string;
  estado: string;
  oferece_licenciatura: boolean;
  num_campus_presencial_licenciatura: number;
  num_polos_licenciatura: number;
  ead_propria_oferece: boolean;
  ead_propria_num_polos: number;
  ead_propria_num_cursos: number;
  uab_oferece: boolean;
  uab_num_polos: number;
  uab_num_cursos: number;
  matriculas_total_ies: number;
  matriculas_licenciatura: number;
  perc_licenciatura_no_total: number;
  matriculas_ead_propria_lic: number;
  matriculas_uab_lic: number;
  perc_ead_propria_na_lic: number;
  perc_uab_na_lic: number;
  perc_ead_total_na_lic: number;
  indice_dependencia_uab: number | null;
  perc_presencial_na_lic: number;
}

interface ApendiceCPayload {
  gerado_em: string;
  fonte: string;
  ano: number;
  registros: ApendiceCRegistro[];
}

const data = raw as ApendiceCPayload;

export function getApendiceCRegistros(): ApendiceCRegistro[] {
  return data.registros;
}

export function getApendiceCFonte(): string {
  return data.fonte;
}

export function getApendiceCGeradoEm(): string {
  return data.gerado_em;
}

export function getApendiceCAno(): number {
  return data.ano;
}
