# Ejercicio 1. Entorno de trabajo: control de versiones y contenedores

## Parte A. Investigación

### 1. ¿Qué es un sistema de control de versiones y qué problema resuelve en un trabajo en equipo?
Un **Sistema de Control de Versiones** (*Version Control System*, VCS) es una herramienta de software que registra los cambios realizados sobre un conjunto de archivos a lo largo del tiempo, almacenando instantáneas (*snapshots*) o diferencias históricas de modo que sea posible recuperar versiones específicas en cualquier momento, auditar quién modificó qué línea y por qué motivo, revertir errores e integrar contribuciones concurrentes (Chacon & Straub, 2014).

En el trabajo en equipo sin un sistema de control de versiones, suelen presentarse problemas críticos:
1. **Sobrescritura accidental de cambios (*lost updates*)**: Dos integrantes editan el mismo archivo simultáneamente y quien guarda al final pisa el trabajo del otro.
2. **Proliferación caótica de copias manuales**: Carpetas como `proyecto_final_v2_corregido_ahora_si.zip` impiden saber cuál es la versión canónica o qué cambió entre una copia y otra.
3. **Falta de trazabilidad y aislamiento**: Si una nueva funcionalidad introduce un fallo en el código base, resulta sumamente costoso identificar qué cambio exacto originó la regresión o desarrollar experimentos sin romper el flujo principal del equipo.

Un VCS distribuido como **Git** resuelve estos problemas permitiendo que cada desarrollador disponga de una copia íntegra del historial, trabaje de manera aislada mediante ramas (*branches*), combine cambios automáticamente mediante algoritmos de fusión de tres vías (*three-way merge*) y detecte explícitamente cualquier colisión antes de sobrescribir información.

---

### 2. Diferencia entre Git y GitHub
Aunque suelen mencionarse juntos, cumplen funciones distintas en el ecosistema de desarrollo:

| Criterio | Git | GitHub |
| :--- | :--- | :--- |
| **Naturaleza** | Herramienta de software libre y de código abierto (creada por Linus Torvalds en 2005) que implementa un sistema de control de versiones distribuido (DVCS). | Plataforma comercial en la nube (propiedad de Microsoft) para alojar repositorios de Git y facilitar la colaboración social y gestión de proyectos. |
| **Dónde se ejecuta** | De manera local en la computadora del desarrollador a través de la línea de comandos (`git`) o clientes gráficos, sin requerir conexión a Internet para confirmar cambios o crear ramas. | En servidores remotos accesibles vía web y protocolos de red (`HTTPS` / `SSH`). |
| **Funciones adicionales** | Gestión del grafo acíclico dirigido (DAG) de confirmaciones, ramas, etiquetas (*tags*), fusiones (*merges*) y áreas de preparación (*staging*). | *Pull Requests*, revisión de código en línea, seguimiento de incidencias (*Issues*), tableros Kanban, automatización CI/CD (*GitHub Actions*) y control de permisos de equipo. |

En síntesis: **Git** es el motor de control de versiones que gestiona el historial del código, mientras que **GitHub** es un servicio de hospedaje remoto y colaboración construido alrededor de Git (existen alternativas a GitHub como GitLab, Bitbucket o Gitea, todas usando Git por debajo).

---

### 3. Definiciones conceptuales y ejemplos prácticos

* **Repositorio (*Repository*)**: Es la estructura de datos que almacena tanto los archivos de un proyecto como la base de datos completa de su historial de revisiones, ramas y metadatos (contenida dentro del subdirectorio oculto `.git/`).
  * *Ejemplo*: La carpeta `practica1-tc/` inicializada con `git init` o clonada desde GitHub mediante `git clone https://github.com/usuario/practica1-tc.git`.
* **Confirmación (*Commit*)**: Es una instantánea inmutable del estado de los archivos preparados (*staged*) del proyecto en un instante determinado. Cada confirmación se identifica de manera única mediante un resumen criptográfico SHA-1 (o SHA-256) de 40 caracteres hexadecimales e incluye un apuntador al commit padre, autor, marca de tiempo y un mensaje descriptivo.
  * *Ejemplo*: Ejecutar `git commit -m "feat(lenguajes): implementa cálculo de cerradura de Kleene y positiva"` tras agregar `src/lenguajes.py` al área de preparación.
