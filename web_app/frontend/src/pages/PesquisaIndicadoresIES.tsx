import React, { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { ListChecks } from 'lucide-react';
import FiltrosIndicadoresC from '../components/FiltrosIndicadoresC';
import IndicadoresIndicadoresC from '../components/IndicadoresIndicadoresC';
import DataTableIndicadoresC from '../components/DataTableIndicadoresC';
import { getApendiceCRegistros, getApendiceCFonte, getApendiceCGeradoEm, getApendiceCAno } from '../lib/apendiceCData';

const PesquisaIndicadoresIES: React.FC = () => {
  const registros = useMemo(() => getApendiceCRegistros(), []);
  const ano = useMemo(() => getApendiceCAno(), []);
  const [busca, setBusca] = useState('');
  const [uf, setUf] = useState('');

  const filtrados = useMemo(() => {
    const termo = busca.trim().toLowerCase();
    return registros.filter((r) => {
      if (uf && r.estado !== uf) return false;
      if (!termo) return true;
      return r.sigla.toLowerCase().includes(termo);
    });
  }, [registros, busca, uf]);

  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1><ListChecks size={28} style={{ marginRight: '0.5rem', verticalAlign: 'middle', color: 'var(--accent-primary)' }} />Indicadores por IES ({ano})</h1>
        <p className="lead" style={{ color: 'var(--text-secondary)' }}>
          Retrato completo das 69 universidades federais em {ano}: campus presenciais, polos e
          cursos de EaD própria e via UAB, matrículas e sua distribuição percentual entre
          presencial, EaD própria e UAB. Busque ou filtre por UF para atualizar os indicadores e
          a tabela.
        </p>
      </div>

      <FiltrosIndicadoresC
        registros={registros}
        totalFiltrado={filtrados.length}
        busca={busca}
        onBuscaChange={setBusca}
        uf={uf}
        onUfChange={setUf}
      />

      <IndicadoresIndicadoresC registros={filtrados} totalGeral={registros.length} />

      <DataTableIndicadoresC registros={filtrados} />

      <p style={{ marginTop: '1rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
        Fonte: {getApendiceCFonte()} — dados exportados em {getApendiceCGeradoEm()}.
      </p>

      <div style={{ marginTop: '1.5rem' }}>
        <Link to="/pesquisa" style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>&larr; Voltar para Pesquisa</Link>
      </div>
    </div>
  );
};

export default PesquisaIndicadoresIES;
