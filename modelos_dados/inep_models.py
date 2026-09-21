from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ---------------------------------------------------------------------------
# Tabelas de referencia geografica
# ---------------------------------------------------------------------------

class Regiao(db.Model):
    __tablename__ = 'comum_regiao'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(12), nullable=False)


class RegiaoIntermediaria(db.Model):
    __tablename__ = 'comum_regiao_intermediaria'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(12), nullable=False)
    estado = db.Column(db.String(2), db.ForeignKey('comum_uf.sigla'), nullable=False)


class RegiaoImediata(db.Model):
    __tablename__ = 'comum_regiao_imediata'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(12), nullable=False)


class Uf(db.Model):
    __tablename__ = 'comum_uf'
    sigla = db.Column(db.String(2), primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    regiao = db.Column(db.Integer, db.ForeignKey('comum_regiao.codigo'), nullable=False)
    codigo = db.Column(db.Integer, nullable=False)


class Mesorregiao(db.Model):
    __tablename__ = 'comum_mesorregiao'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    estado = db.Column(db.String(2), db.ForeignKey('comum_uf.sigla'), nullable=False)


class Microrregiao(db.Model):
    __tablename__ = 'comum_microrregiao'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    mesorregiao = db.Column(db.Integer, db.ForeignKey('comum_mesorregiao.codigo'), nullable=False)


class Municipio(db.Model):
    __tablename__ = 'comum_municipio'
    codigo = db.Column(db.String(12), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), db.ForeignKey('comum_uf.sigla'), nullable=False)
    mesorregiao = db.Column(db.Integer, db.ForeignKey('comum_mesorregiao.codigo'), nullable=False)
    microrregiao = db.Column(db.Integer, db.ForeignKey('comum_microrregiao.codigo'), nullable=False)
    natureza = db.Column(db.Text, nullable=True)
    hierarquia = db.Column(db.String(1), nullable=True)
    regiao_intermediaria = db.Column(db.Integer, db.ForeignKey('comum_regiao_intermediaria.codigo'), nullable=True)
    regiao_imediata = db.Column(db.Integer, db.ForeignKey('comum_regiao_imediata.codigo'), nullable=True)


class MunicipioCenso(db.Model):
    __tablename__ = 'municipio_censo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    municipio = db.Column(db.String(12), db.ForeignKey('comum_municipio.codigo'), nullable=False)
    ano_censo = db.Column(db.Integer, nullable=True)
    domicilios = db.Column(db.Integer, nullable=True)
    populacao = db.Column(db.Integer, nullable=True)
    area = db.Column(db.Integer, nullable=True)
    idade_media = db.Column(db.Integer, nullable=True)
    tx_alfabetizacao = db.Column(db.Float, nullable=True)
    pop_branca = db.Column(db.Integer, nullable=True)
    pop_preta = db.Column(db.Integer, nullable=True)
    pop_parda = db.Column(db.Integer, nullable=True)
    pop_indigena = db.Column(db.Integer, nullable=True)
    pop_amarela = db.Column(db.Integer, nullable=True)
    pop_quilombola = db.Column(db.Integer, nullable=True)
    pop_estrangeiros = db.Column(db.Integer, nullable=True)
    pop_indigena_territorio = db.Column(db.Integer, nullable=True)
    pop_quilombola_territorio = db.Column(db.Integer, nullable=True)
    idx_razao_sexo = db.Column(db.Float, nullable=True)
    idx_envelhecimento = db.Column(db.Float, nullable=True)
    pop_19a24anos = db.Column(db.Integer, nullable=True)
    pop_ajustada = db.Column(db.Integer, nullable=True)


# ---------------------------------------------------------------------------
# Tabelas de area do conhecimento (classificacao CINE)
# ---------------------------------------------------------------------------

class Area(db.Model):
    __tablename__ = 'superior_area'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)


class Area_especifica(db.Model):
    __tablename__ = 'superior_area_especifica'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    area = db.Column(db.Integer, db.ForeignKey('superior_area.codigo'), nullable=False)


class Area_detalhada(db.Model):
    __tablename__ = 'superior_area_detalhada'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    area_especifica = db.Column(db.Integer, db.ForeignKey('superior_area_especifica.codigo'), nullable=False)


class Cine_rotulo(db.Model):
    __tablename__ = 'superior_cine_rotulo'
    codigo = db.Column(db.String(10), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)


class Curso(db.Model):
    __tablename__ = 'superior_curso'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    area_detalhada = db.Column(db.Integer, db.ForeignKey('superior_area_detalhada.codigo'), nullable=False)


# ---------------------------------------------------------------------------
# Tabelas de tipos (lookup)
# ---------------------------------------------------------------------------

class Tp_dimensao(db.Model):
    __tablename__ = 'superior_tp_dimensao'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)


class Tp_nivel_academico(db.Model):
    __tablename__ = 'superior_tp_nivel_academico'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)


class Tp_modal_ensino(db.Model):
    __tablename__ = 'superior_tp_modal_ensino'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)


class Tp_modalidade_ensino(db.Model):
    __tablename__ = 'superior_tp_modalidade_ensino'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)


class Tp_organizacao_academica(db.Model):
    __tablename__ = 'superior_tp_organizacao_academica'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)


class Tp_categoria_administrativa(db.Model):
    __tablename__ = 'superior_tp_categoria_administrativa'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)


class Tp_rede(db.Model):
    __tablename__ = 'superior_tp_rede'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)


class Tp_grau_academico(db.Model):
    __tablename__ = 'superior_tp_grau_academico'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)


# ---------------------------------------------------------------------------
# Instituicoes de Ensino Superior (IES)
# ---------------------------------------------------------------------------

class Mantenedora(db.Model):
    __tablename__ = 'superior_mantenedora'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)


