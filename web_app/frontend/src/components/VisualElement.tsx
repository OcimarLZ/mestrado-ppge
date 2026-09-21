import React from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { assetUrl } from '../lib/content';
import ZoomableImage from './ZoomableImage';

interface VisualData {
  id: number;
  page_content_id: number;
  type: string;
  title: string;
  source: string;
  order: number;
  image_url: string | null;
  sql_query: string | null;
  chart_type: string | null;
  x_axis: string | null;
  y_axis: string | null;
  show_labels: number;
  legend_position: string | null;
  table_html: string | null;
  pdf_page: number | null;
  data?: Record<string, unknown>[] | null;
}

const COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'];

// Prints de tela de codigo/IDE/terminal recebem uma moldura no estilo de editor de
// codigo (barra de titulo com "semaforo", fonte monoespacada) em vez do cartao padrao.
const CODE_SCREENSHOT_RE = /c[oó]digo|script|\bIDE\b|ambiente de desenvolvimento|\bpython\b|terminal/i;

const VisualElement: React.FC<{ visual: VisualData }> = ({ visual }) => {
  const chartData = visual.data ?? null;

  const renderVisual = () => {
    if (visual.type === 'image' && visual.image_url) {
      return (
        <ZoomableImage
          src={visual.image_url}
          alt={visual.title}
          style={{ maxWidth: '100%', height: 'auto', borderRadius: '8px' }}
        />
      );
    }

    if (visual.type === 'table') {
      if (visual.table_html) {
        return <div dangerouslySetInnerHTML={{ __html: visual.table_html }} />;
      }
      if (chartData) {
        return renderDataTable();
      }
    }

    if (visual.type === 'chart' && chartData) {
      return renderChart();
    }

    return null;
  };

  const renderDataTable = () => {
    if (!chartData || chartData.length === 0) return <p style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>Sem dados</p>;
    const cols = Object.keys(chartData[0]);
    return (
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
          <thead>
            <tr>
              {cols.map(col => <th key={col} style={{ border: '1px solid var(--border-color)', padding: '0.5rem', background: 'var(--bg-secondary)', textAlign: 'left' }}>{col}</th>)}
            </tr>
          </thead>
          <tbody>
            {chartData.map((row, i) => (
              <tr key={i}>
                {cols.map(col => <td key={col} style={{ border: '1px solid var(--border-color)', padding: '0.5rem' }}>{String(row[col] ?? '')}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  const renderChart = () => {
    if (!chartData || chartData.length === 0) return null;
    const xKey = visual.x_axis || Object.keys(chartData[0])[0];
    const yKey = visual.y_axis || Object.keys(chartData[0]).find(k => k !== xKey) || Object.keys(chartData[0])[1];
    const showLabels = visual.show_labels === 1;
    const legendPos = visual.legend_position || 'bottom';

    const chartProps = {
      width: 800,
      height: 400,
      data: chartData,
      margin: { top: 20, right: 30, left: 20, bottom: 10 },
    };

    switch (visual.chart_type) {
      case 'line':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData} margin={chartProps.margin}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis dataKey={xKey} tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
              <YAxis tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
              <Tooltip contentStyle={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '8px' }} />
              <Legend verticalAlign={legendPos as any} />
              <Line type="monotone" dataKey={yKey} stroke={COLORS[0]} strokeWidth={2} dot={{ fill: COLORS[0] }} />
            </LineChart>
          </ResponsiveContainer>
        );
      case 'pie':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie data={chartData} dataKey={yKey} nameKey={xKey} cx="50%" cy="50%" outerRadius={140} label={showLabels}>
                {chartData.map((_, idx) => <Cell key={idx} fill={COLORS[idx % COLORS.length]} />)}
              </Pie>
              <Tooltip contentStyle={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '8px' }} />
              <Legend verticalAlign={legendPos as any} />
            </PieChart>
          </ResponsiveContainer>
        );
      default:
        return (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={chartData} margin={chartProps.margin}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis dataKey={xKey} tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
              <YAxis tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
              <Tooltip contentStyle={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '8px' }} />
              <Legend verticalAlign={legendPos as any} />
              <Bar dataKey={yKey} fill={COLORS[0]} radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        );
    }
  };

  const isCodeScreenshot = CODE_SCREENSHOT_RE.test(visual.title || '');

  return (
    <div className={isCodeScreenshot ? 'code-panel' : 'glass-panel'} style={{ padding: isCodeScreenshot ? 0 : '1.5rem', margin: '1.5rem 0', overflow: 'hidden' }}>
      {isCodeScreenshot && (
        <div className="code-panel-titlebar">
          <span className="code-panel-dot" style={{ background: '#ff5f56' }} />
          <span className="code-panel-dot" style={{ background: '#ffbd2e' }} />
          <span className="code-panel-dot" style={{ background: '#27c93f' }} />
        </div>
      )}
      <div style={{ padding: isCodeScreenshot ? '1.25rem' : 0 }}>
        {renderVisual()}
      </div>
      {visual.title && (
        <p style={{
          textAlign: 'center',
          margin: isCodeScreenshot ? '0 0 1rem 0' : '0.75rem 0 0 0',
          padding: isCodeScreenshot ? '0 1.25rem' : 0,
          fontSize: '0.9rem',
          fontWeight: 600,
          fontFamily: isCodeScreenshot ? "'Fira Code', 'Consolas', monospace" : undefined,
        }}>
          {visual.title}
        </p>
      )}
      {visual.source && (
        <p style={{ textAlign: 'center', margin: '0.25rem 0 0 0', padding: isCodeScreenshot ? '0 1.25rem' : 0, fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
          Fonte: {visual.source}
        </p>
      )}
      {visual.pdf_page && (
        <p style={{ textAlign: 'center', margin: isCodeScreenshot ? '0.25rem 0 1.25rem 0' : '0.25rem 0 0 0', padding: isCodeScreenshot ? '0 1.25rem' : 0, fontSize: '0.8rem' }}>
          <a
            href={`${assetUrl('assets/dissertacao.pdf')}#page=${visual.pdf_page}`}
            target="_blank"
            rel="noreferrer"
            style={{ color: 'var(--accent-primary)' }}
          >
            Ver original na dissertação (p. {visual.pdf_page})
          </a>
        </p>
      )}
    </div>
  );
};

export default VisualElement;
