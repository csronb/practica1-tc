# Ejercicio 2. Investigación: Qué es la Teoría de la Computación

## 1. Definición de la Teoría de la Computación y sus preguntas fundamentales

La **Teoría de la Computación** es la rama de las ciencias de la computación y las matemáticas que estudia las capacidades y limitaciones fundamentales de las computadoras mediante modelos matemáticos abstractos de cómputo. Más allá de la tecnología física coyuntural (transistores, procesadores o lenguajes de programación específicos), esta disciplina busca responder una cuestión central: **¿cuáles son las capacidades y limitaciones fundamentales de las computadoras?** (Sipser, 2012).

De forma más específica, la disciplina se plantea tres grandes interrogantes:
1. **¿Qué problemas pueden resolverse mecánicamente mediante un algoritmo y cuáles no?** (Frontera entre lo decidible/computable y lo indecidible).
2. **Si un problema es soluble, ¿cuántos recursos (tiempo de ejecución y espacio de memoria) se requieren como mínimo para resolverlo?** (Frontera entre problemas tratables e intratables).
3. **¿Cómo podemos abstraer y clasificar los distintos modelos de máquinas calculadoras y los lenguajes formales que son capaces de reconocer o generar?** (Relación entre gramáticas, autómatas y expresiones formales).

### Comparación de definiciones de dos autores

1. **Michael Sipser (2012)**: En *Introduction to the Theory of Computation* (3.ª ed., p. 1), Sipser define la Teoría de la Computación como el estudio de modelos matemáticos de cómputo diseñados para determinar qué se puede y qué no se puede calcular, así como la eficiencia con la que puede hacerse, articulando el área en tres pilares interconectados: **autómatas y lenguajes**, **computabilidad** y **complejidad computacional**.
2. **John E. Hopcroft, Rajeev Motwani y Jeffrey D. Ullman (2007)**: En *Introducción a la teoría de autómatas, lenguajes y computación* (3.ª ed., pp. 1–4), definen la disciplina como el estudio de las máquinas abstractas (autómatas) y los sistemas formales de descripción de lenguajes que permiten modelar tanto el hardware digital y el análisis léxico/sintáctico de los compiladores como los límites teóricos de lo que cualquier software puede llegar a decidir.

**Análisis comparativo**:
Ambos enfoques coinciden en que la Teoría de la Computación prescinde de detalles tecnológicos particulares para centrarse en **modelos matemáticos rigurosos** (como los autómatas finitos y las máquinas de Turing) y en los límites intrínsecos del cálculo algorítmico. Sin embargo, difieren en su énfasis pedagógico y epistemológico: mientras que **Sipser (2012)** estructura la disciplina desde la perspectiva de la **complejidad y la clasificabilidad de problemas** (usando los autómatas como escalón hacia la decidibilidad y las clases $\text{P}$ vs $\text{NP}$), **Hopcroft et al. (2007)** ponen un mayor acento en la **ingeniería de lenguajes formales y sus aplicaciones directas** (construcción de compiladores, verificación de circuitos secuenciales, procesadores de texto y expresiones regulares) antes de abordar la computabilidad general.

---

## 2. Orígenes históricos: el programa de Hilbert, las paradojas de la lógica y el *Entscheidungsproblem*

Los cimientos de la Teoría de la Computación surgieron a finales del siglo XIX y principios del siglo XX a raíz de la **crisis de los fundamentos de las matemáticas** (Davis, 2000).

### Las paradojas de la lógica matemática y la teoría de conjuntos
Cuando Georg Cantor desarrolló la teoría de conjuntos infinitos y demostró mediante su célebre **argumento de diagonalización** (1891) que el conjunto de los números reales $\mathbb{R}$ no es numerable ($|\mathbb{R}| > |\mathbb{N}|$), abrió un método de demostración que décadas después sería decisivo para probar la existencia de problemas indecidibles. Poco después, el intento de Gottlob Frege por reducir la aritmética a la lógica pura empleando el principio de comprensión irrestricta se vio sacudido en 1901 por la **Paradoja de Russell**, formulada por Bertrand Russell. Si se define el conjunto $R$ de todos los conjuntos que no se pertenecen a sí mismos:

$$R = \{ x \mid x \notin x \}$$

surge una contradicción insalvable al preguntar si $R \in R$:

$$R \in R \iff R \notin R$$

A esta paradoja se sumaron otras antinomias semánticas y conjuntistas (como la paradoja de Cantor sobre el conjunto de todos los conjuntos, la paradoja de Burali-Forti sobre los ordinales y la paradoja de Berry/mentiroso sobre la autorreferencia). Para subsanar estas contradicciones, Russell y Alfred North Whitehead publicaron *Principia Mathematica* (1910–1913) introduciendo la teoría ramificada de tipos.

