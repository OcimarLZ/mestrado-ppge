import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import * as LucideIcons from 'lucide-react';
import { ArrowLeft, Construction, MessagesSquare, Send } from 'lucide-react';
import topicos from '../data/forumTopicos';
import perguntasPorTopicoJson from '../data/forum_perguntas.json';

interface Resposta {
  id: string;
  texto: string;
  autor: string;
  data: string;
}

interface Pergunta {
  id: string;
  pergunta: string;
  autor: string;
  data: string;
  respostas: Resposta[];
}

const perguntasPorTopico = perguntasPorTopicoJson as Record<string, Pergunta[]>;

// API-ponte (serviço compartilhado no Render, usado também por outras landing pages) que
// grava a pergunta/resposta direto no JSON deste repositório via API do GitHub -- não há
// banco de dados nem conta exigida de quem participa. Ver web_app/forum_api/main.py, onde
// FORUM_PROJETO precisa corresponder exatamente a uma chave do dicionário PROJETOS.
// Enquanto FORUM_API_BASE estiver vazio (serviço ainda não publicado no Render), o
// formulário mostra um aviso em vez de tentar enviar.
const FORUM_API_BASE = '';
const FORUM_PROJETO = 'ocimar-mestrado-ppge';
const isConfigured = Boolean(FORUM_API_BASE);

function formatarData(iso: string): string {
  try {
    return new Date(iso).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
  } catch {
    return '';
  }
}

const HoneypotField: React.FC<{ value: string; onChange: (v: string) => void }> = ({ value, onChange }) => (
  <input
    type="text"
    name="site"
    value={value}
    onChange={(e) => onChange(e.target.value)}
    tabIndex={-1}
    autoComplete="off"
    aria-hidden="true"
    style={{ position: 'absolute', left: '-9999px', width: 1, height: 1, opacity: 0 }}
  />
);

const NovaPerguntaForm: React.FC<{ topicoSlug: string; onEnviada: () => void }> = ({ topicoSlug, onEnviada }) => {
  const [nome, setNome] = useState('');
  const [pergunta, setPergunta] = useState('');
  const [honeypot, setHoneypot] = useState('');
  const [status, setStatus] = useState<'idle' | 'enviando' | 'ok' | 'erro'>('idle');

  const enviar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!pergunta.trim()) return;
    setStatus('enviando');
    try {
      const r = await fetch(`${FORUM_API_BASE}/perguntas`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projeto: FORUM_PROJETO, topico: topicoSlug, pergunta, nome, site: honeypot }),
      });
      if (!r.ok) throw new Error('falha');
      setStatus('ok');
      setPergunta('');
      setNome('');
      onEnviada();
    } catch {
      setStatus('erro');
    }
  };

  if (status === 'ok') {
    return (
      <div className="glass-panel" style={{ padding: '1.5rem 2rem', textAlign: 'center' }}>
        <p style={{ margin: 0 }}>
          Pergunta enviada! Ela passa por um pequeno processo automático e aparece aqui em
          alguns minutos.
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={enviar} className="glass-panel" style={{ padding: '1.5rem 2rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
      <HoneypotField value={honeypot} onChange={setHoneypot} />
      <textarea
        required
        maxLength={500}
        placeholder="Escreva sua pergunta..."
        value={pergunta}
        onChange={(e) => setPergunta(e.target.value)}
        rows={3}
        style={{ width: '100%', resize: 'vertical', fontFamily: 'inherit' }}
      />
      <input
        type="text"
        maxLength={60}
        placeholder="Seu nome (opcional)"
        value={nome}
        onChange={(e) => setNome(e.target.value)}
      />
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <button type="submit" className="btn btn-primary" disabled={status === 'enviando'} style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem' }}>
          <Send size={16} /> {status === 'enviando' ? 'Enviando...' : 'Enviar pergunta'}
        </button>
        {status === 'erro' && <span style={{ color: '#ef4444', fontSize: '0.9rem' }}>Não foi possível enviar. Tente novamente.</span>}
      </div>
    </form>
  );
};

const NovaRespostaForm: React.FC<{ topicoSlug: string; perguntaId: string; onEnviada: () => void }> = ({ topicoSlug, perguntaId, onEnviada }) => {
  const [nome, setNome] = useState('');
  const [resposta, setResposta] = useState('');
  const [honeypot, setHoneypot] = useState('');
  const [status, setStatus] = useState<'idle' | 'enviando' | 'ok' | 'erro'>('idle');

  const enviar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!resposta.trim()) return;
    setStatus('enviando');
    try {
      const r = await fetch(`${FORUM_API_BASE}/respostas`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projeto: FORUM_PROJETO, topico: topicoSlug, pergunta_id: perguntaId, resposta, nome, site: honeypot }),
      });
      if (!r.ok) throw new Error('falha');
      setStatus('ok');
      setResposta('');
      setNome('');
      onEnviada();
    } catch {
      setStatus('erro');
    }
  };

  if (status === 'ok') {
    return <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', margin: '0.5rem 0 0 0' }}>Resposta enviada! Aparece aqui em alguns minutos.</p>;
  }

  return (
    <form onSubmit={enviar} style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '0.75rem' }}>
      <HoneypotField value={honeypot} onChange={setHoneypot} />
      <textarea
        required
        maxLength={1000}
        placeholder="Escreva sua resposta..."
        value={resposta}
        onChange={(e) => setResposta(e.target.value)}
        rows={2}
        style={{ width: '100%', resize: 'vertical', fontFamily: 'inherit', fontSize: '0.9rem' }}
      />
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <input
          type="text"
          maxLength={60}
          placeholder="Seu nome (opcional)"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          style={{ fontSize: '0.9rem', flex: 1 }}
        />
        <button type="submit" disabled={status === 'enviando'} className="btn btn-primary" style={{ fontSize: '0.85rem', padding: '0.4rem 0.9rem' }}>
          {status === 'enviando' ? 'Enviando...' : 'Responder'}
        </button>
      </div>
      {status === 'erro' && <span style={{ color: '#ef4444', fontSize: '0.85rem' }}>Não foi possível enviar. Tente novamente.</span>}
    </form>
  );
};

