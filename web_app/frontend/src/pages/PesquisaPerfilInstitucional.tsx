import React, { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { Building2 } from 'lucide-react';
import SeletorPerfilInstitucional from '../components/SeletorPerfilInstitucional';
import ResumoPerfilInstitucional from '../components/ResumoPerfilInstitucional';
import CursosPerfilInstitucional from '../components/CursosPerfilInstitucional';
import { getPerfisInstitucionais, getPerfilFonte, getPerfilGeradoEm } from '../lib/apendicePerfilData';

const PesquisaPerfilInstitucional: React.FC = () => {
  const registros = useMemo(() => getPerfisInstitucionais(), []);
  const [busca, setBusca] = useState('');
  const [selecionado, setSelecionado] = useState(registros[0]?.nome_ies ?? '');

  const registro = useMemo(
    () => registros.find((r) => r.nome_ies === selecionado) ?? registros[0],
    [registros, selecionado]
  );

  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1><Building2 size={28} style={{ marginRight: '0.5rem', verticalAlign: 'middle', color: 'var(--accent-primary)' }} />Perfil institucional: 2014 → 2024</h1>
        <p className="lead" style={{ color: 'var(--text-secondary)' }}>
          Escolha uma universidade federal para ver como sua oferta de licenciatura mudou entre
          2014 e 2024: matrículas, cursos, campus e polos, e a relação completa de cursos e
          locais de oferta em cada ano.
        </p>
      </div>

      <SeletorPerfilInstitucional
        registros={registros}
        busca={busca}
        onBuscaChange={setBusca}
        selecionado={registro?.nome_ies ?? ''}
        onSelecionadoChange={setSelecionado}
      />

      {registro && (
        <>
          <ResumoPerfilInstitucional registro={registro} />
          <CursosPerfilInstitucional registro={registro} />
        </>
      )}

      <p style={{ marginTop: '1rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
        Fonte: {getPerfilFonte()} — dados exportados em {getPerfilGeradoEm()}.
      </p>

      <div style={{ marginTop: '1.5rem' }}>
        <Link to="/pesquisa" style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>&larr; Voltar para Pesquisa</Link>
      </div>
    </div>
  );
};

export default PesquisaPerfilInstitucional;
