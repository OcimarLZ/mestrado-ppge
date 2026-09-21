# Estrutura Modular para Geração de Planilhas INEP

## 📁 Estrutura de Arquivos

```
relats/pesq/
├── __init__.py                 # Pacote Python
├── gerar_tabela_geral_1.py    # Script principal (refatorado)
├── executar_geracao.py         # Script de execução direta (RECOMENDADO)
├── sql_queries.py             # Todas as consultas SQL organizadas
├── data_processors.py         # Processamento de dados
├── excel_formatter.py         # Formatação Excel
├── exemplo_nova_consulta.py   # Exemplos de como adicionar novas consultas
├── teste_dados_docentes.py    # Script de teste para dados de docentes
└── README_MODULAR.md          # Esta documentação
```

## 🎯 Benefícios da Nova Estrutura

### ✅ **Organização**
- **Separação de responsabilidades**: Cada arquivo tem uma função específica
- **Manutenibilidade**: Fácil localizar e modificar consultas SQL
- **Reutilização**: Funções podem ser usadas em outros scripts

### ✅ **Escalabilidade**
- **Adição de novas consultas**: Processo simples e padronizado
- **Expansão de funcionalidades**: Estrutura preparada para crescimento
- **Modularidade**: Cada componente funciona independentemente

### ✅ **Clareza**
- **Código limpo**: Funções pequenas e focadas
- **Documentação**: Cada função tem docstring explicativa
- **Padrões consistentes**: Nomenclatura e estrutura padronizadas

## 🔧 Como Usar

### ⭐ **Execução Recomendada**
```bash
# Execute o script de execução direta (RECOMENDADO)
python relats/pesq/executar_geracao.py
```

### Execução Alternativa
```bash
# Execute o script principal (pode ter problemas de import)
python relats/pesq/gerar_tabela_geral_1.py
```

### Importação de Módulos
```python
# Para usar em outros scripts
from relats.pesq.sql_queries import get_sql_ies_global
from relats.pesq.data_processors import carregar_dados_por_ano
from relats.pesq.excel_formatter import aplicar_formatacao_planilha
```

## 📊 Módulos Detalhados

### 1. `sql_queries.py`
**Função**: Centraliza todas as consultas SQL

**Organização**:
- Consultas por categoria (IES, municípios, docentes, cursos, licenciaturas)
- Funções parametrizadas para reutilização
- Documentação clara de cada consulta

**Consultas Disponíveis**:
- **IES**: Global, por rede, por categoria administrativa
- **Municípios**: Com IES, com cursos, com cursos de licenciatura, com cursos de licenciatura por modalidade
- **Docentes**: Global, por titulação, filtrados, por categoria
- **Cursos**: Global, por rede, por categoria
- **Licenciaturas**: Global, por rede, por categoria

**Exemplo**:
```python
def get_sql_ies_global():
    """Consulta para dados globais de IES"""
    return """
    SELECT
        i.ano_censo AS ano,
        COUNT(DISTINCT i.ies) AS QtdeIes
    FROM
        ies_censo i
    WHERE
        i.ano_censo > 2004
    GROUP BY
        i.ano_censo
    ORDER BY
        i.ano_censo
    """
```

### 2. `data_processors.py`
**Função**: Processa dados e gera linhas da planilha

**Funcionalidades**:
- `carregar_dados_por_ano()`: Carrega dados simples
- `carregar_dados_agrupados()`: Carrega dados com agrupamento
- `criar_linha_dados()`: Formata linha para planilha
- Funções específicas por categoria de dados

**Exemplo**:
```python
def processar_dados_ies(todas_linhas, sub_categoria_global):
    """Processa dados de IES e adiciona às linhas da planilha"""
    dados_globais = carregar_dados_por_ano(get_sql_ies_global(), "QtdeIes")
    linha_global = criar_linha_dados("Nro de IES", "Nenhum", "Global", sub_categoria_global, dados_globais)
    todas_linhas.append({"dados": linha_global, "secao": "global"})
```

