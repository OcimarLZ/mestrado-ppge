import React from 'react';
import { LayoutDashboard, Construction, MousePointerClick, Filter, Eraser, Maximize2, Monitor } from 'lucide-react';

const PaineisInterativos: React.FC = () => {
  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1><LayoutDashboard size={28} style={{ marginRight: '0.5rem', verticalAlign: 'middle', color: 'var(--accent-primary)' }} />Painéis Interativos</h1>
      </div>

      <div className="glass-panel" style={{ padding: '1.5rem 2rem', marginBottom: '2rem' }}>
        <h3 style={{ marginBottom: '1rem' }}>Como usar os painéis abaixo</h3>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
          Os painéis a seguir são gráficos e tabelas interativos — ou seja, você pode
          clicar neles para filtrar, comparar e explorar os dados, sem precisar instalar
          nada ou saber programar. Veja abaixo o passo a passo básico para usá-los:
        </p>
        <div style={{ display: 'grid', gap: '1.5rem', gridTemplateColumns: 'minmax(260px, 1.3fr) minmax(220px, 1fr)' }}>
          <div>
            <p style={{ margin: 0, fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Filter size={18} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} />
              1. Filtrar
            </p>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', margin: '0.35rem 0 0' }}>
              Clique em um item das caixas de filtro (ex.: um ano, uma UF, uma modalidade)
              para deixar só aquilo selecionado no gráfico. Clique de novo no mesmo item
              para desmarcar e voltar a ver todos os dados. Em cada caixa de filtro, você
              pode escolher <strong>um ou vários itens</strong>, de acordo com o seu
              interesse: mantenha a tecla <strong>Ctrl</strong> pressionada e clique em
              cada item que quiser incluir — por exemplo, na caixa de UF, clique em "SC" e,
              com Ctrl ainda pressionado, clique também em "RS" e "PR" para ver os três
              estados juntos; o mesmo vale para a caixa de ano (ex.: 2014 e 2024, para
              comparar o início e o fim do período) ou para qualquer outra caixa de
              filtro. Essas escolhas em caixas diferentes também se combinam entre si: ao
              selecionar alguns estados e alguns anos ao mesmo tempo, o painel mostra só o
              que atende a todas as condições escolhidas.
            </p>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div>
              <p style={{ margin: 0, fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <MousePointerClick size={18} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} />
                2. Ver os números exatos
              </p>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', margin: '0.35rem 0 0' }}>
                Passe o mouse (sem clicar) sobre uma barra, linha ou ponto do gráfico para
                aparecer uma caixinha com o valor exato daquele dado.
              </p>
            </div>
            <div>
              <p style={{ margin: 0, fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Eraser size={18} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} />
                3. Limpar os filtros
              </p>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', margin: '0.35rem 0 0' }}>
                Para recomeçar, clique novamente nos itens já marcados até desmarcar
                todos, ou recarregue a página (F5) para o painel voltar ao estado inicial.
              </p>
            </div>
            <div>
              <p style={{ margin: 0, fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Maximize2 size={18} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} />
                4. Tela cheia
              </p>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', margin: '0.35rem 0 0' }}>
                No canto inferior direito de cada painel há um ícone de expandir — clique
                nele para ver o painel em tela cheia, mais fácil de ler.
              </p>
            </div>
          </div>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '1.25rem', marginBottom: 0, display: 'flex', alignItems: 'flex-start', gap: '0.5rem' }}>
          <Monitor size={16} style={{ color: 'var(--accent-primary)', flexShrink: 0, marginTop: '0.15rem' }} />
          Os painéis funcionam melhor em computador ou tablet, com uma tela maior — no
          celular, alguns filtros podem ficar pequenos. Os dados podem levar alguns
          segundos para carregar; aguarde o painel aparecer por completo antes de clicar.
        </p>
      </div>

      <div className="glass-panel" style={{ padding: '1.5rem 2rem', marginBottom: '2rem' }}>
        <h3 style={{ marginBottom: '0.5rem' }}>Painel de cursos e discentes (2005–2024)</h3>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
          Painel interativo (Power BI) com os microdados do Censo da Educação Superior do
          INEP no grão curso × instituição × ano, de 2005 a 2024. Reúne indicadores de
          discentes — matrículas, ingressantes, vagas, concluintes, trancamentos e
          desvinculações — filtráveis por dimensão territorial completa (região, UF,
          mesorregião, microrregião, município), tipo de curso (classificação CINE), grau
          acadêmico, modalidade de ensino, categoria administrativa e rede (pública ou
          privada).
        </p>
        <div style={{ position: 'relative', width: '100%', aspectRatio: '600 / 373.5', borderRadius: '8px', overflow: 'hidden' }}>
          <iframe
            title="Painel de cursos e discentes"
            src="https://app.powerbi.com/view?r=eyJrIjoiNmRkYTc1YTctNzk3NC00MzEyLTkwYmMtZWU2YTMzYTE5ZjFjIiwidCI6ImU3MzFkM2I4LTVhMmEtNDMxYy04NTM1LWQ4N2U5ZGYzNDNkNCJ9"
            frameBorder={0}
            allowFullScreen
            style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', border: 'none' }}
          />
        </div>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.75rem' }}>
          Fonte: Elaborado pelo autor a partir dos microdados do Censo da Educação Superior
          (INEP).
        </p>
      </div>

      <div className="glass-panel" style={{ padding: '1.5rem 2rem', marginBottom: '2rem' }}>
        <h3 style={{ marginBottom: '0.5rem' }}>Painel de instituições e docentes (2004–2024)</h3>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
          Painel interativo (Power BI) com os microdados do Censo da Educação Superior do
          INEP no grão instituição (IES) × ano, de 2004 a 2024 (sem dados do Censo 2009).
          Reúne indicadores sobre o corpo docente — total de docentes, docentes em
          exercício por sexo, titulação (doutores, mestres, especialistas, graduados, sem
          graduação), regime de trabalho (integral, integral com dedicação exclusiva,
          parcial, horista), com deficiência e estrangeiros — filtráveis por dimensão
          territorial, mantenedora, organização acadêmica, categoria administrativa e rede
          (pública ou privada).
        </p>
        <div style={{ position: 'relative', width: '100%', aspectRatio: '600 / 373.5', borderRadius: '8px', overflow: 'hidden' }}>
          <iframe
            title="Painel de instituições e docentes"
            src="https://app.powerbi.com/view?r=eyJrIjoiODQ3N2I5YjAtYmIyZS00YzcwLWExMmQtMDVjY2Q3MTRhMTE4IiwidCI6ImU3MzFkM2I4LTVhMmEtNDMxYy04NTM1LWQ4N2U5ZGYzNDNkNCJ9"
            frameBorder={0}
            allowFullScreen
            style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', border: 'none' }}
          />
        </div>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.75rem' }}>
          Fonte: Elaborado pelo autor a partir dos microdados do Censo da Educação Superior
          (INEP).
        </p>
      </div>

      <div className="glass-panel" style={{ padding: '1.5rem 2rem', marginBottom: '2rem' }}>
        <h3 style={{ marginBottom: '0.5rem' }}>Painel de instituições e cursos (2005–2024)</h3>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
          Painel interativo (Power BI) com os microdados do Censo da Educação Superior do
          INEP no grão curso-oferta × instituição × ano, de 2005 a 2024, com os mesmos
          filtros territoriais, de tipo de curso (classificação CINE), grau acadêmico,
          modalidade de ensino, categoria administrativa e rede do painel de cursos e
          discentes acima. Exibe uma matriz instituição (IES) × curso, com drill-down por
          "+/-" para abrir os cursos de cada IES; os valores mostrados usam o último ano
          selecionado no filtro (sem seleção, o ano mais recente disponível).
        </p>
        <div style={{ position: 'relative', width: '100%', aspectRatio: '600 / 373.5', borderRadius: '8px', overflow: 'hidden' }}>
          <iframe
            title="Painel de instituições e cursos"
            src="https://app.powerbi.com/view?r=eyJrIjoiZWZiYzY4ODUtMzk1OC00OTUxLWEzYTItZmVjNDExMWYwZjQ0IiwidCI6ImU3MzFkM2I4LTVhMmEtNDMxYy04NTM1LWQ4N2U5ZGYzNDNkNCJ9"
            frameBorder={0}
            allowFullScreen
            style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', border: 'none' }}
          />
        </div>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.75rem' }}>
          Fonte: Elaborado pelo autor a partir dos microdados do Censo da Educação Superior
          (INEP).
        </p>
      </div>

      <div className="glass-panel" style={{ padding: '1.5rem 2rem', marginBottom: '2rem' }}>
        <h3 style={{ marginBottom: '0.5rem' }}>Painel de matrículas e múltiplas métricas (2005–2024)</h3>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
          Painel interativo (Power BI) com os mesmos microdados do painel de cursos e
          discentes acima, voltado à comparação de várias métricas ao mesmo tempo:
          matrículas, ingressantes, vagas totais, concluintes, trancamentos e
          desvinculações. Um seletor de múltipla escolha permite marcar até 5 métricas
          simultaneamente, cada uma exibida como uma linha no gráfico de evolução anual
          (eixo X = ano do Censo). Além dos filtros territoriais, de grau acadêmico,
          modalidade de ensino, categoria administrativa e rede, inclui filtros por
          classificação CINE do curso (grande área, área detalhada e rótulo CINE).
        </p>
        <div style={{ position: 'relative', width: '100%', aspectRatio: '600 / 373.5', borderRadius: '8px', overflow: 'hidden' }}>
          <iframe
            title="Painel de matrículas e múltiplas métricas"
            src="https://app.powerbi.com/view?r=eyJrIjoiZWE2YjkyNDgtNTY4NS00MDBkLWExNmYtYTlhMmI0ZmFlZjRkIiwidCI6ImU3MzFkM2I4LTVhMmEtNDMxYy04NTM1LWQ4N2U5ZGYzNDNkNCJ9"
            frameBorder={0}
            allowFullScreen
            style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', border: 'none' }}
          />
        </div>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.75rem' }}>
          Fonte: Elaborado pelo autor a partir dos microdados do Censo da Educação Superior
          (INEP).
        </p>
      </div>

      <div className="glass-panel" style={{ padding: '1.5rem 2rem', marginBottom: '2rem' }}>
        <h3 style={{ marginBottom: '0.5rem' }}>Painel comparativo: modalidade, categoria e métricas (2005–2024)</h3>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
          Painel interativo (Power BI) com os mesmos microdados dos painéis acima,
          voltado à comparação simultânea de até 5 combinações de três seletores
          múltiplos: modalidade de ensino (presencial, curso a distância ou ambas),
          categoria administrativa (pública federal/estadual/municipal, privada com ou
          sem fins lucrativos, particular em sentido estrito, comunitária, confessional,
          especial, ou agrupamentos "todas"/"ambas") e métrica (matrículas,
          ingressantes, vagas totais, inscritos, concluintes, trancamentos e
          desvinculações). Cada combinação marcada vira uma linha no gráfico de evolução
          anual (eixo X = ano do Censo). Outros filtros disponíveis: período do PNE/ano,
          organização acadêmica, grau acadêmico, classificação CINE do curso (grande área
          e rótulo) e dimensão territorial completa (região, UF, mesorregião,
          microrregião, município).
        </p>
        <div style={{ position: 'relative', width: '100%', aspectRatio: '600 / 373.5', borderRadius: '8px', overflow: 'hidden' }}>
          <iframe
            title="Painel comparativo: modalidade, categoria e métricas"
            src="https://app.powerbi.com/view?r=eyJrIjoiNDA2MGY0ZDctZGQxYy00NzkyLTkwYjgtMzNlYzRmMDUwMmJhIiwidCI6ImU3MzFkM2I4LTVhMmEtNDMxYy04NTM1LWQ4N2U5ZGYzNDNkNCJ9"
            frameBorder={0}
            allowFullScreen
            style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', border: 'none' }}
          />
        </div>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.75rem' }}>
          Fonte: Elaborado pelo autor a partir dos microdados do Censo da Educação Superior
          (INEP).
        </p>
      </div>

      <div className="glass-panel" style={{ textAlign: 'center', padding: '2rem' }}>
        <Construction size={32} color="var(--accent-primary)" style={{ marginBottom: '0.75rem' }} />
        <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
          Mais painéis interativos serão adicionados aqui em breve.
        </p>
      </div>
    </div>
  );
};

export default PaineisInterativos;
