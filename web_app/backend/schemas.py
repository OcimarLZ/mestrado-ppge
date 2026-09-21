from pydantic import BaseModel
from typing import Optional

# Schemas para DashboardSummary
class DashboardSummaryUpdate(BaseModel):
    total_matriculas_2024: str
    matriculas_ead_2024: str
    matriculas_presencial_2024: str
    participacao_privada_lucrativa: str
    evasao_total: str

class SiteSettingsBase(BaseModel):
    sidebar_title: str
    sidebar_icon: str
    topbar_title: str
    footer_text_1: str
    footer_text_2: str
    hero_title: str
    hero_subtitle: str
    home_body_title: str
    home_body_text: str
    theme_bg_color: str = "#0f172a"
    theme_text_color: str = "#f8fafc"
    theme_primary_color: str = "#10b981"
    theme_card_bg_color: str = "rgba(30, 41, 59, 0.7)"
    theme_font_family: str = "'Inter', system-ui, -apple-system, sans-serif"
    theme_sidebar_bg: str = "#0f172a"
    theme_hero_glow_color: str = "rgba(16,185,129,0.1)"
    theme_name: str = "dark-slate"
    work_type: str = "Dissertação de Mestrado"
    work_program: str = "Programa de Pós-Graduação em Educação – UFFS"
    work_organization: str = "Universidade Federal da Fronteira Sul"
    work_description: str = ""
    work_authors: str = ""
    work_research_group: str = ""
    work_advisor: str = ""
    work_committee: str = ""
    work_abstract: str = ""
    work_abstract_en: str = ""
    work_keywords: str = ""

class SiteSettingsUpdate(BaseModel):
    sidebar_title: Optional[str] = None
    sidebar_icon: Optional[str] = None
    topbar_title: Optional[str] = None
    footer_text_1: Optional[str] = None
    footer_text_2: Optional[str] = None
    hero_title: Optional[str] = None
    hero_subtitle: Optional[str] = None
    home_body_title: Optional[str] = None
    home_body_text: Optional[str] = None
    theme_bg_color: Optional[str] = None
    theme_text_color: Optional[str] = None
    theme_primary_color: Optional[str] = None
    theme_card_bg_color: Optional[str] = None
    theme_font_family: Optional[str] = None
    theme_sidebar_bg: Optional[str] = None
    theme_hero_glow_color: Optional[str] = None
    theme_name: Optional[str] = None
    work_type: Optional[str] = None
    work_program: Optional[str] = None
    work_organization: Optional[str] = None
    work_description: Optional[str] = None
    work_authors: Optional[str] = None
    work_research_group: Optional[str] = None
    work_advisor: Optional[str] = None
    work_committee: Optional[str] = None
    work_abstract: Optional[str] = None
    work_abstract_en: Optional[str] = None
    work_keywords: Optional[str] = None

class SiteSettingsResponse(SiteSettingsBase):
    id: int

    class Config:
        from_attributes = True

# Schemas para HomeCard
class HomeCardBase(BaseModel):
    icon: str
    value: str
    title: str
    description: str
    order: Optional[int] = 0

class HomeCardCreate(HomeCardBase):
    pass

class HomeCardUpdate(BaseModel):
    icon: Optional[str] = None
    value: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None

class HomeCardResponse(HomeCardBase):
    id: int

    class Config:
        from_attributes = True

# Schemas para PageContent
class PageContentBase(BaseModel):
    parent_id: Optional[int] = None
    slug: str
    title: str
    content: Optional[str] = None
    order: Optional[int] = 0
    icon_name: Optional[str] = None
    
    # Visualization fields
    content_type: Optional[str] = "text"
    image_url: Optional[str] = None
    sql_query: Optional[str] = None
    chart_type: Optional[str] = None
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    show_labels: Optional[int] = 0
    legend_position: Optional[str] = "bottom"
    analysis_text: Optional[str] = None
    pdf_page: Optional[int] = None

class PageContentCreate(PageContentBase):
    pass

class PageContentUpdate(BaseModel):
    parent_id: Optional[int] = None
    slug: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    order: Optional[int] = None
    icon_name: Optional[str] = None
    
    content_type: Optional[str] = None
    image_url: Optional[str] = None
    sql_query: Optional[str] = None
    chart_type: Optional[str] = None
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    show_labels: Optional[int] = None
    legend_position: Optional[str] = None
    analysis_text: Optional[str] = None
    pdf_page: Optional[int] = None

class PageContentResponse(PageContentBase):
    id: int

    class Config:
        from_attributes = True

# Schemas para SectionVisual
class SectionVisualBase(BaseModel):
    page_content_id: int
    type: str = "chart"
    title: str = ""
    source: str = ""
    order: int = 0
    image_url: Optional[str] = None
    sql_query: Optional[str] = None
    chart_type: Optional[str] = None
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    show_labels: Optional[int] = 0
    legend_position: Optional[str] = "bottom"
    table_html: Optional[str] = None
    pdf_page: Optional[int] = None

class SectionVisualCreate(SectionVisualBase):
    pass

class SectionVisualUpdate(BaseModel):
    type: Optional[str] = None
    title: Optional[str] = None
    source: Optional[str] = None
    order: Optional[int] = None
    image_url: Optional[str] = None
    sql_query: Optional[str] = None
    chart_type: Optional[str] = None
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    show_labels: Optional[int] = None
    legend_position: Optional[str] = None
    table_html: Optional[str] = None
    pdf_page: Optional[int] = None

class SectionVisualResponse(SectionVisualBase):
    id: int

    class Config:
        from_attributes = True
