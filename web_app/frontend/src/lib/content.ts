// Acesso ao conteudo estatico gerado por web_app/content_export/export_static_site.py.
// Substitui as chamadas axios a uma API FastAPI viva: o build do GitHub Pages nao tem
// backend, entao todo o conteudo do CMS (site_cms.db) fica congelado neste JSON em build-time.
import siteContent from '../data/site-content.json';

const content = siteContent as {
  site_settings: Record<string, unknown>;
  dashboard_summary: Record<string, unknown>;
  home_cards: Record<string, unknown>[];
  tree: Record<string, unknown>[];
  chapters: Record<string, Record<string, unknown>[]>;
};

export function getSiteSettings() {
  return content.site_settings;
}

export function getDashboardSummary() {
  return content.dashboard_summary;
}

export function getHomeCards() {
  return content.home_cards;
}

export function getTree() {
  return content.tree;
}

export function getChapter(slug: string) {
  return content.chapters[slug] ?? null;
}

// asset_url resolve um caminho relativo (ex: "assets/dissertacao.pdf") respeitando o
// `base` configurado no vite.config.ts (necessario para deploy em subpasta no GitHub Pages).
export function assetUrl(relativePath: string) {
  const base = import.meta.env.BASE_URL;
  return `${base}${relativePath}`.replace(/([^:])\/\//g, '$1/');
}
