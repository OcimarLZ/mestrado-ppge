import React, { useCallback, useRef, useState } from 'react';

interface ComparisonSliderProps {
  beforeSrc: string;
  afterSrc: string;
  beforeLabel: string;
  afterLabel: string;
  alt?: string;
}

// Comparador "antes/depois" com controle deslizante -- arrastavel por mouse e por touch
// (Pointer Events cobrem os dois com a mesma logica), mais suporte a teclado (setas) para
// quem navega sem mouse. Nunca depende de hover: o cabo fica visivel e interativo desde
// que o componente aparece na tela, no mesmo espirito das outras interacoes do site
// (zoom e tooltips tambem sao por clique/foco, nunca so por hover).
const ComparisonSlider: React.FC<ComparisonSliderProps> = ({ beforeSrc, afterSrc, beforeLabel, afterLabel, alt }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const draggingRef = useRef(false);
  const [percent, setPercent] = useState(50);

  const updateFromClientX = useCallback((clientX: number) => {
    const el = containerRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const pct = ((clientX - rect.left) / rect.width) * 100;
    setPercent(Math.min(100, Math.max(0, pct)));
  }, []);

  const onPointerDown = (e: React.PointerEvent<HTMLDivElement>) => {
    draggingRef.current = true;
    e.currentTarget.setPointerCapture(e.pointerId);
    updateFromClientX(e.clientX);
  };

  const onPointerMove = (e: React.PointerEvent<HTMLDivElement>) => {
    if (!draggingRef.current) return;
    updateFromClientX(e.clientX);
  };

  const stopDragging = () => {
    draggingRef.current = false;
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'ArrowLeft') {
      e.preventDefault();
      setPercent((p) => Math.max(0, p - 5));
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      setPercent((p) => Math.min(100, p + 5));
    } else if (e.key === 'Home') {
      setPercent(0);
    } else if (e.key === 'End') {
      setPercent(100);
    }
  };

  return (
    <div
      ref={containerRef}
      className="comparison-slider"
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={stopDragging}
      onPointerCancel={stopDragging}
    >
      <img src={afterSrc} alt={alt || afterLabel} className="comparison-slider-img" draggable={false} />
      <img
        src={beforeSrc}
        alt={alt || beforeLabel}
        className="comparison-slider-img comparison-slider-img-before"
        style={{ clipPath: `inset(0 ${100 - percent}% 0 0)` }}
        draggable={false}
      />

      <span className="comparison-slider-label comparison-slider-label-before">{beforeLabel}</span>
      <span className="comparison-slider-label comparison-slider-label-after">{afterLabel}</span>

      <div className="comparison-slider-divider" style={{ left: `${percent}%` }} />
      <div
        className="comparison-slider-handle"
        style={{ left: `${percent}%` }}
        role="slider"
        tabIndex={0}
        aria-label={`Comparação: ${beforeLabel} até ${afterLabel}`}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={Math.round(percent)}
        onKeyDown={onKeyDown}
      >
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <path d="M5 3 1 8l4 5M11 3l4 5-4 5" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
    </div>
  );
};

export default ComparisonSlider;
