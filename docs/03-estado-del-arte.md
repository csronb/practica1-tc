# Ejercicio 3. Estado del arte: cinco artículos

En este documento se desarrolla el análisis crítico y las fichas técnicas de los cinco textos científicos y académicos solicitados: los tres asignados (Gribkoff, 2013; Luna-Benoso et al., 2022; y el artículo fundacional de Turing, 1936/1937) más dos artículos arbitrados con DOI localizados en fuentes indizadas (Wang et al., 2019, sobre el motor industrial de expresiones regulares *Hyperscan* en NSDI; y Weiss et al., 2018, sobre extracción de autómatas finitos deterministas a partir de redes neuronales recurrentes en ICML).

---

## Parte 1. Respuestas a las preguntas específicas sobre los tres textos asignados

### Artículo 1: Gribkoff (2013) — *Applications of deterministic finite automata*

1. **Explique la diferencia entre un autómata finito determinista (AFD) y una máquina de Mealy, y por qué el autocompletado de Apache Lucene requiere la segunda.**
   * **Diferencia formal**: Un **Autómata Finito Determinista (AFD)** $M = (Q, \Sigma, \delta, q_0, F)$ es un *reconocedor* (o clasificador binario) que únicamente produce una respuesta booleana (`Acepta` o `Rechaza`) al terminar de leer toda la cadena de entrada $w$, dependiendo de si $\hat{\delta}(q_0, w) \in F$. Carece de alfabeto de salida y de pesos asociados a sus transiciones. Por el contrario, una **Máquina de Mealy** (o de forma más general un **Transductor de Estado Finito**, *Finite State Transducer*, FST) es una séxtupla $T = (Q, \Sigma, \Gamma, \delta, \omega, q_0)$ que añade un alfabeto de salida $\Gamma$ y una **función de salida asociada a las transiciones** $\omega: Q \times \Sigma \to \Gamma^*$ (a diferencia de la máquina de Moore, donde la salida depende solo del estado). Así, conforme consume cada símbolo de entrada, la máquina de Mealy emite valores o acumula pesos en cada arista recorrida.
   * **Por qué Apache Lucene requiere una máquina de Mealy (FST)**: En un motor de búsqueda y autocompletado como Apache Lucene, no basta con responder *"sí, el prefijo existe en el diccionario"* (que es lo único que haría un AFD o *trie* booleano). El autocompletado necesita **asociar cada término indexado con su frecuencia/peso de relevancia o con un puntero a su lista invertida en disco**, compartir tanto prefijos como sufijos comunes para comprimir millones de términos en memoria RAM (mediante la minimización de Daciuk et al.) y recuperar en tiempo $O(|p|)$ las $k$ sugerencias con mayor puntuación a partir del prefijo tecleado $p$. Esto exige emitir y sumar salidas/pesos sobre las transiciones a medida que se recorre el grafo, lo cual es la definición exacta de un transductor o máquina de Mealy.

2. **El autor modela una máquina expendedora como un AFD y declara vacío el conjunto de estados de aceptación ($F = \emptyset$). Explique qué consecuencia tiene ello para la noción de cadena aceptada.**
   * En la teoría formal de lenguajes, el lenguaje aceptado por un autómata $M = (Q, \Sigma, \delta, q_0, F)$ se define como $L(M) = \{ w \in \Sigma^* \mid \hat{\delta}(q_0, w) \in F \}$. Si se declara el conjunto de estados de aceptación como vacío ($F = \emptyset$), entonces para toda cadena $w \in \Sigma^*$ es imposible que $\hat{\delta}(q_0, w) \in \emptyset$, lo que implica matemáticamente que **el lenguaje reconocido por ese AFD es el lenguaje vacío: $L(M) = \emptyset$** (ninguna secuencia de monedas o botones es "aceptada" en el sentido formal).
   * Gribkoff adopta $F = \emptyset$ porque una máquina expendedora real es un **sistema reactivo continuo** que no "termina" al entregar un refresco, sino que regresa al estado de saldo $\$0.00$ para atender al siguiente cliente y su interés está en la *acción lateral* (dispensar el producto y devolver cambio al cruzar cierta transición). Sin embargo, esto evidencia que una máquina expendedora que entrega productos en transiciones **no debería modelarse como un AFD puro con $F = \emptyset$, sino como una Máquina de Mealy** (donde la transición emite la salida `dispensar`), o bien, si se desea modelar cada transacción individual como un AFD reconocedor, el estado correspondiente a alcanzar el monto requerido ($\ge \$1.00$) debe pertenecer a $F \neq \emptyset$.

