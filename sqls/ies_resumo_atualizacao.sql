WITH ead_proprio AS (
    -- Conta polos (municipios únicos) e cursos (códigos únicos) EaD Próprios
    SELECT cc.ies, 
           COUNT(DISTINCT cc.municipio) AS qt_polos,
           COUNT(DISTINCT cc.curso) AS qt_cursos
    FROM curso_censo cc
    JOIN curso c ON c.codigo = cc.curso
    WHERE cc.ano_censo = 2024 
      AND cc.tp_grau_academico = 2 
      AND cc.tp_modalidade_ensino = 2 
      AND c.fl_uab = 'N'
    GROUP BY cc.ies
),
uab_polos AS (
    -- Conta polos (municipios únicos) UAB usando a união de uab_censo e curso_censo (fl_uab='S')
    SELECT ies, COUNT(DISTINCT municipio) AS qt_polos
    FROM (
        SELECT ies, municipio 
        FROM uab_censo 
        WHERE ano_censo = 2024 AND tp_grau_academico = 2
        UNION
        SELECT cc.ies, cc.municipio 
        FROM curso_censo cc
        JOIN curso c ON c.codigo = cc.curso
        WHERE cc.ano_censo = 2024 AND cc.tp_grau_academico = 2 AND cc.tp_modalidade_ensino = 2 AND c.fl_uab = 'S'
    ) AS u
    GROUP BY ies
),
uab_cursos AS (
    -- Conta cursos (códigos únicos) UAB a partir do curso_censo
    SELECT cc.ies, COUNT(DISTINCT cc.curso) AS qt_cursos
    FROM curso_censo cc
    JOIN curso c ON c.codigo = cc.curso
    WHERE cc.ano_censo = 2024 
      AND cc.tp_grau_academico = 2 
      AND cc.tp_modalidade_ensino = 2 
      AND c.fl_uab = 'S'
    GROUP BY cc.ies
)
SELECT 
    i.sigla AS "Sigla IES",
    COALESCE(p.qt_polos, 0) + COALESCE(up.qt_polos, 0) AS "Coluna E (Total Polos EaD)",
    COALESCE(p.qt_polos, 0) AS "Coluna G (Polos EaD Próprios)",
    COALESCE(p.qt_cursos, 0) AS "Coluna H (Cursos EaD Próprios)",
    COALESCE(up.qt_polos, 0) AS "Coluna J (Polos UAB)",
    COALESCE(uc.qt_cursos, 0) AS "Coluna K (Cursos EaD UAB)"
FROM ies i
LEFT JOIN ead_proprio p ON i.codigo = p.ies
LEFT JOIN uab_polos up ON i.codigo = up.ies
LEFT JOIN uab_cursos uc ON i.codigo = uc.ies
WHERE i.categoria = 1 AND i.org_academica = 1 AND i.sigla <> '-'
ORDER BY i.sigla;
