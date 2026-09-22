// Agregacoes derivadas de LicPoloRegistro[] para os indicadores e graficos da pagina
// Pesquisa > Detalhamento por campus e polo.
import type { LicPoloRegistro, TipoPolo } from './licPolosData';

export interface IndicadoresPolos {
  totalPolos: number;
  totalMunicipios: number;
  totalIes: number;
  totalMatriculas: number;
  mediaMatriculasPorPolo: number;
  percUab: number;
}

export function calcularIndicadoresPolos(registros: LicPoloRegistro[]): IndicadoresPolos {
  const totalMatriculas = registros.reduce((acc, r) => acc + r.matriculas, 0);
  const municipios = new Set(registros.map((r) => `${r.municipio}/${r.municipio_uf}`));
  const ies = new Set(registros.map((r) => r.sigla));
  const totalUab = registros.filter((r) => r.tipo_polo === 'UAB').length;
  return {
    totalPolos: registros.length,
    totalMunicipios: municipios.size,
    totalIes: ies.size,
    totalMatriculas,
    mediaMatriculasPorPolo: registros.length ? totalMatriculas / registros.length : 0,
    percUab: registros.length ? (totalUab / registros.length) * 100 : 0,
  };
}

export interface RankingPolo {
  label: string;
  matriculas: number;
  tipo: TipoPolo;
}

// Top N polos (municipio x IES) por matricula
export function topPolosPorMatricula(registros: LicPoloRegistro[], n = 15): RankingPolo[] {
  return [...registros]
    .sort((a, b) => b.matriculas - a.matriculas)
    .slice(0, n)
    .map((r) => ({ label: `${r.municipio}/${r.municipio_uf} (${r.sigla})`, matriculas: r.matriculas, tipo: r.tipo_polo }));
}

export interface ComposicaoTipo {
  tipo: TipoPolo;
  matriculas: number;
  polos: number;
}

// Matriculas e numero de polos, agrupados por tipo (Presencial / EaD proprio / UAB)
export function composicaoPorTipo(registros: LicPoloRegistro[]): ComposicaoTipo[] {
  const ordem: TipoPolo[] = ['Presencial', 'EaD próprio', 'UAB'];
  return ordem.map((tipo) => {
    const doTipo = registros.filter((r) => r.tipo_polo === tipo);
    return {
      tipo,
      matriculas: doTipo.reduce((acc, r) => acc + r.matriculas, 0),
      polos: doTipo.length,
    };
  });
}