3. **Este documento es material de una asignatura, no un artículo arbitrado, y carece de bibliografía. Señale una afirmación suya que convendría verificar en una fuente arbitrada antes de citarla.**
   * **Afirmación que requiere verificación**: En la sección sobre expresiones regulares y búsqueda de patrones, Gribkoff afirma de manera general que los motores de expresiones regulares en lenguajes de programación modernos compilan las expresiones regulares a AFN/AFD para evaluar cadenas eficientemente, y en la sección de Apache Lucene atribuye mejoras de memoria y rendimiento a los FST sin citar los algoritmos ni las cotas formales.
   * **Por qué debe contrastarse en fuentes arbitradas**:
     1. Respecto a los motores de expresiones regulares en lenguajes como Python (`re`), Perl, Java o JavaScript, las fuentes arbitradas demuestran que **no** utilizan AFN/AFD clásicos de Thompson/Rabin-Scott, sino motores de retroceso recursivo (*backtracking* tipo PCRE) para soportar referencias hacia atrás (*backreferences*), los cuales tienen complejidad exponencial $O(2^{|w|})$ en el peor caso y son vulnerables a ataques de Denegación de Servicio por Expresiones Regulares (**ReDoS**), mientras que solo motores específicos como RE2, GNU grep o Hyperscan (Wang et al., 2019) emplean autómatas finitos garantizando tiempo lineal.
     2. Respecto a la construcción en tiempo lineal de transductores finitos deterministas mínimos acíclicos (usados en Lucene), la fuente primaria arbitrada que debe citarse es el artículo de **Daciuk, Mihov, Watson y Watson (2000)** publicado en *Computational Linguistics* (`https://doi.org/10.1162/089120100561601`) y el trabajo de **Mohri (1997)** sobre transductores de estado finito en procesamiento de lenguaje.

---

### Artículo 2: Luna-Benoso et al. (2022) — *Melanoma detection in dermoscopic images using a cellular automata classifier*

1. **Un autómata celular no es un autómata finito. Explique en qué se asemejan y en qué difieren, precisando qué es el estado, qué es el vecindario y qué función cumple la regla de transición local.**
   * **Semejanzas**: Ambos son sistemas dinámicos discretos en el tiempo y en el espacio de estados; operan en pasos de reloj discretos ($t = 0, 1, 2, \dots$), cada unidad elemental posee un conjunto **finito** de estados posibles $Q$, y su evolución es completamente determinista a partir de una función de transición definida formalmente.
   * **Diferencias fundamentales**:
     * Un **Autómata Finito (AFD)** posee **un único estado global activo** $q \in Q$ en cada instante, procesa una **cadena lineal unidimensional** de entrada símbolo por símbolo de izquierda a derecha, y su transición $\delta(q, a)$ depende exclusivamente del estado actual y del símbolo externo leído.
     * Un **Autómata Celular (AC)** es una **red o retícula espacial $d$-dimensional de múltiples celdas** (por ejemplo, una malla 1D o 2D de píxeles) que evolucionan **en paralelo y de forma síncrona**, sin leer una cinta secuencial externa tras su configuración inicial.
   * **Precisión de los componentes de un Autómata Celular**:
     * **Estado ($s_i^t \in Q$)**: Es el valor discreto (por ejemplo, $Q = \{0, 1\}$ o un nivel de intensidad/clase) que almacena una celda individual $i$ de la retícula en el instante de tiempo $t$. El *estado global* (o configuración) del autómata celular es la asignación de estados de todas las celdas de la malla simultáneamente.
     * **Vecindario ($N(i)$)**: Es el subconjunto geométrico finito de celdas adyacentes a la celda central $i$ (incluida ella misma) cuyos estados influyen directamente en el próximo estado de $i$. En 1D de radio $r=1$ el vecindario consta de 3 celdas $(i-1, i, i+1)$ (autómatas elementales de Wolfram); en 2D los más comunes son el **vecindario de von Neumann** (5 celdas: central más arriba, abajo, izquierda y derecha) y el **vecindario de Moore** (9 celdas: el bloque $3 \times 3$ circundante).
     * **Regla de transición local ($\phi: Q^{|N|} \to Q$)**: Es la función matemática idéntica para todas las celdas que calcula el nuevo estado $s_i^{t+1} = \phi(s_{j_1}^t, \dots, s_{j_k}^t)$ en el instante $t+1$ evaluando únicamente los estados actuales en el instante $t$ de las celdas que conforman el vecindario local $N(i)$. Aplicada síncronamente sobre toda la retícula, induce el comportamiento emergente global del sistema.

