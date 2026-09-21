import sqlite3
import traceback

conn = sqlite3.connect('site_cms.db')
cur = conn.cursor()
queries = [
    "ALTER TABLE page_content ADD COLUMN content_type VARCHAR DEFAULT 'text'",
    "ALTER TABLE page_content ADD COLUMN sql_query TEXT",
    "ALTER TABLE page_content ADD COLUMN chart_type VARCHAR",
    "ALTER TABLE page_content ADD COLUMN x_axis VARCHAR",
    "ALTER TABLE page_content ADD COLUMN y_axis VARCHAR",
    "ALTER TABLE page_content ADD COLUMN show_labels INTEGER DEFAULT 0",
    "ALTER TABLE page_content ADD COLUMN legend_position VARCHAR DEFAULT 'bottom'",
    "ALTER TABLE page_content ADD COLUMN analysis_text TEXT",
    "ALTER TABLE site_settings ADD COLUMN hero_title VARCHAR DEFAULT 'A Educação a Distância no Brasil (2014-2024)'",
    "ALTER TABLE site_settings ADD COLUMN hero_subtitle VARCHAR DEFAULT 'O Público e o Privado na Formação de Professores: Uma análise estrutural e de dados sobre a expansão mercantilizada e a precarização docente.'",
    "ALTER TABLE site_settings ADD COLUMN home_body_title VARCHAR DEFAULT 'O Paradoxo da Formação Docente'",
    "ALTER TABLE site_settings ADD COLUMN home_body_text TEXT DEFAULT 'A pesquisa revela uma transformação profunda no cenário educacional: enquanto o setor público presencial estagna e enfrenta o \"terror da performatividade\" e o contingenciamento de gastos, o setor privado com fins lucrativos expande vertiginosamente suas operações na modalidade EaD.\n\nA \"commoditycidade\" da educação superior transformou a formação de professores em um mercado de massa, afastando a vivência universitária e promovendo uma inclusão excludente baseada em tutoria precarizada e materiais padronizados.'",
    "CREATE TABLE IF NOT EXISTS home_cards (id INTEGER PRIMARY KEY, icon VARCHAR, value VARCHAR, title VARCHAR, description VARCHAR, \"order\" INTEGER DEFAULT 0)",
    "ALTER TABLE page_content ADD COLUMN pdf_page INTEGER",
    "ALTER TABLE section_visuals ADD COLUMN pdf_page INTEGER",
]

for q in queries:
    try:
        cur.execute(q)
        print(f"Executed: {q}")
    except Exception as e:
        print(f"Skipped {q} due to error (likely column exists): {e}")

conn.commit()
conn.close()
