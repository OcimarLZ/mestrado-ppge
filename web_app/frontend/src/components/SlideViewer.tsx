import React, { useEffect, useState, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { ChevronLeft, ChevronRight, Maximize, Minimize, ArrowRight } from 'lucide-react';
import * as LucideIcons from 'lucide-react';
import ZoomableImage from './ZoomableImage';
import ComparisonSlider from './ComparisonSlider';
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

  // Permite marcar percentuais/valores/anos com <span class="slide-pos|slide-neg">
  // diretamente no texto dos slides (ver data/apresentacao.ts) -- conteudo 100%
  // autoral/estatico, nunca entrada de usuario, por isso dangerouslySetInnerHTML e seguro aqui.
  const html = (s?: string) => ({ __html: s || '' });

  const renderBullets = (bullets?: string[], centered?: boolean) => bullets && (
    <ul className={`slide-bullets ${centered ? 'slide-bullets-centered' : ''}`}>
      {bullets.map((b, i) => <li key={i} dangerouslySetInnerHTML={html(b)} />)}
    </ul>
  );

  const renderLogos = (size: 'lg' | 'sm' = 'lg') => (
    <div className={`slide-logos slide-logos-${size}`}>
      <img src={assetUrl('assets/logo_uffs.png')} alt="UFFS" className="logo-uffs" />
      <img src={assetUrl('assets/logo_ppge.png')} alt="PPGE" className="logo-ppge" />
    </div>
  );

  const renderBody = () => {
    switch (slide.kind) {
      case 'cover':
      case 'closing':
        return (
          <div
            className={`slide-cover ${slide.kind === 'cover' ? 'slide-cover-opening' : ''} ${slide.kind === 'closing' ? 'slide-cover-closing' : ''} ${slide.backgroundImage ? 'slide-cover-with-bg' : ''}`}
            style={slide.backgroundImage ? { backgroundImage: `url(${imgUrl(slide.backgroundImage)})` } : undefined}
          >
            {slide.showLogos && renderLogos('lg')}
            <h1>{slide.title}</h1>
            {slide.subtitle && <p className="slide-subtitle">{slide.subtitle}</p>}
            {renderBullets(slide.bullets)}
            {slide.footerNote && <p className="slide-footer-note">{slide.footerNote}</p>}
            {slide.links && slide.links.length > 0 && (
              <div className="slide-links-wrap">
                <div className="slide-links slide-links-vertical">
                  {slide.links.map((l, i) => (
                    <Link key={i} to={l.to} className="slide-link-pill">
                      {l.label} <ArrowRight size={16} />
                    </Link>
                  ))}
                </div>
              </div>
            )}
            {slide.contactInfo && slide.contactInfo.length > 0 && (
              <div className="slide-contact-info">
                {slide.contactInfo.map((c, i) => <p key={i}>{c}</p>)}
              </div>
            )}
          </div>
        );
      case 'text':
        return (
          <div className="slide-body slide-epigraph">
            {slide.title && <h2>{slide.title}</h2>}
            <ul className="slide-bullets slide-bullets-plain">
              {slide.bullets?.map((b, i) => <li key={i}>{b}</li>)}
            </ul>
          </div>
        );
      case 'stats':
        return (
          <div className={`slide-body ${slide.raiseContent ? 'slide-body-top' : ''}`}>
            <h2 className={slide.centerContent ? 'slide-h2-centered' : ''}>{slide.title}</h2>
            {slide.statGroups ? (
              <div className="slide-stat-groups">
                {slide.statGroups.map((g, gi) => (
                  <div key={gi} className="slide-stat-group">
                    <h3 className="slide-stat-group-title">{g.title}</h3>
                    <div className="slide-stat-group-grid">
                      {g.stats.map((s, i) => (
                        <div key={i} className="slide-stat-card slide-stat-card-sub">
                          <div className="stat-value" dangerouslySetInnerHTML={html(s.value)} />
                          <div className="stat-label" dangerouslySetInnerHTML={html(s.label)} />
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="slide-stats-grid">
                {slide.stats?.map((s, i) => (
                  <div key={i} className="slide-stat-card">
                    <div className="stat-value" dangerouslySetInnerHTML={html(s.value)} />
                    <div className="stat-label" dangerouslySetInnerHTML={html(s.label)} />
                  </div>
                ))}
              </div>
            )}
            {renderBullets(slide.bullets, slide.centerBullets)}
          </div>
        );
      case 'icons':
        return (
          <div className={`slide-body ${slide.raiseContent ? 'slide-body-top' : ''}`}>
            <h2 className={slide.centerContent ? 'slide-h2-centered' : ''}>{slide.title}</h2>
            <ul className={`slide-icon-list ${slide.centerContent ? 'slide-icon-list-centered' : ''} ${slide.wideItems ? 'slide-icon-list-wide' : ''} ${slide.largeText ? 'slide-icon-list-large' : ''}`}>
              {slide.items?.map((item, i) => (
                <li key={i}>
                  <span className="slide-icon-badge">
                    {item.label ? item.label : <Icon name={item.icon} size={20} />}
                  </span>
                  <span dangerouslySetInnerHTML={html(item.text)} />
                </li>
              ))}
            </ul>
          </div>
        );
      case 'cards':
        return (
          <div className={`slide-body ${slide.raiseContent ? 'slide-body-top' : ''}`}>
            <h2 className={slide.centerContent ? 'slide-h2-centered' : ''}>{slide.title}</h2>
            {slide.subtitle && <p className={`slide-cards-subtitle ${slide.centerContent ? 'slide-h2-centered' : ''}`}>{slide.subtitle}</p>}
            <div className={`slide-cards-grid ${slide.cardsRowsOf3 ? 'slide-cards-grid-3-2' : ''} ${slide.largeText ? 'slide-cards-large' : ''}`}>
              {slide.cards?.map((c, i) => (
                <div key={i} className="slide-card">
                  {c.icon && <Icon name={c.icon} size={22} className="slide-card-icon" />}
                  <h4>{c.title}</h4>
                  <p dangerouslySetInnerHTML={html(c.text)} />
                </div>
              ))}
            </div>
            {slide.image && (
              <div className="slide-image-area slide-cards-image">
                <figure>
                  <ZoomableImage src={imgUrl(slide.image.file)} alt={slide.image.caption || slide.title} style={{ maxWidth: '100%', maxHeight: '28vh', width: 'auto', borderRadius: '8px' }} />
                  {slide.image.caption && <figcaption>{slide.image.caption}</figcaption>}
                </figure>
              </div>
            )}
            {renderBullets(slide.bullets, slide.centerBullets)}
          </div>
        );
      case 'columns':
        return (
          <div className={`slide-body ${slide.raiseContent ? 'slide-body-top' : ''}`}>
            <h2 className={slide.centerContent ? 'slide-h2-centered' : ''}>{slide.title}</h2>
            <div className="slide-columns">
              {slide.columns?.map((col, i) => (
                <div key={i} className="slide-column">
                  <div className="slide-column-title">
                    {col.icon && <Icon name={col.icon} size={22} />}
                    <h3>{col.title}</h3>
                  </div>
                  <ul className="slide-bullets">
                    {col.items.map((it, j) => <li key={j} dangerouslySetInnerHTML={html(it)} />)}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        );
      case 'image':
        return (
          <div className={`slide-body slide-body-image ${slide.raiseContent ? 'slide-body-top' : ''}`}>
            {slide.title && <h2 className={slide.centerContent ? 'slide-h2-centered' : ''}>{slide.title}</h2>}
            {slide.sideBullets ? (
              <>
                <div className="slide-image-flanked">
                  <p className="slide-flank-text" dangerouslySetInnerHTML={html(slide.bullets?.[0])} />
                  <div className="slide-image-area">
                    {slide.table ? (
                      <figure>
                        <table className="slide-table">
                          <thead>
                            <tr>{slide.table.headers.map((h, i) => <th key={i}>{h}</th>)}</tr>
                          </thead>
                          <tbody>
                            {slide.table.rows.map((row, i) => (
                              <tr key={i}>{row.map((cell, j) => <td key={j} dangerouslySetInnerHTML={html(cell)} />)}</tr>
                            ))}
                          </tbody>
                        </table>
                        {slide.image?.caption && <figcaption>{slide.image.caption}</figcaption>}
                      </figure>
                    ) : slide.image && (
                      <figure>
                        <ZoomableImage src={imgUrl(slide.image.file)} alt={slide.image.caption || slide.title} style={{ maxWidth: '100%', maxHeight: '50vh', width: 'auto', borderRadius: '8px' }} />
                        {slide.image.caption && <figcaption>{slide.image.caption}</figcaption>}
                      </figure>
                    )}
                  </div>
                  <p className="slide-flank-text" dangerouslySetInnerHTML={html(slide.bullets?.[1])} />
                </div>
                {slide.secondaryImages && slide.secondaryImages.length > 0 && (
                  <div className="slide-image-area slide-image-area-secondary slide-image-area-multi">
                    {slide.secondaryImages.map((img, i) => (
                      <figure key={i}>
                        <ZoomableImage src={imgUrl(img.file)} alt={img.caption || slide.title} style={{ maxWidth: '100%', maxHeight: slide.secondaryImageMaxHeight || '20vh', width: 'auto', borderRadius: '8px' }} />
                        {img.caption && <figcaption>{img.caption}</figcaption>}
                      </figure>
                    ))}
                  </div>
                )}
                {slide.bullets && slide.bullets.length > 2 && renderBullets(slide.bullets.slice(2), slide.centerBullets)}
              </>
            ) : (
              <>
                <div className="slide-image-area">
                  {slide.image && (
                    <figure>
                      <ZoomableImage src={imgUrl(slide.image.file)} alt={slide.image.caption || slide.title} style={{ maxWidth: '100%', maxHeight: slide.imageMaxHeight || '58vh', width: 'auto', borderRadius: '8px' }} />
                      {slide.image.caption && <figcaption>{slide.image.caption}</figcaption>}
                    </figure>
                  )}
                </div>
                {slide.secondaryImages && slide.secondaryImages.length > 0 && (
                  <div className="slide-image-area slide-image-area-secondary slide-image-area-multi">
                    {slide.secondaryImages.map((img, i) => (
                      <figure key={i}>
                        <ZoomableImage src={imgUrl(img.file)} alt={img.caption || slide.title} style={{ maxWidth: '100%', maxHeight: slide.secondaryImageMaxHeight || '20vh', width: 'auto', borderRadius: '8px' }} />
                        {img.caption && <figcaption>{img.caption}</figcaption>}
                      </figure>
                    ))}
                  </div>
                )}
                {renderBullets(slide.bullets, slide.centerBullets)}
              </>
            )}
            {slide.links && slide.links.length > 0 && (
              <div className="slide-links-wrap">
                <p className="slide-links-hint">Para entender melhor as ferramentas utilizadas:</p>
                <div className="slide-links">
                  {slide.links.map((l, i) => (
                    <Link key={i} to={l.to} className="slide-link-pill">
                      {l.label} <ArrowRight size={16} />
                    </Link>
                  ))}
                </div>
              </div>
            )}
          </div>
        );
      case 'images':
        return (
          <div className={`slide-body slide-body-image ${slide.raiseContent ? 'slide-body-top' : ''}`}>
            <h2 className={slide.centerContent ? 'slide-h2-centered' : ''}>{slide.title}</h2>
            <div className="slide-image-area slide-image-area-multi">
              {slide.images?.map((img, i) => (
                <figure key={i}>
                  <ZoomableImage src={imgUrl(img.file)} alt={img.caption || slide.title} style={{ maxWidth: '100%', maxHeight: slide.imageMaxHeight || '52vh', width: 'auto', borderRadius: '8px' }} />
                  {img.caption && <figcaption>{img.caption}</figcaption>}
                </figure>
              ))}
            </div>
            {renderBullets(slide.bullets, slide.centerBullets)}
          </div>
        );
      case 'comparison':
        return (
          <div className="slide-body slide-body-image">
            <h2>{slide.title}</h2>
            <div className="slide-image-area">
              {slide.comparison && (
                <figure style={{ maxWidth: 760, width: '100%' }}>
                  <ComparisonSlider
                    beforeSrc={imgUrl(slide.comparison.before.file)}
                    afterSrc={imgUrl(slide.comparison.after.file)}
                    beforeLabel={slide.comparison.beforeLabel}
                    afterLabel={slide.comparison.afterLabel}
                    alt={slide.title}
                  />
                  {slide.note && <figcaption>{slide.note}</figcaption>}
                </figure>
              )}
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