2. **Cuál es el problema que abordan los autores y por qué eligen ese modelo.**
   * **Problema abordado**: La detección y clasificación asistida por computadora de **melanoma** (el tipo más letal de cáncer de piel) frente a lesiones cutáneas benignas (nevos melanocíticos) a partir de imágenes dermatoscópicas digitales, extrayendo descriptores estadísticos de textura de la matriz de coocurrencia de niveles de gris (GLCM) y momentos estadísticos tras segmentar la lesión.
   * **Por qué eligen un clasificador basado en Autómatas Celulares (CAC)**: Porque los autómatas celulares poseen una estructura matricial intrínsecamente compatible con datos tabulares y de imágenes, operan mediante reglas locales sumamente simples y rápidas de evaluar en paralelo, requieren un costo computacional de entrenamiento y memoria mucho menor que las redes neuronales profundas (CNN) —que exigen miles de imágenes y GPUs dedicadas—, y el modelo asociativo basado en memoria de Hamming y evolución celular permite separar eficazmente vectores de características de lesiones benignas y malignas en conjuntos de datos médicos de tamaño moderado.

3. **Qué resultado reportan, con qué conjunto de imágenes lo midieron y con qué métricas.**
   * **Conjunto de imágenes (*Dataset*)**: Evaluaron el método sobre el banco público estándar **PH²** (*Hospital Pedro Hispano*, Portugal), compuesto por **200 imágenes dermatoscópicas** (160 lesiones benignas —80 nevos comunes y 80 nevos atípicos— y 40 melanomas), así como el conjunto **ISIC** (*International Skin Imaging Collaboration*), aplicando técnicas de balanceo de clases (SMOTE) y validación cruzada ($k$-fold, $k=10$ y método *Hold-Out* 80/20).
   * **Métricas empleadas**: Exactitud (*Accuracy*), Sensibilidad o Exhaustividad (*Sensitivity / Recall*), Especificidad (*Specificity*), Precisión (*Precision*), puntaje **F1-score** y Área Bajo la Curva ROC (**AUC**).
   * **Resultados principales reportados**: Sobre el dataset **PH²**, el clasificador basado en autómatas celulares alcanzó una **exactitud (*Accuracy*) de 98.61%**, una **sensibilidad de 97.22%**, una **especificidad de 100%** (y en configuración general valores superiores al **95%–98%** de exactitud y **AUC > 0.97**), superando o igualando a clasificadores clásicos del estado del arte como Máquinas de Soporte Vectorial (SVM), Perceptrón Multicapa (MLP), $k$-NN y Árboles de Decisión (Random Forest).

---

### Artículo 3 (Original clásico elegido): Turing (1936/1937) — *On computable numbers, with an application to the Entscheidungsproblem*[^1]

[^1]: **Nota sobre la fecha de publicación del artículo de Turing (1936 vs. 1937)**: Alan M. Turing entregó el manuscrito a la *London Mathematical Society* el 28 de mayo de 1936 y fue leído el 12 de noviembre de 1936. Los *Proceedings of the London Mathematical Society* (Serie 2, Volumen 42) se publicaban en fascículos periódicos: la primera parte del artículo de Turing (páginas 230–240) apareció impresa en el fascículo de finales de **noviembre/diciembre de 1936**, mientras que la continuación (páginas 241–265) y la encuadernación completa del Volumen 42 llevan fecha de **1937** (además de una corrección publicada en el Volumen 43 en 1937). Por esta razón, el registro oficial del DOI (`10.1112/plms/s2-42.1.230`) indexa el volumen completo en **1937**, mientras que la convención histórica en ciencias de la computación es citarlo como **Turing (1936)** en reconocimiento al año de aparición de la primera parte y de su simultaneidad con el artículo de Church (1936).

