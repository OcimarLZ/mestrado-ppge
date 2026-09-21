# 📊 Estrutura PACs - Geração de Planilhas Excel

## 🎯 **Visão Geral**

Esta estrutura foi criada para gerar planilhas Excel com dados PACs do INEP, seguindo as especificações:

- **Período**: 2014-2024
- **Município**: 4204202
- **Filtros**: Aplicados conforme especificação

## 📁 **Estrutura de Arquivos**

```
relats/pesq/
├── pacs_sql_queries.py          # Consultas SQL para dados PACs
├── pacs_data_processors.py      # Processamento de dados PACs
├── pacs_excel_formatter.py      # Formatação Excel PACs
├── executar_geracao_pacs.py     # Script principal de execução
└── README_PACS.md              # Esta documentação
```

## 🔧 **Configurações Específicas**

### **Período de Dados**
- **Ano inicial**: 2014
- **Ano final**: 2024
- **Colunas**: 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024

### **Filtros Aplicados**
- **Município**: `municipio = '4204202'`
- **Período**: `ano_censo >= 2014 AND ano_censo <= 2024`
- **Licenciaturas**: `tp_grau_academico = 3` (quando aplicável)

## 📊 **Dados Processados**

### **1. Dados de IES**
- **Global**: Total de IES por ano
- **Por Rede**: IES agrupadas por tipo de rede
- **Por Categoria**: IES agrupadas por categoria administrativa
- **Campus**: IES presenciais (modalidade presencial)
- **Polo**: IES a distância (modalidade a distância)

### **2. Dados de Docentes**
- **Total**: Docentes totais por ano
- **Por Titulação**: Doutores, Mestres, Especialistas, Graduados
- **Filtrados**: Apenas categorias 1,2,3,5,7,8,9
- **Por Categoria**: Docentes agrupados por categoria administrativa

### **3. Dados de Cursos**
- **Global**: Total de cursos por ano
- **Por Rede**: Cursos agrupados por tipo de rede
- **Por Categoria**: Cursos agrupados por categoria administrativa

### **4. Dados de Licenciaturas**
- **Global**: Total de licenciaturas por ano
- **Por Rede**: Licenciaturas agrupadas por tipo de rede
- **Por Categoria**: Licenciaturas agrupadas por categoria administrativa

### **5. Dados de Vagas**
- **Total**: Vagas totais por ano
- **Por Modalidade**: Vagas agrupadas por modalidade
- **Licenciaturas por Modalidade**: Vagas de licenciaturas por modalidade
- **Licenciaturas por Categoria e Modalidade**: Vagas de licenciaturas por categoria e modalidade

### **6. Dados de Inscritos**
- **Total**: Inscritos totais por ano
- **Por Modalidade**: Inscritos agrupados por modalidade
- **Licenciaturas por Modalidade**: Inscritos de licenciaturas por modalidade
- **Licenciaturas por Categoria e Modalidade**: Inscritos de licenciaturas por categoria e modalidade

### **7. Dados de Ingressos**
- **Total**: Ingressos totais por ano
- **Por Modalidade**: Ingressos agrupados por modalidade
- **Licenciaturas por Modalidade**: Ingressos de licenciaturas por modalidade
- **Licenciaturas por Categoria e Modalidade**: Ingressos de licenciaturas por categoria e modalidade

### **8. Dados de Matrículas**
- **Total**: Matrículas totais por ano
- **Por Modalidade**: Matrículas agrupadas por modalidade
- **Licenciaturas por Modalidade**: Matrículas de licenciaturas por modalidade
- **Licenciaturas por Categoria e Modalidade**: Matrículas de licenciaturas por categoria e modalidade

### **9. Dados de Concluintes**
- **Total**: Concluintes totais por ano
- **Por Modalidade**: Concluintes agrupados por modalidade
- **Licenciaturas por Modalidade**: Concluintes de licenciaturas por modalidade
- **Licenciaturas por Categoria e Modalidade**: Concluintes de licenciaturas por categoria e modalidade

### **10. Dados de Matrículas Trancadas**
- **Total**: Matrículas trancadas totais por ano
- **Por Modalidade**: Matrículas trancadas agrupadas por modalidade
- **Licenciaturas por Modalidade**: Matrículas trancadas de licenciaturas por modalidade
- **Licenciaturas por Categoria e Modalidade**: Matrículas trancadas de licenciaturas por categoria e modalidade

### **11. Dados de Evadidos**
- **Total**: Evadidos totais por ano
- **Por Modalidade**: Evadidos agrupados por modalidade
- **Licenciaturas por Modalidade**: Evadidos de licenciaturas por modalidade
- **Licenciaturas por Categoria e Modalidade**: Evadidos de licenciaturas por categoria e modalidade

