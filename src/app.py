"""Aplicación con interfaz gráfica en Flet para Operaciones Básicas sobre Lenguajes.

Invoca las funciones puras del módulo `lenguajes.py`, manteniendo desacoplada
la lógica de negocio de la interfaz de usuario. Permite:
- Operación 1: Calcular prefijos, sufijos y subcadenas de una cadena dada y
  exportar los resultados a un archivo de texto.
- Operación 2: Calcular la cerradura de Kleene (Σ*) y la cerradura positiva (Σ+)
  para un alfabeto y longitud máxima dados, validando el límite de 200,000 cadenas
  y ofreciendo la exportación a archivo de texto.
"""

from __future__ import annotations

from pathlib import Path
import flet as ft

from lenguajes import (
    LIMITE_CADENAS,
    cerradura_kleene,
    cerradura_positiva,
    formatear_cadena,
    normalizar_alfabeto,
    prefijos,
    subcadenas,
    sufijos,
)

DIR_SALIDAS = Path("salidas")


def guardar_archivo_texto(nombre_archivo: str, contenido: str) -> Path:
    """Guarda el contenido en la carpeta `salidas/` y devuelve la ruta."""
    DIR_SALIDAS.mkdir(parents=True, exist_ok=True)
    ruta = DIR_SALIDAS / nombre_archivo
    ruta.write_text(contenido, encoding="utf-8")
    return ruta


