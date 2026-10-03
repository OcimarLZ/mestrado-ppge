p = 'build4.py'
s = open(p, encoding='utf-8').read()
blk = open('aff_block.py', encoding='utf-8').read()
marker = "# ---------------------------------------------------------------- consolidado"
assert marker in s and "AFF_ROWS" not in s
call = '''
write_theme("Políticas afirmativas e apoio", "Políticas afirmativas e de apoio social – transferência de renda, assistência estudantil e igualdade racial",
            "Subdivisões: PA.1 transferência de renda; PA.2 BPC; PA.3–PA.5 assistência estudantil; PA.6 igualdade racial; PA.7–PA.8 outros apoios; PA.9 subtotal.",
            AFF_ROWS, ["Agrupamento definido para a análise da dissertação: programas de transferência de renda e de permanência estudantil ao lado das ações de igualdade racial.",
                       "Fontes com critérios distintos (Portal = pago do exercício por ação; RTN = caixa) não são somadas; o subtotal PA.9 usa só o Portal.",
                       "Unidades: transferência de renda, BPC, Auxílio Gás e Pé-de-Meia em R$ bilhões; assistência estudantil e igualdade racial em R$ milhões.",
                       "Mandatos: 2016 (Dilma/Temer), 2019 e 2022 (Bolsonaro), 2025 (Lula III)."])

'''
s = s.replace(marker, blk + call + marker, 1)
s = s.replace(marker, """_i = [c[0] for c in CONS].index("34b") + 1
CONS[_i:_i] = [("34c", "Transferência de renda – Bolsa Família/Auxílio Brasil (pago)", "bf_pago"), ("34d", "BPC/LOAS (pago, RTN)", "bpc_aff"),
               ("34e", "Assistência estudantil – PNAES (pago)", "pnaes_pago"), ("34f", "Políticas afirmativas e de apoio – subtotal pago", "aff_sub")]
""" + marker, 1)
old2 = 'ALLR = {r["id"]: r for lst in ALL_LISTS for r in lst}'
assert old2 in s
s = s.replace(old2, 'ALLR = {r["id"]: r for lst in ALL_LISTS + [AFF_ROWS] for r in lst}')
old3 = ' ("Taxa média de desocupação", "desoc", ""),'
assert old3 in s
s = s.replace(old3, ' ("Bolsa Família / Auxílio Brasil pago (R$ bi)", "bf_pago", "Auxílio Brasil em 2022; novo Bolsa Família em 2025."),\n' + old3)
open(p, 'w', encoding='utf-8').write(s)
print("patched")
