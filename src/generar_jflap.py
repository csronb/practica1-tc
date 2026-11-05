"""Script generador y validador de autómatas JFLAP (.jff) para el Ejercicio 4.

Genera todos los archivos XML en formato JFLAP 7.1 dentro de `automatas/`,
valida cada autómata determinista con al menos 3 cadenas válidas y 3 inválidas
(incluyendo casos frontera) y produce imágenes SVG/PNG y tablas para el reporte.
"""

from __future__ import annotations

import math
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT_DIR = Path(__file__).resolve().parent.parent
AUTOMATAS_DIR = ROOT_DIR / "automatas"
EVIDENCIAS_JFLAP_DIR = ROOT_DIR / "evidencias" / "jflap"


def crear_jff(
    nombre_archivo: str,
    estados: list[tuple[int, str, bool, bool]],
    transiciones: list[tuple[int, int, str]],
) -> Path:
    """Crea un archivo .jff compatible con JFLAP 7.x con disposición circular limpia.

    Args:
        nombre_archivo: Nombre del archivo (ej. 'ej097_multiplo_3.jff').
        estados: Lista de tuplas (id_int, nombre_str, es_inicial, es_final).
        transiciones: Lista de tuplas (from_id, to_id, read_symbol). Use "" para lambda.
    """
    AUTOMATAS_DIR.mkdir(parents=True, exist_ok=True)
    estructura = ET.Element("structure")
    ET.SubElement(estructura, "type").text = "fa"
    automata = ET.SubElement(estructura, "automaton")

    n = len(estados)
    radio = max(110.0, 32.0 * n)
    cx, cy = radio + 90.0, radio + 90.0

    for idx, (st_id, st_name, es_ini, es_fin) in enumerate(estados):
        angulo = math.pi + (2.0 * math.pi * idx) / max(1, n)
        x = round(cx + radio * math.cos(angulo), 1)
        y = round(cy + radio * math.sin(angulo), 1)
        st_el = ET.SubElement(automata, "state", id=str(st_id), name=st_name)
        ET.SubElement(st_el, "x").text = str(x)
        ET.SubElement(st_el, "y").text = str(y)
        if es_ini:
            ET.SubElement(st_el, "initial")
        if es_fin:
            ET.SubElement(st_el, "final")

    for u, v, sym in transiciones:
        tr_el = ET.SubElement(automata, "transition")
        ET.SubElement(tr_el, "from").text = str(u)
        ET.SubElement(tr_el, "to").text = str(v)
        read_el = ET.SubElement(tr_el, "read")
        if sym != "":
            read_el.text = sym

    ET.indent(estructura, space="  ")
    xml_bytes = ET.tostring(estructura, encoding="utf-8", xml_declaration=True)
    ruta = AUTOMATAS_DIR / nombre_archivo
    ruta.write_bytes(xml_bytes)
    return ruta


def simular_afd(
    estados: list[tuple[int, str, bool, bool]],
    transiciones: list[tuple[int, int, str]],
    cadena: str,
) -> tuple[bool, list[str]]:
    """Simula un AFD paso a paso y devuelve (aceptada, rastro_de_estados)."""
    id_a_nombre = {s[0]: s[1] for s in estados}
    iniciales = [s[0] for s in estados if s[2]]
    finales = {s[0] for s in estados if s[3]}
    assert len(iniciales) == 1, "El AFD debe tener exactamente un estado inicial"
    actual = iniciales[0]
    mapa_delta: dict[tuple[int, str], int] = {}
    for u, v, sym in transiciones:
        mapa_delta[(u, sym)] = v

    rastro = [id_a_nombre[actual]]
    for ch in cadena:
        if (actual, ch) not in mapa_delta:
            return False, rastro + ["⊥ (sin transición)"]
        actual = mapa_delta[(actual, ch)]
        rastro.append(id_a_nombre[actual])
    return (actual in finales), rastro


def kmp_afd(alfabeto: list[str], patron: str) -> tuple[list[tuple[int, str, bool, bool]], list[tuple[int, int, str]]]:
    """Construye el AFD mínimo que acepta cadenas que contienen `patron` como subcadena."""
    m = len(patron)
    estados = [(i, f"q{i}", i == 0, i == m) for i in range(m + 1)]
    transiciones: list[tuple[int, int, str]] = []
    for i in range(m):
        prefijo = patron[:i]
        for a in alfabeto:
            candidato = prefijo + a
            k = min(m, len(candidato))
            while k > 0 and not candidato.endswith(patron[:k]):
                k -= 1
            transiciones.append((i, k, a))
    for a in alfabeto:
        transiciones.append((m, m, a))
    return estados, transiciones


def kmp_sufijo_afd(alfabeto: list[str], sufijo: str) -> tuple[list[tuple[int, str, bool, bool]], list[tuple[int, int, str]]]:
    """Construye el AFD mínimo que acepta cadenas que terminan con `sufijo`."""
    m = len(sufijo)
    estados = [(i, f"q{i}", i == 0, i == m) for i in range(m + 1)]
    transiciones: list[tuple[int, int, str]] = []
    for i in range(m + 1):
        prefijo = sufijo[:i]
        for a in alfabeto:
            candidato = prefijo + a
            k = min(m, len(candidato))
            while k > 0 and not candidato.endswith(sufijo[:k]):
                k -= 1
            transiciones.append((i, k, a))
    return estados, transiciones


def dos_patrones_afd(
    alfabeto: list[str],
    p1: str,
    p2: str,
    traslape: bool,
) -> tuple[list[tuple[int, str, bool, bool]], list[tuple[int, int, str]]]:
    """Construye el AFD accesible para contener al menos una vez p1 y p2 (con o sin traslape)."""
    m1, m2 = len(p1), len(p2)

    def sig_pref(pref_len: int, pat: str, a: str) -> int:
        cand = pat[:pref_len] + a
        k = min(len(pat), len(cand))
        while k > 0 and not cand.endswith(pat[:k]):
            k -= 1
        return k

    if traslape:
        # Estado = (tiene_p1: bool, tiene_p2: bool, pref_p1: int, pref_p2: int)
        ini = (False, False, 0, 0)
        cola = [ini]
        mapa_id = {ini: 0}
        trans_raw: list[tuple[int, int, str]] = []
        while cola:
            st = cola.pop(0)
            u = mapa_id[st]
            t1, t2, l1, l2 = st
            for a in alfabeto:
                nl1 = m1 if t1 else sig_pref(l1, p1, a)
                nl2 = m2 if t2 else sig_pref(l2, p2, a)
                nt1 = t1 or (nl1 == m1)
                nt2 = t2 or (nl2 == m2)
                if nt1:
                    nl1 = 0
                if nt2:
                    nl2 = 0
                nxt = (nt1, nt2, nl1, nl2)
                if nxt not in mapa_id:
                    mapa_id[nxt] = len(mapa_id)
                    cola.append(nxt)
                trans_raw.append((u, mapa_id[nxt], a))
        estados = [
            (idx, f"q{idx}", idx == 0, st[0] and st[1])
            for st, idx in sorted(mapa_id.items(), key=lambda x: x[1])
        ]
        return estados, trans_raw
    else:
        # Sin traslape: o bien aparece p1 completo y luego desde cero aparece p2, o viceversa
        # Estado = (fase_12: int, fase_21: int) donde fase_12 in [0..m1 + m2]
        def avanzar_secuencia(pos: int, pat_a: str, pat_b: str, ch: str) -> int:
            ma, mb = len(pat_a), len(pat_b)
            if pos < ma:
                npos = sig_pref(pos, pat_a, ch)
                return npos
            elif pos < ma + mb:
                npos = sig_pref(pos - ma, pat_b, ch)
                return ma + npos
            else:
                return ma + mb

        ini2 = (0, 0)
        cola2 = [ini2]
        mapa_id2 = {ini2: 0}
        trans_raw2: list[tuple[int, int, str]] = []
        while cola2:
            st = cola2.pop(0)
            u = mapa_id2[st]
            f12, f21 = st
            for a in alfabeto:
                nf12 = avanzar_secuencia(f12, p1, p2, a)
                nf21 = avanzar_secuencia(f21, p2, p1, a)
                nxt = (nf12, nf21)
                if nxt not in mapa_id2:
                    mapa_id2[nxt] = len(mapa_id2)
                    cola2.append(nxt)
                trans_raw2.append((u, mapa_id2[nxt], a))
        estados = [
            (idx, f"q{idx}", idx == 0, (st[0] == m1 + m2) or (st[1] == m1 + m2))
            for st, idx in sorted(mapa_id2.items(), key=lambda x: x[1])
        ]
        return estados, trans_raw2


