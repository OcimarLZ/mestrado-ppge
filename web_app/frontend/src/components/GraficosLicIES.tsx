import React, { useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import type { LicIesRegistro } from '../lib/licIesData';
import { topMatriculasLicenciatura, topPresencaEad } from '../lib/licIesAgregados';

// Par categorico validado (CVD-safe, ambos os modos claro/escuro) pelo validador do skill
// dataviz -- nao usa a cor de destaque dinamica do tema do site (a paleta do usuario tem
// mais de um tema com acento em laranja/ambar, o que colidiria com a segunda serie).
const COR_SERIE_1 = '#2a78d6'; // matriculas / polos UAB
const COR_SERIE_2 = '#eb6834'; // municipios com EaD proprio

const tooltipStyle = {
  background: 'var(--bg-card)',
  border: '1px solid var(--glass-border)',
  borderRadius: 8,
  fontSize: '0.8rem',
  color: 'var(--text-primary)',
};

const GraficosLicIES: React.FC<{ registros: LicIesRegistro[] }> = ({ registros }) => {
  const dadosMatriculas = useMemo(() => topMatriculasLicenciatura(registros, 12), [registros]);
  const dadosPresenca = useMemo(() => topPresencaEad(registros, 12), [registros]);

  return (
    <div className="data-charts-grid">
      <div className="data-chart-card">
        <h3 className="data-chart-title">Top 12 IES por matrículas em licenciatura (2024)</h3>
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={dadosMatriculas} margin={{ top: 8, right: 12, left: 0, bottom: 8 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--glass-border)" vertical={false} />
            <XAxis dataKey="sigla" stroke="var(--text-secondary)" fontSize={11} tickLine={false} interval={0} angle={-90} textAnchor="end" height={70} />
            <YAxis stroke="var(--text-secondary)" fontSize={11} tickLine={false} width={44} />
            <Tooltip
              contentStyle={tooltipStyle}
              formatter={(value) => [Number(value ?? 0).toLocaleString('pt-BR'), 'Matrículas']}
              labelFormatter={(_, payload) => payload?.[0]?.payload?.nome ?? ''}
              cursor={{ fill: 'color-mix(in srgb, var(--text-secondary) 10%, transparent)' }}
            />
            <Bar dataKey="matriculas" fill={COR_SERIE_1} radius={[4, 4, 0, 0]} maxBarSize={28} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="data-chart-card">
        <h3 className="data-chart-title">Top 12 IES por presença territorial em EaD</h3>
        <ResponsiveContainer width="100%" height={340}>
          <BarChart data={dadosPresenca} margin={{ top: 8, right: 12, left: 0, bottom: 8 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--glass-border)" vertical={false} />
            <XAxis dataKey="sigla" stroke="var(--text-secondary)" fontSize={11} tickLine={false} interval={0} angle={-90} textAnchor="end" height={70} />
            <YAxis stroke="var(--text-secondary)" fontSize={11} tickLine={false} width={36} allowDecimals={false} />
            <Tooltip
              contentStyle={tooltipStyle}
              labelFormatter={(_, payload) => payload?.[0]?.payload?.nome ?? ''}
              cursor={{ fill: 'color-mix(in srgb, var(--text-secondary) 10%, transparent)' }}
            />
            <Legend wrapperStyle={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }} />
            <Bar dataKey="polosUab" name="Polos UAB" fill={COR_SERIE_1} radius={[4, 4, 0, 0]} maxBarSize={16} />
            <Bar dataKey="polosEadProprio" name="Polos EaD próprio" fill={COR_SERIE_2} radius={[4, 4, 0, 0]} maxBarSize={16} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default GraficosLicIES;
