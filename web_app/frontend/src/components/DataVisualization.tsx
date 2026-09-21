import React from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

interface VisualizationProps {
  data?: Record<string, unknown>[] | null;
  contentType: string;
  chartType?: string | null;
  xAxis?: string | null;
  yAxis?: string | null;
  legendPosition?: string | null;
}

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6'];

const DataVisualization: React.FC<VisualizationProps> = ({ data, contentType, chartType, xAxis, yAxis, legendPosition }) => {
  if (!data || data.length === 0) return <div style={{ padding: '1rem' }}>Nenhum dado disponível para esta visualização.</div>;

  if (contentType === 'table') {
    const columns = Object.keys(data[0]);
    return (
      <div style={{ overflowX: 'auto', margin: '2rem 0' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ background: 'var(--bg-primary)', borderBottom: '2px solid var(--border-color)' }}>
              {columns.map(col => (
                <th key={col} style={{ padding: '0.75rem', color: 'var(--text-primary)' }}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => (
              <tr key={idx} style={{ borderBottom: '1px solid var(--border-color)' }}>
                {columns.map(col => (
                  <td key={col} style={{ padding: '0.75rem', color: 'var(--text-secondary)' }}>{String(row[col] ?? '')}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  if (contentType === 'chart') {
    const renderChart = () => {
      const margin = { top: 20, right: 30, left: 20, bottom: 5 };
      const legendAlign = legendPosition === 'top' || legendPosition === 'bottom' ? 'center' : (legendPosition === 'left' ? 'left' : 'right');
      const legendVerticalAlign = legendPosition === 'top' ? 'top' : (legendPosition === 'bottom' ? 'bottom' : 'middle');
      const layout = legendPosition === 'left' || legendPosition === 'right' ? 'vertical' : 'horizontal';

      if (chartType === 'line') {
        return (
          <LineChart data={data} margin={margin}>
            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
            <XAxis dataKey={xAxis || undefined} stroke="var(--text-secondary)" />
            <YAxis stroke="var(--text-secondary)" />
            <Tooltip contentStyle={{ backgroundColor: 'var(--bg-primary)', border: '1px solid var(--border-color)' }} />
            {legendPosition !== 'none' && <Legend verticalAlign={legendVerticalAlign as any} align={legendAlign as any} layout={layout} />}
            <Line type="monotone" dataKey={yAxis || ''} stroke={COLORS[0]} strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 8 }} />
          </LineChart>
        );
      }

      if (chartType === 'pie') {
        return (
          <PieChart margin={margin}>
            <Tooltip contentStyle={{ backgroundColor: 'var(--bg-primary)', border: '1px solid var(--border-color)' }} />
            {legendPosition !== 'none' && <Legend verticalAlign={legendVerticalAlign as any} align={legendAlign as any} layout={layout} />}
            <Pie data={data} dataKey={yAxis || ''} nameKey={xAxis || ''} cx="50%" cy="50%" outerRadius={120} fill="#8884d8" label>
              {data.map((_, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
          </PieChart>
        );
      }

      // Default is bar
      return (
        <BarChart data={data} margin={margin}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis dataKey={xAxis || undefined} stroke="var(--text-secondary)" />
          <YAxis stroke="var(--text-secondary)" />
          <Tooltip contentStyle={{ backgroundColor: 'var(--bg-primary)', border: '1px solid var(--border-color)' }} cursor={{ fill: 'rgba(255,255,255,0.05)' }} />
          {legendPosition !== 'none' && <Legend verticalAlign={legendVerticalAlign as any} align={legendAlign as any} layout={layout} />}
          <Bar dataKey={yAxis || ''} fill={COLORS[0]}>
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      );
    };

    return (
      <div style={{ width: '100%', height: 400, margin: '2rem 0', padding: '1rem', background: 'var(--bg-secondary)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
        <ResponsiveContainer width="100%" height="100%">
          {renderChart()}
        </ResponsiveContainer>
      </div>
    );
  }

  return null;
};

export default DataVisualization;
