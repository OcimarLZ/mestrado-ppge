import React, { useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import type { LicPoloRegistro, TipoPolo } from '../lib/licPolosData';
import { topPolosPorMatricula, composicaoPorTipo } from '../lib/licPolosAgregados';

// Mesmo par validado (CVD-safe) das outras paginas de dados, com uma terceira cor
// (aqua) para o terceiro tipo de polo -- as tres primeiras cores da paleta do skill
// dataviz validam separacao par-a-par completa em claro e escuro.
const COR_POR_TIPO: Record<TipoPolo, string> = {
  Presencial: '#2a78d6',
  'EaD próprio': '#eb6834',
  UAB: '#1baf7a',
};

const tooltipStyle = {
  background: 'var(--bg-card)',
  border: '1px solid var(--glass-border)',
  borderRadius: 8,
  fontSize: '0.8rem',
  color: 'var(--text-primary)',
};

const GraficosPolos: React.FC<{ registros: LicPoloRegistro[] }> = ({ registros }) => {
  const dadosRanking = useMemo(() => topPolosPorMatricula(registros, 15), [registros]);
  const dadosComposicao = useMemo(() => composicaoPorTipo(registros), [registros]);

  return (
    <div className="data-charts-grid">
      <div className="data-chart-card">
        <h3 className="data-chart-title">Top 15 polos/campus por matrículas</h3>
        <ResponsiveContainer width="100%" height={360}>
          <BarChart data={dadosRanking} layout="vertical" margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--glass-border)" horizontal={false} />
            <XAxis type="number" stroke="var(--text-secondary)" fontSize={11} tickLine={false} />
            <YAxis type="category" dataKey="label" stroke="var(--text-secondary)" fontSize={10} tickLine={false} width={150} />
            <Tooltip
              contentStyle={tooltipStyle}
              formatter={(value, _name, item) => [Number(value ?? 0).toLocaleString('pt-BR'), item?.payload?.tipo ?? 'Matrículas']}
              cursor={{ fill: 'color-mix(in srgb, var(--text-secondary) 10%, transparent)' }}
            />
            <Bar dataKey="matriculas" radius={[0, 4, 4, 0]} maxBarSize={14}>
              {dadosRanking.map((d, i) => (
                <Cell key={i} fill={COR_POR_TIPO[d.tipo]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="data-chart-card">
        <h3 className="data-chart-title">Matrículas por tipo de polo</h3>
        <ResponsiveContainer width="100%" height={360}>
          <BarChart data={dadosComposicao} margin={{ top: 8, right: 12, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--glass-border)" vertical={false} />
            <XAxis dataKey="tipo" stroke="var(--text-secondary)" fontSize={11} tickLine={false} />
            <YAxis stroke="var(--text-secondary)" fontSize={11} tickLine={false} width={44} />
            <Tooltip
              contentStyle={tooltipStyle}
              formatter={(value) => [Number(value ?? 0).toLocaleString('pt-BR'), 'Matrículas']}
              cursor={{ fill: 'color-mix(in srgb, var(--text-secondary) 10%, transparent)' }}
            />
            <Bar dataKey="matriculas" name="matriculas" radius={[4, 4, 0, 0]} maxBarSize={64}>
              {dadosComposicao.map((d, i) => (
                <Cell key={i} fill={COR_POR_TIPO[d.tipo]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default GraficosPolos;
