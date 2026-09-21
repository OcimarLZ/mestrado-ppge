import React, { useEffect } from 'react';
import { NavLink, Outlet, useLocation } from 'react-router-dom';
import { BookOpen, Home, BookText } from 'lucide-react';
import * as LucideIcons from 'lucide-react';
import themes from '../themes';
import { getTree, getSiteSettings, assetUrl } from '../lib/content';

interface TreeNode {
  id: number;
  parent_id: number | null;
  slug: string;
  title: string;
  order: number;
  icon_name: string | null;
  children: TreeNode[];
}

interface SiteSettings {
  sidebar_title: string;
  sidebar_icon: string;
  topbar_title: string;
  footer_text_1: string;
  footer_text_2: string;
  theme_bg_color?: string;
  theme_text_color?: string;
  theme_primary_color?: string;
  theme_card_bg_color?: string;
  theme_font_family?: string;
  theme_sidebar_bg?: string;
  theme_hero_glow_color?: string;
  theme_name?: string;
}

const Layout: React.FC = () => {
  const tree = getTree() as unknown as TreeNode[];
  const settings = getSiteSettings() as unknown as SiteSettings;
  const location = useLocation();

  useEffect(() => {
    if (settings?.theme_bg_color) {
      const root = document.documentElement;
      const match = themes.find(t => t.name === settings.theme_name);
      const sec = match?.colors.textSecondary || '#94a3b8';
      root.style.setProperty('--bg-dark', settings.theme_bg_color);
      root.style.setProperty('--bg-card', settings.theme_card_bg_color || 'rgba(30, 41, 59, 0.7)');
      root.style.setProperty('--text-primary', settings.theme_text_color || '#f8fafc');
      root.style.setProperty('--text-secondary', sec);
      root.style.setProperty('--accent-primary', settings.theme_primary_color || '#10b981');
      root.style.setProperty('--sidebar-bg', settings.theme_sidebar_bg || settings.theme_bg_color);
      root.style.setProperty('--topbar-bg', settings.theme_sidebar_bg || settings.theme_bg_color);
      root.style.setProperty('--hero-glow', settings.theme_hero_glow_color || 'rgba(16,185,129,0.1)');
      if (settings.theme_font_family) {
        root.style.setProperty('--theme-font-family', settings.theme_font_family);
        document.body.style.fontFamily = settings.theme_font_family;
      }
    }
  }, [settings]);

  const scrollToSection = (e: React.MouseEvent, sectionSlug: string) => {
    e.preventDefault();
    const element = document.getElementById(sectionSlug);
    if (element) {
      const headerOffset = 100; // Account for any fixed headers if present
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }
  };

  const renderTreeView = (chapterNode: TreeNode, chapterNumber: number) => {
    const isChapterActive = location.pathname === `/capitulo/${chapterNode.slug}`;
    if (!isChapterActive || chapterNode.children.length === 0) return null;

    return (
      <ul className="tree-view" style={{ paddingLeft: '2.5rem', listStyle: 'none', marginTop: '0.5rem', marginBottom: '0.5rem' }}>
        {chapterNode.children.filter(c => c.order < 900).map((section, idx) => (
          <li key={section.id} style={{ marginBottom: '0.5rem' }}>
            <a 
              href={`#${section.slug}`} 
              onClick={(e) => scrollToSection(e, section.slug)}
              style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', textDecoration: 'none', transition: 'color 0.2s ease' }}
              onMouseOver={(e) => e.currentTarget.style.color = 'var(--accent-primary)'}
              onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-secondary)'}
            >
              • {chapterNumber}.{idx + 1} {section.title}
            </a>
          </li>
        ))}
      </ul>
    );
  };

  return (
    <div className="app-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <BookOpen color="var(--accent-primary)" size={24} />
          <h3>{settings?.sidebar_title || "EaD no Brasil"}</h3>
        </div>
        
        <nav className="sidebar-nav">
          <ul>
            <li>
              <NavLink to="/" className={({ isActive }) => isActive ? 'active' : ''} end>
                <Home size={18} /> Início
              </NavLink>
            </li>
            
            {/* Renderização Dinâmica dos Capítulos */}
            {tree.filter(chapter => chapter.order < 900).map((chapter, idx) => {
              const chapterNumber = idx + 1;
              let IconComponent = BookText; // fallback icon
              
              if (chapter.icon_name) {
                // @ts-ignore
                const DynamicIcon = LucideIcons[chapter.icon_name];
                if (DynamicIcon) IconComponent = DynamicIcon;
              }

              return (
                <li key={chapter.id}>
                  <NavLink to={`/capitulo/${chapter.slug}`} className={({ isActive }) => isActive ? 'active' : ''}>
                    <IconComponent size={18} /> {chapterNumber}. {chapter.title}
                  </NavLink>
                  {renderTreeView(chapter, chapterNumber)}
                </li>
              );
            })}

          </ul>
        </nav>
      </aside>

      {/* Main Content Area */}
      <div className="main-content">
        <header className="topbar">
          <div className="topbar-container">
            <div className="topbar-title">
              <span>{settings?.topbar_title || "Carregando..."}</span>
            </div>
            <div className="topbar-actions" style={{ display: 'flex', gap: '1rem' }}>
              {import.meta.env.DEV && (
                <NavLink to="/admin" className="btn" style={{ padding: '0.5rem 1rem', fontSize: '0.875rem', background: 'transparent', color: 'var(--text-primary)', border: '1px solid var(--border-color)' }}>
                  Admin
                </NavLink>
              )}
              <a href={assetUrl('assets/dissertacao.pdf')} target="_blank" rel="noreferrer" className="btn btn-secondary" style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }}>
                PDF Completo
              </a>
            </div>
          </div>
        </header>

        <div className="page-content">
          <Outlet />
        </div>

        <footer>
          <div className="container footer-content">
            <div className="logos">
              <img src={assetUrl('assets/logo_uffs.png')} alt="Logo UFFS" onError={(e) => { e.currentTarget.style.display = 'none'; }} />
              <img src={assetUrl('assets/logo_ppge.png')} alt="Logo PPGE" onError={(e) => { e.currentTarget.style.display = 'none'; }} />
            </div>
            <div style={{ textAlign: 'right' }}>
              <p style={{ margin: 0, fontSize: '0.875rem' }}>{settings?.footer_text_1}</p>
              <p style={{ margin: 0, fontSize: '0.875rem', color: 'var(--text-secondary)' }}>{settings?.footer_text_2}</p>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default Layout;
