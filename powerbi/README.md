# Painel de cursos (Power BI)

Projeto Power BI no formato **PBIP** (arquivos de texto, versionáveis no git) para o
painel de cursos da educação superior, a partir de `bdados/INEP.db`.

## Como abrir

Dê duplo clique em **`painel_cursos.pbip`** — o Power BI Desktop abre com o modelo e os
relacionamentos já prontos (não precisa colar nada manualmente em "Get Data").

Pré-requisito: **File → Options and settings → Options → Global → Python scripting**
precisa apontar para um Python com `pandas` instalado (o `venv` da raiz do projeto
serve). Sem isso, o Power BI não consegue rodar as partições Python ao abrir/atualizar.

## Estrutura

- **`scripts/*.py`** — um script Python **por tabela** (fato + dimensões), cada um
  autocontido (abre sua própria conexão SQLite, lê, fecha). São a fonte de verdade: tanto
  rodam isolados (para testar/depurar) quanto são a entrada do `build_pbip.py`.
- **`build_pbip.py`** — lê cada arquivo de `scripts/`, roda para descobrir os tipos reais
  de cada coluna, e gera os arquivos `.tmdl` em `painel_cursos.SemanticModel/` (uma
  partição M com `Python.Execute` por tabela, embutindo o conteúdo literal do script).
- **`painel_cursos.SemanticModel/`**, **`painel_cursos.Report/`**, **`painel_cursos.pbip`**
  — o projeto gerado. Não edite esses arquivos à mão; eles são recriados a cada
  `python build_pbip.py`.

## Por que um script por tabela (não um único arquivo com as 12 variáveis)

O conector Python do Power BI reavalia a árvore de dependências do script **uma vez para
cada tabela carregada**. Com um único script monolítico definindo as 12 tabelas, carregar
todas elas relia/reprocessava a tabela fato (~3,9 milhões de linhas) 12 vezes, esgotando a
memória disponível mesmo para as dimensões pequenas (`ArrayMemoryError`, às vezes com
"referência cíclica"). Separar em scripts independentes, cada um com sua própria conexão
SQLite, evita esse reprocessamento — é por isso que o `build_pbip.py` gera uma partição M
isolada por tabela, cada uma rodando só o script daquela tabela.

## Modelo (relacionamentos)

Estrela pura: cada dimensão liga direto na fato, nunca em outra dimensão (ver nota em
`scripts/dim_ies.py` sobre por que essa dimensão não referencia `dim_territorio`).
`dim_versao` não se relaciona com nada — é só uma tabela de 1 linha para consulta manual
de quando os dados foram extraídos.

## Atualizar os dados

Depois de alterar algo em `bdados/INEP.db`: no Power BI, **Home → Refresh** (ele roda os
scripts de novo e relê o banco). Se você mudou o **código SQL/lógica** de algum script em
`scripts/`, regenere o projeto primeiro:

```bash
python powerbi/build_pbip.py
```

e então reabra/recarregue `painel_cursos.pbip` no Power BI Desktop.

**Atenção**: `bdados/INEP.db` é um arquivo local (2,8 GB, não versionado no git). Um
refresh agendado no serviço Power BI (não no Desktop) exigiria um Gateway de Dados
instalado nesta máquina, apontando para esse arquivo.

## Painel de IES (`painel_ies.pbip`)

Segundo painel, com fato **`fato_ies_censo`** (IES × ano, docentes) a partir de
`superior_ies_censo`. Scripts em **`scripts_ies/`**, gerado por **`build_pbip_ies.py`**
(`python powerbi/build_pbip_ies.py`). Dimensões: ano, território, IES, mantenedora, rede,
categoria administrativa, organização acadêmica e `dim_metricas` (slicer de métrica de
docentes). Não há dimensões de curso, CINE, grau nem modalidade. Limites dos dados: sem
Censo 2009; 2005 vem em 2 linhas por IES com valores .5 (somam o total); `ies = 0` =
instituições não identificadas.

## Painel de IES e cursos (`painel_ies_cursos.pbip`)

Fato `fato_curso_censo` (a mesma do painel de cursos), scripts em **`scripts_ies_cursos/`**,
gerado por **`build_pbip_ies_cursos.py`**. Mesmos filtros do painel de cursos e uma única
**matriz** (IES → curso, com +/- para o drill-down). Os valores usam o **último ano
selecionado** no filtro de ano (sem seleção, o mais recente).

## Painel de matrículas e múltiplas métricas (`painel_matriculas.pbip`)

Mesmo modelo conceitual do painel de cursos (mesma fato `fato_curso_censo`, tabelas e
relacionamentos — reaproveitados diretamente das `.tmdl`/visuais de `painel_cursos`),
gerado por **`build_pbip_matriculas.py`** (não tem pasta `scripts_*` própria). Três
diferenças: a) sem o gráfico de quantidade de cursos; b) o gráfico de linhas por
`ano_censo` usa um **parâmetro de campos** (field parameter) com seleção múltipla das 6
métricas (matrículas, ingressantes, vagas totais, concluintes, trancadas, desligados) —
cada métrica marcada (até 5) vira uma linha no eixo Y, substituindo o slicer de métrica
única `dim_metricas`; c) filtros novos por descrição vindos de `dim_cine`: grande área
(área geral CINE), área detalhada e rótulo CINE.

## Painel comparativo (`painel_comparativo.pbip`)

Mesmo modelo conceitual, gerado por **`build_pbip_comparativo.py`** a partir do
`painel_matriculas` como está no disco (não altera esse projeto). Remove os filtros de
modalidade, categoria administrativa, área detalhada e rede; reorganiza o restante
(período PNE/ano, organização acadêmica, grau acadêmico, grande área CINE, rótulo CINE,
território). No lugar entram **três slicers múltiplos** sobre uma tabela calculada
`dim_comparacao` (produto cartesiano de modalidade × categoria × métrica): Modalidade
(Presencial, Curso a distância, Ambas), Categoria (pública federal/estadual/municipal,
privada com/sem fins lucrativos, particular em sentido estrito, comunitária,
confessional, especial, mais os agrupamentos "(todas)"/"Ambas") e Métrica (as mesmas 6 do
`painel_matriculas` mais `qt_inscrito_total`). Cada combinação marcada nos três slicers
vira uma linha no gráfico por `ano_censo`, até `MAX_LINHAS = 5`; acima disso, o título do
gráfico avisa e mostra só as 5 primeiras pela ordem dos grupos. Os rótulos de modalidade/
categoria são conferidos contra `superior_tp_modal_ensino`/`superior_tp_categoria_administrativa`/
`superior_tp_rede` antes de gerar o projeto (`conferir_nomes_no_banco()`).
