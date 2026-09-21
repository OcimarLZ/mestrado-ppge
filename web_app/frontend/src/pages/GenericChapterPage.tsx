import React, { useMemo } from 'react';
import { useParams } from 'react-router-dom';
import DynamicSection, { type VisualData } from '../components/DynamicSection';
import { getChapter } from '../lib/content';

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
  visuals?: VisualData[];
  numbering?: string;
}

const GenericChapterPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();

  const items = useMemo<ContentItem[]>(() => {
    const raw = (getChapter(slug || '') as unknown as ContentItem[] | null) || [];
    const flatItems = raw.filter(item => item.order < 900);
    const prefixMap: Record<number, string> = {};
    const orderCounter: Record<string, number> = {};

    return flatItems.map((item) => {
      let numberStr = "";
      if (item.parent_id === null) {
        numberStr = `${item.order}`;
        prefixMap[item.id] = numberStr;
      } else {
        const parentKey = String(item.parent_id);
        orderCounter[parentKey] = (orderCounter[parentKey] || 0) + 1;
        const parentPrefix = prefixMap[item.parent_id] || "";
        numberStr = `${parentPrefix}.${orderCounter[parentKey]}`;
        prefixMap[item.id] = numberStr;
      }
      return { ...item, numbering: numberStr };
    });
  }, [slug]);

  if (items.length === 0) return <div className="container" style={{ marginTop: '2rem' }}>Capítulo não encontrado ou em construção.</div>;

  const chapter = items[0];
  const sections = items.slice(1);

  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1>{chapter.numbering}. {chapter.title}</h1>
        {chapter.content && <p className="lead" dangerouslySetInnerHTML={{ __html: chapter.content }} />}
      </div>
      
      {sections.map(section => (
        <DynamicSection
          key={section.id}
          sectionData={section}
          prefixNumber={section.numbering}
          visuals={section.visuals}
        />
      ))}
    </div>
  );
};

export default GenericChapterPage;
