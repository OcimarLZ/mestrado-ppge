from sqlalchemy.orm import Session
from models import PageContent

def seed_all(db: Session):
    # This will be run during initialization if the table is empty
    if db.query(PageContent).first():
        return

    # 1. Introdução (Chapter)
    intro = PageContent(slug="introducao", title="Introdução", order=1, icon_name="BookOpen")
    db.add(intro)
    db.commit()
    db.refresh(intro)

    # 1.1 Sections of Introdução
    intro_contexto = PageContent(parent_id=intro.id, slug="contextualizacao", title="Contextualização", order=1, content="<p>Texto da contextualização...</p>")
    intro_prob = PageContent(parent_id=intro.id, slug="problema", title="Problema de Pesquisa", order=2, content="<p>Texto do problema...</p>")
    db.add_all([intro_contexto, intro_prob])
    db.commit()

    # 2. Metodologia (Chapter)
    metodo = PageContent(slug="metodologia", title="Metodologia", order=2, icon_name="Beaker")
    db.add(metodo)
    db.commit()
    db.refresh(metodo)

    metodo_abordagem = PageContent(parent_id=metodo.id, slug="abordagem", title="Abordagem Quali-Quanti", order=1, content="<p>Texto da abordagem...</p>")
    db.add(metodo_abordagem)
    db.commit()

    # 3. Políticas de Educação (Chapter)
    politicas = PageContent(slug="politicas-educacao", title="Políticas de Educação", order=3, icon_name="Landmark")
    db.add(politicas)
    db.commit()
    db.refresh(politicas)

    pol_historia = PageContent(parent_id=politicas.id, slug="historico", title="Histórico", order=1, content="<p>Histórico das políticas...</p>")
    db.add(pol_historia)
    db.commit()

    # 4. Políticas EaD (Chapter)
    ead = PageContent(slug="politicas-ead", title="Políticas de EaD", order=4, icon_name="MonitorPlay")
    db.add(ead)
    db.commit()
    db.refresh(ead)

    ead_evolucao = PageContent(parent_id=ead.id, slug="evolucao", title="Evolução", order=1, content="<p>Evolução da EaD...</p>")
    db.add(ead_evolucao)
    db.commit()

    # 5. EaD nas Federais (Chapter)
    federais = PageContent(slug="ead-federais", title="EaD nas Federais", order=5, icon_name="Building")
    db.add(federais)
    db.commit()
    db.refresh(federais)
    
    fed_dados = PageContent(parent_id=federais.id, slug="dados-federais", title="Dados das Federais", order=1, content="<p>Dados das federais...</p>")
    db.add(fed_dados)
    db.commit()

    # 6. Considerações Finais (Chapter)
    consideracoes = PageContent(slug="consideracoes", title="Considerações Finais", order=6, icon_name="Flag")
    db.add(consideracoes)
    db.commit()
    db.refresh(consideracoes)

    cons_conclusao = PageContent(parent_id=consideracoes.id, slug="conclusao", title="Conclusão", order=1, content="<p>Conclusões...</p>")
    db.add(cons_conclusao)
    db.commit()
