from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base

class DashboardSummary(Base):
    __tablename__ = "dashboard_summary"

    id = Column(Integer, primary_key=True, index=True)
    total_matriculas_2024 = Column(String)
    matriculas_ead_2024 = Column(String)
    matriculas_presencial_2024 = Column(String)
    participacao_privada_lucrativa = Column(String)
    evasao_total = Column(String)

class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, index=True)
    sidebar_title = Column(String, default="EaD no Brasil")
    sidebar_icon = Column(String, default="BookOpen")
    topbar_title = Column(String, default="Formação de Professores (2014-2024)")
    footer_text_1 = Column(String, default="Dissertação de Mestrado © 2026 - Ocimar Luis Zolin")
    footer_text_2 = Column(String, default="Programa de Pós-Graduação em Educação - UFFS")
    hero_title = Column(String, default="A Educação a Distância no Brasil (2014-2024)")
    hero_subtitle = Column(String, default="O Público e o Privado na Formação de Professores: Uma análise estrutural e de dados sobre a expansão mercantilizada e a precarização docente.")
    home_body_title = Column(String, default="O Paradoxo da Formação Docente")
    home_body_text = Column(Text, default="A pesquisa revela uma transformação profunda no cenário educacional: enquanto o setor público presencial estagna e enfrenta o \"terror da performatividade\" e o contingenciamento de gastos, o setor privado com fins lucrativos expande vertiginosamente suas operações na modalidade EaD.\n\nA \"commoditycidade\" da educação superior transformou a formação de professores em um mercado de massa, afastando a vivência universitária e promovendo uma inclusão excludente baseada em tutoria precarizada e materiais padronizados.")
    theme_bg_color = Column(String, default="#0f172a")
    theme_text_color = Column(String, default="#f8fafc")
    theme_primary_color = Column(String, default="#10b981")
    theme_card_bg_color = Column(String, default="rgba(30, 41, 59, 0.7)")
    theme_font_family = Column(String, default="'Inter', system-ui, -apple-system, sans-serif")
    theme_sidebar_bg = Column(String, default="#0f172a")
    theme_hero_glow_color = Column(String, default="rgba(16,185,129,0.1)")
    theme_name = Column(String, default="dark-slate")
    work_type = Column(String, default="Dissertação de Mestrado")
    work_program = Column(String, default="Programa de Pós-Graduação em Educação – UFFS")
    work_organization = Column(String, default="Universidade Federal da Fronteira Sul")
    work_description = Column(Text, default="")
    work_authors = Column(Text, default="")
    work_research_group = Column(String, default="")
    work_advisor = Column(String, default="")
    work_committee = Column(Text, default="")
    work_abstract = Column(Text, default="")
    work_abstract_en = Column(Text, default="")
    work_keywords = Column(String, default="")

class HomeCard(Base):
    __tablename__ = "home_cards"

    id = Column(Integer, primary_key=True, index=True)
    icon = Column(String)
    value = Column(String)
    title = Column(String)
    description = Column(String)
    order = Column(Integer, default=0)

class PageContent(Base):
    __tablename__ = "page_content"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("page_content.id"), nullable=True) # Se nulo, é um Capítulo
    slug = Column(String, index=True, unique=True) # Ex: 'introducao', 'banca-examinadora'
    title = Column(String)
    content = Column(Text, nullable=True)
    order = Column(Integer, default=0)
    icon_name = Column(String, nullable=True)

    # Visualization Fields
    content_type = Column(String, default="text") # 'text', 'chart', 'table', 'image'
    image_url = Column(String, nullable=True)
    sql_query = Column(Text, nullable=True)
    chart_type = Column(String, nullable=True) # 'bar', 'line', 'pie'
    x_axis = Column(String, nullable=True)
    y_axis = Column(String, nullable=True)
    show_labels = Column(Integer, default=0)
    legend_position = Column(String, default="bottom")
    analysis_text = Column(Text, nullable=True)
    pdf_page = Column(Integer, nullable=True)  # página correspondente na dissertação (PDF)

class SectionVisual(Base):
    __tablename__ = "section_visuals"

    id = Column(Integer, primary_key=True, index=True)
    page_content_id = Column(Integer, ForeignKey("page_content.id"))
    type = Column(String, default="chart")  # 'image', 'chart', 'table'
    title = Column(String, default="")    # legenda
    source = Column(String, default="")   # fonte
    order = Column(Integer, default=0)

    # Image
    image_url = Column(String, nullable=True)

    # Chart
    sql_query = Column(Text, nullable=True)
    chart_type = Column(String, nullable=True)  # bar, line, pie
    x_axis = Column(String, nullable=True)
    y_axis = Column(String, nullable=True)
    show_labels = Column(Integer, default=0)
    legend_position = Column(String, default="bottom")

    # Table (pre-generated HTML or from SQL)
    table_html = Column(Text, nullable=True)
    pdf_page = Column(Integer, nullable=True)  # página correspondente na dissertação (PDF)
