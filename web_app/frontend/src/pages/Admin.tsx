import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Save, Plus, Trash2, Edit, Check, BookText } from 'lucide-react';
import * as LucideIcons from 'lucide-react';
import themes from '../themes';
import IconPicker from '../components/IconPicker';
import VisualManager from '../components/VisualManager';

interface SiteSettings {
  sidebar_title: string;
  sidebar_icon: string;
  topbar_title: string;
  footer_text_1: string;
  footer_text_2: string;
  hero_title: string;
  hero_subtitle: string;
  home_body_title: string;
  home_body_text: string;
  theme_bg_color?: string;
  theme_text_color?: string;
  theme_primary_color?: string;
  theme_card_bg_color?: string;
  theme_font_family?: string;
  theme_sidebar_bg?: string;
  theme_hero_glow_color?: string;
  theme_name?: string;
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

interface PageContent {
  id: number;
  parent_id: number | null;
  slug: string;
  title: string;
  content: string;
  order: number;
  icon_name: string | null;
  content_type?: string;
  image_url?: string | null;
  sql_query?: string | null;
  chart_type?: string | null;
  x_axis?: string | null;
  y_axis?: string | null;
  legend_position?: string | null;
  analysis_text?: string | null;
}

const Admin: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'settings' | 'cards' | 'pages'>('settings');
  
  const [settings, setSettings] = useState<SiteSettings | null>(null);
  const [cards, setCards] = useState<HomeCard[]>([]);
  const [pages, setPages] = useState<PageContent[]>([]);
  
  const [editingCard, setEditingCard] = useState<HomeCard | null>(null);
  const [cardForm, setCardForm] = useState<Partial<HomeCard>>({});

  const [editingPage, setEditingPage] = useState<PageContent | null>(null);
  const [pageForm, setPageForm] = useState<Partial<PageContent>>({});

  useEffect(() => {
    fetchSettings();
    fetchCards();
    fetchPages();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/site-settings');
      setSettings(response.data);
    } catch (error) {
      console.error("Error fetching settings:", error);
    }
  };