* **Rama (*Branch*)**: Es un apuntador móvil ligero que referencia a una confirmación específica y permite divergir de la línea principal de desarrollo (`main`) para trabajar en una característica, experimento o corrección de forma aislada sin alterar el código estable.
  * *Ejemplo*: Crear la rama `git switch -c feat/validacion-limite` para programar y probar el límite de 200,000 cadenas mientras `main` permanece intacta.
* **Fusión (*Merge*)**: Es la operación mediante la cual Git integra las historias divergentes de dos ramas en una sola, creando (en el caso no lineal) una nueva confirmación de fusión (*merge commit*) que tiene dos padres.
  * *Ejemplo*: Situarse en `main` (`git switch main`) y ejecutar `git merge feat/validacion-limite` para incorporar los cambios terminados a la rama principal.
* **Conflicto de fusión (*Merge Conflict*)**: Situación que ocurre cuando dos ramas que se intentan fusionar han modificado las mismas líneas de un mismo archivo de maneras distintas (o una rama eliminó un archivo que la otra editó), por lo que Git detiene la fusión automática y solicita la intervención humana para decidir qué versión conservar.
  * *Ejemplo*: La rama `main` define `LIMITE_CADENAS = 200_000` en la línea 15 de `src/lenguajes.py`, mientras que la rama `experimento` modifica esa misma línea 15 a `LIMITE_CADENAS = 100_000`. Al fusionarlas, Git inserta marcadores `<<<<<<< HEAD`, `=======` y `>>>>>>> experimento` para que el autor resuelva la discrepancia.
* **Pull Request (PR)** (o *Merge Request*): Mecanismo provisto por plataformas como GitHub mediante el cual un colaborador solicita formalmente que los cambios empujados a una rama secundaria sean revisados, discutidos, validados por pruebas automatizadas y finalmente fusionados hacia la rama de destino (como `main`).
  * *Ejemplo*: Abrir el Pull Request #1 titulado *"Agrega suite de pruebas unitarias y validaciones de cerradura"* desde la rama `feat/pruebas-extra` hacia `main`, describir los cambios realizados y fusionarlo tras verificar que las pruebas aprueban.
* **Archivo `.gitignore`**: Archivo de texto plano ubicado en la raíz del repositorio cuyas líneas especifican patrones (*glob patterns*) de archivos o directorios que Git debe ignorar deliberadamente y no rastrear ni incluir en las confirmaciones (archivos temporales, binarios compilados, entornos virtuales o credenciales).
  * *Ejemplo*: Incluir las líneas `venv/`, `__pycache__/` y `*.pyc` en `.gitignore` para evitar subir miles de archivos locales del entorno virtual o bytecode de Python al repositorio remoto.
* **Archivo `README.md`**: Documento principal de presentación y documentación de un repositorio, escrito habitualmente en formato Markdown, que las plataformas como GitHub renderizan automáticamente en la página de inicio del proyecto. Explica el propósito del software, su estructura, requisitos e instrucciones de instalación y ejecución.
  * *Ejemplo*: El archivo `README.md` en la raíz de `practica1-tc/` que contiene los datos de portada del alumno, el índice con enlaces a `docs/` y los comandos de Docker Compose para levantar la aplicación y correr `pytest`.

---

### 4. ¿Qué es un contenedor y en qué se diferencia de una máquina virtual (arranque, tamaño y aislamiento)?
Un **contenedor** es una unidad estándar y ligera de software que empaqueta el código de una aplicación junto con todas sus bibliotecas, variables de entorno y dependencias del sistema de archivos, ejecutándose como un proceso aislado sobre el núcleo (*kernel*) compartido del sistema operativo anfitrión mediante mecanismos nativos de Linux como *namespaces* (aislamiento de vistas de procesos, red y montajes) y *cgroups* (control y límite de recursos de CPU y memoria) (Merkel, 2014).

Por el contrario, una **Máquina Virtual (MV)** emula por software un sistema de cómputo físico completo (CPU, discos, tarjetas de red) mediante un hipervisor (como VMware, VirtualBox o KVM) y ejecuta su propio sistema operativo invitado (*guest OS*) con un *kernel* independiente por cada instancia.

