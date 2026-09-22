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
  totalPolosEadProprio: number;
  totalCampusPresencial: number;
  percLicUab: number;
  percLicEadProprio: number;
}

export function calcularIndicadores(registros: LicIesRegistro[]): IndicadoresAgregados {
  const totalMatriculasLic = soma(registros, 'total_matriculas_lic');
  const totalUab = soma(registros, 'mat_lic_uab');
  const totalEadProprio = soma(registros, 'mat_lic_ead_proprio');
  return {
    totalIes: registros.length,
    totalMatriculas: soma(registros, 'total_matriculas'),
    totalMatriculasLic,
    totalPolosUab: soma(registros, 'num_polos_uab'),
    totalPolosEadProprio: soma(registros, 'num_polos_ead_proprio'),
    totalCampusPresencial: soma(registros, 'num_campus_presencial'),
    percLicUab: totalMatriculasLic ? (totalUab / totalMatriculasLic) * 100 : 0,
    percLicEadProprio: totalMatriculasLic ? (totalEadProprio / totalMatriculasLic) * 100 : 0,
  };
}

export interface MatriculasPorIes {
  sigla: string;
  nome: string;
  matriculas: number;
}

// Top N IES por matriculas em licenciatura
export function topMatriculasLicenciatura(registros: LicIesRegistro[], n = 12): MatriculasPorIes[] {
  return [...registros]
    .sort((a, b) => b.total_matriculas_lic - a.total_matriculas_lic)
    .slice(0, n)
    .map((r) => ({ sigla: r.sigla, nome: r.ies_nome, matriculas: r.total_matriculas_lic }));
}

export interface PresencaEadPorIes {
  sigla: string;
  nome: string;
  polosUab: number;
  polosEadProprio: number;
}

// Top N IES por presenca territorial em EaD (polos UAB + polos EaD proprio)
export function topPresencaEad(registros: LicIesRegistro[], n = 12): PresencaEadPorIes[] {
  return [...registros]
    .map((r) => ({
      sigla: r.sigla,
      nome: r.ies_nome,
      polosUab: r.num_polos_uab,
      polosEadProprio: r.num_polos_ead_proprio,
    }))
    .sort((a, b) => (b.polosUab + b.polosEadProprio) - (a.polosUab + a.polosEadProprio))
    .slice(0, n);
}
