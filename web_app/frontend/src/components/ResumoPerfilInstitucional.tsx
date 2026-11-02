import React from 'react';
import type { ApendicePerfilRegistro } from '../lib/apendicePerfilData';

const intFmt = (v?: number) => (v === undefined || v === null ? '—' : v.toLocaleString('pt-BR'));

const KPI_DEFS: { key: keyof ApendicePerfilRegistro['resumo']['2014']; label: string }[] = [
  { key: 'matriculas_total', label: 'Matrículas totais da IES' },
  { key: 'matriculas_licenciatura', label: 'Matrículas em licenciatura' },
  { key: 'num_cursos_licenciatura', label: 'Cursos de licenciatura' },
  { key: 'num_campus', label: 'Campus (municípios)' },
  { key: 'num_polos_ead', label: 'Polos EaD (total)' },
  { key: 'num_polos_proprios', label: 'Polos EaD próprios' },
  { key: 'num_polos_uab', label: 'Polos UAB' },
];

const ResumoPerfilInstitucional: React.FC<{ registro: ApendicePerfilRegistro }> = ({ registro }) => {
  const r2014 = registro.resumo['2014'];
  const r2024 = registro.resumo['2024'];

  return (
    <div className="data-table-wrapper glass-panel perfil-resumo-wrapper">
      <table className="data-table perfil-resumo-table">
        <thead>
          <tr>
            <th>Indicador</th>
            <th className="is-numeric">2014</th>
            <th className="is-numeric">2024</th>
            <th className="is-numeric">Variação</th>
          </tr>
        </thead>
        <tbody>
          {KPI_DEFS.map((kpi) => {
            const v14 = r2014[kpi.key];
            const v24 = r2024[kpi.key];
            const temAmbos = typeof v14 === 'number' && typeof v24 === 'number';
            const delta = temAmbos ? (v24 as number) - (v14 as number) : null;
            return (
              <tr key={kpi.key}>
                <td>{kpi.label}</td>
                <td className="is-numeric">{intFmt(v14)}</td>
                <td className="is-numeric">{intFmt(v24)}</td>
                <td className={`is-numeric ${delta === null ? '' : delta > 0 ? 'dado-positivo' : delta < 0 ? 'dado-negativo' : ''}`}>
                  {delta === null ? '—' : `${delta > 0 ? '+' : ''}${delta.toLocaleString('pt-BR')}`}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default ResumoPerfilInstitucional;