| Dimensión | Contenedor (Docker / Podman) | Máquina Virtual (MV) |
| :--- | :--- | :--- |
| **Tiempo de arranque** | **Milisegundos a pocos segundos**. Como el núcleo del sistema operativo ya está en ejecución, iniciar un contenedor equivale simplemente a lanzar un nuevo proceso aislado en el anfitrión. | **De decenas de segundos a varios minutos**. Debe pasar por el proceso de arranque del BIOS/UEFI virtual, inicializar el *kernel* invitado y levantar todos los demonios y servicios del sistema operativo completo. |
| **Tamaño en disco y memoria** | **Decenas a pocos cientos de megabytes (MB)**. Las imágenes omiten el núcleo y los controladores de hardware, y además reutilizan capas inmutables compartidas (*OverlayFS*) entre contenedores (por ejemplo, `python:3.12-slim` pesa alrededor de 45–50 MB comprimida). | **Varios gigabytes (GB)** (típicamente de 4 GB a 40+ GB por máquina). Cada MV duplica el sistema operativo completo, su propio *kernel*, bibliotecas base y espacio de disco virtual. |
| **Nivel de aislamiento** | **Aislamiento a nivel de proceso / espacio de usuario**. Todos los contenedores comparten el mismo *kernel* del anfitrión; es muy eficiente en rendimiento (casi nativo), aunque una vulnerabilidad crítica en el *kernel* podría comprometer el aislamiento. | **Aislamiento a nivel de hardware virtualizado**. Cada MV está separada por el hipervisor y posee su propio *kernel*, ofreciendo una frontera de seguridad más estricta y la posibilidad de ejecutar sistemas operativos con núcleos distintos al anfitrión. |

---

### 5. Definición de imagen, contenedor, volumen y puerto publicado

* **Imagen (*Image*)**: Es una plantilla de solo lectura, inmutable y estructurada en capas superpuestas (construida a partir de las instrucciones de un `Dockerfile`), que contiene el sistema de archivos raíz mínimo, el intérprete o binario, las bibliotecas instaladas y la configuración predeterminada necesaria para crear contenedores. Una imagen es análoga a una *clase* en programación orientada a objetos o a un ejecutable en reposo en disco.
* **Contenedor (*Container*)**: Es una instancia ejecutable y viva de una imagen. Cuando Docker arranca un contenedor a partir de una imagen, añade una capa delgada de lectura/escritura (*writable layer*) sobre las capas inmutables de la imagen y le asigna su propio espacio de nombres de procesos, red e identificadores. Es análogo a un *objeto* instanciado en memoria o a un proceso en ejecución.
* **Volumen (*Volume* / *Bind Mount*)**: Es un mecanismo que permite persistir datos generados por un contenedor o compartir directorios entre el sistema anfitrión y el contenedor, evitando que los archivos se pierdan cuando el contenedor se elimina y eludiendo el sistema de archivos por capas del contenedor. En `compose.yml`, la línea `- ..:/app` monta la carpeta raíz del repositorio en `/app` dentro del contenedor, permitiendo que cualquier edición en el código fuente o en las pruebas se refleje de inmediato sin reconstruir la imagen.
* **Puerto publicado (*Published Port*)**: Dado que cada contenedor posee su propia interfaz de red virtual aislada, un servicio que escucha dentro del contenedor (por ejemplo, Flet en el puerto `8550`) no es accesible desde fuera por defecto. Publicar un puerto consiste en crear una regla de reenvío (*port mapping* / NAT) entre un puerto de la máquina anfitriona y un puerto del contenedor. En `compose.yml`, `"8550:8550"` redirige el tráfico de `localhost:8550` del equipo anfitrión hacia el puerto `8550` del contenedor `py312`.

---

### 6. ¿Qué es un entorno virtual de Python y por qué no modifica la versión del intérprete?
Un **entorno virtual de Python** (creado con el módulo estándar `venv`) es un árbol de directorios autocontenido y aislado que dispone de su propia carpeta de paquetes de terceros (`site-packages`) y de sus propios scripts de activación (`bin/activate` en POSIX o `Scripts\activate` en Windows), permitiendo que un proyecto instale versiones específicas de bibliotecas (como `flet==0.86.5` y `pytest==8.3.4`) sin entrar en conflicto con otros proyectos ni contaminar la instalación global del sistema (Python Software Foundation, 2024).