### El Programa de Hilbert y los Teoremas de Incompletitud de Gödel
En la década de 1920, el matemático alemán **David Hilbert** propuso un ambicioso proyecto fundacional conocido como el **Programa de Hilbert**. Su objetivo era formalizar todas las matemáticas en un sistema axiomático finito y demostrar, mediante métodos estrictamente finitistas (metamatemáticos), que dicho sistema cumplía tres propiedades:
1. **Completitud**: Toda proposición matemática verdadera formulable en el sistema puede demostrarse formalmente dentro de él (para toda fórmula cerrada $\varphi$, se puede demostrar $\varphi$ o $\neg\varphi$).
2. **Consistencia**: No es posible derivar una contradicción (no se puede demostrar simultáneamente $\varphi$ y $\neg\varphi$).
3. **Decidibilidad (*Entscheidungsproblem*)**: Debe existir un procedimiento mecánico infalible que, dada cualquier fórmula lógica bien formada, determine en un número finito de pasos si es universalmente válida (o demostrable) o no.

El primer golpe demoledor al programa de Hilbert llegó en **1931** cuando **Kurt Gödel** publicó sus dos **Teoremas de Incompletitud** (*Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I*). Mediante una ingeniosa codificación numérica de símbolos y demostraciones (**numeración de Gödel**), Gödel construyó una proposición aritmética autorreferencial $G$ que afirma esencialmente *"Esta proposición no es demostrable en el sistema"*. Gödel demostró que en cualquier sistema axiomático formal consistente y recursivamente enumerable que sea suficientemente potente para expresar la aritmética elemental de los números naturales:
* **Primer Teorema**: El sistema es **incompleto** (existen enunciados verdaderos que no pueden demostrarse ni refutarse dentro del sistema).
* **Segundo Teorema**: El sistema no puede demostrar su propia **consistencia** utilizando únicamente sus propios axiomas.

### El *Entscheidungsproblem* (Problema de la Decisión)
A pesar de la incompletitud demostrada por Gödel para la aritmética, aún quedaba abierto el **Entscheidungsproblem** planteado por David Hilbert y Wilhelm Ackermann en 1928 en su obra *Grundzüge der theoretischen Logik*: ¿existe un algoritmo o procedimiento efectivo general que decida si una fórmula arbitraria del cálculo de predicados de primer orden es universalmente válida?

Para demostrar que tal procedimiento **sí** existe bastaba con exhibirlo; pero para demostrar que **no existe ningún algoritmo posible**, era imprescindible definir primero, con rigor matemático absoluto, **qué es un "procedimiento mecánico efectivo" o "algoritmo"**. En **1936**, de manera independiente pero convergente, **Alonzo Church** (mediante el cálculo $\lambda$ y las funciones recursivas) y **Alan M. Turing** (mediante sus "máquinas automáticas" o máquinas-$a$, hoy llamadas **Máquinas de Turing**) formalizaron el concepto de computabilidad efectiva y demostraron que la respuesta al *Entscheidungsproblem* es **negativa**: no existe ningún algoritmo general capaz de decidir la validez de toda fórmula de la lógica de primer orden (Church, 1936; Turing, 1936). En ese mismo acto fundacional nació la **Teoría de la Computación**.

---

## 3. Las tres ramas de la Teoría de la Computación

De acuerdo con Sipser (2012) y Linz (2017), la Teoría de la Computación se estructura en tres ramas estrechamente vinculadas, ordenadas desde los modelos más generales hasta los más específicos:

| Rama | Pregunta fundamental que responde | Conceptos y modelos centrales |
| :--- | :--- | :--- |
| **1. Teoría de la Computabilidad** | **¿Qué problemas pueden resolverse mediante una computadora y cuáles no?** (Clasifica los problemas en *decidibles*, *semidecidibles / recursivamente enumerables* e *indecidibles*). | Máquinas de Turing, Tesis de Church-Turing, Problema de la Parada (*Halting Problem*), reducciones de mapeo ($A \le_m B$), Teorema de Rice, Problema de Correspondencia de Post (PCP). |
| **2. Teoría de la Complejidad Computacional** | **¿Qué hace que algunos problemas computables sean fáciles (eficientes) de resolver y otros difíciles (intratables)?** ¿Cuánto tiempo y memoria exige un problema en función del tamaño de su entrada? | Medidas de complejidad temporal y espacial, clases $\text{P}$, $\text{NP}$, $\text{NP-completo}$, $\text{PSPACE}$, $\text{EXPTIME}$, Teorema de Cook-Levin, reducciones en tiempo polinomial ($A \le_P B$). |
| **3. Teoría de Autómatas y Lenguajes Formales** | **¿Cuáles son las definiciones y propiedades de los distintos modelos matemáticos de cómputo y qué familias de lenguajes formales pueden reconocer o generar?** | Alfabetos, cadenas, expresiones regulares, Autómatas Finitos (AFD, AFN, AFN-$\lambda$), Gramáticas Libres de Contexto (GLC), Autómatas de Pila (AP), Autómatas Linealmente Acotados (LBA) y Jerarquía de Chomsky. |