def main(page: ft.Page) -> None:
    page.title = "Práctica 1 - Operaciones Básicas sobre Lenguajes (ESCOM - IPN)"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 24

    # Estado en memoria para exportación
    ultimo_reporte_op1: dict[str, str] = {"contenido": ""}
    ultimo_reporte_op2: dict[str, str] = {"contenido": ""}

    # =========================================================================
    # SECCIÓN 1: Subcadenas, prefijos y sufijos
    # =========================================================================
    entrada_cadena = ft.TextField(
        label="Cadena de entrada (w)",
        hint_text="Ejemplo: abba (deje vacío para la cadena vacía λ)",
        value="abba",
        width=450,
    )
    resumen_op1 = ft.Text(weight=ft.FontWeight.BOLD)
    salida_prefijos = ft.TextField(
        label="Prefijos de w",
        multiline=True,
        min_lines=3,
        max_lines=6,
        read_only=True,
    )
    salida_sufijos = ft.TextField(
        label="Sufijos de w",
        multiline=True,
        min_lines=3,
        max_lines=6,
        read_only=True,
    )
    salida_subcadenas = ft.TextField(
        label="Subcadenas distintas de w",
        multiline=True,
        min_lines=4,
        max_lines=8,
        read_only=True,
    )
    estado_export_op1 = ft.Text(color=ft.Colors.GREEN_700)

    def ejecutar_op1(e: ft.ControlEvent | None = None) -> None:
        w = entrada_cadena.value or ""
        n = len(w)
        lista_pref = prefijos(w)
        lista_suf = sufijos(w)
        lista_sub = subcadenas(w)
        max_teorico = (n * (n + 1)) // 2 + 1

        pref_fmt = [formatear_cadena(x) for x in lista_pref]
        suf_fmt = [formatear_cadena(x) for x in lista_suf]
        sub_fmt = [formatear_cadena(x) for x in lista_sub]

        resumen_op1.value = (
            f"Cadena w = '{formatear_cadena(w)}' (|w| = {n})  |  "
            f"Prefijos: {len(lista_pref)} (n+1)  |  "
            f"Sufijos: {len(lista_suf)} (n+1)  |  "
            f"Subcadenas distintas: {len(lista_sub)} (máx. teórico n(n+1)/2 + 1 = {max_teorico})"
        )
        salida_prefijos.value = ", ".join(pref_fmt)
        salida_sufijos.value = ", ".join(suf_fmt)
        salida_subcadenas.value = ", ".join(sub_fmt)

        ultimo_reporte_op1["contenido"] = (
            "=== OPERACIÓN 1: PREFIJOS, SUFIJOS Y SUBCADENAS ===\n"
            f"Cadena de entrada: {formatear_cadena(w)}\n"
            f"Longitud (n): {n}\n"
            f"Total de prefijos (n + 1): {len(lista_pref)}\n"
            f"Total de sufijos (n + 1): {len(lista_suf)}\n"
            f"Total de subcadenas distintas: {len(lista_sub)} (cota máx. {max_teorico})\n\n"
            f"Prefijos ({len(lista_pref)}):\n{', '.join(pref_fmt)}\n\n"
            f"Sufijos ({len(lista_suf)}):\n{', '.join(suf_fmt)}\n\n"
            f"Subcadenas ({len(lista_sub)}):\n{', '.join(sub_fmt)}\n"
        )
        estado_export_op1.value = ""
        page.update()

    def exportar_op1(e: ft.ControlEvent) -> None:
        if not ultimo_reporte_op1["contenido"]:
            ejecutar_op1()
        ruta = guardar_archivo_texto("operacion1_cadenas.txt", ultimo_reporte_op1["contenido"])
        estado_export_op1.value = f"Resultados guardados en: {ruta.as_posix()}"
        page.update()

    # =========================================================================
    # SECCIÓN 2: Cerradura de Kleene (Σ*) y Cerradura Positiva (Σ+)
    # =========================================================================
    entrada_alfabeto = ft.TextField(
        label="Alfabeto Σ (símbolos separados por comas)",
        hint_text="Ejemplo: 0, 1 o a, b, c",
        value="0, 1",
        width=350,
    )
    entrada_longitud = ft.TextField(
        label="Longitud máxima (n)",
        value="3",
        width=180,
    )
    mensaje_op2 = ft.Text(weight=ft.FontWeight.BOLD)
    salida_kleene = ft.TextField(
        label="Cerradura de Kleene (Σ* hasta longitud n)",
        multiline=True,
        min_lines=4,
        max_lines=8,
        read_only=True,
    )
    salida_positiva = ft.TextField(
        label="Cerradura Positiva (Σ+ hasta longitud n)",
        multiline=True,
        min_lines=4,
        max_lines=8,
        read_only=True,
    )
    estado_export_op2 = ft.Text(color=ft.Colors.GREEN_700)

    def ejecutar_op2(e: ft.ControlEvent | None = None) -> None:
        estado_export_op2.value = ""
        partes = (entrada_alfabeto.value or "").split(",")
        simbolos = normalizar_alfabeto(partes)

        try:
            n = int((entrada_longitud.value or "").strip())
        except ValueError:
            mensaje_op2.value = "Error: La longitud máxima n debe ser un número entero."
            mensaje_op2.color = ft.Colors.RED_700
            salida_kleene.value = ""
            salida_positiva.value = ""
            page.update()
            return

        try:
            res_kleene = cerradura_kleene(simbolos, n, limite=LIMITE_CADENAS)
            res_positiva = cerradura_positiva(simbolos, n, limite=LIMITE_CADENAS)
        except ValueError as err:
            mensaje_op2.value = str(err)
            mensaje_op2.color = ft.Colors.RED_700
            salida_kleene.value = ""
            salida_positiva.value = ""
            ultimo_reporte_op2["contenido"] = ""
            page.update()
            return

        kleene_fmt = [formatear_cadena(x) for x in res_kleene]
        positiva_fmt = [formatear_cadena(x) for x in res_positiva]

        mensaje_op2.color = ft.Colors.BLUE_800
        mensaje_op2.value = (
            f"Alfabeto Σ = {{{', '.join(simbolos)}}} (|Σ| = {len(simbolos)}), n = {n}  |  "
            f"|Σ*| (hasta n) = {len(res_kleene):,} cadenas  |  "
            f"|Σ+| (hasta n) = {len(res_positiva):,} cadenas"
        )

        # Si hay más de 2,000 cadenas, mostramos una vista previa en pantalla y exportamos completo
        max_vista = 2000
        if len(kleene_fmt) > max_vista:
            salida_kleene.value = (
                ", ".join(kleene_fmt[:max_vista])
                + f" ... [+{len(kleene_fmt) - max_vista:,} cadenas más; use Exportar para el archivo completo]"
            )
        else:
            salida_kleene.value = ", ".join(kleene_fmt)

        if len(positiva_fmt) > max_vista:
            salida_positiva.value = (
                ", ".join(positiva_fmt[:max_vista])
                + f" ... [+{len(positiva_fmt) - max_vista:,} cadenas más; use Exportar para el archivo completo]"
            )
        else:
            salida_positiva.value = ", ".join(positiva_fmt) if positiva_fmt else "∅ (conjunto vacío)"

        ultimo_reporte_op2["contenido"] = (
            "=== OPERACIÓN 2: CERRADURA DE KLEENE (Σ*) Y CERRADURA POSITIVA (Σ+) ===\n"
            f"Alfabeto Σ: {{{', '.join(simbolos)}}} (|Σ| = {len(simbolos)})\n"
            f"Longitud máxima (n): {n}\n"
            f"Total en Σ* (hasta longitud n): {len(res_kleene)}\n"
            f"Total en Σ+ (hasta longitud n): {len(res_positiva)}\n\n"
            f"Σ* ({len(res_kleene)} cadenas):\n{', '.join(kleene_fmt)}\n\n"
            f"Σ+ ({len(res_positiva)} cadenas):\n"
            f"{', '.join(positiva_fmt) if positiva_fmt else '∅ (conjunto vacío)'}\n"
        )
        page.update()

    def exportar_op2(e: ft.ControlEvent) -> None:
        if not ultimo_reporte_op2["contenido"]:
            ejecutar_op2()
        if not ultimo_reporte_op2["contenido"]:
            estado_export_op2.value = "No hay resultados válidos para exportar."
            page.update()
            return
        ruta = guardar_archivo_texto("operacion2_cerraduras.txt", ultimo_reporte_op2["contenido"])
        estado_export_op2.value = f"Resultados guardados en: {ruta.as_posix()}"
        page.update()

    # Construcción del diseño visual
    page.add(
        ft.Text(
            "Práctica 1: Operaciones Básicas sobre Lenguajes",
            size=24,
            weight=ft.FontWeight.BOLD,
        ),
        ft.Text(
            "Instituto Politécnico Nacional — Escuela Superior de Cómputo (ESCOM) — Teoría de la Computación",
            size=14,
        ),
        ft.Divider(height=20),
        ft.Text(
            "Operación 1. Subcadenas, prefijos y sufijos",
            size=18,
            weight=ft.FontWeight.BOLD,
        ),
        ft.Row(
            [
                entrada_cadena,
                ft.ElevatedButton("Calcular Prefijos, Sufijos y Subcadenas", on_click=ejecutar_op1),
                ft.OutlinedButton("Guardar en archivo (.txt)", on_click=exportar_op1),
            ],
            wrap=True,
        ),
        resumen_op1,
        salida_prefijos,
        salida_sufijos,
        salida_subcadenas,
        estado_export_op1,
        ft.Divider(height=28),
        ft.Text(
            "Operación 2. Cerradura de Kleene (Σ*) y Cerradura Positiva (Σ+)",
            size=18,
            weight=ft.FontWeight.BOLD,
        ),
        ft.Row(
            [
                entrada_alfabeto,
                entrada_longitud,
                ft.ElevatedButton("Calcular Σ* y Σ+", on_click=ejecutar_op2),
                ft.OutlinedButton("Exportar a archivo (.txt)", on_click=exportar_op2),
            ],
            wrap=True,
        ),
        mensaje_op2,
        salida_kleene,
        salida_positiva,
        estado_export_op2,
    )

    # Inicializar con valores por defecto
    ejecutar_op1()
    ejecutar_op2()


if __name__ == "__main__":
    ft.run(main)
