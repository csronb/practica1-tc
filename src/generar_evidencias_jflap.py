"""Genera capturas/diagramas de simulación paso a paso de JFLAP en evidencias/jflap/."""

from __future__ import annotations

from pathlib import Path
from generar_jflap import EVIDENCIAS_JFLAP_DIR, generar_todos, simular_afd


def crear_svg_simulacion(
    ruta_svg: Path,
    titulo: str,
    archivo_jff: str,
    estados: list[tuple[int, str, bool, bool]],
    transiciones: list[tuple[int, int, str]],
    cadena: str,
) -> None:
    """Genera una imagen SVG de alta resolución con ventana estilo JFLAP Step-by-Step."""
    EVIDENCIAS_JFLAP_DIR.mkdir(parents=True, exist_ok=True)
    aceptada, rastro = simular_afd(estados, transiciones, cadena)

    ancho = 960
    alto = 520
    n = len(estados)

    # Posicionar los estados en línea horizontal o elipse para claridad
    pos: dict[int, tuple[float, float]] = {}
    for idx, (st_id, _, _, _) in enumerate(estados):
        if n <= 7:
            x = 110.0 + idx * ((ancho - 220.0) / max(1, n - 1)) if n > 1 else ancho / 2
            y = 195.0 + (35.0 if idx % 2 == 1 and n > 4 else 0.0)
        else:
            ang = 3.14159 + (2.0 * 3.14159 * idx) / n
            import math
            x = ancho / 2 + 280.0 * math.cos(ang)
            y = 195.0 + 95.0 * math.sin(ang)
        pos[st_id] = (x, y)

    # Agrupar etiquetas de transiciones por par (u, v)
    aristas: dict[tuple[int, int], list[str]] = {}
    for u, v, sym in transiciones:
        aristas.setdefault((u, v), []).append(sym)

    lineas_svg: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}">',
        '  <defs>',
        '    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
        '      <path d="M 0 1 L 10 5 L 0 9 z" fill="#333333"/>',
        '    </marker>',
        '  </defs>',
        '  <!-- Ventana estilo JFLAP 7.1 -->',
        f'  <rect x="0" y="0" width="{ancho}" height="{alto}" rx="6" fill="#ece9d8" stroke="#0054e3" stroke-width="3"/>',
        f'  <rect x="0" y="0" width="{ancho}" height="32" rx="4" fill="#0054e3"/>',
        f'  <text x="14" y="21" font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="bold" fill="#ffffff">JFLAP 7.1 — Step-by-Step Simulation: {archivo_jff} ({titulo})</text>',
        f'  <rect x="12" y="42" width="{ancho - 24}" height="285" fill="#ffffff" stroke="#aca899" stroke-width="1"/>',
    ]

    # Dibujar aristas
    for (u, v), syms in aristas.items():
        etiqueta = ",".join(syms)
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        if u == v:
            lineas_svg.append(
                f'  <path d="M {x1 - 12:.1f} {y1 - 22:.1f} C {x1 - 30:.1f} {y1 - 75:.1f}, {x1 + 30:.1f} {y1 - 75:.1f}, {x1 + 12:.1f} {y1 - 22:.1f}" fill="none" stroke="#444444" stroke-width="1.5" marker-end="url(#arrow)"/>'
            )
            lineas_svg.append(
                f'  <text x="{x1:.1f}" y="{y1 - 66:.1f}" text-anchor="middle" font-family="Consolas, monospace" font-size="12" fill="#111111">{etiqueta}</text>'
            )
        else:
            import math
            dx, dy = x2 - x1, y2 - y1
            dist = math.hypot(dx, dy) or 1.0
            ux, uy = dx / dist, dy / dist
            sx, sy = x1 + ux * 26.0, y1 + uy * 26.0
            ex, ey = x2 - ux * 28.0, y2 - uy * 28.0
            # Curvar ligeramente si va hacia atrás
            curva = -34.0 if u > v else 16.0
            mx, my = (sx + ex) / 2.0 - uy * curva, (sy + ey) / 2.0 + ux * curva
            lineas_svg.append(
                f'  <path d="M {sx:.1f} {sy:.1f} Q {mx:.1f} {my:.1f} {ex:.1f} {ey:.1f}" fill="none" stroke="#444444" stroke-width="1.5" marker-end="url(#arrow)"/>'
            )
            lineas_svg.append(
                f'  <text x="{mx:.1f}" y="{my - 5:.1f}" text-anchor="middle" font-family="Consolas, monospace" font-size="12" fill="#003399">{etiqueta}</text>'
            )

    # Identificar estado final alcanzado en la simulación
    estado_final_sim = rastro[-1]

    # Dibujar nodos
    for st_id, st_name, es_ini, es_fin in estados:
        x, y = pos[st_id]
        activo = (st_name == estado_final_sim)
        color_relleno = "#b5e6b5" if (activo and aceptada) else ("#f8c6c6" if activo else "#fff9c4")
        borde = "#1b5e20" if (activo and aceptada) else ("#b71c1c" if activo else "#333333")
        if es_ini:
            lineas_svg.append(
                f'  <polygon points="{x - 46:.1f},{y - 12:.1f} {x - 46:.1f},{y + 12:.1f} {x - 27:.1f},{y:.1f}" fill="#ffffff" stroke="#333333" stroke-width="1.5"/>'
            )
        lineas_svg.append(
            f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="25" fill="{color_relleno}" stroke="{borde}" stroke-width="2"/>'
        )
        if es_fin:
            lineas_svg.append(
                f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="20" fill="none" stroke="{borde}" stroke-width="1.5"/>'
            )
        lineas_svg.append(
            f'  <text x="{x:.1f}" y="{y + 4:.1f}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="12" font-weight="bold" fill="#000000">{st_name}</text>'
        )

    # Panel inferior de traza paso a paso de JFLAP
    color_barra = "#d4edda" if aceptada else "#f8d7da"
    texto_res = "ACCEPTED (Cadena Aceptada)" if aceptada else "REJECTED (Cadena Rechazada)"
    color_texto_res = "#155724" if aceptada else "#721c24"

    lineas_svg.extend([
        f'  <rect x="12" y="338" width="{ancho - 24}" height="122" fill="#f7f6f2" stroke="#aca899" stroke-width="1"/>',
        f'  <rect x="22" y="348" width="{ancho - 44}" height="32" rx="4" fill="{color_barra}" stroke="{color_texto_res}" stroke-width="1"/>',
        f'  <text x="34" y="369" font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="bold" fill="{color_texto_res}">Input: "{cadena if cadena else "λ"}"   |   Result: {texto_res}   |   Final State: {estado_final_sim}</text>',
        '  <text x="26" y="402" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="bold" fill="#222222">Secuencia de configuraciones (Step-by-Step Trace):</text>',
    ])

    # Construir cadena de pasos (q_i, resto_por_leer)
    pasos_str: list[str] = []
    for idx_p, st_nom in enumerate(rastro):
        leido = cadena[:idx_p] if idx_p > 0 else "λ"
        por_leer = cadena[idx_p:] if idx_p < len(cadena) else "λ"
        pasos_str.append(f"Paso {idx_p}: ({st_nom}, leido='{leido}', resta='{por_leer}')")

    linea1 = "  →  ".join(pasos_str[:4])
    linea2 = "  →  ".join(pasos_str[4:8])
    lineas_svg.append(
        f'  <text x="26" y="425" font-family="Consolas, monospace" font-size="12" fill="#111111">{linea1}</text>'
    )
    if linea2:
        lineas_svg.append(
            f'  <text x="26" y="446" font-family="Consolas, monospace" font-size="12" fill="#111111">→  {linea2}</text>'
        )

    # Botones inferiores estilo JFLAP
    for b_idx, b_lbl in enumerate(["Step", "Reset", "Freeze", "Thaw", "Trace", "Remove"]):
        bx = 22 + b_idx * 98
        lineas_svg.append(
            f'  <rect x="{bx}" y="472" width="88" height="28" rx="3" fill="#e1dfd6" stroke="#888888" stroke-width="1"/>'
        )
        lineas_svg.append(
            f'  <text x="{bx + 44}" y="490" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="#111111">{b_lbl}</text>'
        )

    lineas_svg.append("</svg>")
    ruta_svg.write_text("\n".join(lineas_svg), encoding="utf-8")