---

## 4. La Tesis de Church-Turing

### ¿Qué afirma la tesis?
La **Tesis de Church-Turing** (formulada en 1936 a partir de los trabajos de Alonzo Church y Alan Turing) establece una correspondencia entre la noción intuitiva e informal de **algoritmo** (cálculo mecánico o procedimiento efectivo realizado paso a paso sin requerir ingenio humano) y la definición matemática formal de **computabilidad mediante una Máquina de Turing** (o funciones $\lambda$-definibles / recursivas generales):

> **Enunciado de la Tesis de Church-Turing**: *Toda función numérica o problema de decisión que sea "efectivamente calculable" mediante un procedimiento algorítmico mecánico finito puede ser calculado por una Máquina de Turing estándar.*

### ¿Qué modelos se demostraron matemáticamente equivalentes?
El peso científico de la Tesis de Church-Turing radica en que numerosos matemáticos propusieron formalismos radicalmente distintos en su estructura para capturar la idea de cómputo, y **todos ellos resultaron ser matemáticamente equivalentes en poder expresivo** (es decir, cualquier función computable en uno de los modelos es computable en todos los demás):
1. **Máquinas de Turing (Alan Turing, 1936)**: Dispositivos de estado finito con cabezal de lectura/escritura sobre una cinta ilimitada (incluyendo variantes multicinta, no deterministas y la Máquina Universal de Turing).
2. **Cálculo $\lambda$ (Alonzo Church y Stephen Kleene, 1932–1936)**: Sistema formal basado en la abstracción y aplicación de funciones anónimas ($\lambda x. M$).
3. **Funciones $\mu$-recursivas / recursivas generales (Kurt Gödel, Jacques Herbrand y Stephen Kleene, 1934–1936)**: Funciones construidas a partir de funciones iniciales mediante composición, recursión primitiva y el operador de minimización no acotada $\mu$.
4. **Sistemas canónicos de Post (Emil Post, 1936/1943)** y **Algoritmos de Markov**.
5. **Gramáticas irrestrictas de Tipo 0 (Noam Chomsky, 1956)** y **Máquinas de acceso aleatorio (RAM)** / lenguajes de programación modernos (*Turing-completos*).

### ¿Por qué se denomina *tesis* y no *teorema*?
Un **teorema** es una proposición estrictamente matemática cuyos términos están todos formalmente definidos dentro de un sistema axiomático y cuya verdad se demuestra deductivamente (por ejemplo, es un **teorema** demostrado por Turing en 1936 que *toda función $\lambda$-definible es computable por una Máquina de Turing y viceversa*).

Por el contrario, la Tesis de Church-Turing vincula un **concepto matemático formal** (*computable por una Máquina de Turing*) con una **noción intuitiva, pre-formal y filosófica** (*lo que un ser humano o dispositivo mecánico puede calcular efectivamente siguiendo reglas finitas*). Como el concepto intuitivo de "procedimiento efectivo" no posee una definición axiomática previa independiente, no es susceptible de una demostración matemática formal; de ahí que se denomine **tesis** (una hipótesis fundacional o definición de trabajo universalmente aceptada por la evidencia convergente de todos los modelos conocidos y por no haberse encontrado jamás un contraejemplo físico o lógico) (Copeland, 2004; Sipser, 2012).

---

## 5. Alfabeto, cadena y lenguaje: definiciones formales y operaciones

### Definiciones formales fundamentales

* **Símbolo**: Entidad abstracta, indivisible y atómica que no se define formalmente en términos de otros objetos (por ejemplo, letras `a`, `b` o dígitos `0`, `1`).
* **Alfabeto ($\Sigma$)**: Conjunto **finito y no vacío** de símbolos ($\Sigma \neq \emptyset$, $|\Sigma| \in \mathbb{N}^+$).
  * *Ejemplos*: $\Sigma_1 = \{0, 1\}$ (alfabeto binario), $\Sigma_2 = \{a, b, c\}$ (alfabeto latino de tres letras).