class Ies(db.Model):
    __tablename__ = 'superior_ies'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sigla = db.Column(db.String(15), nullable=True)
    endereco_logradouro = db.Column(db.String(100), nullable=False)
    endereco_numero = db.Column(db.String(10), nullable=True)
    endereco_complemento = db.Column(db.String(100), nullable=True)
    bairro = db.Column(db.String(50), nullable=True)
    cep = db.Column(db.Integer, nullable=True)
    municipio = db.Column(db.String(12), db.ForeignKey('comum_municipio.codigo'), nullable=False)
    estado = db.Column(db.String(2), db.ForeignKey('comum_uf.sigla'), nullable=False)
    regiao = db.Column(db.Integer, db.ForeignKey('comum_regiao.codigo'), nullable=False)
    mesorregiao = db.Column(db.Integer, db.ForeignKey('comum_mesorregiao.codigo'), nullable=False)
    microrregiao = db.Column(db.Integer, db.ForeignKey('comum_microrregiao.codigo'), nullable=False)
    org_academica = db.Column(db.Integer, db.ForeignKey('superior_tp_organizacao_academica.codigo'), nullable=False)
    categoria = db.Column(db.Integer, db.ForeignKey('superior_tp_categoria_administrativa.codigo'), nullable=False)
    mantenedora = db.Column(db.Integer, db.ForeignKey('superior_mantenedora.codigo'), nullable=False)
    tp_rede = db.Column(db.Integer, db.ForeignKey('superior_tp_rede.codigo'), nullable=True)


class Unidade(db.Model):
    __tablename__ = 'superior_unidade'
    id = db.Column(db.Integer, primary_key=True)
    denominacao = db.Column(db.String(50), nullable=False)
    cep = db.Column(db.String(8), nullable=True)
    logradouro = db.Column(db.String(255), nullable=True)
    bairro = db.Column(db.String(50), nullable=True)
    municipio = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    ies = db.Column(db.Integer, db.ForeignKey('superior_ies.codigo'), nullable=False)
    link = db.Column(db.Text, nullable=True)


# ---------------------------------------------------------------------------
# Censo anual por IES
# ---------------------------------------------------------------------------

class Ies_censo(db.Model):
    __tablename__ = 'superior_ies_censo'
    id = db.Column(db.Integer, primary_key=True)
    ano_censo = db.Column(db.Integer, nullable=False)
    regiao = db.Column(db.Integer, db.ForeignKey('comum_regiao.codigo'), nullable=False)
    mesorregiao = db.Column(db.Integer, db.ForeignKey('comum_mesorregiao.codigo'), nullable=False)
    microrregiao = db.Column(db.Integer, db.ForeignKey('comum_microrregiao.codigo'), nullable=False)
    estado = db.Column(db.String(2), db.ForeignKey('comum_uf.sigla'), nullable=False)
    municipio = db.Column(db.String(12), db.ForeignKey('comum_municipio.codigo'), nullable=False)
    org_academica = db.Column(db.Integer, db.ForeignKey('superior_tp_organizacao_academica.codigo'), nullable=False)
    categoria = db.Column(db.Integer, db.ForeignKey('superior_tp_categoria_administrativa.codigo'), nullable=False)
    mantenedora = db.Column(db.Integer, db.ForeignKey('superior_mantenedora.codigo'), nullable=False)
    tp_rede = db.Column(db.Integer, db.ForeignKey('superior_tp_rede.codigo'), nullable=True)
    ies = db.Column(db.Integer, db.ForeignKey('superior_ies.codigo'), nullable=False)
    # Tecnicos administrativos
    qt_tec_total = db.Column(db.Integer, nullable=True)
    qt_tec_fundamental_incomp_fem = db.Column(db.Integer, nullable=True)
    qt_tec_fundamental_incomp_masc = db.Column(db.Integer, nullable=True)
    qt_tec_fundamental_comp_fem = db.Column(db.Integer, nullable=True)
    qt_tec_fundamental_comp_masc = db.Column(db.Integer, nullable=True)
    qt_tec_medio_fem = db.Column(db.Integer, nullable=True)
    qt_tec_medio_masc = db.Column(db.Integer, nullable=True)
    qt_tec_superior_fem = db.Column(db.Integer, nullable=True)
    qt_tec_superior_masc = db.Column(db.Integer, nullable=True)
    qt_tec_especializacao_fem = db.Column(db.Integer, nullable=True)
    qt_tec_especializacao_masc = db.Column(db.Integer, nullable=True)
    qt_tec_mestrado_fem = db.Column(db.Integer, nullable=True)
    qt_tec_mestrado_masc = db.Column(db.Integer, nullable=True)
    qt_tec_doutorado_fem = db.Column(db.Integer, nullable=True)
    qt_tec_doutorado_masc = db.Column(db.Integer, nullable=True)
    qt_tec_titulacao_ndef = db.Column(db.Integer, nullable=True)
    # Biblioteca
    in_acesso_portal_capes = db.Column(db.Boolean, nullable=True)
    in_acesso_outras_bases = db.Column(db.Boolean, nullable=True)
    in_assina_outra_base = db.Column(db.Boolean, nullable=True)
    in_repositorio_institucional = db.Column(db.Boolean, nullable=True)
    in_busca_integrada = db.Column(db.Boolean, nullable=True)
    in_servico_internet = db.Column(db.Boolean, nullable=True)
    in_participa_rede_social = db.Column(db.Boolean, nullable=True)
    in_catalogo_online = db.Column(db.Boolean, nullable=True)
    qt_periodico_eletronico = db.Column(db.Integer, nullable=True)
    qt_livro_eletronico = db.Column(db.Integer, nullable=True)
    # Docentes
    qt_doc_total = db.Column(db.Integer, nullable=True)
    qt_doc_exe = db.Column(db.Integer, nullable=True)
    qt_doc_ex_femi = db.Column(db.Integer, nullable=True)
    qt_doc_ex_masc = db.Column(db.Integer, nullable=True)
    qt_doc_ex_genero_ndef = db.Column(db.Integer, nullable=True)
    qt_doc_ex_sem_grad = db.Column(db.Integer, nullable=True)
    qt_doc_ex_grad = db.Column(db.Integer, nullable=True)
    qt_doc_ex_esp = db.Column(db.Integer, nullable=True)
    qt_doc_ex_mest = db.Column(db.Integer, nullable=True)
    qt_doc_ex_dout = db.Column(db.Integer, nullable=True)
    qt_doc_ex_titulacao_ndef = db.Column(db.Integer, nullable=True)
    qt_doc_ex_int = db.Column(db.Integer, nullable=True)
    qt_doc_ex_int_de = db.Column(db.Integer, nullable=True)
    qt_doc_ex_int_sem_de = db.Column(db.Integer, nullable=True)
    qt_doc_ex_parc = db.Column(db.Integer, nullable=True)
    qt_doc_ex_hor = db.Column(db.Integer, nullable=True)
    qt_doc_ex_dedicacao_ndef = db.Column(db.Integer, nullable=True)
    qt_doc_ex_0_29 = db.Column(db.Integer, nullable=True)
    qt_doc_ex_30_34 = db.Column(db.Integer, nullable=True)
    qt_doc_ex_35_39 = db.Column(db.Integer, nullable=True)
    qt_doc_ex_40_44 = db.Column(db.Integer, nullable=True)
    qt_doc_ex_45_49 = db.Column(db.Integer, nullable=True)
    qt_doc_ex_50_54 = db.Column(db.Integer, nullable=True)
    qt_doc_ex_55_59 = db.Column(db.Integer, nullable=True)
    qt_doc_ex_60_mais = db.Column(db.Integer, nullable=True)
    qt_doc_ex_idade_ndef = db.Column(db.Integer, nullable=True)
    qt_doc_ex_branca = db.Column(db.Integer, nullable=True)
    qt_doc_ex_preta = db.Column(db.Integer, nullable=True)
    qt_doc_ex_parda = db.Column(db.Integer, nullable=True)
    qt_doc_ex_amarela = db.Column(db.Integer, nullable=True)
    qt_doc_ex_indigena = db.Column(db.Integer, nullable=True)
    qt_doc_ex_cor_nd = db.Column(db.Integer, nullable=True)
    qt_doc_ex_raca_ndef = db.Column(db.Integer, nullable=True)
    qt_doc_ex_bra = db.Column(db.Integer, nullable=True)
    qt_doc_ex_est = db.Column(db.Integer, nullable=True)
    qt_doc_ex_nacional_ndef = db.Column(db.Integer, nullable=True)
    qt_doc_ex_com_deficiencia = db.Column(db.Integer, nullable=True)


