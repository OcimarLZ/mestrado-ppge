import React from 'react';
import type { ApendicePerfilRegistro } from '../lib/apendicePerfilData';

const Coluna: React.FC<{ ano: string; cursos: ApendicePerfilRegistro['cursos']['2014'] }> = ({ ano, cursos }) => (
  <div className="perfil-cursos-coluna glass-panel">
    <h3 className="data-chart-title">{ano} <span className="perfil-cursos-contagem">({cursos.length} {cursos.length === 1 ? 'curso' : 'cursos'})</span></h3>
    <ul className="perfil-cursos-lista">
      {cursos.map((c, i) => (
        <li key={`${c.curso}-${c.local}-${i}`}>
          <span className="perfil-curso-nome">{c.curso}</span>
          {c.local && <span className="perfil-curso-local">{c.local}</span>}
        </li>
      ))}
      {cursos.length === 0 && <li className="data-table-empty">Nenhum curso registrado.</li>}
    </ul>
  </div>
);

const CursosPerfilInstitucional: React.FC<{ registro: ApendicePerfilRegistro }> = ({ registro }) => (
  <div className="perfil-cursos-grid">
    <Coluna ano="2014" cursos={registro.cursos['2014']} />
    <Coluna ano="2024" cursos={registro.cursos['2024']} />
  </div>
);

export default CursosPerfilInstitucional;