* **Cadena o palabra ($w$)**: Secuencia **finita** de símbolos yuxtapuestos tomados de un alfabeto $\Sigma$. Formalmente, una cadena de longitud $n \ge 1$ sobre $\Sigma$ puede verse como una función $w: \{1, 2, \dots, n\} \to \Sigma$, escrita como $w = a_1 a_2 \dots a_n$ con $a_i \in \Sigma$.
  * **Longitud de una cadena ($|w|$)**: Es el número total de ocurrencias de símbolos que componen la cadena $w$. Por ejemplo, para $w = 0101$, $|w| = 4$.
  * **Cadena vacía ($\lambda$ o $\varepsilon$)**: Es la única cadena que no contiene ningún símbolo, cuya longitud es cero ($|\lambda| = 0$). Actúa como elemento neutro de la concatenación de cadenas.
* **Potencia de un alfabeto ($\Sigma^k$)**: Para todo entero $k \ge 0$, $\Sigma^k$ es el conjunto de todas las cadenas sobre $\Sigma$ cuya longitud es exactamente $k$:

$$\Sigma^k = \{ w \mid w \text{ es una cadena sobre } \Sigma \text{ y } |w| = k \}$$

* **Universo del discurso ($\Sigma^*$)**: Conjunto de todas las cadenas de longitud finita (incluyendo $\lambda$) que pueden formarse con símbolos de $\Sigma$:

$$\Sigma^* = \bigcup_{k=0}^{\infty} \Sigma^k$$

* **Lenguaje formal ($L$)**: Cualquier conjunto de cadenas formadas con símbolos de un alfabeto $\Sigma$; es decir, un lenguaje $L$ sobre $\Sigma$ es cualquier **subconjunto de $\Sigma^*$**:

$$L \subseteq \Sigma^*$$

Un lenguaje puede ser finito o infinito, e incluso puede ser el **lenguaje vacío** $\emptyset = \{\}$ (que tiene cardinalidad $0$) o el lenguaje unitario $\{\lambda\}$ (que tiene cardinalidad $1$, pues contiene a la cadena vacía).

---

### Operaciones sobre cadenas

Sean $u = a_1 a_2 \dots a_n \in \Sigma^*$ (con $|u| = n$) y $v = b_1 b_2 \dots b_m \in \Sigma^*$ (con $|v| = m$):

1. **Concatenación de cadenas ($u \cdot v$ o simplemente $uv$)**: Operación binaria asociativa que consiste en yuxtaponer los símbolos de $v$ inmediatamente al final de los símbolos de $u$:

$$uv = a_1 a_2 \dots a_n b_1 b_2 \dots b_m, \quad \text{cumpliendo } |uv| = |u| + |v| = n + m$$

La cadena vacía $\lambda$ es el elemento neutro bilateral: $\forall w \in \Sigma^*, \; w\lambda = \lambda w = w$. Así, $(\Sigma^*, \cdot, \lambda)$ constituye un **monoide libre** generado por $\Sigma$.
2. **Potencia de una cadena ($w^k$)**: Definida inductivamente para $w \in \Sigma^*$ y $k \in \mathbb{N}$:

$$w^0 = \lambda, \qquad w^{k} = w^{k-1} \cdot w \quad (\text{para } k \ge 1)$$

3. **Reflexión, inversa o transposición de una cadena ($w^R$ o $w^{-1}$)**: Es la cadena escrita en orden inverso de símbolos. Se define inductivamente como:

$$\lambda^R = \lambda, \qquad (ua)^R = a \cdot u^R \quad \text{para todo } u \in \Sigma^*, \; a \in \Sigma$$

Por ejemplo, si $w = \text{abbc}$, entonces $w^R = \text{cbba}$. Además, $(uv)^R = v^R u^R$.
4. **Prefijo, sufijo y subcadena**: Dada $w \in \Sigma^*$:
   * $x$ es **prefijo** de $w$ si $\exists y \in \Sigma^*$ tal que $w = xy$. (Es *prefijo propio* si $x \neq \lambda$ y $x \neq w$).
   * $z$ es **sufijo** de $w$ si $\exists x \in \Sigma^*$ tal que $w = xz$.
   * $y$ es **subcadena** (*substring*) de $w$ si $\exists x, z \in \Sigma^*$ tales que $w = xyz$.

---

### Operaciones sobre lenguajes

Sean $L_1, L_2 \subseteq \Sigma^*$ dos lenguajes sobre el alfabeto $\Sigma$:

1. **Unión ($L_1 \cup L_2$)**: Conjunto de cadenas que pertenecen a $L_1$, a $L_2$ o a ambos:

$$L_1 \cup L_2 = \{ w \in \Sigma^* \mid w \in L_1 \lor w \in L_2 \}$$

2. **Intersección ($L_1 \cap L_2$)**: Conjunto de cadenas que pertenecen simultáneamente a $L_1$ y a $L_2$:

