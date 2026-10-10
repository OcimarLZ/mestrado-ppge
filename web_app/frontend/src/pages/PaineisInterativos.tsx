import React from 'react';
import { LayoutDashboard, Construction } from 'lucide-react';

const PaineisInterativos: React.FC = () => {
  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1><LayoutDashboard size={28} style={{ marginRight: '0.5rem', verticalAlign: 'middle', color: 'var(--accent-primary)' }} />Painéis Interativos</h1>
      </div>

      <div className="glass-panel" style={{ padding: '1.5rem 2rem', marginBottom: '2rem' }}>
        <h3 style={{ marginBottom: '0.5rem' }}>Painel de cursos e discentes (2005–2024)</h3>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
          Painel interativo (Power BI) com os microdados do Censo da Educação Superior do
          INEP no grão curso × instituição × ano, de 2005 a 2024. Reúne indicadores de
          discentes — matrículas, ingressantes, vagas, concluintes, trancamentos e
          desvinculações — filtráveis por dimensão territorial completa (região, UF,
          mesorregião, microrregião, município), tipo de curso (classificação CINE), grau
          acadêmico, modalidade de ensino, categoria administrativa e rede (pública ou
          privada).
        </p>
        <div style={{ position: 'relative', width: '100%', aspectRatio: '600 / 373.5', borderRadius: '8px', overflow: 'hidden' }}>
          <iframe
            title="Painel de cursos e discentes"
            src="https://app.powerbi.com/view?r=eyJrIjoiNmRkYTc1YTctNzk3NC00MzEyLTkwYmMtZWU2YTMzYTE5ZjFjIiwidCI6ImU3MzFkM2I4LTVhMmEtNDMxYy04NTM1LWQ4N2U5ZGYzNDNkNCJ9"
            frameBorder={0}
            allowFullScreen
            style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', border: 'none' }}
          />
        </div>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.75rem' }}>
          Fonte: Elaborado pelo autor a partir dos microdados do Censo da Educação Superior
          (INEP).
        </p>
      </div>

      <div className="glass-panel" style={{ padding: '1.5rem 2rem', marginBottom: '2rem' }}>
        <h3 style={{ marginBottom: '0.5rem' }}>Painel de instituições e docentes (2004–2024)</h3>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
          Painel interativo (Power BI) com os microdados do Censo da Educação Superior do
          INEP no grão instituição (IES) × ano, de 2004 a 2024 (sem dados do Censo 2009).
          Reúne indicadores sobre o corpo docente — total de docentes, docentes em
          exercício por sexo, titulação (doutores, mestres, especialistas, graduados, sem
          graduação), regime de trabalho (integral, integral com dedicação exclusiva,
          parcial, horista), com deficiência e estrangeiros — filtráveis por dimensão
          territorial, mantenedora, organização acadêmica, categoria administrativa e rede
          (pública ou privada).
        </p>
        <div style={{ position: 'relative', width: '100%', aspectRatio: '600 / 373.5', borderRadius: '8px', overflow: 'hidden' }}>
          <iframe
            title="Painel de instituições e docentes"
            src="https://app.powerbi.com/view?r=eyJrIjoiODQ3N2I5YjAtYmIyZS00YzcwLWExMmQtMDVjY2Q3MTRhMTE4IiwidCI6ImU3MzFkM2I4LTVhMmEtNDMxYy04NTM1LWQ4N2U5ZGYzNDNkNCJ9"
            frameBorder={0}
            allowFullScreen
            style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', border: 'none' }}
          />
        </div>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.75rem' }}>
          Fonte: Elaborado pelo autor a partir dos microdados do Censo da Educação Superior
          (INEP).
        </p>
      </div>

      <div className="glass-panel" style={{ padding: '1.5rem 2rem', marginBottom: '2rem' }}>
        <h3 style={{ marginBottom: '0.5rem' }}>Painel de instituições e cursos (2005–2024)</h3>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
          Painel interativo (Power BI) com os microdados do Censo da Educação Superior do
          INEP no grão curso-oferta × instituição × ano, de 2005 a 2024, com os mesmos
          filtros territoriais, de tipo de curso (classificação CINE), grau acadêmico,
          modalidade de ensino, categoria administrativa e rede do painel de cursos e
          discentes acima. Exibe uma matriz instituição (IES) × curso, com drill-down por
          "+/-" para abrir os cursos de cada IES; os valores mostrados usam o último ano
          selecionado no filtro (sem seleção, o ano mais recente disponível).
        </p>
        <div style={{ position: 'relative', width: '100%', aspectRatio: '600 / 373.5', borderRadius: '8px', overflow: 'hidden' }}>
          <iframe
            title="Painel de instituições e cursos"
            src="https://app.powerbi.com/view?r=eyJrIjoiZWZiYzY4ODUtMzk1OC00OTUxLWEzYTItZmVjNDExMWYwZjQ0IiwidCI6ImU3MzFkM2I4LTVhMmEtNDMxYy04NTM1LWQ4N2U5ZGYzNDNkNCJ9"
            frameBorder={0}
            allowFullScreen
            style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', border: 'none' }}
          />
        </div>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.75rem' }}>
          Fonte: Elaborado pelo autor a partir dos microdados do Censo da Educação Superior
          (INEP).
        </p>
      </div>

      <div className="glass-panel" style={{ textAlign: 'center', padding: '2rem' }}>
        <Construction size={32} color="var(--accent-primary)" style={{ marginBottom: '0.75rem' }} />
        <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
          Mais painéis interativos serão adicionados aqui em breve.
        </p>
      </div>
    </div>
  );
};

export default PaineisInterativos;