1. **Qué resultado se demuestra y qué modelo de cómputo se introduce.**
   * **Modelo de cómputo introducido**: Turing introduce las *"computing machines"* o **máquinas automáticas (*$a$-machines*)**, hoy conocidas universalmente como **Máquinas de Turing**. Una máquina-$a$ consta de una cinta dividida en casillas (*squares*) potencialmente infinita, un cabezal capaz de leer un símbolo de la casilla actual ($r$-ésima), escribir un símbolo, desplazarse una casilla a la izquierda ($L$) o a la derecha ($R$), y un conjunto finito de estados internos que Turing denomina *$m$-configurations* ($q_1, q_2, \dots, q_R$). Además, en las secciones §6 y §7 introduce la **Máquina Universal de Turing ($U$)**, una única máquina-$a$ capaz de recibir en su cinta la **"Descripción Estándar" (*Standard Description*, S.D.)** o **"Número de Descripción" (*Description Number*, D.N.)** de cualquier otra máquina-$a$ $\mathcal{M}$ y simular paso a paso su cómputo. Este concepto constituye el fundamento teórico directo de la arquitectura de programa almacenado en memoria de las computadoras modernas.
   * **Resultados fundamentales demostrados**:
     1. Define los **números computables** como aquellos números reales cuya expansión decimal (o binaria) puede ser escrita por una máquina-$a$ **libre de círculos (*circle-free*)** (aquella que continúa imprimiendo infinitos dígitos de primera especie $0$ y $1$ sin quedar atrapada). Demuestra que los números algebraicos, $\pi$ y $e$ son computables, pero que dado que las descripciones de máquinas (D.N.) son un subconjunto de $\mathbb{N}$, el conjunto de los números computables es **numerable**.
     2. Mediante una **aplicación del argumento diagonal de Cantor** (§8), demuestra que **no existe ninguna máquina-$a$ capaz de decidir si una máquina arbitraria $\mathcal{M}$ es *circle-free* (satisfactoria) o *circular***, ni tampoco existe una máquina general que decida si una máquina arbitraria $\mathcal{M}$ imprimirá alguna vez un símbolo dado (por ejemplo, el símbolo `0`) sobre su cinta.
     3. Finalmente (§11), reduce este problema a la lógica de predicados de primer orden: para cada máquina $\mathcal{M}$ construye una fórmula lógica $\text{Un}(\mathcal{M})$ tal que $\text{Un}(\mathcal{M})$ es demostrable en el cálculo funcional restringido de Hilbert si y solo si $\mathcal{M}$ imprime alguna vez el símbolo `0`. Como decidir si $\mathcal{M}$ imprime `0` es indecidible, concluye como corolario que **el *Entscheidungsproblem* de Hilbert no tiene solución** (es indecidible).

2. **Enuncie con precisión la tesis de Church-Turing y explique por qué se denomina tesis y no teorema.**
   * **Enunciado preciso**: *Toda función (o número real / predicado de decisión) que sea "efectivamente calculable" mediante un procedimiento algorítmico mecánico finito puede ser computada por una Máquina de Turing (una máquina-$a$ de Turing, o equivalentemente es $\lambda$-definible en el sentido de Church y general-recursiva en el sentido de Gödel-Kleene).*
   * **Por qué es una tesis y no un teorema**: En la Sección §9 (*"The extent of the computable numbers"*), el propio Turing advierte explícitamente que su argumento para identificar los "números calculables intuitivamente por un calculista humano" con los "números computables por una máquina-$a$" depende de una apelación a la intuición sobre los límites de la mente humana y la observación de símbolos, y no de una deducción axiomática: *"All arguments which can be given are bound to be, fundamentally, appeals to intuition, and for this reason rather unsatisfactory mathematically"*. Un **teorema** requiere que ambos lados de la equivalencia sean objetos matemáticos formalmente definidos (como el teorema demostrado por Turing en el Apéndice de su artículo, donde prueba formalmente que *computabilidad por máquina-$a$ $\iff$ $\lambda$-definibilidad de Church*). En cambio, dado que "procedimiento mecánico efectivo" es una noción pre-formal e intuitiva, la afirmación de que las Máquinas de Turing capturan *exactamente* esa noción no puede demostrarse como teorema y recibe el nombre de **Tesis de Church-Turing**.