### **13. Dados de Turno (Licenciaturas Presenciais)**
- **Ingressos Diurnos**: Ingressos diurnos de licenciaturas presenciais
- **Ingressos Noturnos**: Ingressos noturnos de licenciaturas presenciais
- **Matrículas Diurnas**: Matrículas diurnas de licenciaturas presenciais
- **Matrículas Noturnas**: Matrículas noturnas de licenciaturas presenciais
- **Concluintes Diurnos**: Concluintes diurnos de licenciaturas presenciais
- **Concluintes Noturnos**: Concluintes noturnos de licenciaturas presenciais

### **14. Dados de Gênero (Licenciaturas)**
- **Presencial Masculino**: Ingressos, matrículas e concluintes masculinos presenciais
- **Presencial Feminino**: Ingressos, matrículas e concluintes femininos presenciais
- **A Distância Masculino**: Ingressos, matrículas e concluintes masculinos a distância
- **A Distância Feminino**: Ingressos, matrículas e concluintes femininos a distância

### **14. Dados de Escola Pública (Licenciaturas)**
- **Ingressos**: Ingressos de estudantes de escola pública
- **Matrículas**: Matrículas de estudantes de escola pública
- **Concluintes**: Concluintes de estudantes de escola pública

### **15. Dados de Raça/Cor (Licenciaturas)**
- **Presencial**: Ingressos, matrículas e concluintes por raça/cor (parda, amarela, indígena, preta, branca, cornd)
- **A Distância**: Ingressos, matrículas e concluintes por raça/cor (parda, amarela, indígena, preta, branca, cornd)

## 🚀 **Como Executar**

### **Execução Direta**
```bash
cd relats/pesq
python executar_geracao_pacs.py
```

### **Resultado**
- **Arquivo gerado**: `Dados_PACs.xlsx`
- **Localização**: `relats/pesq/Dados_PACs.xlsx`

## 📋 **Estrutura da Planilha**

### **Colunas**
1. **Tipo Dado**: Tipo de informação (ex: "Nro de IES")
2. **Agrupamento**: Nível de agrupamento (ex: "Nenhum", "Global")
3. **Categoria**: Categoria específica (ex: "Global", "Pública")
4. **Sub_Categoria**: Subcategoria (ex: "Global", "Federal")
5. **2014**: Dados do ano 2014
6. **2015**: Dados do ano 2015
7. **...**: Dados dos anos subsequentes
8. **2024**: Dados do ano 2024

### **Formatação**
- **Cabeçalho**: Azul claro, negrito, centralizado
- **Linhas de dados**: Alternância entre verde claro e cinza claro
- **Bordas**: Todas as células com bordas finas
- **Alinhamento**: Centralizado, com quebra de texto

## 🔍 **Troubleshooting**

### **Erro de Import**
Se ocorrer erro de import, verifique:
1. Se todos os arquivos estão no diretório correto
2. Se as dependências estão instaladas (`openpyxl`, `pandas`)
3. Se o banco de dados está acessível

### **Erro de Dados**
Se não houver dados:
1. Verifique se o município 4204202 existe no banco
2. Confirme se há dados para 2014-2024
3. Verifique as consultas SQL em `pacs_sql_queries.py`

## 📈 **Extensibilidade**

### **Adicionar Novas Consultas**
1. Adicione a função SQL em `pacs_sql_queries.py`
2. Crie função de processamento em `pacs_data_processors.py`
3. Adicione cores em `pacs_excel_formatter.py`
4. Chame a função em `processar_todos_dados_pacs()`

### **Modificar Período**
Para alterar o período:
1. Modifique `ano_inicio` e `ano_fim` nas funções de carregamento
2. Atualize a lista de colunas em `executar_geracao_pacs.py`
3. Ajuste as consultas SQL conforme necessário

### **Modificar Município**
Para alterar o município:
1. Substitua `'4204202'` por outro código em `pacs_sql_queries.py`
2. Atualize a documentação

## 🎨 **Personalização**

### **Cores**
As cores podem ser modificadas em `pacs_excel_formatter.py`:
- `get_cores_formatacao_pacs()`: Cores básicas
- `get_cores_por_secao_pacs()`: Cores por seção

### **Formatação**
A formatação pode ser ajustada em `pacs_excel_formatter.py`:
- `get_alinhamento_pacs()`: Alinhamento das células
- `get_borda_pacs()`: Estilo das bordas
- `ajustar_largura_colunas_pacs()`: Largura das colunas

## 📞 **Suporte**

Para dúvidas ou problemas:
1. Verifique os logs de execução
2. Confirme a conectividade com o banco de dados
3. Valide as consultas SQL individualmente
4. Verifique se todos os arquivos estão presentes

---

**Desenvolvido para processamento de dados PACs do INEP** 📊 