import React, { useEffect, useState, useCallback } from 'react';
import { ChevronLeft, ChevronRight, Maximize, Minimize } from 'lucide-react';
import ZoomableImage from './ZoomableImage';
import { assetUrl } from '../lib/content';
import type { Slide } from '../data/apresentacao';

const imgUrl = (file: string) => assetUrl(`assets/graficos_originais/${file}.png`);

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

  const renderBody = () => {
    switch (slide.kind) {
      case 'cover':
      case 'closing':
        return (
          <div className="slide-cover">
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
      case 'image':
        return (
          <div className="slide-body slide-body-image">
            <h2>{slide.title}</h2>
            <div className="slide-image-area">
              {slide.image && (
                <figure>
                  <ZoomableImage src={imgUrl(slide.image.file)} alt={slide.image.caption || slide.title} style={{ maxWidth: '100%', maxHeight: '48vh', width: 'auto', borderRadius: '8px' }} />
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
                  <ZoomableImage src={imgUrl(img.file)} alt={img.caption || slide.title} style={{ maxWidth: '100%', maxHeight: '40vh', width: 'auto', borderRadius: '8px' }} />
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

  return (
    <div id="slide-viewer-root" className={`slide-viewer ${isFullscreen ? 'is-fullscreen' : ''}`}>
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
