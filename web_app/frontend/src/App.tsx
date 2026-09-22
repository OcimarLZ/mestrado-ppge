import { lazy, Suspense } from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import GenericChapterPage from './pages/GenericChapterPage';
import Apresentacao from './pages/Apresentacao';
import Pesquisa from './pages/Pesquisa';
import PesquisaTema from './pages/PesquisaTema';
import PesquisaDadosIES from './pages/PesquisaDadosIES';
import PesquisaPolosIES from './pages/PesquisaPolosIES';

// O Admin (CRUD contra o FastAPI local) só existe em desenvolvimento: `import.meta.env.DEV`
// é substituído por uma constante em build-time, então o Vite remove este ramo (e o import
// dinâmico do Admin) inteiro do bundle de produção do GitHub Pages, que não tem backend.
const Admin = import.meta.env.DEV ? lazy(() => import('./pages/Admin')) : null;

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="apresentacao" element={<Apresentacao />} />
          <Route path="pesquisa" element={<Pesquisa />} />
          <Route path="pesquisa/dados-ies" element={<PesquisaDadosIES />} />
          <Route path="pesquisa/dados-ies/polos" element={<PesquisaPolosIES />} />
          <Route path="pesquisa/:slug" element={<PesquisaTema />} />
          <Route path="capitulo/:slug" element={<GenericChapterPage />} />
          {Admin && (
            <Route path="admin" element={<Suspense fallback={null}><Admin /></Suspense>} />
          )}
          <Route path="*" element={<div className="section-block text-center mt-4"><h2>Não encontrado</h2><p>Página não encontrada.</p></div>} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