$$L_1 \cap L_2 = \{ w \in \Sigma^* \mid w \in L_1 \land w \in L_2 \}$$

3. **Diferencia ($L_1 \setminus L_2$ o $L_1 - L_2$)**: Conjunto de cadenas que pertenecen a $L_1$ pero no a $L_2$:

$$L_1 \setminus L_2 = \{ w \in \Sigma^* \mid w \in L_1 \land w \notin L_2 \}$$

*(En particular, el **complemento** de $L$ respecto a $\Sigma^*$ es $\overline{L} = \Sigma^* \setminus L$).*
4. **Concatenación de lenguajes ($L_1 \cdot L_2$ o $L_1 L_2$)**: Conjunto de todas las cadenas formadas concatenando una primera parte de $L_1$ con una segunda parte de $L_2$:

$$L_1 L_2 = \{ uv \mid u \in L_1 \land v \in L_2 \}$$

Aquí el lenguaje $\{\lambda\}$ actúa como neutro ($L\{\lambda\} = \{\lambda\}L = L$), mientras que el lenguaje vacío $\emptyset$ actúa como absorbente ($L\emptyset = \emptyset L = \emptyset$).
5. **Potencia de un lenguaje ($L^k$)**: Definida inductivamente para $k \in \mathbb{N}$:

$$L^0 = \{\lambda\}, \qquad L^k = L^{k-1} \cdot L \quad (\text{para } k \ge 1)$$

6. **Reflexión de un lenguaje ($L^R$)**: Conjunto de las reflexiones de todas las cadenas de $L$:

$$L^R = \{ w^R \mid w \in L \}$$

7. **Cerradura de Kleene o estrella de Kleene ($L^*$)**: Unión infinita de todas las potencias no negativas de $L$ (desde $k = 0$):

$$L^* = \bigcup_{k=0}^{\infty} L^k = L^0 \cup L^1 \cup L^2 \cup L^3 \cup \dots = \{\lambda\} \cup L \cup LL \cup LLL \cup \dots$$

8. **Cerradura positiva ($L^+$)**: Unión infinita de todas las potencias positivas de $L$ (desde $k = 1$):

$$L^+ = \bigcup_{k=1}^{\infty} L^k = L^1 \cup L^2 \cup L^3 \cup \dots = L \cdot L^* = L^* \cdot L$$

---

### Explicación de por qué $\Sigma^0 = \{\lambda\}$ y qué distingue a $\Sigma^*$ de $\Sigma^+$

#### ¿Por qué $\Sigma^0 = \{\lambda\}$ y no $\emptyset$?
Existen tres razones matemáticas complementarias (Hopcroft et al., 2007; Brookshear, 1993):
1. **Por la definición de longitud**: $\Sigma^k$ es el conjunto de todas las cadenas formadas con símbolos de $\Sigma$ cuya longitud es exactamente $k$. Para $k = 0$, nos preguntamos qué cadenas tienen longitud $0$ (cero símbolos). Existe exactamente una cadena sin símbolos: la cadena vacía $\lambda$, pues $|\lambda| = 0$. Por lo tanto, el conjunto que la contiene es $\{\lambda\}$ (de cardinalidad $|\Sigma^0| = |\Sigma|^0 = 1$), y no el conjunto vacío $\emptyset$ (cuya cardinalidad sería $0$).
2. **Por la ley del elemento neutro de la concatenación**: Para que la ley de los exponentes $\Sigma^{m+n} = \Sigma^m \cdot \Sigma^n$ se cumpla para $m = 0$, es obligatorio que $\Sigma^{0+n} = \Sigma^0 \cdot \Sigma^n = \Sigma^n$. Si $\Sigma^0$ fuese $\emptyset$, entonces $\emptyset \cdot \Sigma^n = \emptyset \neq \Sigma^n$, anulando toda la recursión inductiva. En cambio, como $\{\lambda\}$ es la identidad de la concatenación de lenguajes, $\{\lambda\} \cdot \Sigma^n = \Sigma^n$.
3. **Por cardinalidad combinatoria**: El número de cadenas de longitud $k$ sobre un alfabeto de $|\Sigma|$ símbolos es $|\Sigma|^k$. Para $k = 0$, todo número elevado a la cero vale $|\Sigma|^0 = 1$, lo que confirma que $\Sigma^0$ debe poseer exactamente un elemento: $\lambda$.

#### ¿Qué distingue a $\Sigma^*$ de $\Sigma^+$?
Dado un alfabeto $\Sigma \neq \emptyset$:

$$\Sigma^* = \bigcup_{k=0}^{\infty} \Sigma^k \qquad \text{mientras que} \qquad \Sigma^+ = \bigcup_{k=1}^{\infty} \Sigma^k$$

