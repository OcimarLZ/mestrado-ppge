// Acesso ao panorama de IES federais x licenciatura (presenca por modalidade + matriculas
// 2024), gerado por web_app/content_export/export_lic_ies_geral.py a partir de
// sqls/cap5/lic_ies_geral.sql. Congelado em JSON pelo mesmo motivo do site-content.json:
// bdados/INEP.db (2,8 GB) nao existe no runner do GitHub Actions.
import raw from '../data/lic_ies_geral.json';

export interface LicIesRegistro {
  ies_nome: string;
  sigla: string;
  estado: string;
  a_ultimo_ano_presencial: number | null;
  b_qtd_mun_presencial: number;
  b_qtd_cursos_presencial: number;
  c_ultimo_ano_ead: number | null;
  d_qtd_mun_ead: number;
  d_qtd_cursos_ead: number;
  e_ultimo_ano_uab: number | null;
  f_qtd_polos_uab: number;
  f_qtd_cursos_uab: number;
  g_total_matriculas_2024: number;
  h_total_matriculas_lic_2024: number;
  i_mat_lic_ead_proprios: number;
  j_mat_lic_ead_uab: number;
  k_perc_licenciatura: number;
  l_perc_ead_proprios: number;
  m_perc_ead_uab: number;
}

interface LicIesPayload {
  gerado_em: string;
  fonte: string;
  colunas: Record<string, string>;
  registros: LicIesRegistro[];
}

const data = raw as LicIesPayload;

export function getLicIesRegistros(): LicIesRegistro[] {
  return data.registros;
}

export function getLicIesFonte(): string {
  return data.fonte;
}

export function getLicIesGeradoEm(): string {
  return data.gerado_em;
}
