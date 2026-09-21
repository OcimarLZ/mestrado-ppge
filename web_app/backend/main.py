import os
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from database import engine, microdata_engine, Base, get_db
from models import DashboardSummary, PageContent, SiteSettings, HomeCard, SectionVisual
from seed_data import seed_all
from schemas import DashboardSummaryUpdate, PageContentCreate, PageContentUpdate, PageContentResponse, SiteSettingsUpdate, HomeCardCreate, HomeCardUpdate, HomeCardResponse, SectionVisualCreate, SectionVisualUpdate

Base.metadata.create_all(bind=engine)

def seed_database(db: Session):
    summary = db.query(DashboardSummary).first()
    if not summary:
        new_summary = DashboardSummary(
            total_matriculas_2024="10.227.251",
            matriculas_ead_2024="5.189.376",
            matriculas_presencial_2024="5.037.875",
            participacao_privada_lucrativa="69,9%",
            evasao_total="1.1 milhão+"
        )
        db.add(new_summary)
        db.commit()

    settings = db.query(SiteSettings).first()
    if not settings:
        new_settings = SiteSettings(
            sidebar_title="EaD no Brasil",
            sidebar_icon="BookOpen",
            topbar_title="Formação de Professores (2014-2024)",
            footer_text_1="Dissertação de Mestrado © 2026 - Ocimar Luis Zolin",
            footer_text_2="Programa de Pós-Graduação em Educação - UFFS",
            hero_title="A Educação a Distância no Brasil (2014-2024)",
            hero_subtitle="O Público e o Privado na Formação de Professores: Uma análise estrutural e de dados sobre a expansão mercantilizada e a precarização docente.",
            home_body_title="O Paradoxo da Formação Docente",
            home_body_text="A pesquisa revela uma transformação profunda no cenário educacional: enquanto o setor público presencial estagna e enfrenta o \"terror da performatividade\" e o contingenciamento de gastos, o setor privado com fins lucrativos expande vertiginosamente suas operações na modalidade EaD.\n\nA \"commoditycidade\" da educação superior transformou a formação de professores em um mercado de massa, afastando a vivência universitária e promovendo uma inclusão excludente baseada em tutoria precarizada e materiais padronizados."
        )
        db.add(new_settings)
        db.commit()

    cards = db.query(HomeCard).all()
    if not cards:
        card1 = HomeCard(icon="TrendingUp", value="69,9%", title="Controle Privado", description="Das matrículas em licenciaturas estão em instituições com fins lucrativos (2024).", order=1)
        card2 = HomeCard(icon="Users", value="5.1M", title="Matrículas EaD", description="A EaD superou o ensino presencial, tornando-se a principal porta de entrada da docência.", order=2)
        card3 = HomeCard(icon="AlertTriangle", value="1.1M+", title="Evasão Histórica", description="Um sistema que processa milhões, mas perde grande parte por evasão no setor público e privado.", order=3)
        db.add_all([card1, card2, card3])
        db.commit()
        
    seed_all(db)

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = next(get_db())
    seed_database(db)
    db.close()
    yield

