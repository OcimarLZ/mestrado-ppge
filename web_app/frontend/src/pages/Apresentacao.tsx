import React from 'react';
import SlideViewer from '../components/SlideViewer';
import slides from '../data/apresentacao';

const Apresentacao: React.FC = () => {
  return <SlideViewer slides={slides} />;
};

export default Apresentacao;
