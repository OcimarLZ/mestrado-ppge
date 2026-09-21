import React, { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import { ZoomIn, X } from 'lucide-react';

interface ZoomableImageProps {
  src: string;
  alt: string;
  style?: React.CSSProperties;
}

// Imagem com "clique para ampliar": abre a versao em tamanho real numa janela
// sobreposta (lightbox), com rolagem, para ler tabelas/graficos densos de perto.
// Funciona em touch tambem (diferente de zoom por hover do mouse).
const ZoomableImage: React.FC<ZoomableImageProps> = ({ src, alt, style }) => {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!open) return;
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setOpen(false);
    };
    document.addEventListener('keydown', onKeyDown);
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', onKeyDown);
      document.body.style.overflow = '';
    };
  }, [open]);

  return (
    <>
      <div
        className="zoomable-image"
        onClick={() => setOpen(true)}
        role="button"
        tabIndex={0}
        aria-label={`Ampliar imagem: ${alt}`}
        onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') setOpen(true); }}
      >
        <img src={src} alt={alt} style={style} />
        <span className="zoomable-image-hint"><ZoomIn size={14} /> Clique para ampliar</span>
      </div>
      {open && createPortal(
        <div className="lightbox-backdrop" onClick={() => setOpen(false)}>
          <button className="lightbox-close" onClick={() => setOpen(false)} aria-label="Fechar">
            <X size={22} />
          </button>
          <div className="lightbox-scroll" onClick={(e) => e.stopPropagation()}>
            <img src={src} alt={alt} className="lightbox-image" />
          </div>
        </div>,
        document.body
      )}
    </>
  );
};

export default ZoomableImage;