app = FastAPI(title="EaD no Brasil - API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    return {"message": "API da Dissertação rodando com hierarquia de capítulos!"}

@app.get("/api/dashboard-summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    summary = db.query(DashboardSummary).first()
    return summary

@app.put("/api/dashboard-summary")
def update_dashboard_summary(data: DashboardSummaryUpdate, db: Session = Depends(get_db)):
    summary = db.query(DashboardSummary).first()
    if not summary:
        raise HTTPException(status_code=404, detail="Dashboard Summary not found")
    
    summary.total_matriculas_2024 = data.total_matriculas_2024
    summary.matriculas_ead_2024 = data.matriculas_ead_2024
    summary.matriculas_presencial_2024 = data.matriculas_presencial_2024
    summary.participacao_privada_lucrativa = data.participacao_privada_lucrativa
    summary.evasao_total = data.evasao_total
    
    db.commit()
    db.refresh(summary)
    return {"message": "Updated successfully"}

@app.get("/api/site-settings")
def get_site_settings(db: Session = Depends(get_db)):
    settings = db.query(SiteSettings).first()
    return settings

@app.put("/api/site-settings")
def update_site_settings(data: SiteSettingsUpdate, db: Session = Depends(get_db)):
    settings = db.query(SiteSettings).first()
    if not settings:
        raise HTTPException(status_code=404, detail="Site Settings not found")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(settings, key, value)
        
    db.commit()
    db.refresh(settings)
    return {"message": "Updated successfully"}

# ---- HOMECARDS ENDPOINTS ----

@app.get("/api/home-cards")
def get_home_cards(db: Session = Depends(get_db)):
    cards = db.query(HomeCard).order_by(HomeCard.order.asc()).all()
    return cards

@app.post("/api/home-cards")
def create_home_card(data: HomeCardCreate, db: Session = Depends(get_db)):
    new_card = HomeCard(**data.dict())
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card

@app.put("/api/home-cards/{card_id}")
def update_home_card(card_id: int, data: HomeCardUpdate, db: Session = Depends(get_db)):
    card = db.query(HomeCard).filter(HomeCard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(card, key, value)
    
    db.commit()
    db.refresh(card)
    return card

@app.delete("/api/home-cards/{card_id}")
def delete_home_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(HomeCard).filter(HomeCard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    db.delete(card)
    db.commit()
    return {"message": "Deleted successfully"}

# ---- NEW HIERARCHICAL ENDPOINTS ----

def build_tree(items, parent_id=None):
    tree = []
    for item in items:
        if item.parent_id == parent_id:
            node = {
                "id": item.id,
                "parent_id": item.parent_id,
                "slug": item.slug,
                "title": item.title,
                "order": item.order,
                "icon_name": item.icon_name,
                "children": build_tree(items, item.id)
            }
            tree.append(node)
    return sorted(tree, key=lambda x: x["order"] or 0)

@app.get("/api/tree")
def get_full_tree(db: Session = Depends(get_db)):
    # Retorna toda a estrutura em formato de árvore (útil para o menu lateral)
    contents = db.query(PageContent).all()
    return build_tree(contents)

@app.get("/api/pages")
def get_all_pages_flat(db: Session = Depends(get_db)):
    # Retorna lista plana para o Admin
    contents = db.query(PageContent).order_by(PageContent.parent_id.asc(), PageContent.order.asc()).all()
    return contents

def get_descendants_flat(items, parent_id):
    result = []
    for item in sorted([i for i in items if i.parent_id == parent_id], key=lambda x: x.order or 0):
        result.append(item)
        result.extend(get_descendants_flat(items, item.id))
    return result

@app.get("/api/capitulo/{slug}")
def get_chapter_content(slug: str, db: Session = Depends(get_db)):
    chapter = db.query(PageContent).filter(PageContent.slug == slug, PageContent.parent_id == None).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
        
    all_contents = db.query(PageContent).all()
    descendants = get_descendants_flat(all_contents, chapter.id)
    
    result = [chapter] + descendants
    all_ids = [c.id for c in result]
    visuals = db.query(SectionVisual).filter(SectionVisual.page_content_id.in_(all_ids)).all()
    visuals_by_section: dict[int, list] = {}
    for v in visuals:
        visuals_by_section.setdefault(v.page_content_id, []).append(v)

    return [
        {
            "id": c.id,
            "parent_id": c.parent_id,
            "slug": c.slug,
            "title": c.title,
            "content": c.content,
            "order": c.order,
            "icon_name": c.icon_name,
            "content_type": c.content_type,
            "image_url": c.image_url,
            "sql_query": c.sql_query,
            "chart_type": c.chart_type,
            "x_axis": c.x_axis,
            "y_axis": c.y_axis,
            "show_labels": c.show_labels,
            "legend_position": c.legend_position,
            "analysis_text": c.analysis_text,
            "pdf_page": c.pdf_page,
            "visuals": [
                {
                    "id": v.id,
                    "page_content_id": v.page_content_id,
                    "type": v.type,
                    "title": v.title,
                    "source": v.source,
                    "order": v.order,
                    "image_url": v.image_url,
                    "sql_query": v.sql_query,
                    "chart_type": v.chart_type,
                    "x_axis": v.x_axis,
                    "y_axis": v.y_axis,
                    "show_labels": v.show_labels,
                    "legend_position": v.legend_position,
                    "table_html": v.table_html,
                    "pdf_page": v.pdf_page,
                }
                for v in visuals_by_section.get(c.id, [])
            ],
        }
        for c in result
    ]


@app.post("/api/pages")
def create_page_content(data: PageContentCreate, db: Session = Depends(get_db)):
    new_content = PageContent(**data.dict())
    db.add(new_content)
    try:
        db.commit()
        db.refresh(new_content)
        return new_content
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/pages/{content_id}")
def update_page_content(content_id: int, data: PageContentUpdate, db: Session = Depends(get_db)):
    content = db.query(PageContent).filter(PageContent.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(content, key, value)
    
    try:
        db.commit()
        db.refresh(content)
        return content
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/pages/{content_id}")
def delete_page_content(content_id: int, db: Session = Depends(get_db)):
    content = db.query(PageContent).filter(PageContent.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Delete children recursively? SQLite might not do CASCADE unless configured.
    def delete_recursive(node_id):
        children = db.query(PageContent).filter(PageContent.parent_id == node_id).all()
        for child in children:
            delete_recursive(child.id)
        node = db.query(PageContent).filter(PageContent.id == node_id).first()
        if node:
            db.delete(node)

    delete_recursive(content_id)
    db.commit()
    return {"message": "Deleted successfully"}

@app.get("/api/pages/{content_id}/data")
def get_page_visualization_data(content_id: int, db: Session = Depends(get_db)):
    content = db.query(PageContent).filter(PageContent.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
        
    if not content.sql_query:
        raise HTTPException(status_code=400, detail="No SQL query defined for this content")
        
    try:
        df = pd.read_sql_query(content.sql_query, con=microdata_engine)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database execution error: {str(e)}")

# ---- SECTION VISUALS ENDPOINTS ----

@app.get("/api/sections/{section_id}/visuals")
def get_section_visuals(section_id: int, db: Session = Depends(get_db)):
    visuals = db.query(SectionVisual).filter(SectionVisual.page_content_id == section_id).order_by(SectionVisual.order.asc()).all()
    return visuals

@app.post("/api/sections/{section_id}/visuals")
def create_section_visual(section_id: int, data: SectionVisualCreate, db: Session = Depends(get_db)):
    section = db.query(PageContent).filter(PageContent.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    new_visual = SectionVisual(**data.dict())
    db.add(new_visual)
    db.commit()
    db.refresh(new_visual)
    return new_visual

@app.put("/api/visuals/{visual_id}")
def update_section_visual(visual_id: int, data: SectionVisualUpdate, db: Session = Depends(get_db)):
    visual = db.query(SectionVisual).filter(SectionVisual.id == visual_id).first()
    if not visual:
        raise HTTPException(status_code=404, detail="Visual not found")
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(visual, key, value)
    db.commit()
    db.refresh(visual)
    return visual

@app.delete("/api/visuals/{visual_id}")
def delete_section_visual(visual_id: int, db: Session = Depends(get_db)):
    visual = db.query(SectionVisual).filter(SectionVisual.id == visual_id).first()
    if not visual:
        raise HTTPException(status_code=404, detail="Visual not found")
    db.delete(visual)
    db.commit()
    return {"message": "Deleted successfully"}

@app.get("/api/visuals/{visual_id}/data")
def get_visual_data(visual_id: int, db: Session = Depends(get_db)):
    visual = db.query(SectionVisual).filter(SectionVisual.id == visual_id).first()
    if not visual:
        raise HTTPException(status_code=404, detail="Visual not found")
    if not visual.sql_query:
        raise HTTPException(status_code=400, detail="No SQL query defined for this visual")
    try:
        df = pd.read_sql_query(visual.sql_query, con=microdata_engine)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database execution error: {str(e)}")
