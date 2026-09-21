import React, { useState, useRef, useEffect } from 'react';
import * as LucideIcons from 'lucide-react';

interface IconPickerProps {
  value: string;
  onChange: (name: string) => void;
}

const ICONS = [
  'BookOpen', 'Book', 'BookMarked', 'BookText', 'Library',
  'GraduationCap', 'School', 'University', 'Backpack',
  'FileText', 'FileSpreadsheet', 'FileBarChart', 'FilePieChart',
  'BarChart3', 'BarChart4', 'LineChart', 'PieChart', 'ChartNoAxesCombined',
  'TrendingUp', 'TrendingDown', 'Activity', 'ArrowUpRight',
  'Users', 'UserPlus', 'UserCheck', 'UserRound', 'UserCog',
  'Globe', 'Earth', 'Map', 'MapPin',
  'Lightbulb', 'Brain', 'Search', 'ZoomIn',
  'AlertTriangle', 'AlertCircle', 'Info', 'CircleHelp',
  'CheckCircle', 'XCircle', 'Ban', 'Shield',
  'Home', 'LayoutDashboard', 'PanelLeft', 'Sidebar',
  'Settings', 'SlidersHorizontal', 'Wrench', 'Cog',
  'Menu', 'List', 'ListTree', 'Folders',
  'Plus', 'Minus', 'X', 'Check', 'Pencil', 'Trash2', 'Save',
  'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
  'ChevronUp', 'ChevronDown', 'ChevronLeft', 'ChevronRight',
  'Maximize2', 'Minimize2', 'Expand', 'Collapse',
  'Download', 'Upload', 'Printer', 'Share2',
  'Link', 'ExternalLink', 'Paperclip', 'Image',
  'Table', 'Grid3x3', 'Columns3', 'Rows3',
  'Sun', 'Moon', 'Palette', 'Paintbrush',
  'Play', 'Pause', 'Video', 'Camera',
  'MessageSquare', 'MessageCircle', 'Mail', 'Bell',
  'Calendar', 'Clock', 'Timer', 'Hourglass',
  'Tag', 'Flag', 'Star', 'Heart', 'Award',
  'Phone', 'Smartphone', 'Monitor', 'Laptop',
  'Wifi', 'Bluetooth', 'Database', 'Cloud',
  'Lock', 'Unlock', 'Key', 'Fingerprint',
  'Eye', 'EyeOff', 'Volume2', 'Speaker',
  'RefreshCw', 'RotateCw', 'Undo2', 'Redo2',
  'Copy', 'Clipboard', 'ClipboardList', 'Notebook',
  'ScrollText', 'Newspaper', 'BookOpenText',
  'Handshake', 'HeartHandshake', 'Goal',
  'Rocket', 'Target', 'Crosshair', 'Compass',
  'Inbox', 'Archive', 'FolderOpen', 'FolderTree',
].sort();

const IconPicker: React.FC<IconPickerProps> = ({ value, onChange }) => {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const filtered = search
    ? ICONS.filter(name => name.toLowerCase().includes(search.toLowerCase()))
    : ICONS;

  return (
    <div ref={ref} style={{ position: 'relative' }}>
      <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
        <div style={{
          display: 'flex', alignItems: 'center', gap: '0.5rem', flex: 1,
          padding: '0.75rem', borderRadius: '4px',
          border: '1px solid var(--border-color)',
          background: 'var(--bg-secondary)', color: 'var(--text-primary)',
          cursor: 'pointer',
        }} onClick={() => setOpen(!open)}>
          {value && (LucideIcons as any)[value] ? (
            React.createElement((LucideIcons as any)[value], { size: 20, style: { flexShrink: 0 } })
          ) : (
            <span style={{ width: 20, height: 20, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.8rem', opacity: 0.5 }}>+</span>
          )}
          <span style={{ flex: 1 }}>{value || 'Clique para escolher um ícone...'}</span>
        </div>
        <button
          type="button"
          onClick={() => setOpen(!open)}
          style={{
            padding: '0.5rem', borderRadius: '4px',
            border: '1px solid var(--border-color)',
            background: 'var(--bg-secondary)', color: 'var(--text-primary)',
            cursor: 'pointer', display: 'flex', alignItems: 'center',
          }}
        >
          {open ? '\u25B2' : '\u25BC'}
        </button>
      </div>

      {open && (
        <div
          style={{
            position: 'absolute', top: '100%', left: 0, right: 0, zIndex: 100,
            marginTop: '4px', borderRadius: '8px',
            border: '1px solid var(--border-color)',
            background: 'var(--bg-dark)', boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
            maxHeight: '320px', display: 'flex', flexDirection: 'column',
          }}
        >
          <div style={{ padding: '0.5rem', borderBottom: '1px solid var(--border-color)' }}>
            <input
              type="text"
              placeholder="Buscar ícone..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              autoFocus
              style={{
                width: '100%', padding: '0.5rem', borderRadius: '4px',
                border: '1px solid var(--border-color)',
                background: 'var(--bg-secondary)', color: 'var(--text-primary)',
                fontSize: '0.85rem',
              }}
            />
          </div>
          <div style={{ overflowY: 'auto', padding: '0.5rem', display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '4px' }}>
            {filtered.map(name => (
              <button
                key={name}
                type="button"
                title={name}
                onClick={() => { onChange(name); setOpen(false); setSearch(''); }}
                style={{
                  display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '2px',
                  padding: '0.5rem 0.25rem', borderRadius: '6px', cursor: 'pointer',
                  border: value === name ? '2px solid var(--accent-primary)' : '2px solid transparent',
                  background: value === name ? 'rgba(16,185,129,0.1)' : 'transparent',
                  color: 'var(--text-primary)', fontSize: '0.65rem',
                  transition: 'background 0.15s',
                }}
                onMouseOver={e => { e.currentTarget.style.background = 'rgba(255,255,255,0.05)'; }}
                onMouseOut={e => { e.currentTarget.style.background = value === name ? 'rgba(16,185,129,0.1)' : 'transparent'; }}
              >
                {(LucideIcons as any)[name] ? React.createElement((LucideIcons as any)[name], { size: 18 }) : <span style={{ fontSize: '1.1rem' }}>?</span>}
                <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: '100%', textAlign: 'center' }}>{name}</span>
              </button>
            ))}
            {filtered.length === 0 && (
              <div style={{ gridColumn: '1 / -1', padding: '1rem', textAlign: 'center', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                Nenhum ícone encontrado
              </div>
            )}
          </div>
          <div style={{ padding: '0.4rem 0.75rem', borderTop: '1px solid var(--border-color)', fontSize: '0.75rem', color: 'var(--text-secondary)', textAlign: 'center' }}>
            {filtered.length} de {ICONS.length} ícones
          </div>
        </div>
      )}
    </div>
  );
};

export default IconPicker;