3. **Qué dificultad encontró en su lectura, dado que se trata de textos con más de setenta años y una notación distinta de la del curso, y cómo la resolvió.**
   * **Dificultades de lectura y notación encontradas**:
     1. **Tipografía gótica (*Fraktur*) y terminología arcaica**: Turing utiliza letras góticas alemanas ($\mathfrak{q}, \mathfrak{b}, \mathfrak{c}, \dots$) para las configuraciones internas (*$m$-configurations*, que hoy llamamos estados $q \in Q$), llama *"complete configuration"* a lo que hoy denominamos *descripción instantánea* (ID), y en lugar de hablar del **Problema de la Parada (*Halting Problem*)** para cadenas finitas, formula sus máquinas para calcular expansiones infinitas de números reales, distinguiendo entre máquinas ***circle-free*** (que siguen imprimiendo dígitos $0$ y $1$ indefinidamente) y máquinas ***circular*** (que se detienen o entran en un bucle sin imprimir más dígitos de primera especie).
     2. **Alternancia de casillas en la cinta ($F$-squares y $E$-squares)**: En lugar de usar una cinta simple, Turing divide la cinta en casillas alternadas: las **casillas $F$ (*figures*)**, donde se escriben de forma permanente los dígitos $0$ y $1$ del número computable resultante, y las **casillas $E$ (*erasable*)**, situadas entre cada par de casillas $F$, que sirven como memoria de trabajo borrable marcada con símbolos auxiliares ($\partial, x, y, z$).
     3. **Uso de "esqueletos funcionales" (*skeleton tables* / *m-functions*)**: Para abreviar la Máquina Universal en las secciones §4–§7, Turing inventa un sistema de macros parametrizadas ($\mathfrak{f}(\mathfrak{C}, \mathfrak{B}, \alpha)$) antes de existir los lenguajes ensambladores o de alto nivel.
   * **Cómo se resolvió la dificultad**: Elaboré una tabla de correspondencia directa entre la terminología de Turing (1936) y la notación moderna del curso (Sipser, 2012; Hopcroft et al., 2007):
     * *$m$-configuration* ($\mathfrak{q}_i$) $\longleftrightarrow$ Estado $q_i \in Q$.
     * *Scanned symbol* ($S(r)$) $\longleftrightarrow$ Símbolo leído $a \in \Gamma$ bajo el cabezal.
     * *Configuration* $(\mathfrak{q}_i, S(r))$ $\longleftrightarrow$ Par $(q_i, a) \in Q \times \Gamma$ del dominio de $\delta$.
     * *Complete configuration* $\longleftrightarrow$ Descripción instantánea $uqv$.
     * *Standard Description (S.D.) / Description Number (D.N.)* $\longleftrightarrow$ Codificación en cadena $\langle M \rangle$ (numeración de Gödel de la máquina).
     * *Circle-free machine* $\longleftrightarrow$ Máquina que no se bloquea antes de producir su salida (análoga complementaria al problema de parada/impresión).
     Además, seguí paso a paso el primer ejemplo concreto de Turing en la sección §3 (la máquina con cuatro estados $\mathfrak{b}, \mathfrak{c}, \mathfrak{k}, \mathfrak{e}$ que imprime la secuencia alternada $010101\dots$ en las casillas $F$ dejando las casillas $E$ en blanco), trazando manualmente el movimiento de la cinta para interiorizar la convención de casillas $F$ y $E$ antes de abordar la diagonalización de la sección §8.

---

## Parte 2. Fichas completas de los cinco artículos

### Ficha 1 — Artículo asignado 1 (Documento de curso)

1. **Cita completa en formato APA 7.ª edición**:
   Gribkoff, E. (2013). *Applications of deterministic finite automata* [Documento de curso, ECS 120: Theory of Computation]. University of California, Davis. https://www.cs.ucdavis.edu/~rogaway/classes/120/spring13/eric-dfa.pdf
2. **Problema que aborda (2–3 líneas)**:
   Examina la brecha entre la formulación matemática abstracta de los autómatas finitos deterministas (AFD) estudiada en los cursos universitarios y su aplicación práctica real en sistemas de ingeniería de software, control de protocolos y motores de indexación de texto.
3. **Método o propuesta de los autores**:
   Realiza una revisión expositiva de cinco dominios de aplicación (máquinas expendedoras, expresiones regulares, protocolos de red TCP, videojuegos e indexación en Apache Lucene), contrastando cuándo basta un AFD puro y cuándo es necesario extenderlo a transductores de estado finito (máquinas de Mealy).
4. **Resultado principal que reporta**:
   Demuestra que aunque los AFD puros son excelentes herramientas pedagógicas y de reconocimiento léxico, las aplicaciones industriales de alto rendimiento (como el autocompletado en memoria de Apache Lucene) requieren máquinas de Mealy/transductores mínimos que asocien salidas y pesos a las transiciones.
5. **Tema de la Unidad Temática I con el que se relaciona (explícito)**:
   **Autómatas Finitos Deterministas (AFD), Expresiones Regulares y Extensiones con Salida (Máquinas de Mealy / Transductores Finitos)**.
6. **Aportación al trabajo del curso (2–3 líneas)**:
   Permite comprender la diferencia práctica entre *reconocer* un lenguaje ($L(M) \subseteq \Sigma^*$) y *transducir* una entrada a una salida, además de ilustrar qué ocurre formalmente cuando el conjunto de estados finales es vacío ($F = \emptyset$, tal como se analiza también en el Ejercicio 126 de la Lista 2).

---

### Ficha 2 — Artículo asignado 2 (Artículo arbitrado de aplicación médica)

1. **Cita completa en formato APA 7.ª edición**:
   Luna-Benoso, B., Martínez-Perales, J. C., Cortés-Galicia, J., Flores-Carapia, R., & Silva-García, V. M. (2022). Melanoma detection in dermoscopic images using a cellular automata classifier. *Computers*, *11*(1), Artículo 8. https://doi.org/10.3390/computers11010008
2. **Problema que aborda (2–3 líneas)**:
   Aborda el diagnóstico temprano y automatizado del melanoma cutáneo a partir de imágenes dermatoscópicas digitales, buscando un clasificador de alta sensibilidad y bajo costo computacional frente a los modelos pesados de aprendizaje profundo.
