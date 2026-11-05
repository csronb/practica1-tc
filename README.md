# Instituto Politécnico Nacional
## Escuela Superior de Cómputo (ESCOM)

---

### Práctica 1: Operaciones Básicas sobre Lenguajes

| Campo | Información |
| :--- | :--- |
| **Alumno (Nombre completo)** | `Cesar Octavio Navarro Bahena` |
| **Número de Boleta** | `2023630464` |
| **Grupo** | `4CM4]` |
| **Carrera** | Ingeniería en Sistemas Computacionales (Plan 2020) |
| **Unidad de Aprendizaje** | Teoría de la Computación |
| **Profesor(a)** | `Gabriel Hurtado Aviles` |
| **Fecha de Entrega** | 22 de septiembre de 2026 |
| **Versión de Flet utilizada** | `flet[web]==0.86.5` |

---

## Índice de la Práctica

El reporte completo de la práctica se encuentra estructurado en documentos Markdown dentro de la carpeta [`docs/`](docs/):

1. [**Ejercicio 1. Entorno de trabajo: control de versiones y contenedores**](docs/01-entorno.md)
   * Parte A: Investigación sobre sistemas de control de versiones, Git vs. GitHub, contenedores vs. máquinas virtuales, entornos virtuales de Python y fijación de etiquetas Docker.
   * Parte B: Configuración del repositorio, `.gitignore`, historial de confirmaciones, ramas y *Pull Request*.
   * Parte C: Los tres entornos de Python (`py311`, `py312`, `py313`), justificación de versiones con fuentes oficiales y explicación línea por línea del `Dockerfile`, `compose.yml`, `requirements.txt` y `pytest.ini`.
2. [**Ejercicio 2. Investigación: qué es la Teoría de la Computación**](docs/02-investigacion.md)
   * Definición y comparación de autores (Sipser, 2012; Hopcroft et al., 2007).
   * Orígenes históricos: paradojas de la lógica, programa de Hilbert, teoremas de Gödel y el *Entscheidungsproblem*.
   * Las tres ramas de la Teoría de la Computación y la Tesis de Church-Turing.
   * Definiciones formales de alfabeto, cadena y lenguaje; operaciones, demostración de por qué $\Sigma^0 = \{\lambda\}$ y distinción entre $\Sigma^*$ y $\Sigma^+$.
   * Tabla de la Jerarquía de Chomsky, definición formal de AFD y AFN, su equivalencia y tres aplicaciones reales de expresiones regulares.
3. [**Ejercicio 3. Estado del arte: cinco artículos**](docs/03-estado-del-arte.md)
   * Análisis y respuestas puntuales sobre Gribkoff (2013), Luna-Benoso et al. (2022) y el trabajo original de Turing (1936/1937).
   * Cinco fichas completas en formato APA 7.ª edición (incluyendo Wang et al., 2019 y Weiss et al., 2018).
   * Tabla comparativa y análisis crítico de cierre (media cuartilla) con identificación de un problema abierto.
4. [**Ejercicio 4. Autómatas finitos en JFLAP**](docs/04-jflap.md)
   * Diseño, invariantes del prefijo leído por estado, tablas de transiciones, pruebas con cadenas válidas/inválidas/frontera y simulaciones paso a paso de los ejercicios con asterisco (`*`) de la Lista 2 (94–150) y Lista 3 (151–263).
   * Archivos `.jff` exportados y versionados en [`automatas/`](automatas/).
5. [**Ejercicio 5. Aplicación con interfaz gráfica**](docs/05-aplicacion.md)
   * Separación entre el núcleo puro ([`src/lenguajes.py`](src/lenguajes.py)) y la interfaz en Flet ([`src/app.py`](src/app.py)).
   * Análisis combinatorio de prefijos ($n+1$), subcadenas ($n(n+1)/2 + 1$), convención sobre $\lambda$ y justificación del límite de $200,000$ cadenas frente a $|\Sigma|^n$.
   * Resultados de la suite [`tests/test_lenguajes.py`](tests/test_lenguajes.py) en los tres contenedores (`py311`, `py312`, `py313`).
6. [**Conclusiones**](docs/conclusiones.md)
7. [**Bibliografía General (APA 7.ª Edición)**](docs/bibliografia.md)

---

## Estructura del Repositorio

```text
practica1-tc/
├── README.md
├── .gitignore
├── requirements.txt
├── pytest.ini
├── docs/
│   ├── 01-entorno.md
│   ├── 02-investigacion.md
│   ├── 03-estado-del-arte.md
│   ├── 04-jflap.md
│   ├── 05-aplicacion.md
│   ├── conclusiones.md
│   └── bibliografia.md
├── entorno/
│   ├── Dockerfile
│   └── compose.yml
├── automatas/
│   └── *.jff (60 autómatas de las Listas 2 y 3)
├── src/
│   ├── lenguajes.py
│   ├── app.py
│   ├── generar_jflap.py
│   └── generar_evidencias_jflap.py
├── tests/
│   └── test_lenguajes.py
└── evidencias/
    ├── git/
    ├── docker/
    ├── jflap/
    └── app/
```

---

## Instrucciones para Levantar el Entorno y Ejecutar las Pruebas

Todos los comandos de contenedores se ejecutan situándose dentro de la carpeta [`entorno/`](entorno/):

```bash
cd entorno
```

### 1. Construir las imágenes de los tres entornos (`py311`, `py312` y `py313`)
```bash
docker compose build
```

### 2. Verificar la versión del intérprete de Python en cada contenedor
```bash
docker compose run --rm py311 python --version
docker compose run --rm py312 python --version
docker compose run --rm py313 python --version
```

### 3. Ejecutar la suite de pruebas automatizadas (`pytest`) en los tres contenedores
```bash
docker compose run --rm py311 pytest -q
docker compose run --rm py312 pytest -q
docker compose run --rm py313 pytest -q
```

### 4. Levantar la aplicación web interactiva con Flet (servicio `py312`)
```bash
docker compose up py312
```
Una vez iniciado el contenedor, abra en su navegador web la dirección:
* **http://localhost:8550**

Para detener y limpiar los contenedores:
```bash
docker compose down
```

### 5. Ejecución alternativa en entorno local (Anexo 3)
Si desea ejecutar las pruebas o la aplicación en un entorno virtual local fuera de Docker:
```bash
py -3.12 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pytest -q
python src/app.py
```