**¿Por qué un entorno virtual no modifica la versión del intérprete?**
Porque `python -m venv` **no descarga ni compila un nuevo intérprete de Python**. En su lugar, únicamente crea un enlace simbólico (*symlink*) o una copia ligera del ejecutable `python` exacto con el que fue invocado y configura las rutas de búsqueda (`sys.prefix` y `sys.exec_prefix`) para que ese mismo intérprete lea e instale bibliotecas en el directorio `site-packages` del entorno virtual. Por ende, si el entorno virtual se crea ejecutando Python 3.12, el entorno virtual ejecutará invariablemente Python 3.12; para disponer de Python 3.11, 3.12 y 3.13 simultáneamente se requiere contar con los tres intérpretes base instalados o, como se diseña en esta práctica, aislar cada versión base en su propio contenedor independiente.

---

### 7. ¿Por qué conviene fijar la versión de la imagen (`python:3.12-slim`) en lugar de emplear `python:latest`?
1. **Reproducibilidad y determinismo**: La etiqueta `:latest` es una referencia móvil (*mutable tag*) que apunta a la última versión estable publicada en Docker Hub en el momento de la descarga (actualmente 3.13, y en el futuro 3.14, 3.15, etc.). Si un integrante del equipo o el docente construye la imagen meses después usando `python:latest`, obtendrá una versión mayor del intérprete distinta a aquella con la que se desarrolló el proyecto, pudiendo romper dependencias (por ejemplo, paquetes cuyas ruedas precompiladas o *wheels* aún no soportan la nueva versión o módulos eliminados de la biblioteca estándar).
2. **Tamaño reducido y menor superficie de ataque (`-slim`)**: La variante predeterminada (`python:latest` o `python:3.12`) se basa en una imagen Debian completa que incluye compiladores (`gcc`), cabeceras de desarrollo, clientes de control de versiones y herramientas de sistema que superan los 900 MB. En cambio, la variante **`python:3.12-slim`** contiene únicamente los paquetes mínimos indispensables de Debian para ejecutar CPython 3.12 (~120–150 MB descomprimida), lo que acelera drásticamente la descarga y construcción de los tres contenedores, reduce el consumo de disco y disminuye la superficie de vulnerabilidades de seguridad.

---

## Parte C. Los tres entornos de Python y explicación línea por línea

### 1. Justificación de la elección de las tres versiones (3.11, 3.12 y 3.13)
De acuerdo con el calendario oficial del ciclo de vida y fin de soporte (*End-of-Life*, EOL) publicado en el **PEP 664**, **PEP 693** y **PEP 719**, así como el portal oficial *Status of Python versions* de la Python Software Foundation (2025), y los metadatos de publicación del paquete **`flet` v0.86.5** en el Python Package Index (PyPI, `Requires-Python >=3.10`):

| Servicio | Imagen Base | Estado y Fin de Soporte (EOL) | Justificación Técnica |
| :--- | :--- | :--- | :--- |
| **`py311`** | `python:3.11-slim` | Lanzada el 24/10/2022; soporte de seguridad hasta **octubre de 2027** (PEP 664). | Representa la versión más antigua utilizada en la matriz de pruebas que cuenta con soporte oficial vigente de seguridad y cumple holgadamente con el requisito `Requires-Python >= 3.10` de `flet==0.86.5`, permitiendo verificar la retrocompatibilidad del código (incluyendo anotaciones de tipos modernas con `from __future__ import annotations`). |
| **`py312`** | `python:3.12-slim` | Lanzada el 02/10/2023; soporte de seguridad hasta **octubre de 2028** (PEP 693). | Es la **versión de referencia del curso** establecida para la Unidad de Aprendizaje. Es el contenedor designado para publicar el puerto `8550` y servir la aplicación web interactiva con Flet hacia el navegador del equipo anfitrión. |
| **`py313`** | `python:3.13-slim` | Lanzada el 07/10/2024; soporte de seguridad hasta **octubre de 2029** (PEP 719). | Versión reciente del lenguaje que introduce optimizaciones en el intérprete y limpieza de módulos obsoletos (PEP 594). Ejecutar la misma suite de `pytest` en `py313` demuestra que nuestro programa y sus dependencias no dependen de comportamientos obsoletos o que hayan cambiado en revisiones recientes. |