3. **Método o propuesta de los autores**:
   Propone una tubería de visión por computadora que segmenta la lesión cutánea, extrae características estadísticas y de textura mediante matrices de coocurrencia de niveles de gris (GLCM) y entrena un clasificador asociativo basado en la evolución de un **Autómata Celular** (*Cellular Automata Classifier*, CAC).
4. **Resultado principal que reporta**:
   Alcanza una exactitud (*accuracy*) de **98.61%**, sensibilidad de **97.22%** y especificidad de **100%** sobre el banco de imágenes dermatoscópicas **PH²** (y alto desempeño en ISIC), superando a clasificadores tradicionales como SVM, MLP y Random Forest.
5. **Tema de la Unidad Temática I con el que se relaciona (explícito)**:
   **Modelos de Cómputo de Estado Finito, Funciones de Transición ($\delta$) y su generalización espacial a Autómatas Celulares**.
6. **Aportación al trabajo del curso (2–3 líneas)**:
   Ejemplifica cómo el concepto de espacio de estados discretos y reglas de transición deterministas estudiado en ESCOM trasciende el análisis de cadenas para resolver problemas reales de reconocimiento de patrones y diagnóstico médico en bioingeniería.

---

### Ficha 3 — Artículo asignado 3 (Obra clásica fundacional original)

1. **Cita completa en formato APA 7.ª edición**:
   Turing, A. M. (1937). On computable numbers, with an application to the Entscheidungsproblem. *Proceedings of the London Mathematical Society*, *s2-42*(1), 230–265. https://doi.org/10.1112/plms/s2-42.1.230 *(Publicado originalmente en fascículos entre noviembre de 1936 y 1937; citado convencionalmente como Turing, 1936).*
2. **Problema que aborda (2–3 líneas)**:
   Investiga cómo caracterizar con rigor matemático absoluto qué significa que un número real o una función sea "calculable por medios mecánicos finitos", con el fin de resolver el *Entscheidungsproblem* (problema de la decisión) planteado por David Hilbert en 1928.
3. **Método o propuesta de los autores**:
   Define un modelo matemático abstracto de cómputo (la máquina-$a$ o Máquina de Turing), introduce la codificación numérica de programas para construir la Máquina Universal de Turing ($U$) y aplica el método de diagonalización de Cantor junto con una reducción a la lógica de predicados de primer orden.
4. **Resultado principal que reporta**:
   Demuestra la existencia de problemas indecidibles por cualquier procedimiento mecánico (como decidir si una máquina arbitraria es *circle-free* o si imprimirá un símbolo dado), prueba la equivalencia con las funciones $\lambda$-definibles de Church y demuestra que el *Entscheidungsproblem* de Hilbert es insoluble.
5. **Tema de la Unidad Temática I con el que se relaciona (explícito)**:
   **Orígenes de la Teoría de la Computación, Programa de Hilbert, *Entscheidungsproblem*, Computabilidad y Tesis de Church-Turing**.
6. **Aportación al trabajo del curso (2–3 líneas)**:
   Es el texto fundacional de las ciencias de la computación: introduce simultáneamente el modelo formal que corona el Nivel 0 de la Jerarquía de Chomsky, el concepto de computadora universal de programa almacenado y la técnica de diagonalización y reducción para probar límites del cómputo.

---

### Ficha 4 — Primer artículo localizado por el alumno (Aplicación en redes y ciberseguridad)

