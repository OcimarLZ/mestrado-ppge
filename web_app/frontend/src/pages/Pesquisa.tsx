import React from 'react';
import { Link } from 'react-router-dom';
import * as LucideIcons from 'lucide-react';
import { ArrowRight, Database } from 'lucide-react';
import temas from '../data/pesquisa';

const Pesquisa: React.FC = () => {
  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1>Pesquisa</h1>
        <p className="lead" style={{ color: 'var(--text-secondary)' }}>
          Os principais achados e indicadores da pesquisa, organizados por tema — um resumo
          navegável dos capítulos 3 a 6 e das Considerações Finais da dissertação.
        </p>
      </div>

      <div className="grid-3">
        <Link to="/pesquisa/dados-ies" className="glass-panel pesquisa-index-card pesquisa-index-card-data">
          <Database color="var(--accent-primary)" size={32} />
          <h3 style={{ margin: '1rem 0 0.5rem 0' }}>Explorar dados: IES x licenciatura</h3>
          <p style={{ fontSize: '0.9rem', flex: 1 }}>
            Tabela interativa com as 69 universidades federais que ofertam licenciatura: presença
            por modalidade e matrículas do Censo 2024, IES a IES.
          </p>
          <span className="pesquisa-index-card-link">
            Abrir tabela <ArrowRight size={16} />
          </span>
        </Link>
        {temas.map((tema) => {
          // @ts-ignore
          const Icon = LucideIcons[tema.icon] || LucideIcons.BarChart3;
          return (
            <Link key={tema.slug} to={`/pesquisa/${tema.slug}`} className="glass-panel pesquisa-index-card">
              <Icon color="var(--accent-primary)" size={32} />
              <h3 style={{ margin: '1rem 0 0.5rem 0' }}>{tema.title}</h3>
              <p style={{ fontSize: '0.9rem', flex: 1 }}>{tema.summary}</p>
              <span className="pesquisa-index-card-link">
                Ver achados <ArrowRight size={16} />
              </span>
            </Link>
          );
        })}
      </div>
    </div>
  );
};

export default Pesquisa;
