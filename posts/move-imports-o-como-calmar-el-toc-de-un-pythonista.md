<!--
.. title: move-imports, o cómo calmar el TOC de un pythonista
.. slug: move-imports-o-como-calmar-el-toc-de-un-pythonista
.. date: 2020-05-12 16:13:41 UTC-03:00
.. tags: scripts
.. category: scripts
.. link:
.. description:
.. type: text
-->

Una historia de éxito: un grupito pequeño de programadores (o quizas sólo uno)
a pura pasión, café y feedback de sus usuarios mete miles de lineas de código
que logran hacer funcionar un negocio.

Parte del éxito, supongamos, es porque el sistema está hecho en Python, que se eligió porque es versátil y pragmático para obtener resultados rápidos.
Pero se sabe: en el vértigo la pasión, el feedback y el café no cabían muchas elegancias ni había tiempo para estilos o convenciones. *Caminante no hay camino, se hace camino al andar*, dijo Machado, refiriéndose a la deuda técnica que toman las startups en sus inicios.

El negocio comienza a crecer, hay más demandas de los clientes y la cosa está tan fea que algo, alguito, hay que mejorar. Como, por suerte, la cosa va bien, se contratan nuevos programadores que tengan experiencia en Python específicamente. Y estos nuevos programadores experimentados, los *pythonistas*, vienen con
sus mañosas convenciones del lenguaje a cuestas. Una de ellas está [tallada en piedra](https://pep8.org#imports): salvo ineludibles excepciones, **los *imports* van en la cabecera del módulo y en un orden en particular**.

Hay justificación, dicen los pythonistas. Simplificar la lectura, saber a simple vista de qué depende un módulo, tener bloques de código más chicos, no repetirse. Pero, aceptémoslo, es un [TOC](https://es.wikipedia.org/wiki/Trastorno_obsesivo-compulsivo).

<!-- TEASER_END -->

### `move-imports`, un script para calmar el TOC de los *import* inlines

La startup tiene cientos de módulos con imports en cualquier lado. Especialmente en los tests, donde existía una razón de fuerza mayor en el setup, cuyo *workaround* barato fue adoptar la convención **tallada sobre diamante** de que algunos tipos de imports (modelos de datos) debían hacerse adentro de la función de prueba.

*"¡Vade retro Satana!"* se espantan entonces los pythonistas, encuentran el hueco para deshacerse de esa razón de fuerza mayor y se fabrican una herramienta (al que ponen el nada ingenioso nombre de "[move-imports](https://github.com/mgaitan/move-imports)") para adaptar automáticamente los cientos de módulos a la convención. Porque somos vagos sólo para las cosas aburridas.

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">being a programmer, I&#39;m too lazy to spend 8 hours mindlessly performing a function, but not too lazy to spend 16 hours automating it.</p>&mdash; Martín Gaitán (@tin_nqn_) <a href="https://twitter.com/tin_nqn_/status/1253521851894181889?ref_src=twsrc%5Etfw">April 24, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>


Por ejemplo un módulo `path/to_refactor.py` con este contenido:

```python
from math import sin

def spam():
    from math import cos
    import datetime as dt
    return sin(1), cos(0), dt.datetime.now()

def ham():
    from math import tan
    return tan(1)
```

se "refactoriza" con este comando

```
$ move-imports path/to_refactor.py --isort
```

y queda así:

```python
import datetime as dt
from math import cos, sin, tan


def spam():
    return sin(1), cos(0), dt.datetime.now()

def ham():
    return tan(1)
```

El `--isort` es opcional pero muy recomendado, ya que le pasa [isort](https://github.com/timothycrosley/isort) para juntar imports del mismo módulo, quitar repetidos y ordenarlos como el Zen manda.

Un chichecito es que si encuentra que se puede marcar un import inline
con un comentario (por ejemplo `# noqa`) en la misma linea o alguna linea arriba del import para ignorarlo de la lista de bloques a mover.

### ¿Cómo funciona?

El módulo [ast](https://docs.python.org/3/library/ast.html) de la biblioteca estándar de Python es el que permite "parsear" el código fuente y obtener un árbol de objetos que representan la grámatica. Cada tipo de sentencia python es un nodo de este árbol, que puede a su vez tener sus propias nodos anidados.

Por ejemplo, el módulo `to_refactor.py` de arriba (en su versión original),
se ve así

```python
In [4]: mod =  ast.parse(Path('path/to_refactor.py').read_text())
In [5]: mod.body
Out[5]:
[<_ast.Import at 0x7f221c354eb8>,
 <_ast.ImportFrom at 0x7f221c354898>,
 <_ast.FunctionDef at 0x7f221c354c18>,
 <_ast.FunctionDef at 0x7f221c33d240>]
```

A nosotros nos importa encontrar los nodos tipo `ast.Import` y `ast.ImportFrom` que son los que corresponden a sentencias `import x` y `from x import y`.

Podemos caminar todos los nodos recursivamente y obtener una gran lista plana
de todos los nodos con `ast.walk(mod)` donde `mod` es el nodo inicial, el módulo.

Un dato que incluye un nodo de `ast` es el número de línea donde esa sentencia comienza. Por ejemplo el `ImportFrom` de arriba

```python
In [7]: mod.body[1].lineno
Out[7]: 2
```

Podemos asumir que el bloque de líneas de código que componen un nodo termina justo antes de que empiece el que le sigue, así que es plausible una función que encuentre los segmentos (las lineas del source) donde hay *imports* y los recorte (es decir, reescriba el módulo sin esas lineas) y luego pegue todas las recortadas juntas justo a continuación de los imports que ya existen en la cabecera (o en la línea 1 si no había).

Si bien Python 3.8 trae una función llamada [get_source_segment](https://docs.python.org/3/library/ast.html#ast.get_source_segment) que sería útil para este fin, hay dos motivos para hacerlo por nuestra cuenta:

1. que funcione con otras versiones no tan nuevas de python
2. que no descarte comentarios que puedan estar justo arriba de un nodo a mover (por omisión, los comentarios no representan nodos en ast, así que hay que tratarlos desde la edición texto)

Y eso es [casi todo](https://github.com/mgaitan/move-imports/blob/master/move_imports.py).

### Es parte del trabajo, amigos

Las buenas startups (y las buenas personas que de alguna manera "cortan el queso" en ellas) comprenden que para mantener programadores y programadoras motivadas no se trata tanto de cervezas, festejos y merchandasing de regalo, sino de alimentar la creatividad y de dar cierta autonomía para que sean "quienes se embarran todos los días" quienes decidan cómo mejorar, y brindar los recursos para hacerlo.

A veces se puede más, a veces se puede menos, hay que saber adaptarse. Pero ayudar a solucionar esta picazones chiquitas (y mejor, haciendo algo que les puede servir a más personas, haciéndolo público) lleva tan solo algunas horas y repercute positivamente no sólo en el código, sino en el confort de un equipo y la motivación de las personas.

¡Por más horas de ñoñes rascándose picazones!