  const fetchCards = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/home-cards');
      setCards(response.data);
    } catch (error) {
      console.error("Error fetching cards:", error);
    }
  };

  const fetchPages = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/pages');
      setPages(response.data);
    } catch (error) {
      console.error("Error fetching pages:", error);
    }
  };

  const handleSettingsChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    if (settings) {
      setSettings({ ...settings, [e.target.name]: e.target.value });
    }
  };

  const selectTheme = (themeName: string) => {
    const theme = themes.find(t => t.name === themeName);
    if (!theme || !settings) return;
    setSettings({
      ...settings,
      theme_name: theme.name,
      theme_bg_color: theme.colors.bg,
      theme_text_color: theme.colors.text,
      theme_primary_color: theme.colors.accent,
      theme_card_bg_color: theme.colors.card,
      theme_font_family: theme.colors.font,
      theme_sidebar_bg: theme.colors.sidebar,
      theme_hero_glow_color: theme.colors.hero_glow,
    });
  };

  const saveSettings = async () => {
    if (!settings) return;
    try {
      await axios.put('http://127.0.0.1:8000/api/site-settings', settings);
      alert('Configurações atualizadas com sucesso!');
    } catch (error) {
      console.error("Error updating settings:", error);
      alert('Erro ao atualizar configurações.');
    }
  };

  const handleCardFormChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setCardForm({ ...cardForm, [e.target.name]: e.target.value });
  };

  const saveCard = async () => {
    try {
      if (editingCard) {
        await axios.put(`http://127.0.0.1:8000/api/home-cards/${editingCard.id}`, cardForm);
        alert('Card atualizado com sucesso!');
      } else {
        await axios.post('http://127.0.0.1:8000/api/home-cards', cardForm);
        alert('Card criado com sucesso!');
      }
      setEditingCard(null);
      setCardForm({});
      fetchCards();
    } catch (error) {
      console.error("Error saving card:", error);
      alert('Erro ao salvar card.');
    }
  };

  const deleteCard = async (id: number) => {
    if (window.confirm("Tem certeza que deseja excluir este card?")) {
      try {
        await axios.delete(`http://127.0.0.1:8000/api/home-cards/${id}`);
        fetchCards();
      } catch (error) {
        console.error("Error deleting card:", error);
        alert('Erro ao excluir card.');
      }
    }
  };

  const handlePageFormChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setPageForm({ ...pageForm, [e.target.name]: e.target.value });
  };

  const savePageContent = async () => {
    try {
      if (editingPage) {
        await axios.put(`http://127.0.0.1:8000/api/pages/${editingPage.id}`, pageForm);
        alert('Conteúdo atualizado com sucesso!');
      } else {
        await axios.post('http://127.0.0.1:8000/api/pages', pageForm);
        alert('Conteúdo criado com sucesso!');
      }
      setEditingPage(null);
      setPageForm({});
      fetchPages();
    } catch (error) {
      console.error("Error saving page content:", error);
      alert('Erro ao salvar conteúdo.');
    }
  };

  const deletePageContent = async (id: number) => {
    if (window.confirm("Tem certeza que deseja excluir esta seção?")) {
      try {
        await axios.delete(`http://127.0.0.1:8000/api/pages/${id}`);
        fetchPages();
      } catch (error) {
        console.error("Error deleting page content:", error);
        alert('Erro ao excluir conteúdo.');
      }
    }
  };

  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1>Painel de Administração</h1>
        <p className="lead">Gerencie o conteúdo dinâmico do site</p>
      </div>

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '1rem' }}>
        <button 
          className={`btn ${activeTab === 'settings' ? 'btn-primary' : ''}`}
          onClick={() => setActiveTab('settings')}
          style={{ background: activeTab !== 'settings' ? 'transparent' : '', color: activeTab !== 'settings' ? 'var(--text-primary)' : '' }}
        >
          Configurações Gerais
        </button>
        <button 
          className={`btn ${activeTab === 'cards' ? 'btn-primary' : ''}`}
          onClick={() => setActiveTab('cards')}
          style={{ background: activeTab !== 'cards' ? 'transparent' : '', color: activeTab !== 'cards' ? 'var(--text-primary)' : '' }}
        >
          Cards (Números)
        </button>
        <button 
          className={`btn ${activeTab === 'pages' ? 'btn-primary' : ''}`}
          onClick={() => setActiveTab('pages')}
          style={{ background: activeTab !== 'pages' ? 'transparent' : '', color: activeTab !== 'pages' ? 'var(--text-primary)' : '' }}
        >
          Conteúdo das Páginas
        </button>
      </div>

      {activeTab === 'settings' && settings && (
        <section className="section-block">
          <h2>Editar Configurações Gerais</h2>
          <div className="glass-panel" style={{ padding: '2rem' }}>
            <h3 style={{ marginTop: 0 }}>Textos da Barra Superior e Lateral</h3>
            <div className="grid-2">
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Título da Barra Lateral</label>
                <input type="text" name="sidebar_title" value={settings.sidebar_title} onChange={handleSettingsChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Título da Barra Superior</label>
                <input type="text" name="topbar_title" value={settings.topbar_title} onChange={handleSettingsChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
              </div>
            </div>
            
            <h3 style={{ marginTop: '2rem' }}>Textos da Página Inicial (Hero)</h3>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Título Principal (Hero)</label>
              <input type="text" name="hero_title" value={settings.hero_title} onChange={handleSettingsChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Subtítulo (Hero)</label>
              <textarea name="hero_subtitle" value={settings.hero_subtitle} onChange={handleSettingsChange} rows={3} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', resize: 'vertical' }} />
            </div>

            <h3 style={{ marginTop: '2rem' }}>Textos da Página Inicial (Corpo)</h3>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Título do Corpo</label>
              <input type="text" name="home_body_title" value={settings.home_body_title} onChange={handleSettingsChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Parágrafos do Corpo (Quebre linhas para parágrafos)</label>
              <textarea name="home_body_text" value={settings.home_body_text} onChange={handleSettingsChange} rows={6} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', resize: 'vertical' }} />
            </div>

            <h3 style={{ marginTop: '2rem' }}>Rodapé</h3>
            <div className="grid-2">
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Texto Rodapé 1</label>
                <input type="text" name="footer_text_1" value={settings.footer_text_1} onChange={handleSettingsChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Texto Rodapé 2</label>
                <input type="text" name="footer_text_2" value={settings.footer_text_2} onChange={handleSettingsChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
              </div>
            </div>

            <h3 style={{ marginTop: '2rem' }}>Identificação do Trabalho</h3>
            <div className="grid-2">
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Tipo de Trabalho</label>
                <select name="work_type" value={settings.work_type || ''} onChange={handleSettingsChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }}>
                  <option value="TCC">TCC (Trabalho de Conclusão de Curso)</option>
                  <option value="Monografia">Monografia</option>
                  <option value="Dissertação de Mestrado">Dissertação de Mestrado</option>
                  <option value="Tese de Doutorado">Tese de Doutorado</option>
                  <option value="Artigo Científico">Artigo Científico</option>
                  <option value="Resumo Expandido">Resumo Expandido</option>
                  <option value="Relatório Técnico">Relatório Técnico</option>
                  <option value="Outro">Outro</option>
                </select>
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Autores</label>
                <input type="text" name="work_authors" value={settings.work_authors || ''} onChange={handleSettingsChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} placeholder="Ex: Ocimar Luis Zolin" />
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Orientador</label>
                <input type="text" name="work_advisor" value={settings.work_advisor || ''} onChange={handleSettingsChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} placeholder="Ex: Prof. Dr. Nome do Orientador" />
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Grupo de Pesquisa</label>
                <input type="text" name="work_research_group" value={settings.work_research_group || ''} onChange={handleSettingsChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} placeholder="Ex: Grupo de Estudos e Pesquisas em Educação" />
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Programa/Curso</label>
                <input type="text" name="work_program" value={settings.work_program || ''} onChange={handleSettingsChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} placeholder="Ex: Programa de Pós-Graduação em Educação" />
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Instituição/Organização</label>
                <input type="text" name="work_organization" value={settings.work_organization || ''} onChange={handleSettingsChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} placeholder="Ex: Universidade Federal da Fronteira Sul" />
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Evento/Periódico (se aplicável)</label>
                <input type="text" name="work_description" value={settings.work_description || ''} onChange={handleSettingsChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} placeholder="Ex: Revista Brasileira de Educação" />
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Palavras-chave</label>
                <input type="text" name="work_keywords" value={settings.work_keywords || ''} onChange={handleSettingsChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} placeholder="Ex: Educação a Distância; Formação de Professores; Mercantilização" />
              </div>
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Membros da Banca Examinadora</label>
              <textarea name="work_committee" value={settings.work_committee || ''} onChange={handleSettingsChange} rows={3} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', resize: 'vertical' }} placeholder="Um por linha:&#10;Prof. Dr. Nome 1 – Instituição&#10;Profa. Dra. Nome 2 – Instituição" />
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Resumo (Português)</label>
              <textarea name="work_abstract" value={settings.work_abstract || ''} onChange={handleSettingsChange} rows={6} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', resize: 'vertical' }} />
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Abstract (English)</label>
              <textarea name="work_abstract_en" value={settings.work_abstract_en || ''} onChange={handleSettingsChange} rows={6} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', resize: 'vertical' }} />
            </div>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.5rem', marginBottom: '1.5rem' }}>
              Estas informações aparecerão na seção superior da página inicial.
            </p>

            <h3 style={{ marginTop: '2rem' }}>Tema Visual</h3>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
              Escolha um tema pré-definido para o site. As cores são aplicadas automaticamente.
            </p>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
              {themes.map(theme => {
                const isActive = (settings?.theme_name || 'dark-slate') === theme.name;
                return (
                  <button
                    key={theme.name}
                    onClick={() => selectTheme(theme.name)}
                    style={{
                      cursor: 'pointer',
                      background: theme.colors.bg,
                      border: isActive ? `3px solid ${theme.colors.accent}` : '2px solid transparent',
                      borderRadius: '12px',
                      padding: '1rem',
                      textAlign: 'center',
                      transition: 'all 0.2s ease',
                      position: 'relative',
                      minHeight: '120px',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '0.5rem',
                      opacity: isActive ? 1 : 0.7,
                    }}
                    onMouseOver={e => { e.currentTarget.style.opacity = '1'; e.currentTarget.style.transform = 'translateY(-4px)'; }}
                    onMouseOut={e => { e.currentTarget.style.opacity = isActive ? '1' : '0.7'; e.currentTarget.style.transform = 'none'; }}
                  >
                    {isActive && (
                      <span style={{ position: 'absolute', top: '6px', right: '6px', background: theme.colors.accent, borderRadius: '50%', width: '22px', height: '22px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <Check size={14} color="#fff" />
                      </span>
                    )}
                    <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap', justifyContent: 'center' }}>
                      <span style={{ width: '24px', height: '24px', borderRadius: '50%', background: theme.colors.accent, display: 'inline-block' }} />
                      <span style={{ width: '24px', height: '24px', borderRadius: '50%', background: theme.colors.text, display: 'inline-block' }} />
                      <span style={{ width: '24px', height: '24px', borderRadius: '50%', background: theme.colors.card, display: 'inline-block', border: '1px solid rgba(255,255,255,0.2)' }} />
                    </div>
                    <strong style={{ color: theme.colors.text, fontSize: '0.85rem' }}>{theme.label}</strong>
                    <span style={{ color: theme.colors.text, opacity: 0.7, fontSize: '0.75rem' }}>{theme.description}</span>
                  </button>
                );
              })}
            </div>
            <details style={{ marginBottom: '1rem' }}>
              <summary style={{ cursor: 'pointer', color: 'var(--accent-primary)', fontWeight: 600, fontSize: '0.9rem' }}>
                Personalização Avançada (cores individuais)
              </summary>
              <div className="grid-2" style={{ marginTop: '1rem' }}>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold', fontSize: '0.85rem' }}>Cor de Fundo (bg)</label>
                  <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                    <input type="color" name="theme_bg_color" value={settings.theme_bg_color || '#0f172a'} onChange={handleSettingsChange} style={{ width: '40px', height: '36px', padding: '1px', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'transparent', cursor: 'pointer' }} />
                    <input type="text" name="theme_bg_color" value={settings.theme_bg_color || ''} onChange={handleSettingsChange} style={{ flex: 1, padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontFamily: 'monospace', fontSize: '0.85rem' }} />
                  </div>
                </div>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold', fontSize: '0.85rem' }}>Cor do Texto</label>
                  <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                    <input type="color" name="theme_text_color" value={settings.theme_text_color || '#f8fafc'} onChange={handleSettingsChange} style={{ width: '40px', height: '36px', padding: '1px', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'transparent', cursor: 'pointer' }} />
                    <input type="text" name="theme_text_color" value={settings.theme_text_color || ''} onChange={handleSettingsChange} style={{ flex: 1, padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontFamily: 'monospace', fontSize: '0.85rem' }} />
                  </div>
                </div>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold', fontSize: '0.85rem' }}>Cor Primária (Acento)</label>
                  <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                    <input type="color" name="theme_primary_color" value={settings.theme_primary_color || '#10b981'} onChange={handleSettingsChange} style={{ width: '40px', height: '36px', padding: '1px', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'transparent', cursor: 'pointer' }} />
                    <input type="text" name="theme_primary_color" value={settings.theme_primary_color || ''} onChange={handleSettingsChange} style={{ flex: 1, padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontFamily: 'monospace', fontSize: '0.85rem' }} />
                  </div>
                </div>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold', fontSize: '0.85rem' }}>Cor dos Cards (bg)</label>
                  <input type="text" name="theme_card_bg_color" value={settings.theme_card_bg_color || ''} onChange={handleSettingsChange} style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontFamily: 'monospace', fontSize: '0.85rem' }} placeholder="rgba(30, 41, 59, 0.7)" />
                </div>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold', fontSize: '0.85rem' }}>Cor do Menu (bg)</label>
                  <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                    <input type="color" name="theme_sidebar_bg" value={settings.theme_sidebar_bg || settings.theme_bg_color || '#0f172a'} onChange={handleSettingsChange} style={{ width: '40px', height: '36px', padding: '1px', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'transparent', cursor: 'pointer' }} />
                    <input type="text" name="theme_sidebar_bg" value={settings.theme_sidebar_bg || ''} onChange={handleSettingsChange} style={{ flex: 1, padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontFamily: 'monospace', fontSize: '0.85rem' }} />
                  </div>
                </div>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold', fontSize: '0.85rem' }}>Glow Hero</label>
                  <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                    <input type="color" name="theme_hero_glow_color" value={settings.theme_hero_glow_color || '#10b981'} onChange={handleSettingsChange} style={{ width: '40px', height: '36px', padding: '1px', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'transparent', cursor: 'pointer' }} />
                    <input type="text" name="theme_hero_glow_color" value={settings.theme_hero_glow_color || ''} onChange={handleSettingsChange} style={{ flex: 1, padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontFamily: 'monospace', fontSize: '0.85rem' }} />
                  </div>
                </div>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold', fontSize: '0.85rem' }}>Fonte</label>
                  <input type="text" name="theme_font_family" value={settings.theme_font_family || ''} onChange={handleSettingsChange} style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontSize: '0.85rem' }} placeholder="'Inter', system-ui, -apple-system, sans-serif" />
                </div>
              </div>
            </details>

            <button className="btn btn-primary" onClick={saveSettings} style={{ marginTop: '1rem' }}>
              <Save size={20} /> Salvar Configurações
            </button>
          </div>
        </section>
      )}

      {activeTab === 'cards' && (
        <section className="section-block">
          {(editingCard || Object.keys(cardForm).length > 0) ? (
            <div className="glass-panel" style={{ padding: '2rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <h3>{editingCard ? 'Editar Card' : 'Criar Novo Card'}</h3>
                <button className="btn" style={{ background: 'transparent', color: 'var(--text-primary)' }} onClick={() => { setEditingCard(null); setCardForm({}); }}>
                  Voltar para Lista
                </button>
              </div>

              <div className="grid-2">
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem' }}>Título do Card</label>
                  <input type="text" name="title" value={cardForm.title || ''} onChange={handleCardFormChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
                </div>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem' }}>Valor (ex: 69,9%, 5.1M)</label>
                  <input type="text" name="value" value={cardForm.value || ''} onChange={handleCardFormChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
                </div>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem' }}>Ícone</label>
                  <IconPicker value={cardForm.icon || ''} onChange={(name) => setCardForm({ ...cardForm, icon: name })} />
                </div>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem' }}>Ordem</label>
                  <input type="number" name="order" value={cardForm.order || 0} onChange={handleCardFormChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
                </div>
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Descrição</label>
                <textarea name="description" value={cardForm.description || ''} onChange={handleCardFormChange} rows={3} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', resize: 'vertical' }} />
              </div>

              <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                <button className="btn btn-primary" onClick={saveCard} style={{ padding: '0.75rem 2rem' }}>
                  <Save size={20} /> Salvar Card
                </button>
              </div>
            </div>
          ) : (
            <>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h2>Gerenciar Cards (Home)</h2>
                <button className="btn" style={{ background: 'var(--accent-secondary)' }} onClick={() => { setEditingCard(null); setCardForm({ order: cards.length + 1 }); }}>
                  <Plus size={20} /> Novo Card
                </button>
              </div>
              
              <div className="grid-3" style={{ gridTemplateColumns: `repeat(auto-fit, minmax(250px, 1fr))` }}>
                {cards.map(card => (
                  <div key={card.id} className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                    <div>
                      <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem' }}>{card.title}</h3>
                      <div className="stat-value" style={{ fontSize: '1.5rem' }}>{card.value}</div>
                      <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Ícone: {card.icon}</p>
                      <p style={{ fontSize: '0.85rem' }}>{card.description}</p>
                    </div>
                    
                    <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end', marginTop: '1rem' }}>
                      <button className="btn" style={{ padding: '0.5rem', fontSize: '0.85rem', background: '#3b82f6', color: '#ffffff' }} onClick={() => { setEditingCard(card); setCardForm(card); }}>
                        <Edit size={16} /> Editar
                      </button>
                      <button className="btn" style={{ padding: '0.5rem', fontSize: '0.85rem', background: '#ef4444', color: '#ffffff' }} onClick={() => deleteCard(card.id)}>
                        <Trash2 size={16} /> Excluir
                      </button>
                    </div>
                  </div>
                ))}
                {cards.length === 0 && <p>Nenhum card encontrado.</p>}
              </div>
            </>
          )}
        </section>
      )}

      {activeTab === 'pages' && (
        <section className="section-block">
          
          {(editingPage || Object.keys(pageForm).length > 0) ? (
            <div className="glass-panel" style={{ padding: '2rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <h3>{editingPage ? 'Editar Seção' : 'Criar Nova Seção'}</h3>
                <button className="btn" style={{ background: 'transparent', color: 'var(--text-primary)' }} onClick={() => { setEditingPage(null); setPageForm({}); }}>
                  Voltar para Lista
                </button>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Pertence ao Capítulo/Seção (Deixe em branco para criar um Capítulo Raiz)</label>
                <select name="parent_id" value={pageForm.parent_id || ''} onChange={(e) => setPageForm({ ...pageForm, parent_id: e.target.value ? parseInt(e.target.value) : null })} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }}>
                  <option value="">-- É um Capítulo Raiz --</option>
                  {pages.map(p => (
                    <option key={p.id} value={p.id}>{p.title} (ID: {p.id})</option>
                  ))}
                </select>
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Slug (ex: introducao, sub-secao-1)</label>
                <input type="text" name="slug" value={pageForm.slug || ''} onChange={handlePageFormChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Título de Exibição</label>
                <input type="text" name="title" value={pageForm.title || ''} onChange={handlePageFormChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
              </div>
              <div className="grid-2" style={{ gap: '1rem' }}>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem' }}>Ordem de Exibição</label>
                  <input type="number" name="order" value={pageForm.order || 0} onChange={handlePageFormChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
                </div>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem' }}>Ícone</label>
                  <IconPicker value={pageForm.icon_name || ''} onChange={(name) => setPageForm({ ...pageForm, icon_name: name })} />
                </div>
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Tipo de Conteúdo</label>
                <select name="content_type" value={pageForm.content_type || 'text'} onChange={(e) => setPageForm({ ...pageForm, content_type: e.target.value })} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }}>
                  <option value="text">Apenas Texto</option>
                  <option value="chart">Gráfico</option>
                  <option value="table">Tabela</option>
                  <option value="image">Imagem Estática</option>
                  <option value="html">HTML Externo</option>
                </select>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem' }}>
                  {pageForm.content_type === 'text' || pageForm.content_type === 'html' ? 'Conteúdo (Texto / HTML)' : 'Texto Introdutório (Acima)'}
                </label>
                <textarea name="content" value={pageForm.content || ''} onChange={handlePageFormChange} style={{ width: '100%', minHeight: pageForm.content_type === 'text' || pageForm.content_type === 'html' ? '500px' : '200px', padding: '1rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', resize: 'vertical', fontSize: '1.05rem', lineHeight: '1.6', fontFamily: pageForm.content_type === 'html' ? 'monospace' : 'inherit' }} />
              </div>

              {pageForm.content_type === 'image' && (
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem' }}>URL da Imagem</label>
                  <input type="text" name="image_url" value={pageForm.image_url || ''} onChange={handlePageFormChange} placeholder="Ex: https://..." style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
                </div>
              )}

              {(pageForm.content_type === 'chart' || pageForm.content_type === 'table') && (
                <div style={{ padding: '1rem', border: '1px dashed var(--accent-primary)', borderRadius: '4px', marginBottom: '1rem' }}>
                  <h4 style={{ marginTop: 0, color: 'var(--accent-primary)' }}>Configurações de Visualização</h4>
                  
                  <div style={{ marginBottom: '1rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem' }}>Consulta SQL</label>
                    <textarea name="sql_query" value={pageForm.sql_query || ''} onChange={handlePageFormChange} placeholder="SELECT * FROM table" style={{ width: '100%', minHeight: '150px', padding: '1rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: '#1e1e1e', color: '#d4d4d4', fontFamily: 'monospace', resize: 'vertical' }} />
                  </div>
                  
                  {pageForm.content_type === 'chart' && (
                    <div className="grid-2" style={{ gap: '1rem', marginBottom: '1rem' }}>
                      <div>
                        <label style={{ display: 'block', marginBottom: '0.5rem' }}>Tipo de Gráfico</label>
                        <select name="chart_type" value={pageForm.chart_type || 'bar'} onChange={(e) => setPageForm({ ...pageForm, chart_type: e.target.value })} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }}>
                          <option value="bar">Barras</option>
                          <option value="line">Linhas</option>
                          <option value="pie">Pizza</option>
                        </select>
                      </div>
                      <div>
                        <label style={{ display: 'block', marginBottom: '0.5rem' }}>Coluna Eixo X</label>
                        <input type="text" name="x_axis" value={pageForm.x_axis || ''} onChange={handlePageFormChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
                      </div>
                      <div>
                        <label style={{ display: 'block', marginBottom: '0.5rem' }}>Coluna Eixo Y</label>
                        <input type="text" name="y_axis" value={pageForm.y_axis || ''} onChange={handlePageFormChange} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
                      </div>
                      <div>
                        <label style={{ display: 'block', marginBottom: '0.5rem' }}>Posição da Legenda</label>
                        <select name="legend_position" value={pageForm.legend_position || 'bottom'} onChange={(e) => setPageForm({ ...pageForm, legend_position: e.target.value })} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }}>
                          <option value="top">Topo</option>
                          <option value="bottom">Rodapé</option>
                          <option value="left">Esquerda</option>
                          <option value="right">Direita</option>
                          <option value="none">Ocultar</option>
                        </select>
                      </div>
                    </div>
                  )}

                  <div style={{ marginBottom: '1rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem' }}>Texto de Análise (Abaixo)</label>
                    <textarea name="analysis_text" value={pageForm.analysis_text || ''} onChange={handlePageFormChange} style={{ width: '100%', minHeight: '200px', padding: '1rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', resize: 'vertical', fontSize: '1.05rem', lineHeight: '1.6' }} />
                  </div>

                  {editingPage && editingPage.id > 0 && (
                    <VisualManager sectionId={editingPage.id} />
                  )}
                </div>
              )}

              <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
                <button className="btn btn-primary" onClick={savePageContent} style={{ padding: '0.75rem 2rem' }}>
                  <Save size={20} /> Salvar Conteúdo
                </button>
                <button className="btn" style={{ background: 'transparent', color: 'var(--text-primary)' }} onClick={() => { setEditingPage(null); setPageForm({}); }}>
                  Cancelar
                </button>
              </div>
            </div>
          ) : (
            <>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h2>Gerenciar Seções de Páginas</h2>
                <button className="btn" style={{ background: 'var(--accent-secondary)' }} onClick={() => { setEditingPage(null); setPageForm({ slug: '' }); }}>
                  <Plus size={20} /> Nova Seção
                </button>
              </div>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                {pages.filter(p => p.parent_id === null).sort((a, b) => a.order - b.order).map(root => {
                  const children = pages.filter(p => p.parent_id === root.id).sort((a, b) => a.order - b.order);
                  return (
                    <div key={root.id} style={{ background: 'var(--bg-secondary)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
                        <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                          {root.icon_name && (LucideIcons as any)[root.icon_name]
                            ? React.createElement((LucideIcons as any)[root.icon_name], { size: 20 })
                            : <BookText size={20} style={{ opacity: 0.4 }} />}
                          {root.title} {root.order >= 900 && <span style={{ color: '#ef4444', fontSize: '0.85rem', marginLeft: '0.5rem' }}>(Inativo)</span>}
                        </h3>
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                          <button className="btn" style={{ padding: '0.4rem 0.75rem', fontSize: '0.8rem', background: root.order >= 900 ? '#10b981' : '#f59e0b', color: '#fff' }} onClick={async () => {
                            const newOrder = root.order >= 900 ? root.order - 900 : root.order + 900;
                            await axios.put(`http://127.0.0.1:8000/api/pages/${root.id}`, { order: newOrder });
                            fetchPages();
                          }}>
                            {root.order >= 900 ? 'Ativar' : 'Desativar'}
                          </button>
                          <button className="btn" style={{ padding: '0.4rem 0.75rem', fontSize: '0.8rem', background: '#3b82f6', color: '#fff' }} onClick={() => { setEditingPage(root); setPageForm(root); }}>
                            <Edit size={14} style={{ marginRight: '4px' }} /> Editar
                          </button>
                          <button className="btn" style={{ padding: '0.4rem 0.75rem', fontSize: '0.8rem', background: '#ef4444', color: '#fff' }} onClick={() => deletePageContent(root.id)}>
                            <Trash2 size={14} style={{ marginRight: '4px' }} /> Excluir
                          </button>
                        </div>
                      </div>
                      
                      <div className="grid-2" style={{ gap: '1rem' }}>
                        {children.map(child => (
                          <div key={child.id} className="glass-panel" style={{ padding: '1rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                            <div>
                              <h4 style={{ margin: '0 0 0.5rem 0', fontSize: '1.05rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                {child.icon_name && (LucideIcons as any)[child.icon_name]
                                  ? React.createElement((LucideIcons as any)[child.icon_name], { size: 16 })
                                  : <BookText size={16} style={{ opacity: 0.3 }} />}
                                {child.title} {child.order >= 900 && <span style={{ color: '#ef4444', fontSize: '0.8rem', marginLeft: '0.5rem' }}>(Inativo)</span>}
                              </h4>
                              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Slug: {child.slug} | Ordem: {child.order}</p>
                            </div>
                            <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end', marginTop: '1rem' }}>
                              <button className="btn" style={{ padding: '0.4rem 0.75rem', fontSize: '0.75rem', background: child.order >= 900 ? '#10b981' : '#f59e0b', color: '#fff' }} onClick={async () => {
                                const newOrder = child.order >= 900 ? child.order - 900 : child.order + 900;
                                await axios.put(`http://127.0.0.1:8000/api/pages/${child.id}`, { order: newOrder });
                                fetchPages();
                              }}>
                                {child.order >= 900 ? 'Ativar' : 'Desativar'}
                              </button>
                              <button className="btn" style={{ padding: '0.4rem 0.75rem', fontSize: '0.75rem', background: '#3b82f6', color: '#fff' }} onClick={() => { setEditingPage(child); setPageForm(child); }}>
                                <Edit size={14} />
                              </button>
                              <button className="btn" style={{ padding: '0.4rem 0.75rem', fontSize: '0.75rem', background: '#ef4444', color: '#fff' }} onClick={() => deletePageContent(child.id)}>
                                <Trash2 size={14} />
                              </button>
                            </div>
                          </div>
                        ))}
                        {children.length === 0 && <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', padding: '1rem' }}>Nenhuma sub-seção.</div>}
                      </div>
                    </div>
                  );
                })}
                {pages.length === 0 && <p>Nenhum conteúdo encontrado.</p>}
              </div>
            </>
          )}
        </section>
      )}

    </div>
  );
};

export default Admin;