Como ninguna cadena en $\Sigma^1, \Sigma^2, \dots$ tiene longitud cero, la cadena vacía $\lambda$ **nunca** pertenece a $\Sigma^+$, mientras que **siempre** pertenece a $\Sigma^*$ (a través de $\Sigma^0 = \{\lambda\}$). Por lo tanto, la diferencia exacta entre la cerradura de Kleene y la cerradura positiva de un alfabeto es únicamente la presencia de la cadena vacía $\lambda$:

$$\Sigma^* = \Sigma^+ \cup \{\lambda\} \qquad \text{y} \qquad \Sigma^+ = \Sigma^* \setminus \{\lambda\}$$

*(Nota: Para un lenguaje arbitrario $L$, se cumple que $L^* = L^+ \cup \{\lambda\}$, y $L^+ = L^*$ si y solo si $\lambda \in L$; pero para un alfabeto $\Sigma$, cuyos elementos son símbolos individuales de longitud $1$, $\lambda \notin \Sigma$ y por ende $\Sigma^*$ y $\Sigma^+$ siempre difieren exactamente en $\lambda$).*

---

## 6. La Jerarquía de Chomsky

En 1956, el lingüista y científico cognitivo **Noam Chomsky** propuso una clasificación jerárquica de las gramáticas formales generativas $G = (V, \Sigma, P, S)$ según las restricciones impuestas sobre sus reglas de producción $P$, demostrando que cada nivel anida propiamente dentro del siguiente ($\mathcal{L}_3 \subsetneq \mathcal{L}_2 \subsetneq \mathcal{L}_1 \subsetneq \mathcal{L}_0$) y se corresponde biunívocamente con una clase de autómatas reconocedores (Chomsky, 1956, 1959; Hopcroft et al., 2007):

| Nivel | Nombre de la familia de lenguajes | Gramática que lo genera | Forma de las reglas de producción ($\alpha \to \beta$) | Máquina (Autómata) que lo reconoce | Ejemplo característico |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tipo 3** | **Lenguajes Regulares** ($\mathcal{L}_3$) | Gramática Regular (lineal por la derecha o lineal por la izquierda) | $A \to aB$ o $A \to a$ (o $A \to \lambda$), donde $A, B \in V$ y $a \in \Sigma$ | **Autómata Finito** Determinista (AFD), No Determinista (AFN) o con transiciones $\lambda$ (AFN-$\lambda$) | $\{ a^n b^m \mid n, m \ge 0 \}$ o cadenas con subcadena `010` |
| **Tipo 2** | **Lenguajes Libres de Contexto** (Incontextuales, $\mathcal{L}_2$) | Gramática Libre de Contexto (GLC / CFG) | $A \to \gamma$, donde $A \in V$ es una sola variable y $\gamma \in (V \cup \Sigma)^*$ | **Autómata de Pila No Determinista** (NPDA / AP) | $\{ a^n b^n \mid n \ge 0 \}$ y expresiones con paréntesis balanceados |
| **Tipo 1** | **Lenguajes Sensibles al Contexto** (Dependientes del contexto, $\mathcal{L}_1$) | Gramática Sensible al Contexto (GSC / CSG) o monótona | $\alpha A \beta \to \alpha \gamma \beta$ con $\gamma \neq \lambda$ (o en forma monótona: $|\alpha| \le |\beta|$) | **Autómata Linealmente Acotado** (*Linear Bounded Automaton*, LBA: Máquina de Turing no determinista con cinta acotada a $O(n)$) | $\{ a^n b^n c^n \mid n \ge 1 \}$ y $\{ ww \mid w \in \{a,b\}^* \}$ |
| **Tipo 0** | **Lenguajes Recursivamente Enumerables** (Estructurados por frases, $\mathcal{L}_0$) | Gramática Irrestricta (sin restricciones) | $\alpha \to \beta$, donde $\alpha \in (V \cup \Sigma)^+$, $\beta \in (V \cup \Sigma)^*$ y $\alpha$ contiene al menos una variable de $V$ | **Máquina de Turing** estándar (determinista o no determinista) | El lenguaje universal $A_{\text{TM}} = \{ \langle M, w \rangle \mid M \text{ acepta } w \}$ |

---

## 7. Autómatas finitos y expresiones regulares

