# Organização por Categorias - Sistema de Relatórios INEP

## ✅ Nova Organização Implementada

O sistema agora está organizado por **categorias** para separar os trabalhos da **Ana** e do **Ocimar**.

## 📁 Estrutura das Categorias

### 🎓 **Trabalho do Ocimar - UNOESC**
**Localização**: `relats/unoesc/`
**Foco**: Relatórios sobre licenciaturas e análise educacional

**Relatórios incluídos**:
- Matrículas em Licenciaturas por Rede
- Ingressos em Licenciaturas por Rede e Modalidade
- Inscritos em Licenciaturas por Rede e Modalidade
- Concluintes em Licenciaturas por Rede e Modalidade
- Evadidos em Licenciaturas por Rede e Modalidade
- Trancadas em Licenciaturas por Rede e Modalidade
- Relação Concluintes/Trancados/Evadidos por Ingressante
- Gráfico Licenciaturas por Categoria
- Gráfico Cursos por Tipo de Rede e Modalidade
- Top 5 Cursos de Licenciatura
- Top 5 Cursos de Licenciatura - Dados Detalhados

### 📊 **Trabalho da Ana - Análise Geral**
**Localização**: `relats/`
**Foco**: Relatórios gerais sobre IES, discentes e cursos

**Relatórios incluídos**:
- Tabela de IES
- Discentes Geral
- Cursos por Área
- Docentes Geral
- Evolução de Vagas e Ingressos por Ano

## 🔧 Modificações Realizadas

### 1. **Estrutura de Dados**
- Substituído `RELATORIOS` por `CATEGORIAS`
- Cada categoria contém seus próprios relatórios
- Adicionado campo `pasta` para indicar localização do arquivo

### 2. **Rotas Atualizadas**
- `/executar/<categoria_id>/<relatorio_id>` - Executa relatório específico
- `/status/<categoria_id>/<relatorio_id>` - Status do relatório
- `/limpar_status/<categoria_id>/<relatorio_id>` - Limpa status

### 3. **Interface Reorganizada**
- Menu organizado por categorias com cabeçalhos coloridos
- Cada categoria em um card separado
- Relatórios agrupados dentro de cada categoria

### 4. **Execução de Relatórios**
- Suporte para relatórios em diferentes pastas
- Wrapper script adaptado para diferentes localizações
- Status tracking com IDs únicos por categoria

## 🚀 Como Usar

### 1. **Acessar o Sistema**
```
http://172.20.3.68:5000
```

### 2. **Navegar pelas Categorias**
- **Trabalho do Ocimar**: Relatórios sobre licenciaturas UNOESC
- **Trabalho da Ana**: Relatórios gerais de análise

### 3. **Executar Relatórios**
- Clique em "Executar" em qualquer relatório
- O sistema identifica automaticamente a pasta correta
- Status é rastreado individualmente

### 4. **Visualizar Resultados**
- Clique em "Visualizar Resultados" no menu superior
- Tabelas HTML e gráficos PNG organizados por categoria

## 📋 Adicionar Novos Relatórios

### Para adicionar um relatório à categoria do Ocimar:
```python
'novo_relatorio': {
    'nome': 'Nome do Relatório',
    'descricao': 'Descrição do relatório',
    'arquivo': 'novo_relatorio.py',
    'pasta': 'unoesc'
}
```

### Para adicionar um relatório à categoria da Ana:
```python
'novo_relatorio': {
    'nome': 'Nome do Relatório',
    'descricao': 'Descrição do relatório',
    'arquivo': 'novo_relatorio.py',
    'pasta': 'relats'
}
```

## 🎯 Benefícios da Nova Organização

✅ **Separação clara** entre trabalhos da Ana e do Ocimar
✅ **Interface organizada** com categorias visuais
✅ **Fácil manutenção** e adição de novos relatórios
✅ **Execução flexível** para diferentes localizações de arquivos
✅ **Status tracking** individual por relatório
✅ **Navegação intuitiva** por categoria

## 📁 Arquivos Modificados

- `app.py` - Nova estrutura de categorias e rotas
- `templates/index.html` - Interface reorganizada
- `CATEGORIAS` - Configuração centralizada dos relatórios

A organização por categorias torna o sistema mais profissional e fácil de usar! 