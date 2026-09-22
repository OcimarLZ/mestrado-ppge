import React from 'react';
import { Link } from 'react-router-dom';
import { Database } from 'lucide-react';
import DataTableLicIES from '../components/DataTableLicIES';
import { getLicIesFonte, getLicIesGeradoEm } from '../lib/licIesData';

const PesquisaDadosIES: React.FC = () => {
  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1><Database size={28} style={{ marginRight: '0.5rem', verticalAlign: 'middle', color: 'var(--accent-primary)' }} />Universidades federais e a licenciatura a distância</h1>
        <p className="lead" style={{ color: 'var(--text-secondary)' }}>
          Panorama, IES a IES, da oferta de licenciatura por modalidade (presencial, EaD própria
          e via UAB) e das matrículas do Censo da Educação Superior 2024. Clique nos títulos das
          colunas para ordenar, ou use a busca e o filtro de UF para localizar uma instituição.
        </p>
      </div>

      <DataTableLicIES />

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
