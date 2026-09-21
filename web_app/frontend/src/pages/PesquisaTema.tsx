import React from 'react';
import { useParams, Link } from 'react-router-dom';
import * as LucideIcons from 'lucide-react';
import { ArrowRight } from 'lucide-react';
import temas from '../data/pesquisa';
import ZoomableImage from '../components/ZoomableImage';
import { assetUrl } from '../lib/content';

const PesquisaTema: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const tema = temas.find((t) => t.slug === slug);

  if (!tema) {
    return <div className="container" style={{ marginTop: '2rem' }}>Tema não encontrado.</div>;
  }

  // @ts-ignore
  const Icon = LucideIcons[tema.icon] || LucideIcons.BarChart3;

  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1><Icon size={28} style={{ marginRight: '0.5rem', verticalAlign: 'middle', color: 'var(--accent-primary)' }} />{tema.title}</h1>
      </div>

      <div className="text-content">
        {tema.intro.map((p, i) => <p key={i}>{p}</p>)}
      </div>

      <div className="grid-3">
        {tema.cards.map((card, i) => (
          <div key={i} className="glass-panel pesquisa-card">
            <div className="pesquisa-card-value">{card.value}</div>
            <p className="pesquisa-card-label">{card.label}</p>
          </div>
        ))}
      </div>

      {tema.images.length > 0 && (
        <div className="pesquisa-images">
          {tema.images.map((img, i) => (
            <figure key={i} className="glass-panel" style={{ padding: '1.5rem' }}>
              <ZoomableImage src={assetUrl(`assets/graficos_originais/${img.file}.png`)} alt={img.caption} style={{ maxWidth: '100%', height: 'auto', borderRadius: '8px' }} />
              <figcaption style={{ textAlign: 'center', marginTop: '0.75rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{img.caption}</figcaption>
            </figure>
          ))}
        </div>
      )}

      <div className="glass-panel" style={{ marginTop: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Leia a análise completa em:</span>
        <Link to={`/capitulo/${tema.chapterSlug}`} className="btn btn-primary">
          {tema.chapterLabel} <ArrowRight size={16} />
        </Link>
      </div>

      <div style={{ marginTop: '1.5rem' }}>
        <Link to="/pesquisa" style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>&larr; Voltar para Pesquisa</Link>
      </div>
    </div>
  );
};

export default PesquisaTema;
