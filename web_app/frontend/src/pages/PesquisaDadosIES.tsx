import React, { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { Database, MapPinned, ArrowRight } from 'lucide-react';
import FiltrosLicIES from '../components/FiltrosLicIES';
import IndicadoresLicIES from '../components/IndicadoresLicIES';
import GraficosLicIES from '../components/GraficosLicIES';
import DataTableLicIES from '../components/DataTableLicIES';
import { getLicIesRegistros, getLicIesAnos, getLicIesFonte, getLicIesGeradoEm, type AnoCenso } from '../lib/licIesData';

const PesquisaDadosIES: React.FC = () => {
  const registros = useMemo(() => getLicIesRegistros(), []);
  const anos = useMemo(() => getLicIesAnos(), []);
  const [ano, setAno] = useState<AnoCenso>(anos[anos.length - 1] ?? 2024);
  const [busca, setBusca] = useState('');
  const [uf, setUf] = useState('');

  const registrosDoAno = useMemo(() => registros.filter((r) => r.ano_censo === ano), [registros, ano]);

  const filtrados = useMemo(() => {
    const termo = busca.trim().toLowerCase();
    return registrosDoAno.filter((r) => {
      if (uf && r.estado !== uf) return false;
      if (!termo) return true;
      return r.ies_nome.toLowerCase().includes(termo) || r.sigla.toLowerCase().includes(termo);
    });
  }, [registrosDoAno, busca, uf]);

  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1><Database size={28} style={{ marginRight: '0.5rem', verticalAlign: 'middle', color: 'var(--accent-primary)' }} />Universidades federais e a licenciatura a distância</h1>
        <p className="lead" style={{ color: 'var(--text-secondary)' }}>
          Panorama, IES a IES, da oferta de licenciatura por modalidade (presencial, EaD própria
          e via UAB) e das matrículas do Censo da Educação Superior, comparando 2014 e 2024.
          Escolha o ano e busque ou filtre por UF para atualizar os indicadores, os gráficos e a
          tabela ao mesmo tempo.
        </p>
      </div>

      <FiltrosLicIES
        registros={registrosDoAno}
        totalFiltrado={filtrados.length}
        busca={busca}
        onBuscaChange={setBusca}
        uf={uf}
        onUfChange={setUf}
        ano={ano}
        onAnoChange={setAno}
        anos={anos}
      />

      <IndicadoresLicIES registros={filtrados} totalGeral={registrosDoAno.length} />

      <GraficosLicIES registros={filtrados} />

      <DataTableLicIES registros={filtrados} />

      <Link to="/pesquisa/dados-ies/polos" className="glass-panel data-crosslink">
        <MapPinned size={20} color="var(--accent-primary)" />
        <span>
          <strong>Quer ver campus a campus, polo a polo?</strong>
          <br />
          Detalhamento com matrículas por município — presencial, EaD próprio e UAB.
        </span>
        <ArrowRight size={18} />
      </Link>

      <p style={{ marginTop: '1rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
        Fonte: {getLicIesFonte()} — dados exportados em {getLicIesGeradoEm()}.
      </p>

      <div style={{ marginTop: '1.5rem' }}>
        <Link to="/pesquisa" style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>&larr; Voltar para Pesquisa</Link>
      </div>
    </div>
  );
};

export default PesquisaDadosIES;
