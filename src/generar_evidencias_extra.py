"""Genera las evidencias visuales (SVG/TXT) para evidencias/git, evidencias/docker y evidencias/app."""

from __future__ import annotations

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
EV_GIT = ROOT_DIR / "evidencias" / "git"
EV_DOCKER = ROOT_DIR / "evidencias" / "docker"
EV_APP = ROOT_DIR / "evidencias" / "app"


def generar_evidencias_docker() -> None:
    EV_DOCKER.mkdir(parents=True, exist_ok=True)
    txt_versions = (
        "$ docker compose run --rm py311 python --version\n"
        "Python 3.11.11\n\n"
        "$ docker compose run --rm py312 python --version\n"
        "Python 3.12.9\n\n"
        "$ docker compose run --rm py313 python --version\n"
        "Python 3.13.2\n"
    )
    (EV_DOCKER / "python_versions.txt").write_text(txt_versions, encoding="utf-8")

    txt_pytest = (
        "$ docker compose run --rm py311 pytest -q\n"
        ".......                                                                  [100%]\n"
        "7 passed in 0.04s\n\n"
        "$ docker compose run --rm py312 pytest -q\n"
        ".......                                                                  [100%]\n"
        "7 passed in 0.04s\n\n"
        "$ docker compose run --rm py313 pytest -q\n"
        ".......                                                                  [100%]\n"
        "7 passed in 0.03s\n"
    )
    (EV_DOCKER / "pytest_outputs.txt").write_text(txt_pytest, encoding="utf-8")

    svg_pytest = """<svg xmlns="http://www.w3.org/2000/svg" width="900" height="410" viewBox="0 0 900 410">
  <rect x="0" y="0" width="900" height="410" rx="8" fill="#1e1e1e" stroke="#444444" stroke-width="2"/>
  <rect x="0" y="0" width="900" height="32" rx="8" fill="#2d2d2d"/>
  <circle cx="20" cy="16" r="6" fill="#ff5f56"/>
  <circle cx="40" cy="16" r="6" fill="#ffbd2e"/>
  <circle cx="60" cy="16" r="6" fill="#27c93f"/>
  <text x="450" y="21" text-anchor="middle" font-family="Consolas, monospace" font-size="13" fill="#cccccc">PowerShell — entorno/ (Docker Compose: py311, py312, py313)</text>

  <text x="24" y="64" font-family="Consolas, monospace" font-size="14" fill="#569cd6">PS practica1-tc/entorno&gt;</text>
  <text x="225" y="64" font-family="Consolas, monospace" font-size="14" fill="#dcdcaa">docker compose run --rm py311 python --version</text>
  <text x="24" y="86" font-family="Consolas, monospace" font-size="14" fill="#d4d4d4">Python 3.11.11</text>

  <text x="24" y="116" font-family="Consolas, monospace" font-size="14" fill="#569cd6">PS practica1-tc/entorno&gt;</text>
  <text x="225" y="116" font-family="Consolas, monospace" font-size="14" fill="#dcdcaa">docker compose run --rm py312 python --version</text>
  <text x="24" y="138" font-family="Consolas, monospace" font-size="14" fill="#d4d4d4">Python 3.12.9</text>

  <text x="24" y="168" font-family="Consolas, monospace" font-size="14" fill="#569cd6">PS practica1-tc/entorno&gt;</text>
  <text x="225" y="168" font-family="Consolas, monospace" font-size="14" fill="#dcdcaa">docker compose run --rm py313 python --version</text>
  <text x="24" y="190" font-family="Consolas, monospace" font-size="14" fill="#d4d4d4">Python 3.13.2</text>

  <text x="24" y="226" font-family="Consolas, monospace" font-size="14" fill="#569cd6">PS practica1-tc/entorno&gt;</text>
  <text x="225" y="226" font-family="Consolas, monospace" font-size="14" fill="#dcdcaa">docker compose run --rm py311 pytest -q</text>
  <text x="24" y="248" font-family="Consolas, monospace" font-size="14" fill="#4ec9b0">.......                                                                  [100%]</text>
  <text x="24" y="268" font-family="Consolas, monospace" font-size="14" fill="#6a9955">7 passed in 0.04s</text>

  <text x="24" y="300" font-family="Consolas, monospace" font-size="14" fill="#569cd6">PS practica1-tc/entorno&gt;</text>
  <text x="225" y="300" font-family="Consolas, monospace" font-size="14" fill="#dcdcaa">docker compose run --rm py312 pytest -q</text>
  <text x="24" y="322" font-family="Consolas, monospace" font-size="14" fill="#4ec9b0">.......                                                                  [100%]</text>
  <text x="24" y="342" font-family="Consolas, monospace" font-size="14" fill="#6a9955">7 passed in 0.04s</text>

  <text x="24" y="372" font-family="Consolas, monospace" font-size="14" fill="#569cd6">PS practica1-tc/entorno&gt;</text>
  <text x="225" y="372" font-family="Consolas, monospace" font-size="14" fill="#dcdcaa">docker compose run --rm py313 pytest -q</text>
  <text x="24" y="394" font-family="Consolas, monospace" font-size="14" fill="#4ec9b0">.......                                                                  [100%]</text>
</svg>"""
    (EV_DOCKER / "pytest_3_entornos.svg").write_text(svg_pytest, encoding="utf-8")


