import React, { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { MapPinned } from 'lucide-react';
import FiltrosPolos from '../components/FiltrosPolos';
import IndicadoresPolos from '../components/IndicadoresPolos';
import GraficosPolos from '../components/GraficosPolos';
import DataTablePolos from '../components/DataTablePolos';
import { getLicPolosRegistros, getLicPolosAnos, getLicPolosFonte, getLicPolosGeradoEm, getLicPolosNotaMetodologica, type TipoPolo } from '../lib/licPolosData';
import type { AnoCenso } from '../lib/licIesData';

const PesquisaPolosIES: React.FC = () => {
  const registros = useMemo(() => getLicPolosRegistros(), []);
  const anos = useMemo(() => getLicPolosAnos(), []);
  const [ano, setAno] = useState<AnoCenso>(anos[anos.length - 1] ?? 2024);
  const [busca, setBusca] = useState('');
  const [uf, setUf] = useState('');
  const [tipo, setTipo] = useState<TipoPolo | ''>('');

  const registrosDoAno = useMemo(() => registros.filter((r) => r.ano_censo === ano), [registros, ano]);

  const filtrados = useMemo(() => {
    const termo = busca.trim().toLowerCase();
    return registrosDoAno.filter((r) => {
      if (uf && r.ies_uf !== uf) return false;
      if (tipo && r.tipo_polo !== tipo) return false;
      if (!termo) return true;
      return (
        r.ies_nome.toLowerCase().includes(termo) ||
        r.sigla.toLowerCase().includes(termo) ||
        r.municipio.toLowerCase().includes(termo)
      );
    });
  }, [registrosDoAno, busca, uf, tipo]);

  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1><MapPinned size={28} style={{ marginRight: '0.5rem', verticalAlign: 'middle', color: 'var(--accent-primary)' }} />Detalhamento por campus e polo</h1>
        <p className="lead" style={{ color: 'var(--text-secondary)' }}>
          Cada campus presencial e cada polo de EaD (próprio ou via UAB) das licenciaturas nas
          universidades federais, com o número de matrículas naquele local — 2014 e 2024.
        </p>
      </div>

      <FiltrosPolos
        registros={registrosDoAno}
        totalFiltrado={filtrados.length}
        busca={busca}
        onBuscaChange={setBusca}
        uf={uf}
        onUfChange={setUf}
        tipo={tipo}
        onTipoChange={setTipo}
        ano={ano}
        onAnoChange={setAno}
        anos={anos}
      />

      <IndicadoresPolos registros={filtrados} totalGeral={registrosDoAno.length} />

      <GraficosPolos registros={filtrados} />

      <DataTablePolos registros={filtrados} />

      <p style={{ marginTop: '1rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
        Fonte: {getLicPolosFonte()} — dados exportados em {getLicPolosGeradoEm()}.
        <br />
        {getLicPolosNotaMetodologica()}
      </p>

      <div style={{ marginTop: '1.5rem' }}>
        <Link to="/pesquisa/dados-ies" style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>&larr; Voltar para o panorama por IES</Link>
      </div>
    </div>
  );
};

export default PesquisaPolosIES;
