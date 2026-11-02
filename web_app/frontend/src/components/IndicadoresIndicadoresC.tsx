import React, { useMemo } from 'react';
import type { ApendiceCRegistro } from '../lib/apendiceCData';

const intFmt = (v: number) => Math.round(v).toLocaleString('pt-BR');
const pctFmt = (v: number) => `${(v * 100).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%`;

const IndicadoresIndicadoresC: React.FC<{ registros: ApendiceCRegistro[]; totalGeral: number }> = ({ registros, totalGeral }) => {
  const ind = useMemo(() => {
    const totalIes = registros.length;
    const comEadPropria = registros.filter((r) => r.ead_propria_oferece).length;
    const comUab = registros.filter((r) => r.uab_oferece).length;
    const totalMatriculasLic = registros.reduce((s, r) => s + (r.matriculas_licenciatura || 0), 0);
    const totalMatriculasUab = registros.reduce((s, r) => s + (r.matriculas_uab_lic || 0), 0);
    const totalPolosUab = registros.reduce((s, r) => s + (r.uab_num_polos || 0), 0);
    const totalPolosEadProprio = registros.reduce((s, r) => s + (r.ead_propria_num_polos || 0), 0);
    const percLicUab = totalMatriculasLic > 0 ? totalMatriculasUab / totalMatriculasLic : 0;
    return { totalIes, comEadPropria, comUab, totalMatriculasLic, percLicUab, totalPolosUab, totalPolosEadProprio };
  }, [registros]);

  const tiles = [
    { label: 'Instituições no filtro', value: `${ind.totalIes} de ${totalGeral}` },
    { label: 'Matrículas em licenciatura', value: intFmt(ind.totalMatriculasLic) },
    { label: '% licenciatura via UAB', value: pctFmt(ind.percLicUab) },
    { label: 'IES com EaD própria', value: intFmt(ind.comEadPropria) },
    { label: 'IES com UAB', value: intFmt(ind.comUab) },
    { label: 'Polos UAB', value: intFmt(ind.totalPolosUab) },
    { label: 'Polos EaD próprio', value: intFmt(ind.totalPolosEadProprio) },
  ];

  return (
    <div className="data-indicators-grid">
      {tiles.map((t) => (
        <div key={t.label} className="data-indicator-tile">
          <div className="data-indicator-value">{t.value}</div>
          <div className="data-indicator-label">{t.label}</div>
        </div>
      ))}
    </div>
  );
};

export default IndicadoresIndicadoresC;