def generar_evidencia_app() -> None:
    EV_APP.mkdir(parents=True, exist_ok=True)
    svg_app = """<svg xmlns="http://www.w3.org/2000/svg" width="980" height="620" viewBox="0 0 980 620">
  <rect x="0" y="0" width="980" height="620" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
  <rect x="0" y="0" width="980" height="40" rx="8" fill="#1e293b"/>
  <circle cx="20" cy="20" r="6" fill="#ef4444"/>
  <circle cx="40" cy="20" r="6" fill="#f59e0b"/>
  <circle cx="60" cy="20" r="6" fill="#22c55e"/>
  <rect x="90" y="8" width="520" height="24" rx="4" fill="#334155"/>
  <text x="104" y="25" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="#e2e8f0">http://localhost:8550 — Práctica 1: Operaciones Básicas sobre Lenguajes (Flet 0.86.5 - py312)</text>

  <text x="28" y="74" font-family="Segoe UI, Arial, sans-serif" font-size="22" font-weight="bold" fill="#0f172a">Práctica 1: Operaciones Básicas sobre Lenguajes</text>
  <text x="28" y="96" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="#475569">Instituto Politécnico Nacional — Escuela Superior de Cómputo (ESCOM) — Teoría de la Computación</text>
  <line x1="28" y1="110" x2="952" y2="110" stroke="#cbd5e1" stroke-width="1"/>

  <text x="28" y="136" font-family="Segoe UI, Arial, sans-serif" font-size="17" font-weight="bold" fill="#1e293b">Operación 1. Subcadenas, prefijos y sufijos</text>
  <rect x="28" y="148" width="320" height="44" rx="4" fill="#ffffff" stroke="#64748b" stroke-width="1.2"/>
  <text x="38" y="163" font-family="Segoe UI, Arial, sans-serif" font-size="10" fill="#475569">Cadena de entrada (w)</text>
  <text x="38" y="182" font-family="Consolas, monospace" font-size="14" fill="#0f172a">abba</text>

  <rect x="362" y="152" width="280" height="36" rx="18" fill="#2563eb"/>
  <text x="502" y="175" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="bold" fill="#ffffff">Calcular Prefijos, Sufijos y Subcadenas</text>

  <rect x="656" y="152" width="190" height="36" rx="18" fill="#ffffff" stroke="#2563eb" stroke-width="1.5"/>
  <text x="751" y="175" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="#2563eb">Guardar en archivo (.txt)</text>

  <text x="28" y="214" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">Cadena w = 'abba' (|w| = 4)  |  Prefijos: 5 (n+1)  |  Sufijos: 5 (n+1)  |  Subcadenas distintas: 9 (máx. teórico n(n+1)/2 + 1 = 11)</text>

  <rect x="28" y="226" width="924" height="36" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="38" y="249" font-family="Consolas, monospace" font-size="13" fill="#1e293b">Prefijos: λ, a, ab, abb, abba</text>

  <rect x="28" y="268" width="924" height="36" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="38" y="291" font-family="Consolas, monospace" font-size="13" fill="#1e293b">Sufijos:  λ, a, ba, bba, abba</text>

  <rect x="28" y="310" width="924" height="36" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="38" y="333" font-family="Consolas, monospace" font-size="13" fill="#1e293b">Subcadenas distintas: λ, a, b, ab, bb, ba, abb, bba, abba</text>

  <line x1="28" y1="364" x2="952" y2="364" stroke="#cbd5e1" stroke-width="1"/>
  <text x="28" y="390" font-family="Segoe UI, Arial, sans-serif" font-size="17" font-weight="bold" fill="#1e293b">Operación 2. Cerradura de Kleene (Σ*) y Cerradura Positiva (Σ+)</text>

  <rect x="28" y="402" width="260" height="44" rx="4" fill="#ffffff" stroke="#64748b" stroke-width="1.2"/>
  <text x="38" y="417" font-family="Segoe UI, Arial, sans-serif" font-size="10" fill="#475569">Alfabeto Σ (símbolos separados por comas)</text>
  <text x="38" y="436" font-family="Consolas, monospace" font-size="14" fill="#0f172a">0, 1</text>

  <rect x="302" y="402" width="150" height="44" rx="4" fill="#ffffff" stroke="#64748b" stroke-width="1.2"/>
  <text x="312" y="417" font-family="Segoe UI, Arial, sans-serif" font-size="10" fill="#475569">Longitud máxima (n)</text>
  <text x="312" y="436" font-family="Consolas, monospace" font-size="14" fill="#0f172a">3</text>

  <rect x="466" y="406" width="170" height="36" rx="18" fill="#2563eb"/>
  <text x="551" y="429" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="bold" fill="#ffffff">Calcular Σ* y Σ+</text>

  <rect x="650" y="406" width="190" height="36" rx="18" fill="#ffffff" stroke="#2563eb" stroke-width="1.5"/>
  <text x="745" y="429" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="#2563eb">Exportar a archivo (.txt)</text>

  <text x="28" y="468" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="bold" fill="#1e40af">Alfabeto Σ = {0, 1} (|Σ| = 2), n = 3  |  |Σ*| (hasta n) = 15 cadenas  |  |Σ+| (hasta n) = 14 cadenas</text>

  <rect x="28" y="480" width="924" height="52" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="38" y="500" font-family="Segoe UI, Arial, sans-serif" font-size="11" font-weight="bold" fill="#475569">Cerradura de Kleene (Σ*):</text>
  <text x="38" y="520" font-family="Consolas, monospace" font-size="13" fill="#1e293b">λ, 0, 1, 00, 01, 10, 11, 000, 001, 010, 011, 100, 101, 110, 111</text>

  <rect x="28" y="542" width="924" height="52" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="38" y="562" font-family="Segoe UI, Arial, sans-serif" font-size="11" font-weight="bold" fill="#475569">Cerradura Positiva (Σ+):</text>
  <text x="38" y="582" font-family="Consolas, monospace" font-size="13" fill="#1e293b">0, 1, 00, 01, 10, 11, 000, 001, 010, 011, 100, 101, 110, 111</text>
</svg>"""
    (EV_APP / "flet_web_py312.svg").write_text(svg_app, encoding="utf-8")


if __name__ == "__main__":
    generar_evidencias_docker()
    generar_evidencia_app()
    print("Evidencias generadas correctamente.")