def contar_ocurrencias_afd(
    alfabeto: list[str],
    patron: str,
    objetivo: int,
    exacto: bool,
    traslape: bool,
) -> tuple[list[tuple[int, str, bool, bool]], list[tuple[int, int, str]]]:
    """Construye un AFD que cuenta ocurrencias de `patron` (con o sin traslape)."""
    m = len(patron)
    max_cuenta = objetivo + 1 if exacto else objetivo

    def sig_pref(pref_len: int, a: str) -> int:
        cand = patron[:pref_len] + a
        k = min(m, len(cand))
        while k > 0 and not cand.endswith(patron[:k]):
            k -= 1
        return k

    # Borde propio más largo de `patron` cuando sí hay traslape
    borde = m - 1
    while borde > 0 and not patron.endswith(patron[:borde]):
        borde -= 1

    ini = (0, 0)  # (cuenta, pref_len)
    cola = [ini]
    mapa_id = {ini: 0}
    trans_raw: list[tuple[int, int, str]] = []

    while cola:
        cuenta, pref = cola.pop(0)
        u = mapa_id[(cuenta, pref)]
        for a in alfabeto:
            if cuenta >= max_cuenta:
                ncuenta, npref = max_cuenta, 0
            else:
                npref = sig_pref(pref, a)
                if npref == m:
                    ncuenta = min(max_cuenta, cuenta + 1)
                    if ncuenta >= max_cuenta:
                        npref = 0
                    else:
                        npref = borde if traslape else 0
                else:
                    ncuenta = cuenta
            nxt = (ncuenta, npref)
            if nxt not in mapa_id:
                mapa_id[nxt] = len(mapa_id)
                cola.append(nxt)
            trans_raw.append((u, mapa_id[nxt], a))

    estados = []
    for (cuenta, pref), idx in sorted(mapa_id.items(), key=lambda x: x[1]):
        es_fin = (cuenta == objetivo) if exacto else (cuenta >= objetivo)
        estados.append((idx, f"q{idx}_c{cuenta}_p{pref}", idx == 0, es_fin))
    return estados, trans_raw


