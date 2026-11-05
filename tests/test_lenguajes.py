"""Suite de pruebas automatizadas con pytest para el módulo `lenguajes`.

Cubre los casos mínimos solicitados en el Ejercicio 5:
1. La cadena vacía ("").
2. Un alfabeto de un solo símbolo (|Σ| = 1).
3. Los prefijos y sufijos de una cadena de longitud 1.
4. La diferencia entre Σ* y Σ+ para la longitud cero (n = 0).
5. Verificación del rechazo cuando el número de cadenas supera 200,000.
"""

import pytest

from lenguajes import (
    LIMITE_CADENAS,
    cerradura_kleene,
    cerradura_positiva,
    contar_cadenas_cerradura,
    formatear_cadena,
    prefijos,
    subcadenas,
    sufijos,
)


def test_cadena_vacia():
    """Verifica prefijos, sufijos y subcadenas para la cadena vacía λ."""
    assert prefijos("") == [""]
    assert sufijos("") == [""]
    assert subcadenas("") == [""]
    assert formatear_cadena("") == "λ"


def test_prefijos_y_sufijos_longitud_1():
    """Verifica prefijos, sufijos y subcadenas de una cadena de longitud 1."""
    assert prefijos("a") == ["", "a"]
    assert sufijos("a") == ["", "a"]
    assert subcadenas("a") == ["", "a"]


def test_subcadenas_prefijos_sufijos_general():
    """Verifica propiedades combinatorias en cadenas de longitud arbitraria."""
    w = "abc"
    # n + 1 prefijos y n + 1 sufijos
    assert len(prefijos(w)) == len(w) + 1
    assert prefijos(w) == ["", "a", "ab", "abc"]
    assert len(sufijos(w)) == len(w) + 1
    assert sufijos(w) == ["", "c", "bc", "abc"]
    # Como todos los símbolos de "abc" son distintos, alcanza n(n+1)/2 + 1 = 7
    assert len(subcadenas(w)) == (3 * 4) // 2 + 1
    assert subcadenas(w) == ["", "a", "b", "c", "ab", "bc", "abc"]

    # Con símbolos repetidos, elimina duplicados
    assert subcadenas("aba") == ["", "a", "b", "ab", "ba", "aba"]


def test_diferencia_kleene_y_positiva_longitud_cero():
    """Verifica que para n = 0, Σ* = {λ} mientras que Σ+ = ∅."""
    alfabeto = ["0", "1"]
    assert cerradura_kleene(alfabeto, 0) == [""]
    assert cerradura_positiva(alfabeto, 0) == []


def test_alfabeto_un_solo_simbolo():
    """Verifica Σ* y Σ+ para un alfabeto unario Σ = {'a'}."""
    alfabeto = ["a"]
    assert cerradura_kleene(alfabeto, 3) == ["", "a", "aa", "aaa"]
    assert cerradura_positiva(alfabeto, 3) == ["a", "aa", "aaa"]
    assert contar_cadenas_cerradura(1, 5, incluir_vacia=True) == 6
    assert contar_cadenas_cerradura(1, 5, incluir_vacia=False) == 5


def test_cerradura_alfabeto_binario():
    """Verifica Σ* y Σ+ para Σ = {'0', '1'} con n = 2."""
    alfabeto = ["0", "1"]
    esperado_positiva = ["0", "1", "00", "01", "10", "11"]
    assert cerradura_positiva(alfabeto, 2) == esperado_positiva
    assert cerradura_kleene(alfabeto, 2) == [""] + esperado_positiva


def test_rechazo_limite_doscientas_mil_cadenas():
    """Verifica que se rechacen combinaciones que generen más de 200,000 cadenas."""
    # Para |Σ| = 10 y n = 6, Σ+ tiene 10 + 100 + 1,000 + 10,000 + 100,000 + 1,000,000 = 1,111,110 > 200,000
    alfabeto_10 = [str(i) for i in range(10)]
    with pytest.raises(ValueError, match="Límite excedido"):
        cerradura_kleene(alfabeto_10, 6)

    with pytest.raises(ValueError, match="Límite excedido"):
        cerradura_positiva(alfabeto_10, 6)

    # En cambio, para |Σ| = 10 y n = 5, genera 111,111 cadenas (<= 200,000), lo cual es válido
    assert contar_cadenas_cerradura(10, 5, incluir_vacia=True) == 111_111 <= LIMITE_CADENAS