const PerguntaCard: React.FC<{ topicoSlug: string; pergunta: Pergunta }> = ({ topicoSlug, pergunta }) => {
  const [mostrarForm, setMostrarForm] = useState(false);
  const [respostasExtra, setRespostasExtra] = useState(0);

  return (
    <div className="glass-panel" style={{ padding: '1.5rem 2rem' }}>
      <p style={{ fontWeight: 700, marginBottom: '0.25rem' }}>{pergunta.pergunta}</p>
      <p style={{ margin: '0 0 1rem 0', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
        {pergunta.autor} · {formatarData(pergunta.data)}
      </p>

      {pergunta.respostas.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginBottom: '1rem', paddingLeft: '1rem', borderLeft: '2px solid var(--glass-border)' }}>
          {pergunta.respostas.map((r) => (
            <div key={r.id}>
              <p style={{ margin: 0 }}>{r.texto}</p>
              <p style={{ margin: 0, fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                {r.autor} · {formatarData(r.data)}
              </p>
            </div>
          ))}
        </div>
      )}

      {respostasExtra > 0 && (
        <p style={{ fontSize: '0.8rem', color: 'var(--accent-primary)', margin: '0 0 0.5rem 0' }}>
          Sua resposta foi enviada e vai aparecer aqui em alguns minutos.
        </p>
      )}

      {mostrarForm ? (
        <NovaRespostaForm topicoSlug={topicoSlug} perguntaId={pergunta.id} onEnviada={() => setRespostasExtra((n) => n + 1)} />
      ) : (
        <button onClick={() => setMostrarForm(true)} style={{ fontSize: '0.85rem', background: 'none', border: 'none', color: 'var(--accent-primary)', cursor: 'pointer', padding: 0 }}>
          Responder
        </button>
      )}
    </div>
  );
};

const ForumTopico: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const topico = topicos.find((t) => t.slug === slug);
  const [novasPerguntas, setNovasPerguntas] = useState(0);

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
  const perguntas = perguntasPorTopico[topico.slug] || [];

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
        <div style={{ marginBottom: '2rem' }}>
          <NovaPerguntaForm topicoSlug={topico.slug} onEnviada={() => setNovasPerguntas((n) => n + 1)} />
        </div>
      ) : (
        <div className="glass-panel" style={{ textAlign: 'center', padding: '2rem', marginBottom: '2rem' }}>
          <Construction size={32} color="var(--accent-primary)" style={{ marginBottom: '0.75rem' }} />
          <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
            O envio de novas perguntas está sendo configurado. Em breve será possível
            perguntar e responder diretamente aqui.
          </p>
        </div>
      )}

      {novasPerguntas > 0 && (
        <p style={{ fontSize: '0.85rem', color: 'var(--accent-primary)' }}>
          Sua pergunta foi enviada e vai aparecer nesta lista em alguns minutos.
        </p>
      )}

      {perguntas.length === 0 ? (
        <div className="glass-panel" style={{ textAlign: 'center', padding: '3rem 2rem' }}>
          <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
            Nenhuma pergunta publicada neste tópico ainda. Seja o primeiro a perguntar!
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {perguntas.map((p) => (
            <PerguntaCard key={p.id} topicoSlug={topico.slug} pergunta={p} />
          ))}
        </div>
      )}
    </div>
  );
};

export default ForumTopico;