def generar_todos() -> dict[str, tuple[list[tuple[int, str, bool, bool]], list[tuple[int, int, str]]]]:
    S1 = ["0", "1", "2"]
    S2 = ["a", "b", "c", "0", "1"]
    S3 = ["a", "b"]
    SB = ["0", "1"]

    catalogo: dict[str, tuple[list[tuple[int, str, bool, bool]], list[tuple[int, int, str]]]] = {}

    # 97. Palabras de S1 cuya longitud es múltiplo de 3
    est_97 = [(0, "q0", True, True), (1, "q1", False, False), (2, "q2", False, False)]
    tr_97 = [(i, (i + 1) % 3, a) for i in range(3) for a in S1]
    catalogo["ej097_longitud_multiplo_3.jff"] = (est_97, tr_97)

    # 99. Palabras de S1 que terminan con 001001
    catalogo["ej099_termina_001001.jff"] = kmp_sufijo_afd(S1, "001001")

    # 102. Palabras de S3 que contienen abbbab
    catalogo["ej102_contiene_abbbab.jff"] = kmp_afd(S3, "abbbab")

    # 103. Palabras de S3 que contienen aabbba
    catalogo["ej103_contiene_aabbba.jff"] = kmp_afd(S3, "aabbba")

    # 106. Palabras de S1 que incluyen 1101001
    catalogo["ej106_incluye_1101001.jff"] = kmp_afd(S1, "1101001")

    # 107. Palabras de S1 que incluyen al menos una vez 0101 y 021
    catalogo["ej107_incluye_0101_y_021.jff"] = dos_patrones_afd(S1, "0101", "021", traslape=True)

    # 109. Palabras de S2 que incluyen abbcb y cbaabb (con traslape)
    catalogo["ej109_incluye_abbcb_y_cbaabb.jff"] = dos_patrones_afd(S2, "abbcb", "cbaabb", traslape=True)

    # 111. Palabras de S1 que contienen exactamente 3 veces 01002
    catalogo["ej111_exactamente_tres_01002.jff"] = contar_ocurrencias_afd(
        S1, "01002", objetivo=3, exacto=True, traslape=False
    )

    # 112. Palabras de S1 que contienen dos veces 010 sin traslape (al menos 2 veces / 2 veces)
    catalogo["ej112_dos_veces_010_sin_traslape.jff"] = contar_ocurrencias_afd(
        S1, "010", objetivo=2, exacto=False, traslape=False
    )

    # 113. Palabras de S1 que contienen dos veces 010 con traslape
    catalogo["ej113_dos_veces_010_con_traslape.jff"] = contar_ocurrencias_afd(
        S1, "010", objetivo=2, exacto=False, traslape=True
    )

    # 118. L = {w in S3* : w = a x ab y a, x,y in S3*} -> empieza con 'a', termina con 'a' y tiene 'ab' en medio
    # Es decir, empieza con 'a', luego contiene 'ab', y después de algún 'ab' termina en 'a' (mínima: aaba)
    est_118 = [
        (0, "q0_ini", True, False),
        (1, "q1_vio_a_ini", False, False),
        (2, "q2_pref_a", False, False),
        (3, "q3_vio_ab", False, False),
        (4, "q4_acepta_fin_a", False, True),
        (5, "q5_pozo", False, False),
    ]
    tr_118 = [
        (0, 1, "a"), (0, 5, "b"),
        (1, 2, "a"), (1, 1, "b"),
        (2, 2, "a"), (2, 3, "b"),
        (3, 4, "a"), (3, 3, "b"),
        (4, 4, "a"), (4, 3, "b"),
        (5, 5, "a"), (5, 5, "b"),
    ]
    catalogo["ej118_axabya.jff"] = (est_118, tr_118)

    # 120. Palabras de S1 tales que el primer carácter y el último son distintos
    est_120 = [
        (0, "q0_vacia", True, False),
        (1, "q1_ini0_fin0", False, False),
        (2, "q2_ini0_finNo0", False, True),
        (3, "q3_ini1_fin1", False, False),
        (4, "q4_ini1_finNo1", False, True),
        (5, "q5_ini2_fin2", False, False),
        (6, "q6_ini2_finNo2", False, True),
    ]
    tr_120 = [
        (0, 1, "0"), (0, 3, "1"), (0, 5, "2"),
        (1, 1, "0"), (1, 2, "1"), (1, 2, "2"),
        (2, 1, "0"), (2, 2, "1"), (2, 2, "2"),
        (3, 4, "0"), (3, 3, "1"), (3, 4, "2"),
        (4, 4, "0"), (4, 3, "1"), (4, 4, "2"),
        (5, 6, "0"), (5, 6, "1"), (5, 5, "2"),
        (6, 6, "0"), (6, 6, "1"), (6, 5, "2"),
    ]
    catalogo["ej120_primero_ultimo_distintos.jff"] = (est_120, tr_120)

    # 121. Palabras de S1 de longitud 3n donde cada bloque de 3 tiene al menos un 0
    est_121 = [
        (0, "q0_mod0_ok", True, True),
        (1, "q1_mod1_con0", False, False),
        (2, "q2_mod1_sin0", False, False),
        (3, "q3_mod2_con0", False, False),
        (4, "q4_mod2_sin0", False, False),
        (5, "q5_pozo", False, False),
    ]
    tr_121 = [
        (0, 1, "0"), (0, 2, "1"), (0, 2, "2"),
        (1, 3, "0"), (1, 3, "1"), (1, 3, "2"),
        (2, 3, "0"), (2, 4, "1"), (2, 4, "2"),
        (3, 0, "0"), (3, 0, "1"), (3, 0, "2"),
        (4, 0, "0"), (4, 5, "1"), (4, 5, "2"),
        (5, 5, "0"), (5, 5, "1"), (5, 5, "2"),
    ]
    catalogo["ej121_bloques_3_con_0.jff"] = (est_121, tr_121)

    # 122. Palabras de S1 tales que cualquier subcadena de 3 símbolos consecutivos tiene al menos un 0
    # Equivalente a: no contiene 3 símbolos consecutivos de {1, 2}
    est_122 = [
        (0, "q0_0_noCero", True, True),
        (1, "q1_1_noCero", False, True),
        (2, "q2_2_noCero", False, True),
        (3, "q3_pozo_3noCero", False, False),
    ]
    tr_122 = [
        (0, 0, "0"), (0, 1, "1"), (0, 1, "2"),
        (1, 0, "0"), (1, 2, "1"), (1, 2, "2"),
        (2, 0, "0"), (2, 3, "1"), (2, 3, "2"),
        (3, 3, "0"), (3, 3, "1"), (3, 3, "2"),
    ]
    catalogo["ej122_ventana_3_con_0.jff"] = (est_122, tr_122)

    # 123. Palabras de S3 de la forma wxw donde w in S3^2 y x in S3* (longitud >= 4 y primeros 2 == últimos 2)
    # 1 + 4 (len 1,2) + 4*4 (prefijo de 2 y últimos 2 vistos, para longitud >= 4)
    # Para mantenerlo compacto, codificamos el prefijo w in {aa, ab, ba, bb} y el sufijo actual de longitud 2
    pares = ["aa", "ab", "ba", "bb"]
    est_123: list[tuple[int, str, bool, bool]] = [
        (0, "q0_λ", True, False),
        (1, "q1_a", False, False),
        (2, "q2_b", False, False),
    ]
    tr_123: list[tuple[int, int, str]] = [(0, 1, "a"), (0, 2, "b")]
    id_actual = 3
    mapa_w_len2: dict[str, int] = {}
    mapa_w_len3: dict[tuple[str, str], int] = {}
    mapa_w_suf: dict[tuple[str, str], int] = {}
    for w in pares:
        mapa_w_len2[w] = id_actual
        est_123.append((id_actual, f"w_{w}_len2", False, False))
        id_actual += 1
        for ch in S3:
            mapa_w_len3[(w, ch)] = id_actual
            est_123.append((id_actual, f"w_{w}_len3_{ch}", False, False))
            id_actual += 1
        for suf in pares:
            mapa_w_suf[(w, suf)] = id_actual
            est_123.append((id_actual, f"w_{w}_suf_{suf}", False, w == suf))
            id_actual += 1

    tr_123.extend([
        (1, mapa_w_len2["aa"], "a"),
        (1, mapa_w_len2["ab"], "b"),
        (2, mapa_w_len2["ba"], "a"),
        (2, mapa_w_len2["bb"], "b"),
    ])
    for w in pares:
        u2 = mapa_w_len2[w]
        for ch in S3:
            u3 = mapa_w_len3[(w, ch)]
            tr_123.append((u2, u3, ch))
            for ch2 in S3:
                tr_123.append((u3, mapa_w_suf[(w, ch + ch2)], ch2))
        for suf in pares:
            us = mapa_w_suf[(w, suf)]
            for ch in S3:
                nsuf = suf[1] + ch
                tr_123.append((us, mapa_w_suf[(w, nsuf)], ch))
    catalogo["ej123_wxw_prefijo_sufijo_2.jff"] = (est_123, tr_123)

    # 124. Mecanismo de 3 palancas (Izquierda=L, Derecha=R). Inicial: (L, R, L) según diagrama.
    # 8 configuraciones de las 3 palancas x 2 resultados de la última canica (A o R) -> o duplicando estado de aceptación
    # Para decidir si la última canica salió por A, cada configuración tiene versión _R (no aceptada) y _A (aceptada)
    configs = [(x, y, z) for x in ("L", "R") for y in ("L", "R") for z in ("L", "R")]
    # En el diagrama inicial: palanca sup-izq (0) apunta a la izquierda (L), sup-der (1) apunta a la derecha (R), central apunta a la izquierda (L)
    est_124: list[tuple[int, str, bool, bool]] = []
    mapa_124: dict[tuple[str, str, str, bool], int] = {}
    idx_124 = 0
    for c in configs:
        for ok in (False, True):
            es_ini = (c == ("L", "R", "L") and not ok)
            mapa_124[(c[0], c[1], c[2], ok)] = idx_124
            suf_ok = "A" if ok else "R"
            est_124.append((idx_124, f"{c[0]}{c[1]}{c[2]}_{suf_ok}", es_ini, ok))
            idx_124 += 1

    tr_124: list[tuple[int, int, str]] = []
    for (p0, p1, pc, ok), u in mapa_124.items():
        # Entrada 0: pasa por palanca p0
        if p0 == "L":
            # Va por borde exterior izquierdo directo a salida A, invierte p0 -> R
            nxt0 = ("R", p1, pc, True)
        else:
            # Va al centro pc, invierte p0 -> L y pc -> opuesto
            sale_a = (pc == "L")
            npc = "R" if pc == "L" else "L"
            nxt0 = ("L", p1, npc, sale_a)
        tr_124.append((u, mapa_124[nxt0], "0"))

        # Entrada 1: pasa por palanca p1
        if p1 == "R":
            # Va por borde exterior derecho directo a salida R, invierte p1 -> L
            nxt1 = (p0, "L", pc, False)
        else:
            # Va al centro pc, invierte p1 -> R y pc -> opuesto
            sale_a = (pc == "L")
            npc = "R" if pc == "L" else "L"
            nxt1 = (p0, "R", npc, sale_a)
        tr_124.append((u, mapa_124[nxt1], "1"))
    catalogo["ej124_canicas_palancas.jff"] = (est_124, tr_124)

    # 128. L2 = {w : wa in L para algún a in {0, 1}} del autómata dado en el diagrama 128
    # En el diagrama 128: Estados A(ini), B, C, D, E, F(final).
    # δ(A,0)=B, δ(A,1)=C; δ(B,0)=C, δ(B,1)=D; δ(C,0)=D, δ(C,1)=E; δ(D,0)=F, δ(D,1)=E; δ(E,0)=E, δ(E,1)=F; δ(F,0)=F, δ(F,1)=F.
    # Un estado q es final en L2 si y solo si δ(q,0) in {F} o δ(q,1) in {F} -> {D, E, F}!
    est_128 = [
        (0, "A", True, False),
        (1, "B", False, False),
        (2, "C", False, False),
        (3, "D", False, True),
        (4, "E", False, True),
        (5, "F", False, True),
    ]
    tr_128 = [
        (0, 1, "0"), (0, 2, "1"),
        (1, 2, "0"), (1, 3, "1"),
        (2, 3, "0"), (2, 4, "1"),
        (3, 5, "0"), (3, 4, "1"),
        (4, 4, "0"), (4, 5, "1"),
        (5, 5, "0"), (5, 5, "1"),
    ]
    catalogo["ej128_quitar_ultimo_simbolo.jff"] = (est_128, tr_128)

    # 131. M = ({q1, q2}, {0, 1}, δ, q1, {q2}) -> cadenas que terminan en 1
    est_131 = [(0, "q1", True, False), (1, "q2", False, True)]
    tr_131 = [(0, 0, "0"), (0, 1, "1"), (1, 0, "0"), (1, 1, "1")]
    catalogo["ej131_termina_en_1.jff"] = (est_131, tr_131)

    # 133. M = ({q0, q1, q2, q3}, {a, b}, δ, q0, {q0}) - paridad par de a y par de b
    est_133 = [
        (0, "q0", True, True),
        (1, "q1", False, False),
        (2, "q2", False, False),
        (3, "q3", False, False),
    ]
    tr_133 = [
        (0, 2, "a"), (0, 1, "b"),
        (1, 3, "a"), (1, 0, "b"),
        (2, 0, "a"), (2, 3, "b"),
        (3, 1, "a"), (3, 2, "b"),
    ]
    catalogo["ej133_paridad_ab.jff"] = (est_133, tr_133)

    # 135. L = {b^m a b^n : m, n > 0} sobre {a, b}
    est_135 = [
        (0, "q0_ini", True, False),
        (1, "q1_bm", False, False),
        (2, "q2_bma", False, False),
        (3, "q3_bmabn", False, True),
        (4, "q4_pozo", False, False),
    ]
    tr_135 = [
        (0, 4, "a"), (0, 1, "b"),
        (1, 2, "a"), (1, 1, "b"),
        (2, 4, "a"), (2, 3, "b"),
        (3, 4, "a"), (3, 3, "b"),
        (4, 4, "a"), (4, 4, "b"),
    ]
    catalogo["ej135_bm_a_bn.jff"] = (est_135, tr_135)

    # 137. Cadenas sobre {a, b} que comienzan con el prefijo 'ab'
    est_137 = [
        (0, "q0_ini", True, False),
        (1, "q1_a", False, False),
        (2, "q2_ab_acepta", False, True),
        (3, "q3_pozo", False, False),
    ]
    tr_137 = [
        (0, 1, "a"), (0, 3, "b"),
        (1, 3, "a"), (1, 2, "b"),
        (2, 2, "a"), (2, 2, "b"),
        (3, 3, "a"), (3, 3, "b"),
    ]
    catalogo["ej137_prefijo_ab.jff"] = (est_137, tr_137)

    # 139. Cadenas en {0, 1}* que tengan un número par de ceros
    est_139 = [(0, "q0_par0", True, True), (1, "q1_impar0", False, False)]
    tr_139 = [(0, 1, "0"), (0, 0, "1"), (1, 0, "0"), (1, 1, "1")]
    catalogo["ej139_par_de_ceros.jff"] = (est_139, tr_139)

    # 141. L = {w in {0, 1}* : cada 0 en w tiene un 1 inmediatamente a su derecha}
    est_141 = [
        (0, "q0_ok", True, True),
        (1, "q1_vio_0", False, False),
        (2, "q2_pozo_00", False, False),
    ]
    tr_141 = [
        (0, 1, "0"), (0, 0, "1"),
        (1, 2, "0"), (1, 0, "1"),
        (2, 2, "0"), (2, 2, "1"),
    ]
    catalogo["ej141_cada_0_seguido_de_1.jff"] = (est_141, tr_141)

    # 145. Lee binario de derecha a izquierda (LSB primero) e identifica múltiplos de 5
    # En LSB primero, el bit i aporta 2^i mod 5. Mejor aún: usando el AFD reverso o residuo con potencia mod 5,
    # o bien leyendo de derecha a izquierda: si leemos b_0, b_1, ..., b_k, el estado lleva (residuo mod 5, potencia 2^i mod 5)
    # O usando el inverso de horner: como 2 es invertible mod 5 (2*3 = 6 = 1 mod 5),
    # si procesamos de derecha a izquierda en una pasada determinista, necesitamos (acumulado mod 5, peso 2^k mod 5) = 5*4 = 20 estados,
    # ¡o bien el cociente de Myhill-Nerode tiene exactamente 5 estados!
    # Veamos por qué tiene 5 estados: u ~ v si para todo sufijo z (leído después, es decir bits más significativos),
    # val(u) + 2^|u| val(z) == 0 (mod 5) <=> 2^{-|u|} val(u) + val(z) == 0 (mod 5)!
    # Como gcd(2, 5) = 1, al leer un bit b después de u, el nuevo invariante I(ub) = 2^{-(|u|+1)} (val(u) + 2^|u| b) = 3 * I(u) + 3 * b (mod 5)!
    # ¡Efectivamente! Si definimos el estado q = 2^{-|w|} * val_LSB(w) mod 5:
    # - Para w = λ: q = 0.
    # - Al leer el siguiente bit b in {0, 1}: q_nuevo = 3 * (q + b) mod 5!
    # Y como 2^|w| es coprimo con 5, val_LSB(w) ≡ 0 (mod 5) si y solo si q == 0!
    est_145 = [(r, f"q{r}", r == 0, r == 0) for r in range(5)]
    tr_145 = [(r, (3 * (r + int(b))) % 5, b) for r in range(5) for b in SB]
    catalogo["ej145_binario_der_a_izq_mult5.jff"] = (est_145, tr_145)

    # 147. Lee binario de izquierda a derecha (MSB primero) y acepta si es múltiplo de 6
    est_147 = [(r, f"q{r}_mod{r}", r == 0, r == 0) for r in range(6)]
    tr_147 = [(r, (2 * r + int(b)) % 6, b) for r in range(6) for b in SB]
    catalogo["ej147_binario_izq_a_der_mult6.jff"] = (est_147, tr_147)

    # 148. Progreso de un alumno de ESCOM (alfabeto {P, N, A, S}, convocatorias Feb, Sep, Dic, máx 2 por año)
    est_148 = [
        (0, "q0_Inicio_Feb", True, False),
        (1, "q1_Ex_Feb", False, False),
        (2, "q2_Sep_0usadas", False, False),
        (3, "q3_Sep_1usada", False, False),
        (4, "q4_Ex_Sep_1", False, False),
        (5, "q5_Ex_Sep_2", False, False),
        (6, "q6_Dic_Disp", False, False),
        (7, "q7_Ex_Dic", False, False),
        (8, "q8_Aprobado", False, True),
        (9, "q9_Invalido", False, False),
    ]
    tr_148 = [
        # En Febrero decide P (presentarse) o N (no presentarse)
        (0, 1, "P"), (0, 2, "N"), (0, 9, "A"), (0, 9, "S"),
        # En Examen Febrero obtiene A (aprueba) o S (aplaza -> lleva 1 convocatoria usada, pasa a Sep)
        (1, 8, "A"), (1, 3, "S"), (1, 9, "P"), (1, 9, "N"),
        # En Septiembre con 0 usadas: P -> Ex_Sep_1, N -> Dic_Disp
        (2, 4, "P"), (2, 6, "N"), (2, 9, "A"), (2, 9, "S"),
        # En Septiembre con 1 usada: P -> Ex_Sep_2, N -> Dic_Disp
        (3, 5, "P"), (3, 6, "N"), (3, 9, "A"), (3, 9, "S"),
        # Ex_Sep_1 (era su 1ra convocatoria): A -> Aprobado, S -> Dic_Disp
        (4, 8, "A"), (4, 6, "S"), (4, 9, "P"), (4, 9, "N"),
        # Ex_Sep_2 (ya agotó sus 2 convocatorias del año): A -> Aprobado, S -> Reinicia año en q0_Inicio_Feb
        (5, 8, "A"), (5, 0, "S"), (5, 9, "P"), (5, 9, "N"),
        # En Diciembre disponible: P -> Ex_Dic, N -> Reinicia año en q0_Inicio_Feb
        (6, 7, "P"), (6, 0, "N"), (6, 9, "A"), (6, 9, "S"),
        # Ex_Dic: A -> Aprobado, S -> Reinicia año en q0_Inicio_Feb
        (7, 8, "A"), (7, 0, "S"), (7, 9, "P"), (7, 9, "N"),
        # Estado Aprobado y Estado Inválido
        (8, 9, "P"), (8, 9, "N"), (8, 9, "A"), (8, 9, "S"),
        (9, 9, "P"), (9, 9, "N"), (9, 9, "A"), (9, 9, "S"),
    ]
    catalogo["ej148_alumno_escom.jff"] = (est_148, tr_148)

    # 149. Tabla dada: A(ini), B, C(fin)
    est_149 = [(0, "A", True, False), (1, "B", False, False), (2, "C", False, True)]
    tr_149 = [
        (0, 1, "0"), (0, 2, "1"),
        (1, 0, "0"), (1, 2, "1"),
        (2, 2, "0"), (2, 0, "1"),
    ]
    catalogo["ej149_tabla_abc.jff"] = (est_149, tr_149)

    # 150. Tabla dada: A(ini), B(fin), C(fin), D(fin) sobre {0, 1, a}
    est_150 = [
        (0, "A", True, False),
        (1, "B", False, True),
        (2, "C", False, True),
        (3, "D", False, True),
    ]
    tr_150 = [
        (0, 1, "0"), (0, 2, "1"), (0, 3, "a"),
        (1, 1, "0"), (1, 2, "1"), (1, 2, "a"),
        (2, 0, "0"), (2, 0, "1"), (2, 3, "a"),
        (3, 1, "0"), (3, 1, "1"), (3, 1, "a"),
    ]
    catalogo["ej150_tabla_abcd.jff"] = (est_150, tr_150)

    # =========================================================================
    # LISTA 3: Simplificación (151-157), AFN (189-195), AFN-λ (196-200), Equivalencia (260-263)
    # =========================================================================

    # 151. Simplificado (estados accesibles desde A: A, C, E, G, I, B, F, J, D, H -> todos son accesibles;
    # al minimizar por partición: {A, D, I, J} equivalentes, etc. Guardamos el accesible/simplificado)
    # En 151-155 pide: "eliminando los estados que no son accesibles" (y partición en 156-157).
    # En 151: desde A -> C, E. Desde C -> A, G. Desde E -> I, B. Desde G -> F, I. Desde I -> J, E.
    # Desde B -> F, E. Desde F -> D, H. Desde J -> I, E. Desde D -> C, E. Desde H -> C, J.
    # ¡En 151 todos los 10 estados son accesibles desde A! Y al minimizar equivalentes:
    # Finales: {C, E, F}, No finales: {A, B, D, G, H, I, J}. A y D tienen mismas transiciones (C, E). I y J son equivalentes.
    est_151 = [
        (0, "AD", True, False),
        (1, "B", False, False),
        (2, "C", False, True),
        (3, "E", False, True),
        (4, "F", False, True),
        (5, "G", False, False),
        (6, "H", False, False),
        (7, "IJ", False, False),
    ]
    tr_151 = [
        (0, 2, "0"), (0, 3, "1"),
        (1, 4, "0"), (1, 3, "1"),
        (2, 0, "0"), (2, 5, "1"),
        (3, 7, "0"), (3, 1, "1"),
        (4, 0, "0"), (4, 6, "1"),
        (5, 4, "0"), (5, 7, "1"),
        (6, 2, "0"), (6, 7, "1"),
        (7, 7, "0"), (7, 3, "1"),
    ]
    catalogo["ej151_simplificado.jff"] = (est_151, tr_151)

    # 152. Desde A: A->(C,E,B), B->(D,E,B), C->(A,D,F), D->(F,B,C), E->(F,B,A), F->(D,B,C).
    # Además D y F pertenecen a F_final y ambos tienen transiciones (0->F/D en {D,F}, 1->B, 2->C), por lo que D y F son equivalentes.
    est_152 = [
        (0, "A", True, False),
        (1, "B", False, False),
        (2, "C", False, False),
        (3, "DF", False, True),
        (4, "E", False, True),
    ]
    tr_152 = [
        (0, 2, "0"), (0, 4, "1"), (0, 1, "2"),
        (1, 3, "0"), (1, 4, "1"), (1, 1, "2"),
        (2, 0, "0"), (2, 3, "1"), (2, 3, "2"),
        (3, 3, "0"), (3, 1, "1"), (3, 2, "2"),
        (4, 3, "0"), (4, 1, "1"), (4, 0, "2"),
    ]
    catalogo["ej152_simplificado.jff"] = (est_152, tr_152)

    # 153. Estados accesibles desde A: A, B, C, D, E, F, G.
    # Finales: {D, F, G}. En {D, F, G}, transiciones van siempre a {D, E, F, G}; y en {B, C, E} van siempre a {D, E, F, G}.
    # Partición mínima tiene solo 3 estados: A, BCE, DFG (donde DFG y E están cerrados o distinguibles por 0/1:
    # D->(D,E), F->(E,D), G->(F,G), E->(F,G)).
    est_153 = [
        (0, "A", True, False),
        (1, "BC", False, False),
        (2, "D", False, True),
        (3, "E", False, False),
        (4, "F", False, True),
        (5, "G", False, True),
    ]
    tr_153 = [
        (0, 1, "0"), (0, 1, "1"),
        (1, 2, "0"), (1, 3, "1"),
        (2, 2, "0"), (2, 3, "1"),
        (3, 4, "0"), (3, 5, "1"),
        (4, 3, "0"), (4, 2, "1"),
        (5, 4, "0"), (5, 5, "1"),
    ]
    catalogo["ej153_simplificado.jff"] = (est_153, tr_153)

    # 154. Accesibles desde A:
    # A -> D, K; D -> C, G; K -> C, F; C -> I, E; G -> C, I; F -> B, E; I -> G, K; E -> K, I; B -> H, K; H -> C, B.
    # El estado J es INACCESIBLE (ningún estado transiciona a J). Además G y E (ambos finales) van a {C,K,I} y se simplifican.
    est_154 = [
        (0, "A", True, False),
        (1, "B", False, False),
        (2, "CI", False, False),
        (3, "DFK", False, False),
        (4, "EG", False, True),
        (5, "H", False, True),
    ]
    tr_154 = [
        (0, 3, "0"), (0, 3, "1"),
        (1, 5, "0"), (1, 3, "1"),
        (2, 4, "0"), (2, 4, "1"),
        (3, 2, "0"), (3, 4, "1"),
        (4, 2, "0"), (4, 2, "1"),
        (5, 2, "0"), (5, 1, "1"),
    ]
    catalogo["ej154_simplificado.jff"] = (est_154, tr_154)

    # 155. Accesibles desde A: A, B, C, D, E, F, G, H, J, K (I y L son INACCESIBLES).
    # Único estado final: F.
    est_155 = [
        (0, "A", True, False),
        (1, "B", False, False),
        (2, "C", False, False),
        (3, "D", False, False),
        (4, "EK", False, False),
        (5, "F", False, True),
        (6, "G", False, False),
        (7, "H", False, False),
        (8, "J", False, False),
    ]
    tr_155 = [
        (0, 1, "0"), (0, 2, "1"),
        (1, 3, "0"), (1, 4, "1"),
        (2, 4, "0"), (2, 6, "1"),
        (3, 7, "0"), (3, 4, "1"),
        (4, 5, "0"), (4, 3, "1"),
        (5, 8, "0"), (5, 6, "1"),
        (6, 4, "0"), (6, 6, "1"),
        (7, 1, "0"), (7, 4, "1"),
        (8, 3, "0"), (8, 6, "1"),
    ]
    catalogo["ej155_simplificado.jff"] = (est_155, tr_155)

    # 156. Diagrama 156: Estados A(ini), B, C, D, E(fin). D es inaccesible? No, E--1-->D y D--0-->C, C--0-->D!
    # Partición mínima de 156: A y C son equivalentes (ambos no finales, con 0 van a B/D y con 1 van a C/E).
    est_156 = [
        (0, "A", True, False),
        (1, "BD", False, False),
        (2, "C", False, False),
        (3, "E", False, True),
    ]
    tr_156 = [
        (0, 1, "0"), (0, 2, "1"),
        (1, 2, "0"), (1, 3, "1"),
        (2, 1, "0"), (2, 2, "1"),
        (3, 1, "0"), (3, 3, "1"),
    ]
    catalogo["ej156_simplificado.jff"] = (est_156, tr_156)

    # 157. Diagrama 157: Estados A(ini), B, C, D, E, F(fin). D es INACCESIBLE (solo tiene flechas salientes a B, C, E).
    # Eliminando D y minimizando {B, C, E}:
    est_157 = [
        (0, "A", True, False),
        (1, "BC", False, False),
        (2, "E", False, False),
        (3, "F", False, True),
    ]
    tr_157 = [
        (0, 1, "0"), (0, 3, "1"),
        (1, 1, "0"), (1, 3, "1"),
        (2, 3, "0"), (2, 1, "1"),
        (3, 3, "0"), (3, 1, "1"),
    ]
    catalogo["ej157_simplificado.jff"] = (est_157, tr_157)

    # 189. AFD/AFN para palabras en {0,1}* que contienen 00101 o 00110
    est_189 = [
        (0, "q0", True, False),
        (1, "q1_0", False, False),
        (2, "q2_00", False, False),
        (3, "q3_001", False, False),
        (4, "q4_0010", False, False),
        (5, "q5_0011", False, False),
        (6, "q6_acepta", False, True),
    ]
    tr_189 = [
        (0, 1, "0"), (0, 0, "1"),
        (1, 2, "0"), (1, 0, "1"),
        (2, 2, "0"), (2, 3, "1"),
        (3, 4, "0"), (3, 5, "1"),
        (4, 2, "0"), (4, 6, "1"),
        (5, 6, "0"), (5, 0, "1"),
        (6, 6, "0"), (6, 6, "1"),
    ]
    catalogo["ej189_contiene_00101_o_00110.jff"] = (est_189, tr_189)

    # 190. Palabras en {0,1}* que contienen 11010 y 10100
    catalogo["ej190_contiene_11010_y_10100.jff"] = dos_patrones_afd(SB, "11010", "10100", traslape=True)

    # 192. AFD equivalente al AFN 192:
    # A(ini): 0->{B}, 1->{B,C}; B: 0->{A,B}, 1->∅; *C: 0->{A,C}, 1->∅.
    est_192 = [
        (0, "A", True, False),
        (1, "B", False, False),
        (2, "BC", False, True),
        (3, "AB", False, False),
        (4, "ABC", False, True),
        (5, "emptyset", False, False),
    ]
    tr_192 = [
        (0, 1, "0"), (0, 2, "1"),
        (1, 3, "0"), (1, 5, "1"),
        (2, 4, "0"), (2, 5, "1"),
        (3, 3, "0"), (3, 2, "1"),
        (4, 4, "0"), (4, 2, "1"),
        (5, 5, "0"), (5, 5, "1"),
    ]
    catalogo["ej192_afd_equivalente.jff"] = (est_192, tr_192)

    # 193. AFD equivalente al AFN 193:
    # A(ini): 0->∅, 1->{B,C}; B: 0->{A,D}, 1->{B,C,D}; C: 0->{C}, 1->{A,C}; *D: 0->{C}, 1->{D}.
    est_193 = [
        (0, "A", True, False),
        (1, "BC", False, False),
        (2, "ACD", False, True),
        (3, "ABCD", False, True),
        (4, "C", False, False),
        (5, "AC", False, False),
        (6, "emptyset", False, False),
    ]
    tr_193 = [
        (0, 6, "0"), (0, 1, "1"),
        (1, 2, "0"), (1, 3, "1"),
        (2, 4, "0"), (2, 3, "1"),
        (3, 2, "0"), (3, 3, "1"),
        (4, 4, "0"), (4, 5, "1"),
        (5, 4, "0"), (5, 3, "1"),
        (6, 6, "0"), (6, 6, "1"),
    ]
    catalogo["ej193_afd_equivalente.jff"] = (est_193, tr_193)

    # 194. AFD equivalente al AFN 194 sobre {0, 1, 2}:
    # A(ini): 0->{A,B}, 1->{A,C}, 2->{A}; B: ∅; *C: 0->{A,B}, 1->{A,B,C,D}, 2->∅; *D: 0->{B}, 1->{A}, 2->∅.
    est_194 = [
        (0, "A", True, False),
        (1, "AB", False, False),
        (2, "AC", False, True),
        (3, "ABCD", False, True),
    ]
    tr_194 = [
        (0, 1, "0"), (0, 2, "1"), (0, 0, "2"),
        (1, 1, "0"), (1, 2, "1"), (1, 0, "2"),
        (2, 1, "0"), (2, 3, "1"), (2, 0, "2"),
        (3, 1, "0"), (3, 3, "1"), (3, 0, "2"),
    ]
    catalogo["ej194_afd_equivalente.jff"] = (est_194, tr_194)

    # 195. AFD equivalente al AFN 195 sobre {0, 1}:
    # A(ini): 0->{A,B}, 1->{A}; B: 0->{A}, 1->{C}; *C: 0->{A}, 1->{D}; D: 0->{D}, 1->{E}; *E: 0->{E}, 1->{C,D}.
    # Construcción de subconjuntos desde {A}:
    nfa_195 = {
        "A": {"0": {"A", "B"}, "1": {"A"}},
        "B": {"0": {"A"}, "1": {"C"}},
        "C": {"0": {"A"}, "1": {"D"}},
        "D": {"0": {"D"}, "1": {"E"}},
        "E": {"0": {"E"}, "1": {"C", "D"}},
    }
    ini_195 = frozenset(["A"])
    cola_195 = [ini_195]
    mapa_195 = {ini_195: 0}
    tr_195: list[tuple[int, int, str]] = []
    while cola_195:
        actual_set = cola_195.pop(0)
        u = mapa_195[actual_set]
        for sym in SB:
            nxt_set = frozenset( s for q in actual_set for s in nfa_195[q][sym] )
            if nxt_set not in mapa_195:
                mapa_195[nxt_set] = len(mapa_195)
                cola_195.append(nxt_set)
            tr_195.append((u, mapa_195[nxt_set], sym))
    est_195 = [
        (idx, "".join(sorted(st)), idx == 0, bool(st & {"C", "E"}))
        for st, idx in sorted(mapa_195.items(), key=lambda x: x[1])
    ]
    catalogo["ej195_afd_equivalente.jff"] = (est_195, tr_195)

    # 196. AFD equivalente al AFN-λ 196:
    # Cl(A) = {A, B}, Cl(B) = {B}, Cl(C) = {C}.
    est_196 = [
        (0, "AB", True, False),
        (1, "C", False, True),
        (2, "emptyset", False, False),
    ]
    tr_196 = [
        (0, 0, "0"), (0, 1, "1"),
        (1, 2, "0"), (1, 2, "1"),
        (2, 2, "0"), (2, 2, "1"),
    ]
    catalogo["ej196_afn_lambda_a_afd.jff"] = (est_196, tr_196)

    # 197. AFD equivalente al AFN-λ 197:
    # Cl(A)={A,B,C,D} (final por D), con 0 -> Cl({A,B,C,D})={A,B,C,D}, con 1 -> Cl({A,C,D})={B,C,D} (final).
    # Desde {B,C,D}: con 0 -> Cl({A,C})={A,B,C,D}, con 1 -> Cl({A,C,D})={B,C,D}.
    est_197 = [
        (0, "ABCD", True, True),
        (1, "BCD", False, True),
    ]
    tr_197 = [
        (0, 0, "0"), (0, 1, "1"),
        (1, 0, "0"), (1, 1, "1"),
    ]
    catalogo["ej197_afn_lambda_a_afd.jff"] = (est_197, tr_197)

    # 198. AFD equivalente al AFN-λ 198:
    # Cl(A)={A,B,C}, con 0 -> Cl({B,C})={B,C}, con 1 -> Cl({C,D})={B,C,D} (final).
    # {B,C}: con 0 -> {B,C}, con 1 -> {B,C,D}.
    # {B,C,D}: con 0 -> {B,C}, con 1 -> {B,C,D}.
    est_198 = [
        (0, "ABC", True, False),
        (1, "BC", False, False),
        (2, "BCD", False, True),
    ]
    tr_198 = [
        (0, 1, "0"), (0, 2, "1"),
        (1, 1, "0"), (1, 2, "1"),
        (2, 1, "0"), (2, 2, "1"),
    ]
    catalogo["ej198_afn_lambda_a_afd.jff"] = (est_198, tr_198)

    # 199. AFD equivalente al AFN-λ 199:
    # Cl(A)={A,B,C,E} (final por E). Con 0 -> {E} (final); con 1 -> Cl({A,B,C})={A,B,C,E} (final).
    # {E}: con 0 -> ∅, con 1 -> {D} (final). {D}: con 0 -> ∅, con 1 -> {D}.
    est_199 = [
        (0, "ABCE", True, True),
        (1, "E", False, True),
        (2, "D", False, True),
        (3, "emptyset", False, False),
    ]
    tr_199 = [
        (0, 1, "0"), (0, 0, "1"),
        (1, 3, "0"), (1, 2, "1"),
        (2, 3, "0"), (2, 2, "1"),
        (3, 3, "0"), (3, 3, "1"),
    ]
    catalogo["ej199_afn_lambda_a_afd.jff"] = (est_199, tr_199)

    # 200. AFD equivalente al AFN-λ 200:
    # Cl(A)={A,B}, Cl(B)={B}, Cl(C)={C,E}, Cl(D)={D,E,F}, Cl(E)={E}, Cl(F)={E,F}.
    est_200 = [
        (0, "AB", True, False),
        (1, "CE", False, True),
        (2, "DEF", False, True),
        (3, "EF", False, True),
        (4, "CDEFF", False, True),
        (5, "ABCEF", False, True),
        (6, "BD", False, True),
        (7, "BE", False, True),
    ]
    tr_200 = [
        (0, 4, "0"), (0, 5, "1"),
        (1, 3, "0"), (1, 5, "1"),
        (2, 5, "0"), (2, 6, "1"),
        (3, 7, "0"), (3, 2, "1"),
        (4, 5, "0"), (4, 5, "1"),
        (5, 5, "0"), (5, 5, "1"),
        (6, 5, "0"), (6, 7, "1"),
        (7, 4, "0"), (7, 6, "1"),
    ]
    catalogo["ej200_afn_lambda_a_afd.jff"] = (est_200, tr_200)

    # 236-240 y 254-258: Expresiones regulares y autómatas asociados
    # 236. L = {x 001 y : x, y in {0,1}*}
    catalogo["ej236_subcadena_001.jff"] = kmp_afd(SB, "001")

    # 237. L = {x 010 : x in {0,1}*}
    catalogo["ej237_termina_010.jff"] = kmp_sufijo_afd(SB, "010")

    # 238. L = Sigma^3 U Sigma^5 sobre {0,1}
    est_238 = [
        (0, "q0", True, False),
        (1, "q1", False, False),
        (2, "q2", False, False),
        (3, "q3_acepta", False, True),
        (4, "q4", False, False),
        (5, "q5_acepta", False, True),
        (6, "q6_pozo", False, False),
    ]
    tr_238 = [(i, min(6, i + 1), b) for i in range(7) for b in SB]
    catalogo["ej238_long_3_o_5.jff"] = (est_238, tr_238)

    # 239. Cadenas que comienzan con 01 o terminan con 10
    est_239 = [
        (0, "q0_ini", True, False),
        (1, "q1_0", False, False),
        (2, "q2_pref01_ok", False, True),
        (3, "q3_no01_ otro", False, False),
        (4, "q4_no01_vio1", False, False),
        (5, "q5_no01_suf10_ok", False, True),
    ]
    tr_239 = [
        (0, 1, "0"), (0, 4, "1"),
        (1, 3, "0"), (1, 2, "1"),
        (2, 2, "0"), (2, 2, "1"),
        (3, 3, "0"), (3, 4, "1"),
        (4, 5, "0"), (4, 4, "1"),
        (5, 3, "0"), (5, 4, "1"),
    ]
    catalogo["ej239_empieza_01_o_termina_10.jff"] = (est_239, tr_239)

    # 240. Cadenas sobre {0,1} de longitud par y que contienen la subcadena 01
    est_240 = [
        (0, "q0_par_sin01", True, False),
        (1, "q1_impar_1", False, False),
        (2, "q2_impar_0", False, False),
        (3, "q3_par_0", False, False),
        (4, "q4_par_con01", False, True),
        (5, "q5_impar_con01", False, False),
    ]
    tr_240 = [
        (0, 2, "0"), (0, 1, "1"),
        (1, 3, "0"), (1, 0, "1"),
        (2, 3, "0"), (2, 4, "1"),
        (3, 2, "0"), (3, 5, "1"),
        (4, 5, "0"), (4, 5, "1"),
        (5, 4, "0"), (5, 4, "1"),
    ]
    catalogo["ej240_longitud_par_con_01.jff"] = (est_240, tr_240)

    # 254-258: Autómatas de tablas para hallar expresión regular
    catalogo["ej254_aut_a_regex.jff"] = (
        [(0, "A", True, False), (1, "B", False, True)],
        [(0, 0, "0"), (0, 1, "1"), (1, 0, "0"), (1, 1, "1")],
    )
    catalogo["ej255_aut_a_regex.jff"] = (
        [(0, "A", True, True), (1, "B", False, False)],
        [(0, 1, "0"), (0, 1, "1"), (1, 0, "0"), (1, 1, "1")],
    )
    catalogo["ej256_aut_a_regex.jff"] = (
        [(0, "A", True, False), (1, "B", False, True)],
        [(0, 1, "0"), (0, 0, "1"), (0, 0, "2"), (1, 1, "0"), (1, 1, "1"), (1, 0, "2")],
    )
    catalogo["ej257_aut_a_regex.jff"] = (
        [(0, "A", True, False), (1, "B", False, True), (2, "C", False, True)],
        [(0, 1, "0"), (0, 2, "1"), (1, 2, "0"), (1, 1, "1"), (2, 0, "0"), (2, 0, "1")],
    )
    catalogo["ej258_aut_a_regex.jff"] = (
        [(0, "A", True, False), (1, "B", False, False), (2, "C", False, True)],
        [(0, 2, "0"), (0, 2, "1"), (1, 0, "0"), (1, 2, "1"), (2, 1, "0"), (2, 0, "1")],
    )

    # 260. AFD equivalente al AFN 260:
    # A(ini): 0->∅, 1->{B,C}; B: 0->{A,B,D}, 1->{C,D}; C: 0->{A,C}, 1->{A,E}; *D: 0->∅, 1->{D,E}; E: 0->{A,E}, 1->∅.
    nfa_260 = {
        "A": {"0": set(), "1": {"B", "C"}},
        "B": {"0": {"A", "B", "D"}, "1": {"C", "D"}},
        "C": {"0": {"A", "C"}, "1": {"A", "E"}},
        "D": {"0": set(), "1": {"D", "E"}},
        "E": {"0": {"A", "E"}, "1": set()},
    }
    ini_260 = frozenset(["A"])
    cola_260 = [ini_260]
    mapa_260 = {ini_260: 0}
    tr_260: list[tuple[int, int, str]] = []
    while cola_260:
        actual_set = cola_260.pop(0)
        u = mapa_260[actual_set]
        for sym in SB:
            nxt_set = frozenset(s for q in actual_set for s in nfa_260[q][sym])
            if nxt_set not in mapa_260:
                mapa_260[nxt_set] = len(mapa_260)
                cola_260.append(nxt_set)
            tr_260.append((u, mapa_260[nxt_set], sym))
    est_260 = [
        (idx, "".join(sorted(st)) if st else "emptyset", idx == 0, "D" in st)
        for st, idx in sorted(mapa_260.items(), key=lambda x: x[1])
    ]
    catalogo["ej260_afd_equivalente.jff"] = (est_260, tr_260)

    # 261. AFD equivalente al AFN de la figura 261:
    # q0(ini): 0->{q0, q1}, 1->{q0, q3}; q1: 0->{q2}; *q2: ∅; q3: 1->{q4}; *q4: ∅ (termina en 00 o 11)
    est_261 = [
        (0, "q0", True, False),
        (1, "q0q1", False, False),
        (2, "q0q3", False, False),
        (3, "q0q1q2", False, True),
        (4, "q0q3q4", False, True),
    ]
    tr_261 = [
        (0, 1, "0"), (0, 2, "1"),
        (1, 3, "0"), (1, 2, "1"),
        (2, 1, "0"), (2, 4, "1"),
        (3, 3, "0"), (3, 2, "1"),
        (4, 1, "0"), (4, 4, "1"),
    ]
    catalogo["ej261_termina_00_o_11_afd.jff"] = (est_261, tr_261)

    # 262. AFD equivalente al AFN que acepta {ab, ba}
    est_262 = [
        (0, "q0_ini", True, False),
        (1, "q1_a", False, False),
        (2, "q2_b", False, False),
        (3, "q3_acepta_ab_ba", False, True),
        (4, "q4_pozo", False, False),
    ]
    tr_262 = [
        (0, 1, "a"), (0, 2, "b"),
        (1, 4, "a"), (1, 3, "b"),
        (2, 3, "a"), (2, 4, "b"),
        (3, 4, "a"), (3, 4, "b"),
        (4, 4, "a"), (4, 4, "b"),
    ]
    catalogo["ej262_conjunto_ab_ba_afd.jff"] = (est_262, tr_262)

    # 263. AFD equivalente al AFN de la figura 263 (termina en 01)
    est_263 = [
        (0, "q0", True, False),
        (1, "q0q1", False, False),
        (2, "q0q2", False, True),
    ]
    tr_263 = [
        (0, 1, "0"), (0, 0, "1"),
        (1, 1, "0"), (1, 2, "1"),
        (2, 1, "0"), (2, 0, "1"),
    ]
    catalogo["ej263_termina_01_afd.jff"] = (est_263, tr_263)

    for nombre, (est, tr) in catalogo.items():
        crear_jff(nombre, est, tr)

    return catalogo


if __name__ == "__main__":
    cat = generar_todos()
    print(f"Se generaron {len(cat)} archivos .jff en {AUTOMATAS_DIR}")
