import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Plus, Trash2, Edit, Save, X } from 'lucide-react';

interface Visual {
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
}

interface VisualManagerProps {
  sectionId: number;
}

const emptyForm = () => ({
  type: 'chart',
  title: '',
  source: '',
  order: 0,
  image_url: '',
  sql_query: '',
  chart_type: 'bar',
  x_axis: '',
  y_axis: '',
  show_labels: 0,
  legend_position: 'bottom',
  table_html: '',
  pdf_page: '',
});

const VisualManager: React.FC<VisualManagerProps> = ({ sectionId }) => {
  const [visuals, setVisuals] = useState<Visual[]>([]);
  const [editing, setEditing] = useState<Visual | null>(null);
  const [form, setForm] = useState<any>(emptyForm());
  const [showForm, setShowForm] = useState(false);

  const fetchVisuals = () => {
    axios.get(`http://127.0.0.1:8000/api/sections/${sectionId}/visuals`)
      .then(res => setVisuals(res.data))
      .catch(() => {});
  };

  useEffect(() => { fetchVisuals(); }, [sectionId]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const val = e.target.name === 'show_labels' ? (e.target.value === '1' ? 1 : 0) : e.target.value;
    setForm({ ...form, [e.target.name]: val });
  };

  const save = async () => {
    const payload = {
      ...form,
      page_content_id: sectionId,
      order: parseInt(form.order) || 0,
      pdf_page: form.pdf_page ? parseInt(form.pdf_page) : null,
    };
    try {
      if (editing) {
        await axios.put(`http://127.0.0.1:8000/api/visuals/${editing.id}`, payload);
      } else {
        await axios.post(`http://127.0.0.1:8000/api/sections/${sectionId}/visuals`, payload);
      }
      setShowForm(false);
      setEditing(null);
      setForm(emptyForm());
      fetchVisuals();
    } catch (err) {
      alert('Erro ao salvar elemento visual');
    }
  };

  const del = async (id: number) => {
    if (window.confirm('Excluir este elemento visual?')) {
      await axios.delete(`http://127.0.0.1:8000/api/visuals/${id}`);
      fetchVisuals();
    }
  };

  const edit = (v: Visual) => {
    setEditing(v);
    setForm({
      type: v.type,
      title: v.title,
      source: v.source,
      order: v.order,
      image_url: v.image_url || '',
      sql_query: v.sql_query || '',
      chart_type: v.chart_type || 'bar',
      x_axis: v.x_axis || '',
      y_axis: v.y_axis || '',
      show_labels: v.show_labels,
      legend_position: v.legend_position || 'bottom',
      table_html: v.table_html || '',
      pdf_page: v.pdf_page ? String(v.pdf_page) : '',
    });
    setShowForm(true);
  };

  return (
    <div style={{ marginTop: '2rem', borderTop: '1px solid var(--border-color)', paddingTop: '1.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h4 style={{ margin: 0 }}>Elementos Visuais da Seção</h4>
        <button className="btn" style={{ padding: '0.4rem 0.75rem', fontSize: '0.85rem', background: 'var(--accent-secondary)', color: '#fff' }} onClick={() => { setEditing(null); setForm(emptyForm()); setShowForm(true); }}>
          <Plus size={16} /> Novo
        </button>
      </div>

      <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
        Use <code style={{ background: 'var(--bg-card)', padding: '0.1rem 0.3rem', borderRadius: '3px' }}>[v:ID]</code> no texto da seção para inserir o elemento visual.
        O ID de cada elemento é exibido na listagem abaixo.
      </p>

      {showForm && (
        <div className="glass-panel" style={{ padding: '1.25rem', marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <strong>{editing ? 'Editar' : 'Novo'} Elemento Visual</strong>
            <button className="btn" style={{ padding: '0.3rem 0.5rem', fontSize: '0.8rem', background: 'transparent', color: 'var(--text-primary)' }} onClick={() => { setShowForm(false); setEditing(null); }}><X size={16} /></button>
          </div>
          <div className="grid-2" style={{ gap: '0.75rem' }}>
            <div>
              <label style={{ fontSize: '0.85rem', display: 'block', marginBottom: '0.25rem' }}>Tipo</label>
              <select name="type" value={form.type} onChange={handleChange} style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontSize: '0.85rem' }}>
                <option value="chart">Gráfico</option>
                <option value="table">Tabela</option>
                <option value="image">Imagem</option>
              </select>
            </div>
            <div>
              <label style={{ fontSize: '0.85rem', display: 'block', marginBottom: '0.25rem' }}>Ordem</label>
              <input type="number" name="order" value={form.order} onChange={handleChange} style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontSize: '0.85rem' }} />
            </div>
            <div style={{ gridColumn: 'span 2' }}>
              <label style={{ fontSize: '0.85rem', display: 'block', marginBottom: '0.25rem' }}>Título/Legenda</label>
              <input type="text" name="title" value={form.title} onChange={handleChange} style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontSize: '0.85rem' }} />
            </div>
            <div style={{ gridColumn: 'span 2' }}>
              <label style={{ fontSize: '0.85rem', display: 'block', marginBottom: '0.25rem' }}>Fonte</label>
              <input type="text" name="source" value={form.source} onChange={handleChange} style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontSize: '0.85rem' }} />
            </div>
            <div>
              <label style={{ fontSize: '0.85rem', display: 'block', marginBottom: '0.25rem' }}>Página na dissertação (PDF)</label>
              <input type="number" name="pdf_page" value={form.pdf_page} onChange={handleChange} placeholder="ex: 173" style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontSize: '0.85rem' }} />
            </div>

            {form.type === 'image' && (
              <div style={{ gridColumn: 'span 2' }}>
                <label style={{ fontSize: '0.85rem', display: 'block', marginBottom: '0.25rem' }}>URL da Imagem</label>
                <input type="text" name="image_url" value={form.image_url} onChange={handleChange} style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontSize: '0.85rem' }} placeholder="http://127.0.0.1:8000/static/imagem.png" />
              </div>
            )}

            {form.type === 'table' && (
              <div style={{ gridColumn: 'span 2' }}>
                <label style={{ fontSize: '0.85rem', display: 'block', marginBottom: '0.25rem' }}>HTML da Tabela (ou use SQL abaixo)</label>
                <textarea name="table_html" value={form.table_html} onChange={handleChange} rows={4} style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontSize: '0.85rem', fontFamily: 'monospace', resize: 'vertical' }} placeholder="<table>...</table>" />
              </div>
            )}

            {(form.type === 'chart' || form.type === 'table') && (
              <>
                <div style={{ gridColumn: 'span 2' }}>
                  <label style={{ fontSize: '0.85rem', display: 'block', marginBottom: '0.25rem' }}>Consulta SQL (deixe em branco se usar HTML fixo)</label>
                  <textarea name="sql_query" value={form.sql_query} onChange={handleChange} rows={3} style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: '#1e1e1e', color: '#d4d4d4', fontSize: '0.85rem', fontFamily: 'monospace', resize: 'vertical' }} />
                </div>
                {form.type === 'chart' && (
                  <>
                    <div>
                      <label style={{ fontSize: '0.85rem', display: 'block', marginBottom: '0.25rem' }}>Tipo de Gráfico</label>
                      <select name="chart_type" value={form.chart_type} onChange={handleChange} style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontSize: '0.85rem' }}>
                        <option value="bar">Barras</option>
                        <option value="line">Linhas</option>
                        <option value="pie">Pizza</option>
                      </select>
                    </div>
                    <div>
                      <label style={{ fontSize: '0.85rem', display: 'block', marginBottom: '0.25rem' }}>Eixo X</label>
                      <input type="text" name="x_axis" value={form.x_axis} onChange={handleChange} style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontSize: '0.85rem' }} />
                    </div>
                    <div>
                      <label style={{ fontSize: '0.85rem', display: 'block', marginBottom: '0.25rem' }}>Eixo Y</label>
                      <input type="text" name="y_axis" value={form.y_axis} onChange={handleChange} style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontSize: '0.85rem' }} />
                    </div>
                    <div>
                      <label style={{ fontSize: '0.85rem', display: 'block', marginBottom: '0.25rem' }}>Legenda</label>
                      <select name="legend_position" value={form.legend_position} onChange={handleChange} style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontSize: '0.85rem' }}>
                        <option value="bottom">Rodapé</option>
                        <option value="top">Topo</option>
                        <option value="left">Esquerda</option>
                        <option value="right">Direita</option>
                        <option value="none">Ocultar</option>
                      </select>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', paddingTop: '1.25rem' }}>
                      <input type="checkbox" name="show_labels" checked={form.show_labels === 1} onChange={(e) => setForm({ ...form, show_labels: e.target.checked ? 1 : 0 })} />
                      <label style={{ fontSize: '0.85rem' }}>Exibir rótulos</label>
                    </div>
                  </>
                )}
              </>
            )}
          </div>
          <button className="btn btn-primary" onClick={save} style={{ marginTop: '1rem', padding: '0.5rem 1.5rem', fontSize: '0.85rem' }}>
            <Save size={16} /> Salvar Elemento Visual
          </button>
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {visuals.map(v => (
          <div key={v.id} className="glass-panel" style={{ padding: '0.75rem 1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', fontSize: '0.85rem' }}>
              <code style={{ background: 'var(--accent-primary)', color: '#fff', padding: '0.15rem 0.5rem', borderRadius: '4px', fontWeight: 700 }}>[v:{v.id}]</code>
              <span style={{ textTransform: 'uppercase', fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600 }}>{v.type}</span>
              <span>{v.title || '(sem título)'}</span>
            </div>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button className="btn" style={{ padding: '0.3rem 0.5rem', fontSize: '0.75rem', background: 'transparent', color: 'var(--text-primary)' }} onClick={() => edit(v)}><Edit size={14} /></button>
              <button className="btn" style={{ padding: '0.3rem 0.5rem', fontSize: '0.75rem', background: 'transparent', color: '#ef4444' }} onClick={() => del(v.id)}><Trash2 size={14} /></button>
            </div>
          </div>
        ))}
        {visuals.length === 0 && !showForm && (
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', textAlign: 'center', padding: '1rem' }}>
            Nenhum elemento visual cadastrado. Clique em "Novo" para adicionar.
          </p>
        )}
      </div>
    </div>
  );
};

export default VisualManager;