### Definición formal del Autómata Finito Determinista (AFD)
Un **Autómata Finito Determinista (AFD)** es una quíntupla $M = (Q, \Sigma, \delta, q_0, F)$ donde (Hopcroft et al., 2007; Sipser, 2012):
1. $Q$ es un conjunto **finito** y no vacío de **estados**.
2. $\Sigma$ es un **alfabeto** finito de símbolos de entrada.
3. $\delta: Q \times \Sigma \to Q$ es la **función de transición** total, que dado un estado actual $q \in Q$ y un símbolo leído $a \in \Sigma$, devuelve exactamente un estado siguiente $\delta(q, a) \in Q$.
4. $q_0 \in Q$ es el **estado inicial** en el que arranca el autómata.
5. $F \subseteq Q$ es el conjunto de **estados de aceptación** (o estados finales).

La **función de transición extendida** $\hat{\delta}: Q \times \Sigma^* \to Q$ se define por inducción sobre la estructura de la cadena de entrada:

$$\hat{\delta}(q, \lambda) = q, \qquad \hat{\delta}(q, wa) = \delta(\hat{\delta}(q, w), a) \quad \forall w \in \Sigma^*, \; a \in \Sigma$$

El **lenguaje aceptado o reconocido** por el AFD $M$ es:

$$L(M) = \{ w \in \Sigma^* \mid \hat{\delta}(q_0, w) \in F \}$$

---

### Definición formal del Autómata Finito No Determinista (AFN)
Un **Autómata Finito No Determinista (AFN)** es igualmente una quíntupla $N = (Q, \Sigma, \delta, q_0, F)$ donde $Q, \Sigma, q_0$ y $F$ tienen la misma definición que en un AFD, pero la función de transición mapea hacia el **conjunto potencia** de $Q$ ($\mathcal{P}(Q)$ o $2^Q$):

$$\delta: Q \times \Sigma \to \mathcal{P}(Q)$$

*(En un **AFN-$\lambda$**, el dominio se amplía para permitir transiciones espontáneas sin consumir entrada: $\delta: Q \times (\Sigma \cup \{\lambda\}) \to \mathcal{P}(Q)$).*

La función de transición extendida $\hat{\delta}: Q \times \Sigma^* \to \mathcal{P}(Q)$ de un AFN se define como:

$$\hat{\delta}(q, \lambda) = \{q\}, \qquad \hat{\delta}(q, wa) = \bigcup_{p \in \hat{\delta}(q, w)} \delta(p, a)$$

y extendida a un subconjunto de estados $Z \subseteq Q$ como $\hat{\delta}(Z, w) = \bigcup_{q \in Z} \hat{\delta}(q, w)$. Una cadena $w$ es aceptada por el AFN $N$ si **al menos uno** de los cómputos posibles termina en un estado de aceptación:

$$L(N) = \{ w \in \Sigma^* \mid \hat{\delta}(q_0, w) \cap F \neq \emptyset \}$$

---

### Equivalencia entre AFD, AFN y Expresiones Regulares
Aunque un AFN parece más flexible al poder ramificar su cómputo en varios estados simultáneos (o ninguno), **los AFD y los AFN reconocen exactamente la misma clase de lenguajes: los lenguajes regulares** (Rabin & Scott, 1959):
1. **Todo AFD es un caso particular de AFN**: Basta definir $\delta_{\text{AFN}}(q, a) = \{\delta_{\text{AFD}}(q, a)\}$.
2. **Construcción de subconjuntos (*Powerset Construction*, Rabin & Scott, 1959)**: Dado cualquier AFN $N = (Q_N, \Sigma, \delta_N, q_0, F_N)$ con $|Q_N| = n$ estados, se puede construir un AFD equivalente $D = (Q_D, \Sigma, \delta_D, \{q_0\}, F_D)$ donde cada estado de $D$ es un subconjunto de estados de $N$:
   * $Q_D = \mathcal{P}(Q_N)$ (con a lo sumo $2^n$ estados, de los cuales solo se conservan los accesibles desde $\{q_0\}$).
   * $\delta_D(S, a) = \bigcup_{q \in S} \delta_N(q, a)$ para todo $S \subseteq Q_N, \; a \in \Sigma$.
   * $F_D = \{ S \subseteq Q_N \mid S \cap F_N \neq \emptyset \}$.
   Por inducción sobre $|w|$ se demuestra que $\hat{\delta}_D(\{q_0\}, w) = \hat{\delta}_N(q_0, w)$, por lo que $L(D) = L(N)$.
3. **Teorema de Kleene (Kleene, 1956)**: Un lenguaje es regular (reconocido por algún AFD/AFN) **si y solo si** puede describirse mediante una **expresión regular** (construcción de Thompson de ER a AFN-$\lambda$ y método de eliminación de estados / algoritmo de McNaughton-Yamada-Kleene de AFD a ER).

---

### Tres problemas reales en los que se aplican las expresiones regulares