---

### 2. Explicación línea por línea de los archivos del entorno (Anexo 2)

#### A. Archivo [`requirements.txt`](../requirements.txt)
```text
flet[web]==0.86.5
pytest==8.3.4
```
* `flet[web]==0.86.5`: Declara la dependencia del marco de trabajo gráfico Flet fijada exactamente en la versión `0.86.5`. El extra opcional `[web]` instala el servidor web asíncrono subyacente (Uvicorn/FastAPI y los activos web de Flutter), indispensable para servir la interfaz como aplicación web desde un contenedor sin entorno de escritorio gráfico (X11/Wayland).
* `pytest==8.3.4`: Fija el marco de pruebas unitarias `pytest` en su versión exacta `8.3.4`, garantizando que los tres contenedores ejecuten el mismo motor de pruebas de manera reproducible.

---

#### B. Archivo [`entorno/Dockerfile`](../entorno/Dockerfile)
```dockerfile
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLET_FORCE_WEB_SERVER=true
ENV FLET_SERVER_PORT=8550

CMD ["python", "src/app.py"]
```
* `ARG PYTHON_VERSION=3.12`: Define un argumento de tiempo de construcción (*build-time argument*) llamado `PYTHON_VERSION` con valor por defecto `3.12`. Permite reutilizar un **único `Dockerfile`** parametrizado para construir las tres imágenes (`3.11`, `3.12` y `3.13`) desde `compose.yml`.
* `FROM python:${PYTHON_VERSION}-slim`: Establece la imagen base oficial de Python en su variante ligera Debian `-slim`, interpolando el valor de `PYTHON_VERSION` recibido.
* `RUN python -m venv /opt/venv`: Ejecuta el módulo `venv` para crear un entorno virtual aislado en `/opt/venv`. Se ubica deliberadamente en `/opt/venv` (fuera de `/app`) porque en `compose.yml` el directorio `/app` es sustituido en tiempo de ejecución por el volumen montado `..:/app`; si el entorno virtual estuviera dentro de `/app/venv`, quedaría oculto por el montaje del volumen del anfitrión.
* `ENV PATH="/opt/venv/bin:$PATH"`: Antepone el directorio de binarios del entorno virtual (`/opt/venv/bin`) a la variable de entorno `PATH` de la imagen. En contenedores esto equivale a activar permanentemente el entorno virtual para todos los comandos `RUN`, `CMD` o `docker compose run` posteriores (`python`, `pip`, `pytest`).
* `WORKDIR /app`: Define `/app` como el directorio de trabajo actual dentro del contenedor (creándolo si no existe) para todas las instrucciones subsiguientes.
* `COPY requirements.txt .`: Copia únicamente el archivo `requirements.txt` desde el contexto de construcción hacia `/app/requirements.txt` antes de copiar el resto del código fuente, aprovechando el sistema de caché de capas de Docker (la capa de instalación de paquetes no se vuelve a ejecutar mientras `requirements.txt` no cambie).
* `RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt`: Actualiza `pip` e instala las dependencias fijadas dentro de `/opt/venv`. La bandera `--no-cache-dir` evita almacenar archivos `.whl` descargados en la caché de `pip`, reduciendo el tamaño final de la imagen.
* `COPY . .`: Copia el resto de los archivos del repositorio (respetando exclusiones si hubiera `.dockerignore`) hacia `/app` dentro de la imagen.
* `ENV FLET_FORCE_WEB_SERVER=true`: Configura la variable de entorno de Flet que fuerza el arranque de la aplicación en modo servidor web headless (escuchando en todas las interfaces `0.0.0.0`), ya que dentro del contenedor no existe un servidor gráfico de escritorio.
* `ENV FLET_SERVER_PORT=8550`: Indica a Flet que el servidor web interno debe escuchar peticiones HTTP/WebSocket en el puerto TCP `8550`.
* `CMD ["python", "src/app.py"]`: Define el comando predeterminado (en formato *exec* sin shell intermedio) que ejecuta el contenedor al iniciarse con `docker compose up`, lanzando la interfaz gráfica en `src/app.py`.

---