1. **Cita completa en formato APA 7.ª edición**:
   Wang, X., Hong, Y., Chang, H., Park, K., Langdale, G., Hu, J., & Zhu, H. (2019). Hyperscan: A fast multi-pattern regex matcher for modern CPUs. En *Proceedings of the 16th USENIX Symposium on Networked Systems Design and Implementation (NSDI '19)* (pp. 631–648). USENIX Association. https://doi.org/10.5555/3323234.3323286 *(Actas indizadas en ACM Digital Library / USENIX; versión extendida relacionada en ACM ToN).*
2. **Problema que aborda (2–3 líneas)**:
   En sistemas de detección de intrusiones en red (NIDS como Snort y Suricata) e inspección profunda de paquetes (DPI), evaluar miles de expresiones regulares simultáneamente con un AFN resulta demasiado lento ($O(m \cdot |w|)$), mientras que construir un único AFD combinado provoca una explosión exponencial de estados ($O(2^m)$) que agota la memoria caché del procesador.
3. **Método o propuesta de los autores**:
   Presentan **Hyperscan**, una biblioteca industrial que descompone las expresiones regulares mediante un **análisis de grafos de Glushkov (AFN)** en subcadenas literales fijas y sub-autómatas finitos deterministas acotados (*DFA*), combinando algoritmos de filtrado de cadenas múltiples acelerados por instrucciones vectoriales SIMD con la simulación determinista de autómatas solo cuando se detectan las cadenas ancla.
4. **Resultado principal que reporta**:
   Logra un rendimiento de inspección de tráfico de red entre **8.7x y 14x más rápido** que motores basados en autómatas tradicionales (como RE2 de Google y PCRE2) y reduce drásticamente la huella de memoria frente a los AFD puros al evaluar conjuntos de más de 20,000 reglas de seguridad de Snort.
5. **Tema de la Unidad Temática I con el que se relaciona (explícito)**:
   **Expresiones Regulares, Equivalencia entre AFN y AFD (Explosión Exponencial en la Construcción de Subconjuntos) y Operaciones de Subcadenas/Prefijos**.
6. **Aportación al trabajo del curso (2–3 líneas)**:
   Conecta directamente la teoría vista en el Ejercicio 4 y 5 (conversión de AFN a AFD y búsqueda de subcadenas) con un problema crítico de ingeniería de redes y seguridad informática, explicando cómo mitigar en la práctica el crecimiento exponencial $2^{|Q|}$ de la construcción de Rabin-Scott.

---

### Ficha 5 — Segundo artículo localizado por el alumno (Aplicación en Inteligencia Artificial y verificación de modelos)

1. **Cita completa en formato APA 7.ª edición**:
   Weiss, G., Goldberg, Y., & Yahav, E. (2018). Extracting automata from recurrent neural networks using queries and counterexamples. En J. Dy & A. Krause (Eds.), *Proceedings of the 35th International Conference on Machine Learning (ICML 2018)*, *Proceedings of Machine Learning Research* (Vol. 80, pp. 5247–5256). PMLR / ACM Digital Library. https://doi.org/10.48550/arXiv.1711.09576
2. **Problema que aborda (2–3 líneas)**:
   Las Redes Neuronales Recurrentes (RNN, como LSTM y GRU) entrenadas para procesar secuencias de lenguaje natural o código actúan como "cajas negras" de estado continuo, haciendo sumamente difícil interpretar qué reglas gramaticales aprendieron o verificar formalmente si cumplen especificaciones de seguridad.
3. **Método o propuesta de los autores**:
   Adaptan el algoritmo de aprendizaje exacto **$L^*$ de Angluin** (1987) utilizando a la red neuronal recurrente como maestro (*oracle*) mediante consultas de pertenencia ($\text{Membership Queries}$) y una abstracción finita de su espacio de estados continuos para generar contraejemplos ($\text{Equivalence Queries}$), extrayendo automáticamente un **Autómata Finito Determinista (AFD) mínimo** que aproxima con fidelidad el comportamiento de la RNN.
4. **Resultado principal que reporta**:
   Consiguen extraer AFD compactos y exactos (con $>99\%$ de precisión respecto a la red neuronal) en lenguajes regulares complejos (como gramáticas de Tomita, paridad balanceada y validación de correos electrónicos), permitiendo incluso descubrir contraejemplos donde una RNN con $100\%$ de exactitud en su conjunto de prueba fallaba ante cadenas ligeramente más largas.
5. **Tema de la Unidad Temática I con el que se relaciona (explícito)**:
   **Autómatas Finitos Deterministas (AFD), Minimización/Partición de Estados Equivalentes y Lenguajes Regulares (Nivel 3 de la Jerarquía de Chomsky)**.
6. **Aportación al trabajo del curso (2–3 líneas)**:
   Muestra la vigencia contemporánea de los AFD y la simplificación de estados (vista en la Lista 3 de JFLAP) dentro de la Inteligencia Artificial Explicable (XAI) y la verificación formal de modelos de aprendizaje profundo.

---

## Parte 3. Tabla comparativa y análisis de cierre

### Tabla comparativa de los cinco textos

| Texto | Arbitrado | Año | Modelo que usa | Campo de aplicación |
| :--- | :---: | :---: | :--- | :--- |
| **1. Gribkoff** | No (Documento de curso universitario) | 2013 | Autómata Finito Determinista (AFD) y Máquina de Mealy (Transductor de Estado Finito, FST) | Enseñanza de la teoría, protocolos de red (TCP) y autocompletado/búsqueda en Apache Lucene |
| **2. Luna-Benoso et al.** | Sí (*Computers*, MDPI, con revisión por pares y DOI) | 2022 | Autómata Celular (CAC) con reglas de transición locales y memoria asociativa | Bioingeniería / Visión artificial médica (detección de melanoma en imágenes dermatoscópicas) |
| **3. Turing (original elegido)** | Sí (*Proceedings of the London Mathematical Society*, con DOI) | 1936 / 1937 | Máquina-$a$ (Máquina de Turing estándar), Máquina Universal de Turing ($U$) y Cálculo $\lambda$ | Fundamentos de las matemáticas, lógica de primer orden (*Entscheidungsproblem*) y teoría de la computabilidad |
| **4. Wang et al. (localizado 1)** | Sí (*USENIX NSDI '19*, actas arbitradas de congreso top) | 2019 | Expresiones regulares, Autómata de Glushkov (AFN) y descomposición híbrida en AFD acotados | Redes de computadoras y ciberseguridad (inspección profunda de paquetes DPI y NIDS a alta velocidad) |
| **5. Weiss et al. (localizado 2)** | Sí (*ICML 2018*, actas arbitradas de congreso top en IA) | 2018 | Autómata Finito Determinista (AFD) mínimo extraído mediante el algoritmo $L^*$ de Angluin | Inteligencia Artificial Explicable (XAI), procesamiento de lenguaje natural y verificación de redes neuronales (RNN) |

---

### Análisis comparativo de cierre (media cuartilla)

#### ¿Qué tienen en común los cinco textos?
A pesar de abarcar más de ocho décadas de historia (desde 1936 hasta 2022) y áreas tan diversas como la lógica matemática pura, la oncología dermatológica, la ciberseguridad de redes y la interpretabilidad de redes neuronales profundas, los cinco textos comparten un núcleo conceptual idéntico: **la discretización del cómputo mediante espacios finitos de estados y funciones de transición bien definidas**. Tanto la máquina-$a$ de Turing (1936/1937) como los AFD/Mealy de Gribkoff (2013), los autómatas híbridos de Wang et al. (2019), los AFD extraídos por Weiss et al. (2018) y las celdas del autómata celular de Luna-Benoso et al. (2022) descansan sobre el principio de que el comportamiento complejo de un sistema puede capturarse mediante reglas locales de transición $\delta$ que evolucionan paso a paso a partir de una configuración inicial.

#### ¿En qué difieren en rigor y en propósito?
En cuanto a **rigor metodológico**, existe un contraste marcado entre el documento pedagógico de **Gribkoff (2013)** —que carece de revisión por pares, demostraciones formales y referencias bibliográficas, buscando únicamente motivar a estudiantes de pregrado— y los cuatro trabajos arbitrados. Entre estos últimos, el artículo de **Turing (1936/1937)** representa la cúspide del rigor deductivo matemático y filosófico (donde cada afirmación se construye desde cero para demostrar un teorema de imposibilidad absoluta sobre el *Entscheidungsproblem*), mientras que **Luna-Benoso et al. (2022)**, **Wang et al. (2019)** y **Weiss et al. (2018)** combinan la formulación teórica de autómatas con el **rigor experimental y empírico** propio de la ciencia de la computación aplicada: validación cruzada estadística sobre bancos de datos clínicos (PH², ISIC), pruebas de rendimiento (*benchmarks*) en ciclos de CPU por byte sobre tráfico real de red (Snort) y cotas de fidelidad en extracción de lenguajes regulares. En cuanto a **propósito**, Turing busca establecer las fronteras teóricas de lo computable; Gribkoff busca divulgar; Luna-Benoso et al. y Wang et al. buscan optimizar la clasificación y el filtrado en dominios reales; y Weiss et al. emplean la teoría clásica de autómatas para auditar modelos modernos de aprendizaje profundo.

#### Problema abierto identificado a partir de la lectura
A partir de la intersección entre **Weiss et al. (2018)** y **Wang et al. (2019)** (con el trasfondo de indecidibilidad de **Turing, 1936**), emerge un **problema abierto fundamental en la ciencia de la computación contemporánea**: **la extracción escalable y verificación formal de autómatas y gramáticas a partir de Grandes Modelos de Lenguaje (LLMs basados en arquitecturas *Transformer*) y redes neuronales de gran escala**. Mientras que para una RNN pequeña es factible extraer un AFD mínimo mediante el algoritmo $L^*$, cuando el lenguaje subyacente posee miles de estados o estructuras sensibles al contexto, la combinación de la explosión exponencial de estados ($2^{|Q|}$) y el costo de las consultas de equivalencia vuelve intratable la extracción exacta. Determinar bajo qué restricciones arquitectónicas es posible destilar de forma garantizada y en tiempo polinomial un autómata verificable a partir de un modelo neuronal moderno —para garantizar, por ejemplo, que un agente de IA nunca genere salidas que violen una gramática o política de seguridad formal— sigue siendo un problema abierto de primer orden entre la teoría de autómatas y la inteligencia artificial.