# ---------------------------------------------------------------------------
# Censo anual por curso
# ---------------------------------------------------------------------------

class Curso_censo(db.Model):
    __tablename__ = 'superior_curso_censo'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    ano_censo = db.Column(db.Integer, nullable=True)
    regiao = db.Column(db.Integer, db.ForeignKey('comum_regiao.codigo'), nullable=True)
    estado = db.Column(db.String(2), db.ForeignKey('comum_uf.sigla'), nullable=True)
    municipio = db.Column(db.String(12), db.ForeignKey('comum_municipio.codigo'), nullable=True)
    dimensao = db.Column(db.Integer, db.ForeignKey('superior_tp_dimensao.codigo'), nullable=True)
    org_academica = db.Column(db.Integer, db.ForeignKey('superior_tp_organizacao_academica.codigo'), nullable=True)
    categoria = db.Column(db.Integer, db.ForeignKey('superior_tp_categoria_administrativa.codigo'), nullable=True)
    tp_rede = db.Column(db.Integer, db.ForeignKey('superior_tp_rede.codigo'), nullable=True)
    ies = db.Column(db.Integer, db.ForeignKey('superior_ies.codigo'), nullable=True)
    curso = db.Column(db.Integer, db.ForeignKey('superior_curso.codigo'), nullable=True)
    cine_rotulo = db.Column(db.String(10), db.ForeignKey('superior_cine_rotulo.codigo'), nullable=True)
    area_geral = db.Column(db.Integer, db.ForeignKey('superior_area.codigo'), nullable=True)
    area_especifica = db.Column(db.Integer, db.ForeignKey('superior_area_especifica.codigo'), nullable=True)
    area_detalhada = db.Column(db.Integer, db.ForeignKey('superior_area_detalhada.codigo'), nullable=True)
    tp_grau_academico = db.Column(db.Integer, db.ForeignKey('superior_tp_grau_academico.codigo'), nullable=True)
    in_gratuito = db.Column(db.Boolean, nullable=True)
    tp_modalidade_ensino = db.Column(db.Integer, db.ForeignKey('superior_tp_modal_ensino.codigo'), nullable=True)
    tp_nivel_academico = db.Column(db.Integer, db.ForeignKey('superior_tp_nivel_academico.codigo'), nullable=True)
    # Vagas
    qt_curso = db.Column(db.Integer, nullable=True)
    qt_vg_total = db.Column(db.Integer, nullable=True)
    qt_vg_total_diurno = db.Column(db.Integer, nullable=True)
    qt_vg_total_noturno = db.Column(db.Integer, nullable=True)
    qt_vg_total_ead = db.Column(db.Integer, nullable=True)
    qt_vg_nova = db.Column(db.Integer, nullable=True)
    qt_vg_proc_seletivo = db.Column(db.Integer, nullable=True)
    qt_vg_remanesc = db.Column(db.Integer, nullable=True)
    qt_vg_prog_especial = db.Column(db.Integer, nullable=True)
    # Inscricoes
    qt_inscrito_total = db.Column(db.Integer, nullable=True)
    qt_inscrito_total_diurno = db.Column(db.Integer, nullable=True)
    qt_inscrito_total_noturno = db.Column(db.Integer, nullable=True)
    qt_inscrito_total_ead = db.Column(db.Integer, nullable=True)
    qt_insc_vg_nova = db.Column(db.Integer, nullable=True)
    qt_insc_proc_seletivo = db.Column(db.Integer, nullable=True)
    qt_insc_vg_remanesc = db.Column(db.Integer, nullable=True)
    qt_insc_vg_prog_especial = db.Column(db.Integer, nullable=True)
    # Ingressantes
    qt_ing = db.Column(db.Integer, nullable=True)
    qt_ing_fem = db.Column(db.Integer, nullable=True)
    qt_ing_masc = db.Column(db.Integer, nullable=True)
    qt_ing_diurno = db.Column(db.Integer, nullable=True)
    qt_ing_noturno = db.Column(db.Integer, nullable=True)
    qt_ing_vg_nova = db.Column(db.Integer, nullable=True)
    qt_ing_vestibular = db.Column(db.Integer, nullable=True)
    qt_ing_enem = db.Column(db.Integer, nullable=True)
    qt_ing_avaliacao_seriada = db.Column(db.Integer, nullable=True)
    qt_ing_selecao_simplifica = db.Column(db.Integer, nullable=True)
    qt_ing_egr = db.Column(db.Integer, nullable=True)
    qt_ing_outro_tipo_selecao = db.Column(db.Integer, nullable=True)
    qt_ing_proc_seletivo = db.Column(db.Integer, nullable=True)
    qt_ing_vg_remanesc = db.Column(db.Integer, nullable=True)
    qt_ing_vg_prog_especial = db.Column(db.Integer, nullable=True)
    qt_ing_outra_forma = db.Column(db.Integer, nullable=True)
    qt_ing_0_17 = db.Column(db.Integer, nullable=True)
    qt_ing_18_24 = db.Column(db.Integer, nullable=True)
    qt_ing_25_29 = db.Column(db.Integer, nullable=True)
    qt_ing_30_34 = db.Column(db.Integer, nullable=True)
    qt_ing_35_39 = db.Column(db.Integer, nullable=True)
    qt_ing_40_49 = db.Column(db.Integer, nullable=True)
    qt_ing_50_59 = db.Column(db.Integer, nullable=True)
    qt_ing_60_mais = db.Column(db.Integer, nullable=True)
    qt_ing_branca = db.Column(db.Integer, nullable=True)
    qt_ing_preta = db.Column(db.Integer, nullable=True)
    qt_ing_parda = db.Column(db.Integer, nullable=True)
    qt_ing_amarela = db.Column(db.Integer, nullable=True)
    qt_ing_indigena = db.Column(db.Integer, nullable=True)
    qt_ing_cornd = db.Column(db.Integer, nullable=True)
    # Matriculados
    qt_mat = db.Column(db.Integer, nullable=True)
    qt_mat_fem = db.Column(db.Integer, nullable=True)
    qt_mat_masc = db.Column(db.Integer, nullable=True)
    qt_mat_diurno = db.Column(db.Integer, nullable=True)
    qt_mat_noturno = db.Column(db.Integer, nullable=True)
    qt_mat_0_17 = db.Column(db.Integer, nullable=True)
    qt_mat_18_24 = db.Column(db.Integer, nullable=True)
    qt_mat_25_29 = db.Column(db.Integer, nullable=True)
    qt_mat_30_34 = db.Column(db.Integer, nullable=True)
    qt_mat_35_39 = db.Column(db.Integer, nullable=True)
    qt_mat_40_49 = db.Column(db.Integer, nullable=True)
    qt_mat_50_59 = db.Column(db.Integer, nullable=True)
    qt_mat_60_mais = db.Column(db.Integer, nullable=True)
    qt_mat_branca = db.Column(db.Integer, nullable=True)
    qt_mat_preta = db.Column(db.Integer, nullable=True)
    qt_mat_parda = db.Column(db.Integer, nullable=True)
    qt_mat_amarela = db.Column(db.Integer, nullable=True)
    qt_mat_indigena = db.Column(db.Integer, nullable=True)
    qt_mat_cornd = db.Column(db.Integer, nullable=True)
    # Concluintes
    qt_conc = db.Column(db.Integer, nullable=True)
    qt_conc_fem = db.Column(db.Integer, nullable=True)
    qt_conc_masc = db.Column(db.Integer, nullable=True)
    qt_conc_diurno = db.Column(db.Integer, nullable=True)
    qt_conc_noturno = db.Column(db.Integer, nullable=True)
    qt_conc_0_17 = db.Column(db.Integer, nullable=True)
    qt_conc_18_24 = db.Column(db.Integer, nullable=True)
    qt_conc_25_29 = db.Column(db.Integer, nullable=True)
    qt_conc_30_34 = db.Column(db.Integer, nullable=True)
    qt_conc_35_39 = db.Column(db.Integer, nullable=True)
    qt_conc_40_49 = db.Column(db.Integer, nullable=True)
    qt_conc_50_59 = db.Column(db.Integer, nullable=True)
    qt_conc_60_mais = db.Column(db.Integer, nullable=True)
    qt_conc_branca = db.Column(db.Integer, nullable=True)
    qt_conc_preta = db.Column(db.Integer, nullable=True)
    qt_conc_parda = db.Column(db.Integer, nullable=True)
    qt_conc_amarela = db.Column(db.Integer, nullable=True)
    qt_conc_indigena = db.Column(db.Integer, nullable=True)
    qt_conc_cornd = db.Column(db.Integer, nullable=True)
    # Nacionalidade e deficiencia
    qt_ing_nacbras = db.Column(db.Integer, nullable=True)
    qt_ing_nacestrang = db.Column(db.Integer, nullable=True)
    qt_mat_nacbras = db.Column(db.Integer, nullable=True)
    qt_mat_nacestrang = db.Column(db.Integer, nullable=True)
    qt_conc_nacbras = db.Column(db.Integer, nullable=True)
    qt_conc_nacestrang = db.Column(db.Integer, nullable=True)
    qt_aluno_deficiente = db.Column(db.Integer, nullable=True)
    qt_ing_deficiente = db.Column(db.Integer, nullable=True)
    qt_mat_deficiente = db.Column(db.Integer, nullable=True)
    qt_conc_deficiente = db.Column(db.Integer, nullable=True)
    # Financiamento
    qt_ing_financ = db.Column(db.Integer, nullable=True)
    qt_ing_financ_reemb = db.Column(db.Integer, nullable=True)
    qt_ing_fies = db.Column(db.Integer, nullable=True)
    qt_ing_rpfies = db.Column(db.Integer, nullable=True)
    qt_ing_financ_reemb_outros = db.Column(db.Integer, nullable=True)
    qt_ing_financ_nreemb = db.Column(db.Integer, nullable=True)
    qt_ing_prounii = db.Column(db.Integer, nullable=True)
    qt_ing_prounip = db.Column(db.Integer, nullable=True)
    qt_ing_nrpfies = db.Column(db.Integer, nullable=True)
    qt_ing_financ_nreemb_outros = db.Column(db.Integer, nullable=True)
    qt_mat_financ = db.Column(db.Integer, nullable=True)
    qt_mat_financ_reemb = db.Column(db.Integer, nullable=True)
    qt_mat_fies = db.Column(db.Integer, nullable=True)
    qt_mat_rpfies = db.Column(db.Integer, nullable=True)
    qt_mat_financ_reemb_outros = db.Column(db.Integer, nullable=True)
    qt_mat_financ_nreemb = db.Column(db.Integer, nullable=True)
    qt_mat_prounii = db.Column(db.Integer, nullable=True)
    qt_mat_prounip = db.Column(db.Integer, nullable=True)
    qt_mat_nrpfies = db.Column(db.Integer, nullable=True)
    qt_mat_financ_nreemb_outros = db.Column(db.Integer, nullable=True)
    qt_conc_financ = db.Column(db.Integer, nullable=True)
    qt_conc_financ_reemb = db.Column(db.Integer, nullable=True)
    qt_conc_fies = db.Column(db.Integer, nullable=True)
    qt_conc_rpfies = db.Column(db.Integer, nullable=True)
    qt_conc_financ_reemb_outros = db.Column(db.Integer, nullable=True)
    qt_conc_financ_nreemb = db.Column(db.Integer, nullable=True)
    qt_conc_prounii = db.Column(db.Integer, nullable=True)
    qt_conc_prounip = db.Column(db.Integer, nullable=True)
    qt_conc_nrpfies = db.Column(db.Integer, nullable=True)
    qt_conc_financ_nreemb_outros = db.Column(db.Integer, nullable=True)
    # Reserva de vagas
    qt_ing_reserva_vaga = db.Column(db.Integer, nullable=True)
    qt_ing_rvredepublica = db.Column(db.Integer, nullable=True)
    qt_ing_rvetnico = db.Column(db.Integer, nullable=True)
    qt_ing_rvpdef = db.Column(db.Integer, nullable=True)
    qt_ing_rvsocial_rf = db.Column(db.Integer, nullable=True)
    qt_ing_rvoutros = db.Column(db.Integer, nullable=True)
    qt_mat_reserva_vaga = db.Column(db.Integer, nullable=True)
    qt_mat_rvredepublica = db.Column(db.Integer, nullable=True)
    qt_mat_rvetnico = db.Column(db.Integer, nullable=True)
    qt_mat_rvpdef = db.Column(db.Integer, nullable=True)
    qt_mat_rvsocial_rf = db.Column(db.Integer, nullable=True)
    qt_mat_rvoutros = db.Column(db.Integer, nullable=True)
    qt_conc_reserva_vaga = db.Column(db.Integer, nullable=True)
    qt_conc_rvredepublica = db.Column(db.Integer, nullable=True)
    qt_conc_rvetnico = db.Column(db.Integer, nullable=True)
    qt_conc_rvpdef = db.Column(db.Integer, nullable=True)
    qt_conc_rvsocial_rf = db.Column(db.Integer, nullable=True)
    qt_conc_rvoutros = db.Column(db.Integer, nullable=True)
    # Situacao
    qt_sit_trancada = db.Column(db.Integer, nullable=True)
    qt_sit_desvinculado = db.Column(db.Integer, nullable=True)
    qt_sit_transferido = db.Column(db.Integer, nullable=True)
    qt_sit_falecido = db.Column(db.Integer, nullable=True)
    # Processo seletivo
    qt_ing_procescpublica = db.Column(db.Integer, nullable=True)
    qt_ing_procescprivada = db.Column(db.Integer, nullable=True)
    qt_ing_procnaoinformada = db.Column(db.Integer, nullable=True)
    qt_mat_procescpublica = db.Column(db.Integer, nullable=True)
    qt_mat_procescprivada = db.Column(db.Integer, nullable=True)
    qt_mat_procnaoinformada = db.Column(db.Integer, nullable=True)
    qt_conc_procescpublica = db.Column(db.Integer, nullable=True)
    qt_conc_procescprivada = db.Column(db.Integer, nullable=True)
    qt_conc_procnaoinformada = db.Column(db.Integer, nullable=True)
    # PARFOR / apoio / mobilidade
    qt_parfor = db.Column(db.Integer, nullable=True)
    qt_ing_parfor = db.Column(db.Integer, nullable=True)
    qt_mat_parfor = db.Column(db.Integer, nullable=True)
    qt_conc_parfor = db.Column(db.Integer, nullable=True)
    qt_apoio_social = db.Column(db.Integer, nullable=True)
    qt_ing_apoio_social = db.Column(db.Integer, nullable=True)
    qt_mat_apoio_social = db.Column(db.Integer, nullable=True)
    qt_conc_apoio_social = db.Column(db.Integer, nullable=True)
    qt_ativ_extracurricular = db.Column(db.Integer, nullable=True)
    qt_ing_ativ_extracurricular = db.Column(db.Integer, nullable=True)
    qt_mat_ativ_extracurricular = db.Column(db.Integer, nullable=True)
    qt_conc_ativ_extracurricular = db.Column(db.Integer, nullable=True)
    qt_mob_academica = db.Column(db.Integer, nullable=True)
    qt_ing_mob_academica = db.Column(db.Integer, nullable=True)
    qt_mat_mob_academica = db.Column(db.Integer, nullable=True)
    qt_conc_mob_academica = db.Column(db.Integer, nullable=True)
    # Reserva especifica (cotas diversas)
    qt_ing_rvppi = db.Column(db.Integer, nullable=True)
    qt_ing_rvquilo = db.Column(db.Integer, nullable=True)
    qt_ing_rvrefu = db.Column(db.Integer, nullable=True)
    qt_ing_rvpovt = db.Column(db.Integer, nullable=True)
    qt_ing_rvidoso = db.Column(db.Integer, nullable=True)
    qt_ing_rvintern = db.Column(db.Integer, nullable=True)
    qt_ing_rvmedal = db.Column(db.Integer, nullable=True)
    qt_ing_rvtrans = db.Column(db.Integer, nullable=True)
    qt_mat_rvppi = db.Column(db.Integer, nullable=True)
    qt_mat_rvquilo = db.Column(db.Integer, nullable=True)
    qt_mat_rvrefu = db.Column(db.Integer, nullable=True)
    qt_mat_rvpovt = db.Column(db.Integer, nullable=True)
    qt_mat_rvidoso = db.Column(db.Integer, nullable=True)
    qt_mat_rvintern = db.Column(db.Integer, nullable=True)
    qt_mat_rvmedal = db.Column(db.Integer, nullable=True)
    qt_mat_rvtrans = db.Column(db.Integer, nullable=True)
    qt_conc_rvppi = db.Column(db.Integer, nullable=True)
    qt_conc_rvquilo = db.Column(db.Integer, nullable=True)
    qt_conc_rvrefu = db.Column(db.Integer, nullable=True)
    qt_conc_rvpovt = db.Column(db.Integer, nullable=True)
    qt_conc_rvidoso = db.Column(db.Integer, nullable=True)
    qt_conc_rvintern = db.Column(db.Integer, nullable=True)
    qt_conc_rvmedal = db.Column(db.Integer, nullable=True)
    qt_conc_rvtrans = db.Column(db.Integer, nullable=True)


