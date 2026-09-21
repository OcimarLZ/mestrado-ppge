import React from 'react';
import * as LucideIcons from 'lucide-react';
import DataVisualization from './DataVisualization';
import ContentWithVisuals from './ContentWithVisuals';
import ZoomableImage from './ZoomableImage';

export interface ContentItem {
  id: number;
  parent_id: number | null;
  slug: string;
  title: string;
  content: string;
  order: number;
  icon_name: string | null;
  content_type?: string;
  image_url?: string | null;
  chart_type?: string | null;
  x_axis?: string | null;
  y_axis?: string | null;
  legend_position?: string | null;
  analysis_text?: string | null;
  data?: Record<string, unknown>[] | null;
}

export interface VisualData {
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

interface DynamicSectionProps {
  sectionData?: ContentItem;
  fallbackTitle?: string;
  icon?: React.ReactNode;
  children?: React.ReactNode;
  prefixNumber?: string;
  visuals?: VisualData[];
}

const DynamicSection: React.FC<DynamicSectionProps> = ({ sectionData, fallbackTitle, icon, children, prefixNumber, visuals }) => {
  if (!sectionData) {
    return (
      <section className="section-block" style={{ opacity: 0.6 }}>
        <h2>{icon} {fallbackTitle}</h2>
        <div className="text-content">
          <p><em>(Conteúdo ainda não sincronizado ou carregando do banco de dados...)</em></p>
        </div>
        {children}
      </section>
    );
  }

  let IconComponent = icon;
  if (sectionData.icon_name) {
    // @ts-ignore
    const DynamicIcon = LucideIcons[sectionData.icon_name];
    if (DynamicIcon) {
      IconComponent = <DynamicIcon size={24} color="var(--accent-primary)" />;
    }
  }

  const renderContent = (html: string) => (
    <ContentWithVisuals html={html} visuals={visuals} />
  );

  return (
    <section id={sectionData.slug} className="section-block">
      <h2>
        {IconComponent && <span style={{ marginRight: '0.5rem', display: 'inline-flex', alignItems: 'center' }}>{IconComponent}</span>}
        {prefixNumber && `${prefixNumber}. `}{sectionData.title}
      </h2>

      {sectionData.content_type === 'html' && sectionData.content && (
        <div style={{ width: '100%', margin: '2rem 0' }} dangerouslySetInnerHTML={{ __html: sectionData.content }} />
      )}
      {sectionData.content_type !== 'html' && sectionData.content && renderContent(sectionData.content)}

      {(sectionData.content_type === 'chart' || sectionData.content_type === 'table') && (
        <DataVisualization
          data={sectionData.data}
          contentType={sectionData.content_type}
          chartType={sectionData.chart_type}
          xAxis={sectionData.x_axis}
          yAxis={sectionData.y_axis}
          legendPosition={sectionData.legend_position}
        />
      )}

      {sectionData.content_type === 'image' && sectionData.image_url && (
        <div style={{ margin: '2rem 0', textAlign: 'center' }}>
          <ZoomableImage src={sectionData.image_url} alt={sectionData.title} style={{ maxWidth: '100%', height: 'auto', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }} />
        </div>
      )}

      {sectionData.analysis_text && (
        <div className="text-content" style={{ marginTop: '2rem' }} dangerouslySetInnerHTML={{ __html: sectionData.analysis_text }} />
      )}

      {children}
    </section>
  );
};

export default DynamicSection;