### 3. `excel_formatter.py`
**Função**: Gerencia formatação da planilha Excel

**Funcionalidades**:
- Cores e estilos padronizados
- Formatação de cabeçalho e linhas
- Ajuste automático de largura de colunas
- Relatório de formatação aplicada

**Exemplo**:
```python
def aplicar_formatacao_planilha(ws, todas_linhas, colunas):
    """Aplica formatação completa à planilha"""
    aplicar_formatacao_cabecalho(ws, colunas)
    aplicar_formatacao_linhas(ws, todas_linhas, colunas)
```

## ➕ Como Adicionar Novas Consultas

### Passo 1: Adicionar Consulta SQL
```python
# Em sql_queries.py
def get_sql_nova_consulta():
    """Consulta para novos dados"""
    return """
    SELECT
        c.ano_censo AS ano,
        COUNT(DISTINCT c.curso) AS QtdeCursos
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_grau_academico = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """
```

### Passo 2: Criar Função de Processamento
```python
# Em data_processors.py
def processar_novos_dados(todas_linhas, sub_categoria):
    """Processa novos dados e adiciona às linhas da planilha"""
    dados_novos = carregar_dados_por_ano(get_sql_nova_consulta(), "QtdeCursos")
    linha_nova = criar_linha_dados("Nro de Cursos", "Nenhum", "Bacharelados", sub_categoria, dados_novos)
    todas_linhas.append({"dados": linha_nova, "secao": "novos_dados"})
```

### Passo 3: Integrar no Processamento Principal
```python
# Em data_processors.py, função processar_todos_dados()
def processar_todos_dados():
    todas_linhas = []
    sub_categoria_global = "Global"
    
    # Processa cada categoria de dados
    processar_dados_ies(todas_linhas, sub_categoria_global)
    # ... outras funções ...
    
    # ADICIONE SUA NOVA FUNÇÃO:
    processar_novos_dados(todas_linhas, sub_categoria_global)
    
    return todas_linhas
```

### Passo 4: Adicionar Cores (Opcional)
```python
# Em excel_formatter.py, função get_cores_por_secao()
def get_cores_por_secao():
    cores = get_cores_formatacao()
    return {
        # ... cores existentes ...
        "novos_dados": cores["verde_claro"],  # Nova seção
    }
```

## 🚨 Solução de Problemas

### Erro de Import Relativo
Se você encontrar o erro:
```
ImportError: attempted relative import with no known parent package
```

**Solução**: Use o script `executar_geracao.py` em vez de `gerar_tabela_geral_1.py`:

```bash
# ✅ CORRETO - Use este script
python relats/pesq/executar_geracao.py

# ❌ EVITE - Este pode dar erro de import
python relats/pesq/gerar_tabela_geral_1.py
```

### Execução a partir do Diretório Raiz
Se estiver no diretório raiz do projeto:

```bash
# Execute a partir do diretório raiz
python relats/pesq/executar_geracao.py
```

## 📈 Vantagens para Expansão Futura

### 🔄 **Facilidade de Manutenção**
- Consultas SQL centralizadas e documentadas
- Funções pequenas e focadas
- Padrões consistentes

### 🚀 **Escalabilidade**
- Estrutura preparada para novas categorias de dados
- Processo padronizado para adição de consultas
- Reutilização de código

### 🎨 **Flexibilidade**
- Formatação personalizável por seção
- Fácil adição de novos tipos de dados
- Configuração centralizada de cores e estilos

### 📊 **Organização**
- Separação clara entre dados, processamento e formatação
- Código legível e bem documentado
- Estrutura modular e extensível

## 🎯 Próximos Passos

1. **Testar a nova estrutura** com os dados existentes
2. **Adicionar novas consultas** seguindo o padrão estabelecido
3. **Expandir funcionalidades** conforme necessário
4. **Documentar novas adições** para manter a organização

---

**✅ A nova estrutura modular torna o código mais organizado, manutenível e preparado para expansões futuras!**

**💡 Dica**: Use sempre `executar_geracao.py` para evitar problemas de import! 