# ---------------------------------------------------------------------------
# Censo da Educacao Superior (agregado por IES/curso/area)
# ---------------------------------------------------------------------------

class Censo_es(db.Model):
    __tablename__ = 'superior_censo_es'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    ano_censo = db.Column(db.Integer, nullable=True)
    regiao = db.Column(db.Integer, db.ForeignKey('comum_regiao.codigo'), nullable=True)
    estado = db.Column(db.String(2), db.ForeignKey('comum_uf.sigla'), nullable=True)
    municipio = db.Column(db.String(12), db.ForeignKey('comum_municipio.codigo'), nullable=True)
    dimensao = db.Column(db.Integer, db.ForeignKey('superior_tp_dimensao.codigo'), nullable=True)
    org_academica = db.Column(db.Integer, db.ForeignKey('superior_tp_organizacao_academica.codigo'), nullable=True)
    categoria = db.Column(db.Integer, db.ForeignKey('superior_tp_categoria_administrativa.codigo'), nullable=True)
    tp_rede = db.Column(db.Integer, db.ForeignKey('superior_tp_rede.codigo'), nullable=True)
    ies = db.Column(db.Integer, db.ForeignKey('superior_ies.codigo'), nullable=True)
    curso = db.Column(db.Integer, db.ForeignKey('superior_curso.codigo'), nullable=True)
    cine_rotulo = db.Column(db.String(10), db.ForeignKey('superior_cine_rotulo.codigo'), nullable=True)
    area_geral = db.Column(db.Integer, db.ForeignKey('superior_area.codigo'), nullable=True)
    area_especifica = db.Column(db.Integer, db.ForeignKey('superior_area_especifica.codigo'), nullable=True)
    area_detalhada = db.Column(db.Integer, db.ForeignKey('superior_area_detalhada.codigo'), nullable=True)
    tp_grau_academico = db.Column(db.Integer, db.ForeignKey('superior_tp_grau_academico.codigo'), nullable=True)
    in_gratuito = db.Column(db.Boolean, nullable=True)
    tp_modalidade_ensino = db.Column(db.Integer, db.ForeignKey('superior_tp_modal_ensino.codigo'), nullable=True)
    tp_nivel_academico = db.Column(db.Integer, db.ForeignKey('superior_tp_nivel_academico.codigo'), nullable=True)
    # Vagas
    qt_curso = db.Column(db.Integer, nullable=True)
    qt_vg_total = db.Column(db.Integer, nullable=True)
    qt_vg_total_diurno = db.Column(db.Integer, nullable=True)
    qt_vg_total_noturno = db.Column(db.Integer, nullable=True)
    qt_vg_total_ead = db.Column(db.Integer, nullable=True)
    # Ingressantes
    qt_ing = db.Column(db.Integer, nullable=True)
    qt_ing_fem = db.Column(db.Integer, nullable=True)
    qt_ing_masc = db.Column(db.Integer, nullable=True)
    qt_ing_diurno = db.Column(db.Integer, nullable=True)
    qt_ing_noturno = db.Column(db.Integer, nullable=True)
    qt_ing_vestibular = db.Column(db.Integer, nullable=True)
    qt_ing_enem = db.Column(db.Integer, nullable=True)
    qt_ing_0_24 = db.Column(db.Integer, nullable=True)
    qt_ing_25_29 = db.Column(db.Integer, nullable=True)
    qt_ing_30_49 = db.Column(db.Integer, nullable=True)
    qt_ing_50_mais = db.Column(db.Integer, nullable=True)
    qt_ing_branca = db.Column(db.Integer, nullable=True)
    qt_ing_preta = db.Column(db.Integer, nullable=True)
    qt_ing_parda = db.Column(db.Integer, nullable=True)
    qt_ing_amarela = db.Column(db.Integer, nullable=True)
    qt_ing_indigena = db.Column(db.Integer, nullable=True)
    qt_ing_cornd = db.Column(db.Integer, nullable=True)
    qt_ing_nacbras = db.Column(db.Integer, nullable=True)
    qt_ing_nacestrang = db.Column(db.Integer, nullable=True)
    qt_ing_financ = db.Column(db.Integer, nullable=True)
    qt_ing_financ_reemb = db.Column(db.Integer, nullable=True)
    qt_ing_fies = db.Column(db.Integer, nullable=True)
    qt_ing_rpfies = db.Column(db.Integer, nullable=True)
    qt_ing_financ_reemb_outros = db.Column(db.Integer, nullable=True)
    qt_ing_financ_nreemb = db.Column(db.Integer, nullable=True)
    qt_ing_prounii = db.Column(db.Integer, nullable=True)
    qt_ing_prounip = db.Column(db.Integer, nullable=True)
    qt_ing_nrpfies = db.Column(db.Integer, nullable=True)
    qt_ing_financ_nreemb_outros = db.Column(db.Integer, nullable=True)
    qt_ing_reserva_vaga = db.Column(db.Integer, nullable=True)
    qt_ing_rvredepublica = db.Column(db.Integer, nullable=True)
    qt_ing_rvetnico = db.Column(db.Integer, nullable=True)
    qt_ing_rvpdef = db.Column(db.Integer, nullable=True)
    qt_ing_rvsocial_rf = db.Column(db.Integer, nullable=True)
    qt_ing_rvoutros = db.Column(db.Integer, nullable=True)
    qt_ing_deficiente = db.Column(db.Integer, nullable=True)
    qt_ing_procescpublica = db.Column(db.Integer, nullable=True)
    qt_ing_procescprivada = db.Column(db.Integer, nullable=True)
    qt_ing_procnaoinformada = db.Column(db.Integer, nullable=True)
    qt_ing_mob_academica = db.Column(db.Integer, nullable=True)
    # Matriculados
    qt_mat = db.Column(db.Integer, nullable=True)
    qt_mat_fem = db.Column(db.Integer, nullable=True)
    qt_mat_masc = db.Column(db.Integer, nullable=True)
    qt_mat_diurno = db.Column(db.Integer, nullable=True)
    qt_mat_noturno = db.Column(db.Integer, nullable=True)
    qt_mat_0_24 = db.Column(db.Integer, nullable=True)
    qt_mat_25_29 = db.Column(db.Integer, nullable=True)
    qt_mat_30_49 = db.Column(db.Integer, nullable=True)
    qt_mat_50_mais = db.Column(db.Integer, nullable=True)
    qt_mat_branca = db.Column(db.Integer, nullable=True)
    qt_mat_preta = db.Column(db.Integer, nullable=True)
    qt_mat_parda = db.Column(db.Integer, nullable=True)
    qt_mat_amarela = db.Column(db.Integer, nullable=True)
    qt_mat_indigena = db.Column(db.Integer, nullable=True)
    qt_mat_cornd = db.Column(db.Integer, nullable=True)
    qt_mat_nacbras = db.Column(db.Integer, nullable=True)
    qt_mat_nacestrang = db.Column(db.Integer, nullable=True)
    qt_mat_deficiente = db.Column(db.Integer, nullable=True)
    qt_mat_financ = db.Column(db.Integer, nullable=True)
    qt_mat_financ_reemb = db.Column(db.Integer, nullable=True)
    qt_mat_fies = db.Column(db.Integer, nullable=True)
    qt_mat_rpfies = db.Column(db.Integer, nullable=True)
    qt_mat_financ_reemb_outros = db.Column(db.Integer, nullable=True)
    qt_mat_financ_nreemb = db.Column(db.Integer, nullable=True)
    qt_mat_prounii = db.Column(db.Integer, nullable=True)
    qt_mat_prounip = db.Column(db.Integer, nullable=True)
    qt_mat_nrpfies = db.Column(db.Integer, nullable=True)
    qt_mat_financ_nreemb_outros = db.Column(db.Integer, nullable=True)
    qt_mat_reserva_vaga = db.Column(db.Integer, nullable=True)
    qt_mat_rvredepublica = db.Column(db.Integer, nullable=True)
    qt_mat_rvetnico = db.Column(db.Integer, nullable=True)
    qt_mat_rvpdef = db.Column(db.Integer, nullable=True)
    qt_mat_rvsocial_rf = db.Column(db.Integer, nullable=True)
    qt_mat_rvoutros = db.Column(db.Integer, nullable=True)
    qt_mat_procescpublica = db.Column(db.Integer, nullable=True)
    qt_mat_procescprivada = db.Column(db.Integer, nullable=True)
    qt_mat_procnaoinformada = db.Column(db.Integer, nullable=True)
    qt_mat_mob_academica = db.Column(db.Integer, nullable=True)
    # Concluintes
    qt_conc = db.Column(db.Integer, nullable=True)
    qt_conc_fem = db.Column(db.Integer, nullable=True)
    qt_conc_masc = db.Column(db.Integer, nullable=True)
    qt_conc_diurno = db.Column(db.Integer, nullable=True)
    qt_conc_noturno = db.Column(db.Integer, nullable=True)
    qt_conc_0_24 = db.Column(db.Integer, nullable=True)
    qt_conc_25_29 = db.Column(db.Integer, nullable=True)
    qt_conc_30_49 = db.Column(db.Integer, nullable=True)
    qt_conc_50_mais = db.Column(db.Integer, nullable=True)
    qt_conc_branca = db.Column(db.Integer, nullable=True)
    qt_conc_preta = db.Column(db.Integer, nullable=True)
    qt_conc_parda = db.Column(db.Integer, nullable=True)
    qt_conc_amarela = db.Column(db.Integer, nullable=True)
    qt_conc_indigena = db.Column(db.Integer, nullable=True)
    qt_conc_cornd = db.Column(db.Integer, nullable=True)
    qt_conc_nacbras = db.Column(db.Integer, nullable=True)
    qt_conc_nacestrang = db.Column(db.Integer, nullable=True)
    qt_conc_deficiente = db.Column(db.Integer, nullable=True)
    qt_conc_financ = db.Column(db.Integer, nullable=True)
    qt_conc_financ_reemb = db.Column(db.Integer, nullable=True)
    qt_conc_fies = db.Column(db.Integer, nullable=True)
    qt_conc_rpfies = db.Column(db.Integer, nullable=True)
    qt_conc_financ_reemb_outros = db.Column(db.Integer, nullable=True)
    qt_conc_financ_nreemb = db.Column(db.Integer, nullable=True)
    qt_conc_prounii = db.Column(db.Integer, nullable=True)
    qt_conc_prounip = db.Column(db.Integer, nullable=True)
    qt_conc_nrpfies = db.Column(db.Integer, nullable=True)
    qt_conc_financ_nreemb_outros = db.Column(db.Integer, nullable=True)
    qt_conc_reserva_vaga = db.Column(db.Integer, nullable=True)
    qt_conc_rvredepublica = db.Column(db.Integer, nullable=True)
    qt_conc_rvetnico = db.Column(db.Integer, nullable=True)
    qt_conc_rvpdef = db.Column(db.Integer, nullable=True)
    qt_conc_rvsocial_rf = db.Column(db.Integer, nullable=True)
    qt_conc_rvoutros = db.Column(db.Integer, nullable=True)
    qt_conc_procescpublica = db.Column(db.Integer, nullable=True)
    qt_conc_procescprivada = db.Column(db.Integer, nullable=True)
    qt_conc_procnaoinformada = db.Column(db.Integer, nullable=True)
    # Situacao
    qt_sit_trancada = db.Column(db.Integer, nullable=True)
    qt_sit_desvinculado = db.Column(db.Integer, nullable=True)
    qt_sit_transferido = db.Column(db.Integer, nullable=True)
    qt_sit_falecido = db.Column(db.Integer, nullable=True)
    qt_aluno_deficiente = db.Column(db.Integer, nullable=True)
    qt_mob_academica = db.Column(db.Integer, nullable=True)
    qt_conc_mob_academica = db.Column(db.Integer, nullable=True)


