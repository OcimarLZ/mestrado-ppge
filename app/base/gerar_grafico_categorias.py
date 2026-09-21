import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
import json
import os
import pandas as pd

def gerar_dados_evolucao_categorias():
    """
    Conecta ao banco, consulta os dados de evolução de IES por categoria
    para um município e período específicos, e gera um arquivo JSON.
    """
    db_path = os.path.abspath('D:/ProjetosPY/inep/INEP.db')
    db_uri = f'sqlite:///{db_path}'
    
    session = None
    try:
        engine = sqlalchemy.create_engine(db_uri)
        Session = sessionmaker(bind=engine)
        session = Session()
        Base = declarative_base()

        # Redefine models
        class Tp_categoria_administrativa(Base):
            __tablename__ = 'tp_categoria_administrativa'
            codigo = Column(Integer, primary_key=True)
            nome = Column(String)

        class Curso_censo(Base):
            __tablename__ = 'curso_censo'
            id = Column(Integer, primary_key=True)
            ano_censo = Column(Integer)
            municipio = Column(String)
            categoria = Column(Integer, ForeignKey('tp_categoria_administrativa.codigo'))
            ies = Column(Integer)

        # Query with filters - now using Curso_censo
        results = session.query(
            Curso_censo.ano_censo,
            Tp_categoria_administrativa.nome,
            sqlalchemy.func.count(Curso_censo.ies.distinct())
        ).join(
            Tp_categoria_administrativa, Curso_censo.categoria == Tp_categoria_administrativa.codigo
        ).filter(
            Curso_censo.municipio == '4204202',
            Curso_censo.ano_censo.between(2014, 2023)
        ).group_by(
            Curso_censo.ano_censo,
            Tp_categoria_administrativa.nome
        ).order_by(
            Curso_censo.ano_censo,
            Tp_categoria_administrativa.nome
        ).all()

        if not results:
            print("Nenhum dado encontrado para os filtros especificados.")
            return

        # Use pandas to pivot the data
        df = pd.DataFrame(results, columns=['ano', 'categoria', 'total'])
        pivot_df = df.pivot(index='ano', columns='categoria', values='total').fillna(0)
        
        # Ensure all years from 2014-2023 are present
        all_years = range(2014, 2024)
        pivot_df = pivot_df.reindex(all_years, fill_value=0).astype(int)

        # Convert to the desired JSON structure for Chart.js
        labels = [str(year) for year in pivot_df.index]
        datasets = []
        for column in pivot_df.columns:
            datasets.append({
                "label": column,
                "data": pivot_df[column].tolist()
            })
        
        final_json_data = {"labels": labels, "datasets": datasets}

        # Write JSON file
        json_path = os.path.abspath('D:/ProjetosPY/inep/acs/dados_evolucao_categorias.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(final_json_data, f, ensure_ascii=False, indent=4)
        
        print(f"Dados de evolução por categoria salvos com sucesso em '{json_path}'")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if session and session.is_active:
            session.close()

if __name__ == '__main__':
    gerar_dados_evolucao_categorias()