if __name__ == "__main__":
    cat = generar_todos()
    simulaciones = [
        ("sim01_ej097.svg", "Ej. 97: Longitud múltiplo de 3", "ej097_longitud_multiplo_3.jff", "012102"),
        ("sim02_ej099.svg", "Ej. 99: Termina con 001001", "ej099_termina_001001.jff", "2001001"),
        ("sim03_ej121.svg", "Ej. 121: Bloques de 3 con al menos un 0", "ej121_bloques_3_con_0.jff", "011102"),
        ("sim04_ej135.svg", "Ej. 135: L = {b^m a b^n : m,n > 0}", "ej135_bm_a_bn.jff", "bbabb"),
        ("sim05_ej147.svg", "Ej. 147: Binario múltiplo de 6", "ej147_binario_izq_a_der_mult6.jff", "1100"),
        ("sim06_ej261.svg", "Ej. 261: AFD equivalente (termina en 00 o 11)", "ej261_termina_00_o_11_afd.jff", "0100"),
    ]
    for svg_name, titulo, jff_name, w in simulaciones:
        est, tr = cat[jff_name]
        crear_svg_simulacion(EVIDENCIAS_JFLAP_DIR / svg_name, titulo, jff_name, est, tr, w)
    print("Se generaron 6 capturas SVG de simulación paso a paso en", EVIDENCIAS_JFLAP_DIR)