# ---------------------------------------------------------------------------
# UAB - Universidade Aberta do Brasil (censo por polo/curso)
# ---------------------------------------------------------------------------

class Uab_censo(db.Model):
    __tablename__ = 'superior_uab_censo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ano_censo = db.Column(db.Integer, nullable=True)
    regiao = db.Column(db.Integer, db.ForeignKey('comum_regiao.codigo'), nullable=True)
    estado = db.Column(db.String(2), db.ForeignKey('comum_uf.sigla'), nullable=True)
    ies = db.Column(db.Integer, db.ForeignKey('superior_ies.codigo'), nullable=True)
    tp_grau_academico = db.Column(db.Integer, db.ForeignKey('superior_tp_grau_academico.codigo'), nullable=True)
    nm_curso = db.Column(db.String(120), nullable=True)
    situacao_oferta = db.Column(db.String(20), nullable=True)
    id_polo = db.Column(db.Integer, nullable=True)
    regiao_polo = db.Column(db.Integer, db.ForeignKey('comum_regiao.codigo'), nullable=True)
    uf_polo = db.Column(db.String(2), db.ForeignKey('comum_uf.sigla'), nullable=True)
    situacao_polo = db.Column(db.String(20), nullable=True)
    nm_polo = db.Column(db.String(50), nullable=True)
    municipio = db.Column(db.String(12), db.ForeignKey('comum_municipio.codigo'), nullable=True)
    qt_cadastrados = db.Column(db.Integer, nullable=True)
    qt_cursando = db.Column(db.Integer, nullable=True)
    qt_desvinculado = db.Column(db.Integer, nullable=True)
    qt_falecido = db.Column(db.Integer, nullable=True)
    qt_formado = db.Column(db.Integer, nullable=True)
    qt_trancado = db.Column(db.Integer, nullable=True)
    qt_desistente = db.Column(db.Integer, nullable=True)
    qt_retido_tcc = db.Column(db.Integer, nullable=True)
    qt_transferido = db.Column(db.Integer, nullable=True)
    qt_nao_concluinte = db.Column(db.Integer, nullable=True)
    qt_matricula_cancelada = db.Column(db.Integer, nullable=True)
    qt_nao_matriculado_semestre = db.Column(db.Integer, nullable=True)
    st_formacao_professores = db.Column(db.String(1), nullable=True)
    id_nivel_academico = db.Column(db.Integer, db.ForeignKey('superior_tp_nivel_academico.codigo'), nullable=True)


# ---------------------------------------------------------------------------
# Tabelas auxiliares de IES nao identificadas na carga UAB
# ---------------------------------------------------------------------------

class Ies_nao_ident(db.Model):
    __tablename__ = 'superior_ies_nao_ident'
    nm_ies = db.Column(db.Text, primary_key=True)
    ies = db.Column(db.Integer, nullable=True)


class Registros_ies_nao_ident(db.Model):
    __tablename__ = 'superior_registros_ies_nao_ident'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_uab_censo = db.Column(db.Integer, nullable=True)
    nm_ies = db.Column(db.Text, nullable=True)
    nm_polo = db.Column(db.Text, nullable=True)
    status = db.Column(db.Text, nullable=True)

