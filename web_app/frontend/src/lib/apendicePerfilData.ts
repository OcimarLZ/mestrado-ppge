// Acesso ao perfil institucional 2014 x 2024 (fusão dos Apêndices IV e III da dissertação:
// resumo de KPIs + lista de cursos e locais de oferta), gerado por
// web_app/content_export/export_apendices_c_d_e.py a partir de
// planilhas/Apêndice D - Resumo cursos licenciaturas_federais.xlsx e
// planilhas/Apêndice E - Cursos licenciaturas_federais.xlsx.
import raw from '../data/apendice_perfil_institucional.json';

export type AnoPerfil = '2014' | '2024';

export interface ApendicePerfilKPIs {
  matriculas_total?: number;
  matriculas_licenciatura?: number;
  num_cursos_licenciatura?: number;
  num_campus?: number;
  num_polos_ead?: number;
  num_polos_proprios?: number;
  num_polos_uab?: number;
}

export interface ApendiceCursoLocal {
  curso: string;
  local: string | null;
}

export interface ApendicePerfilRegistro {
  nome_ies: string;
  sigla: string | null;
  estado: string | null;
  resumo: Record<AnoPerfil, ApendicePerfilKPIs>;
  cursos: Record<AnoPerfil, ApendiceCursoLocal[]>;
}

interface ApendicePerfilPayload {
  gerado_em: string;
  fonte: string;
  anos: number[];
  registros: ApendicePerfilRegistro[];
}

const data = raw as ApendicePerfilPayload;

export function getPerfisInstitucionais(): ApendicePerfilRegistro[] {
  return data.registros;
}

export function getPerfilFonte(): string {
  return data.fonte;
}

export function getPerfilGeradoEm(): string {
  return data.gerado_em;
}

export function getPerfilAnos(): number[] {
  return data.anos;
}
