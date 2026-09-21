import React from 'react';
import { FileText, GraduationCap, Building2, BookOpen, Users, Award, Languages, Tags } from 'lucide-react';

import * as LucideIcons from 'lucide-react';
import { getSiteSettings, getHomeCards, assetUrl } from '../lib/content';

interface SiteSettings {
  hero_title: string;
  hero_subtitle: string;
  home_body_title: string;
  home_body_text: string;
  work_type?: string;
  work_program?: string;
  work_organization?: string;
  work_description?: string;
  work_authors?: string;
  work_research_group?: string;
  work_advisor?: string;
  work_committee?: string;
  work_abstract?: string;
  work_abstract_en?: string;
  work_keywords?: string;
}

interface HomeCard {
  id: number;
  icon: string;
  value: string;
  title: string;
  description: string;
  order: number;
}

const Home: React.FC = () => {
  const settings = getSiteSettings() as unknown as SiteSettings;
  const cards = getHomeCards() as unknown as HomeCard[];

  return (
    <>
      <section className="section-block" style={{ paddingTop: '2rem', paddingBottom: 0 }}>
        <div className="glass-panel" style={{ display: 'flex', flexWrap: 'wrap', gap: '1.5rem 2.5rem', justifyContent: 'center', padding: '1.5rem 2rem' }}>
          {settings?.work_type && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <GraduationCap size={20} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} />
              <span style={{ fontSize: '0.9rem' }}>{settings.work_type}</span>
            </div>
          )}
          {settings?.work_program && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <BookOpen size={20} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} />
              <span style={{ fontSize: '0.9rem' }}>{settings.work_program}</span>
            </div>
          )}
          {settings?.work_organization && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Building2 size={20} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} />
              <span style={{ fontSize: '0.9rem' }}>{settings.work_organization}</span>
            </div>
          )}
          {settings?.work_description && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <FileText size={20} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} />
              <span style={{ fontSize: '0.9rem' }}>{settings.work_description}</span>
            </div>
          )}
        </div>
      </section>

      <section className="hero">
        <div className="container">
          <h1>{settings?.hero_title || "A Educação a Distância no Brasil (2014-2024)"}</h1>
          <p className="subtitle">
            {settings?.hero_subtitle || "O Público e o Privado na Formação de Professores..."}
          </p>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
            <a href={assetUrl('assets/dissertacao.pdf')} target="_blank" rel="noreferrer" className="btn btn-primary">
              <FileText size={20} />
              Baixar Dissertação
            </a>
          </div>
        </div>
      </section>

      <section className="section-block" style={{ paddingTop: '1.5rem', paddingBottom: 0 }}>
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', padding: '1.5rem 2rem' }}>
          {settings?.work_authors && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <Users size={18} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} />
              <span style={{ fontSize: '0.95rem' }}><strong>Autor(es):</strong> {settings.work_authors}</span>
            </div>
          )}
          {settings?.work_advisor && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <Award size={18} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} />
              <span style={{ fontSize: '0.95rem' }}><strong>Orientador(a):</strong> {settings.work_advisor}</span>
            </div>
          )}
          {settings?.work_research_group && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <BookOpen size={18} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} />
              <span style={{ fontSize: '0.95rem' }}><strong>Grupo de Pesquisa:</strong> {settings.work_research_group}</span>
            </div>
          )}
        </div>
      </section>

      {settings?.work_committee && (
        <section className="section-block" style={{ paddingBottom: 0 }}>
          <h2 style={{ fontSize: '1.3rem' }}>Banca Examinadora</h2>
          <div className="glass-panel" style={{ padding: '1.5rem 2rem' }}>
            {settings.work_committee.split('\n').filter(l => l.trim()).map((line, idx) => (
              <p key={idx} style={{ margin: '0 0 0.25rem 0' }}>{line.trim()}</p>
            ))}
          </div>
        </section>
      )}

      <section className="section-block">
        <h2>{settings?.home_body_title || "O Paradoxo da Formação Docente"}</h2>
        <div className="text-content">
          {settings?.home_body_text ? (
            settings.home_body_text.split('\n').map((paragraph, idx) => (
              paragraph.trim() && <p key={idx}>{paragraph}</p>
            ))
          ) : (
            <p>Carregando texto...</p>
          )}
        </div>
      </section>

      {settings?.work_abstract && (
        <section className="section-block" style={{ paddingBottom: 0 }}>
          <h2 style={{ fontSize: '1.3rem' }}>Resumo</h2>
          <div className="text-content">
            {settings.work_abstract.split('\n').filter(l => l.trim()).map((paragraph, idx) => (
              <p key={idx}>{paragraph}</p>
            ))}
          </div>
        </section>
      )}

      {settings?.work_abstract_en && (
        <section className="section-block" style={{ paddingBottom: 0 }}>
          <h2 style={{ fontSize: '1.3rem' }}><Languages size={22} style={{ marginRight: '0.5rem' }} />Abstract</h2>
          <div className="text-content">
            {settings.work_abstract_en.split('\n').filter(l => l.trim()).map((paragraph, idx) => (
              <p key={idx}>{paragraph}</p>
            ))}
          </div>
        </section>
      )}

      {settings?.work_keywords && (
        <section className="section-block" style={{ paddingBottom: 0 }}>
          <h2 style={{ fontSize: '1.3rem' }}><Tags size={22} style={{ marginRight: '0.5rem' }} />Palavras-chave</h2>
          <div className="glass-panel" style={{ padding: '1.25rem 2rem' }}>
            <p style={{ margin: 0, fontSize: '1.05rem' }}>{settings.work_keywords}</p>
          </div>
        </section>
      )}

      <section className="section-block">
        <h2 className="text-center mb-4" style={{ justifyContent: 'center' }}>Números que Impressionam</h2>
        <div className="grid-3" style={{ gridTemplateColumns: `repeat(auto-fit, minmax(250px, 1fr))` }}>
          {cards.map(card => {
            // @ts-ignore
            let IconComp = LucideIcons[card.icon] || FileText;
            return (
              <div key={card.id} className="glass-panel text-center">
                <IconComp color="var(--accent-primary)" size={40} style={{ margin: '0 auto' }} />
                <div className="stat-value">{card.value}</div>
                <div className="stat-label">{card.title}</div>
                <p style={{ fontSize: '0.875rem' }}>{card.description}</p>
              </div>
            );
          })}
        </div>
      </section>
    </>
  );
};

export default Home;