#### C. Archivo [`entorno/compose.yml`](../entorno/compose.yml)
* `services:`: Bloque raíz de Docker Compose V2 que declara los contenedores que conforman la aplicación (ya no se incluye la clave obsoleta `version: '3.8'`).
* `py311:` / `py312:` / `py313:`: Nombres lógicos de los tres servicios que representan cada entorno de Python.
* `build:`: Indica cómo construir la imagen de cada servicio:
  * `context: ..`: Establece el directorio padre (la raíz del repositorio `practica1-tc/`) como contexto de construcción para que el `Dockerfile` pueda acceder a `requirements.txt` y `src/`.
  * `dockerfile: entorno/Dockerfile`: Especifica la ruta relativa del `Dockerfile` dentro del contexto.
  * `args: PYTHON_VERSION: "3.11"` (o `"3.12"`, `"3.13"`): Pasa el argumento de construcción al `ARG PYTHON_VERSION` del `Dockerfile`.
* `container_name: tc_p1_py311` (y equivalentes): Asigna un nombre fijo e identificable a cada contenedor creado.
* `ports: - "8550:8550"` (en `py312`): Publica y enlaza el puerto `8550` de la máquina anfitriona con el puerto `8550` del contenedor `py312`, permitiendo abrir `http://localhost:8550` en el navegador.
* `volumes: - ..:/app`: Monta el directorio raíz del repositorio (`..`) dentro de `/app` en el contenedor (*bind mount*), permitiendo ejecutar pruebas y reflejar cambios en el código en tiempo real sin reconstruir las imágenes.
* `command: pytest -q` (en `py311` y `py313`): Sobrescribe el `CMD` predeterminado del `Dockerfile` para que los contenedores de verificación ejecuten directamente la suite de pruebas en modo silencioso (`-q`).

---

#### D. Archivo [`pytest.ini`](../pytest.ini)
* `[pytest]`: Cabecera de configuración de `pytest`.
* `pythonpath = src`: Agrega automáticamente la carpeta `src/` a `sys.path` durante la ejecución de pruebas, permitiendo que `tests/test_lenguajes.py` importe `from lenguajes import ...` limpiamente sin modificar la variable de entorno `PYTHONPATH`.
* `testpaths = tests`: Indica a `pytest` que busque los archivos de prueba dentro del directorio `tests/`.

---

#### E. Comandos de ejecución y diagnóstico
* `docker compose build`: Construye las tres imágenes (`py311`, `py312`, `py313`) pasando a cada una su respectivo argumento `PYTHON_VERSION`.
* `docker compose run --rm py311 python --version` (y equivalentes para `py312`, `py313`): Crea un contenedor efímero del servicio indicado, ejecuta `python --version` para comprobar la versión exacta del intérprete y elimina el contenedor automáticamente al terminar gracias a la bandera `--rm`.
* `docker compose run --rm py311 pytest -q` (y equivalentes para `py312`, `py313`): Ejecuta la suite de pruebas automatizadas dentro de cada uno de los tres contenedores efímeros en modo conciso (`-q`).
* `docker compose up py312`: Levanta el contenedor de referencia `py312` ejecutando su `CMD` por defecto (`python src/app.py`) y expone la aplicación web de Flet en `http://localhost:8550`.
* `docker compose down`: Detiene los contenedores en ejecución y elimina los contenedores y redes virtuales creados por Compose.
* `docker image ls`: Lista las imágenes almacenadas localmente para verificar las tres imágenes construidas y su tamaño.
* `docker compose logs py312`: Muestra la salida estándar y de errores (*logs*) del contenedor `py312` para diagnosticar posibles fallos.

---

## Evidencias del Ejercicio 1

* **Historial de confirmaciones y ramas (`git log --oneline --graph --all`)**: Véase [`evidencias/git/git_log.txt`](../evidencias/git/git_log.txt) y [`evidencias/git/git_log.png`](../evidencias/git/git_log.png).
* **Pull Request y fusión de rama**: Véase [`evidencias/git/pull_request_merge.png`](../evidencias/git/pull_request_merge.png).
* **Verificación de versiones de Python (`python --version`) en los tres entornos**: Véase [`evidencias/docker/python_versions.txt`](../evidencias/docker/python_versions.txt) y [`evidencias/docker/python_versions.png`](../evidencias/docker/python_versions.png).