1. **Análisis léxico (*Lexical Analysis / Tokenization*) en compiladores e intérpretes**:
   En la primera fase de cualquier compilador (como `gcc`, `clang` o el propio intérprete CPython), herramientas generadoras de analizadores léxicos como **Flex/Lex** reciben especificaciones mediante expresiones regulares para identificar identificadores (`[a-zA-Z_][a-zA-Z0-9_]*`), literales numéricos en punto flotante (`[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?`), operadores y palabras reservadas. El generador convierte esas expresiones regulares en un AFN mediante la construcción de Thompson, aplica la construcción de subconjuntos para obtener un AFD y finalmente lo minimiza (algoritmo de Hopcroft) para escanear el código fuente en tiempo lineal $O(|w|)$ (Aho et al., 2006).
2. **Inspección profunda de paquetes (DPI) y Sistemas de Detección de Intrusiones en Redes (NIDS como Snort y Suricata)**:
   Los cortafuegos de capa de aplicación y motores de ciberseguridad como **Snort**, **Suricata** o la biblioteca **Hyperscan** de Intel utilizan miles de firmas escritas como expresiones regulares para detectar en tiempo real ataques de inyección SQL (`SQLi`), *Cross-Site Scripting* (`XSS`), comandos de *shellcode* o tráfico de *malware* dentro del flujo de paquetes TCP/IP a velocidades de decenas de gigabits por segundo, compilando las expresiones en autómatas finitos deterministas e híbridos libres de retroceso (*backtracking*) (Yu et al., 2006; Wang et al., 2019).
3. **Búsqueda de motivos de secuencias genómicas y proteómicas en Bioinformática (PROSITE / análisis de ADN y ARN)**:
   En biología computacional, las secuencias de nucleótidos ($\Sigma = \{\text{A}, \text{C}, \text{G}, \text{T}\}$) y de aminoácidos (alfabeto de 20 símbolos) se modelan como cadenas sobre un alfabeto finito. Bases de datos internacionales como **PROSITE** codifican dominios funcionales de proteínas, sitios activos enzimáticos o sitios de corte de enzimas de restricción mediante expresiones regulares (por ejemplo, el motivo de glicosilación N-ligada `N[^P][ST][^P]`, que representa una Asparagina seguida de cualquier aminoácido distinto de Prolina, seguido de Serina o Treonina, y otro aminoácido distinto de Prolina), permitiendo localizar regiones biológicamente activas en genomas completos de millones de pares de bases (Navarro & Raffinot, 2002).

---

## Referencias citadas en este documento

* Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, techniques, and tools* (2.ª ed.). Addison-Wesley.
* Brookshear, J. G. (1993). *Teoría de la computación: Lenguajes formales, autómatas y complejidad*. Addison-Wesley Iberoamericana.
* Chomsky, N. (1956). Three models for the description of language. *IRE Transactions on Information Theory*, 2(3), 113–124. https://doi.org/10.1109/TIT.1956.1056813
* Chomsky, N. (1959). On certain formal properties of grammars. *Information and Control*, 2(2), 137–167. https://doi.org/10.1016/S0019-9958(59)90362-6
* Church, A. (1936). An unsolvable problem of elementary number theory. *American Journal of Mathematics*, 58(2), 345–363. https://doi.org/10.2307/2371045
* Copeland, B. J. (Ed.). (2004). *The essential Turing: Seminal writings in computing, logic, philosophy, artificial intelligence, and artificial life plus The secrets of Enigma*. Oxford University Press.
* Davis, M. (2000). *The universal computer: The road from Leibniz to Turing*. W. W. Norton & Company.
* Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2007). *Introducción a la teoría de autómatas, lenguajes y computación* (3.ª ed.). Pearson Educación.
* Kleene, S. C. (1956). Representation of events in nerve nets and finite automata. En C. E. Shannon & J. McCarthy (Eds.), *Automata studies* (pp. 3–41). Princeton University Press. https://doi.org/10.1515/9781400882618-002
* Linz, P. (2017). *An introduction to formal languages and automata* (6.ª ed.). Jones & Bartlett Learning.
* Navarro, G., & Raffinot, M. (2002). *Flexible pattern matching in strings: Practical on-line search algorithms for texts and biological sequences*. Cambridge University Press. https://doi.org/10.1017/CBO9781316135228
* Rabin, M. O., & Scott, D. (1959). Finite automata and their decision problems. *IBM Journal of Research and Development*, 3(2), 114–125. https://doi.org/10.1147/rd.32.0114
* Sipser, M. (2012). *Introduction to the theory of computation* (3.ª ed.). Cengage Learning.
* Turing, A. M. (1936). On computable numbers, with an application to the Entscheidungsproblem. *Proceedings of the London Mathematical Society*, s2-42(1), 230–265. https://doi.org/10.1112/plms/s2-42.1.230
