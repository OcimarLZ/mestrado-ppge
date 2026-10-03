import React, { useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import * as LucideIcons from 'lucide-react';
import { ArrowLeft, Construction, MessagesSquare } from 'lucide-react';
import topicos from '../data/forumTopicos';

// Comentários via Cusdis (https://cusdis.com) -- escolhido por não exigir conta de quem
// participa (basta um nome para comentar), sem anúncios e de código aberto; diferente do
// giscus (que foi descartado porque exigia conta no GitHub de cada participante), o Cusdis
// só exige uma conta do pesquisador, para moderar os comentários e criar o "app" do site.
//
// Para ativar, uma única vez, em https://cusdis.com (criar conta gratuita):
//   1. Criar um "app" com o domínio do site (ocimarlz.github.io).
//   2. Copiar o "App ID" gerado e colar na constante CUSDIS_APP_ID abaixo.
// Cada tópico usa seu próprio slug como data-page-id, então as conversas de cada tópico
// ficam separadas automaticamente -- não é preciso configurar nada por tópico.
const CUSDIS_APP_ID = '';
const CUSDIS_HOST = 'https://cusdis.com';

const isConfigured = Boolean(CUSDIS_APP_ID);

const ForumTopico: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const topico = topicos.find((t) => t.slug === slug);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isConfigured || !topico || !containerRef.current) return;
    containerRef.current.innerHTML = '';

    const thread = document.createElement('div');
    thread.id = 'cusdis_thread';
    thread.setAttribute('data-host', CUSDIS_HOST);
    thread.setAttribute('data-app-id', CUSDIS_APP_ID);
    thread.setAttribute('data-page-id', topico.slug);
    thread.setAttribute('data-page-url', window.location.href);
    thread.setAttribute('data-page-title', topico.title);
    containerRef.current.appendChild(thread);

    const script = document.createElement('script');
    script.src = `${CUSDIS_HOST}/js/cusdis.es.js`;
    script.async = true;
    script.defer = true;
    containerRef.current.appendChild(script);

    return () => {
      if (containerRef.current) containerRef.current.innerHTML = '';
    };
  }, [topico]);

  if (!topico) {
    return (
      <div className="container" style={{ marginTop: '2rem' }}>
        <p>Tópico não encontrado.</p>
        <Link to="/forum">Voltar ao Fórum</Link>
      </div>
    );
  }

  // @ts-ignore
  const Icon = LucideIcons[topico.icon] || MessagesSquare;

  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <Link to="/forum" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', marginBottom: '1rem', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
        <ArrowLeft size={16} /> Todos os tópicos
      </Link>

      <div className="chapter-header">
        <h1><Icon size={28} style={{ marginRight: '0.5rem', verticalAlign: 'middle', color: 'var(--accent-primary)' }} />{topico.title}</h1>
        <p className="lead" style={{ color: 'var(--text-secondary)' }}>{topico.description}</p>
      </div>

      {isConfigured ? (
        <div ref={containerRef} key={topico.slug} />
      ) : (
        <div className="glass-panel" style={{ textAlign: 'center', padding: '3rem 2rem' }}>
          <Construction size={40} color="var(--accent-primary)" style={{ marginBottom: '1rem' }} />
          <h2 style={{ marginBottom: '0.5rem' }}>Em Construção...</h2>
          <p style={{ color: 'var(--text-secondary)', maxWidth: 480, margin: '0 auto' }}>
            Os comentários deste tópico estão sendo configurados. Em breve será possível
            perguntar e responder diretamente aqui.
          </p>
        </div>
      )}
    </div>
  );
};

export default ForumTopico;
