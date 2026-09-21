import React, { useEffect, useState, useCallback } from 'react';
import { ChevronLeft, ChevronRight, Maximize, Minimize } from 'lucide-react';
import * as LucideIcons from 'lucide-react';
import ZoomableImage from './ZoomableImage';
import { assetUrl } from '../lib/content';
import type { Slide } from '../data/apresentacao';

const imgUrl = (file: string) => assetUrl(`assets/graficos_originais/${file}.png`);

const Icon: React.FC<{ name?: string; size?: number; className?: string }> = ({ name, size = 20, className }) => {
  // @ts-ignore
  const Comp = (name && LucideIcons[name]) || LucideIcons.Circle;
  return <Comp size={size} className={className} />;
};

const SlideViewer: React.FC<{ slides: Slide[] }> = ({ slides }) => {
  const [index, setIndex] = useState(0);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const goTo = useCallback((i: number) => {
    setIndex(Math.max(0, Math.min(slides.length - 1, i)));
  }, [slides.length]);

  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (['ArrowRight', ' ', 'PageDown'].includes(e.key)) { e.preventDefault(); goTo(index + 1); }
      else if (['ArrowLeft', 'PageUp'].includes(e.key)) { e.preventDefault(); goTo(index - 1); }
      else if (e.key === 'Home') goTo(0);
      else if (e.key === 'End') goTo(slides.length - 1);
    };
    document.addEventListener('keydown', onKeyDown);
    return () => document.removeEventListener('keydown', onKeyDown);
  }, [index, goTo, slides.length]);

  useEffect(() => {
    const onFsChange = () => setIsFullscreen(!!document.fullscreenElement);
    document.addEventListener('fullscreenchange', onFsChange);
    return () => document.removeEventListener('fullscreenchange', onFsChange);
  }, []);

  const toggleFullscreen = () => {
    if (document.fullscreenElement) {
      document.exitFullscreen();
    } else {
      document.getElementById('slide-viewer-root')?.requestFullscreen();
    }
  };

  const slide = slides[index];

  const renderBullets = (bullets?: string[]) => bullets && (
    <ul className="slide-bullets">
      {bullets.map((b, i) => <li key={i}>{b}</li>)}
    </ul>
  );

  const renderLogos = (size: 'lg' | 'sm' = 'lg') => (
    <div className={`slide-logos slide-logos-${size}`}>
      <img src={assetUrl('assets/logo_uffs.png')} alt="UFFS" />
      <img src={assetUrl('assets/logo_ppge.png')} alt="PPGE" />
    </div>
  );

  const renderBody = () => {
    switch (slide.kind) {
      case 'cover':
      case 'closing':
        return (
          <div className="slide-cover">
            {slide.showLogos && renderLogos('lg')}
            <h1>{slide.title}</h1>
            {slide.subtitle && <p className="slide-subtitle">{slide.subtitle}</p>}
            {renderBullets(slide.bullets)}
          </div>
        );
      case 'stats':
        return (
          <div className="slide-body">
            <h2>{slide.title}</h2>
            <div className="slide-stats-grid">
              {slide.stats?.map((s, i) => (
                <div key={i} className="slide-stat-card">
                  <div className="stat-value">{s.value}</div>
                  <div className="stat-label">{s.label}</div>
                </div>
              ))}
            </div>
            {renderBullets(slide.bullets)}
          </div>
        );
      case 'icons':
        return (
          <div className="slide-body">
            <h2>{slide.title}</h2>
            <ul className="slide-icon-list">
              {slide.items?.map((item, i) => (
                <li key={i}>
                  <span className="slide-icon-badge">
                    {item.label ? item.label : <Icon name={item.icon} size={20} />}
                  </span>
                  <span>{item.text}</span>
                </li>
              ))}
            </ul>
          </div>
        );
      case 'cards':
        return (
          <div className="slide-body">
            <h2>{slide.title}</h2>
            {slide.subtitle && <p className="slide-cards-subtitle">{slide.subtitle}</p>}
            <div className="slide-cards-grid">
              {slide.cards?.map((c, i) => (
                <div key={i} className="slide-card">
                  {c.icon && <Icon name={c.icon} size={22} className="slide-card-icon" />}
                  <h4>{c.title}</h4>
                  <p>{c.text}</p>
                </div>
              ))}
            </div>
          </div>
        );
      case 'columns':
        return (
          <div className="slide-body">
            <h2>{slide.title}</h2>
            <div className="slide-columns">
              {slide.columns?.map((col, i) => (
                <div key={i} className="slide-column">
                  <div className="slide-column-title">
                    {col.icon && <Icon name={col.icon} size={22} />}
                    <h3>{col.title}</h3>
                  </div>
                  <ul className="slide-bullets">
                    {col.items.map((it, j) => <li key={j}>{it}</li>)}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        );
      case 'image':
        return (
          <div className="slide-body slide-body-image">
            <h2>{slide.title}</h2>
            <div className="slide-image-area">
              {slide.image && (
                <figure>
                  <ZoomableImage src={imgUrl(slide.image.file)} alt={slide.image.caption || slide.title} style={{ maxWidth: '100%', maxHeight: '42vh', width: 'auto', borderRadius: '8px' }} />
                  {slide.image.caption && <figcaption>{slide.image.caption}</figcaption>}
                </figure>
              )}
            </div>
            {renderBullets(slide.bullets)}
          </div>
        );
      case 'images':
        return (
          <div className="slide-body slide-body-image">
            <h2>{slide.title}</h2>
            <div className="slide-image-area slide-image-area-multi">
              {slide.images?.map((img, i) => (
                <figure key={i}>
                  <ZoomableImage src={imgUrl(img.file)} alt={img.caption || slide.title} style={{ maxWidth: '100%', maxHeight: '38vh', width: 'auto', borderRadius: '8px' }} />
                  {img.caption && <figcaption>{img.caption}</figcaption>}
                </figure>
              ))}
            </div>
            {renderBullets(slide.bullets)}
          </div>
        );
      default:
        return (
          <div className="slide-body">
            <h2>{slide.title}</h2>
            {renderBullets(slide.bullets)}
          </div>
        );
    }
  };

  const isCoverLike = slide.kind === 'cover' || slide.kind === 'closing';

  return (
    <div id="slide-viewer-root" className={`slide-viewer ${isFullscreen ? 'is-fullscreen' : ''}`}>
      {!isCoverLike && (
        <div className="slide-brand-bar">
          <img src={assetUrl('assets/logo_uffs_horizontal.png')} alt="UFFS" />
          <span>PPGE · Educação a Distância no Brasil (2014-2024)</span>
        </div>
      )}
      <div className="slide-frame">
        {renderBody()}
      </div>

      <div className="slide-controls">
        <button onClick={() => goTo(index - 1)} disabled={index === 0} aria-label="Slide anterior"><ChevronLeft size={20} /></button>
        <span className="slide-counter">{index + 1} / {slides.length}</span>
        <button onClick={() => goTo(index + 1)} disabled={index === slides.length - 1} aria-label="Próximo slide"><ChevronRight size={20} /></button>
        <button onClick={toggleFullscreen} aria-label="Tela cheia" className="slide-fullscreen-btn">
          {isFullscreen ? <Minimize size={18} /> : <Maximize size={18} />}
        </button>
      </div>
    </div>
  );
};

export default SlideViewer;
