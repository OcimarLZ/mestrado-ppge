// Agregacoes derivadas de LicIesRegistro[] para os indicadores e graficos da pagina
// Pesquisa > Explorar dados. Ficam num modulo a parte para nao acoplar a logica de
// agregacao aos componentes de apresentacao (indicadores, graficos, tabela).
import type { LicIesRegistro } from './licIesData';

const soma = (registros: LicIesRegistro[], campo: keyof LicIesRegistro) =>
  registros.reduce((acc, r) => acc + (Number(r[campo]) || 0), 0);

export interface IndicadoresAgregados {
  totalIes: number;
  totalMatriculas: number;
  totalMatriculasLic: number;
  totalPolosUab: number;
  totalMunPresencial: number;
  totalMunEad: number;
  percLicUab: number;
  percLicEadProprio: number;
}

export function calcularIndicadores(registros: LicIesRegistro[]): IndicadoresAgregados {
  const totalMatriculasLic = soma(registros, 'h_total_matriculas_lic_2024');
  const totalUab = soma(registros, 'j_mat_lic_ead_uab');
  const totalEadProprio = soma(registros, 'i_mat_lic_ead_proprios');
  return {
    totalIes: registros.length,
    totalMatriculas: soma(registros, 'g_total_matriculas_2024'),
    totalMatriculasLic,
    totalPolosUab: soma(registros, 'f_qtd_polos_uab'),
    totalMunPresencial: soma(registros, 'b_qtd_mun_presencial'),
    totalMunEad: soma(registros, 'd_qtd_mun_ead'),
    percLicUab: totalMatriculasLic ? (totalUab / totalMatriculasLic) * 100 : 0,
    percLicEadProprio: totalMatriculasLic ? (totalEadProprio / totalMatriculasLic) * 100 : 0,
  };
}

export interface MatriculasPorIes {
  sigla: string;
  nome: string;
  matriculas: number;
}

// Top N IES por matriculas em licenciatura (2024)
export function topMatriculasLicenciatura(registros: LicIesRegistro[], n = 12): MatriculasPorIes[] {
  return [...registros]
    .sort((a, b) => b.h_total_matriculas_lic_2024 - a.h_total_matriculas_lic_2024)
    .slice(0, n)
    .map((r) => ({ sigla: r.sigla, nome: r.ies_nome, matriculas: r.h_total_matriculas_lic_2024 }));
}

export interface PresencaEadPorIes {
  sigla: string;
  nome: string;
  polosUab: number;
  municipiosEadProprio: number;
}

// Top N IES por presenca territorial em EaD (polos UAB + municipios com EaD proprio)
export function topPresencaEad(registros: LicIesRegistro[], n = 12): PresencaEadPorIes[] {
  return [...registros]
    .map((r) => ({
      sigla: r.sigla,
      nome: r.ies_nome,
      polosUab: r.f_qtd_polos_uab,
      municipiosEadProprio: r.d_qtd_mun_ead,
    }))
    .sort((a, b) => (b.polosUab + b.municipiosEadProprio) - (a.polosUab + a.municipiosEadProprio))
    .slice(0, n);
}
