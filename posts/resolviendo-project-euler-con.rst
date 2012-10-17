A través del blog de `Juanjo Conti <http://www.juanjoconti.com.ar>`_
descubrí `Project Euler <http://projecteuler.net>`_, una serie de
desafíos matemáticos de enunciación sencilla para resolver con
computadoras.

Juanjo estuvo resolviendo los primeros problemas, y yo quise hacer mi
intento. `El
primero <http://projecteuler.net/index.php?section=problems&id=1>`_
plantea obtener la suma de todos los multiplos de 3 o de 5 menores a
1000.

Lo resolví con esta pythonica (lo es?) línea:

::

    sum([i for i in range(1000) if (i % 3 == 0 or i % 5==0)])

El resultado es 233168.

Breve explicación
~~~~~~~~~~~~~~~~~

Se basa en el uso de `list
comprehensions <http://docs.python.org/tutorial/datastructures.html#list-comprehensions>`_,
una de las "joyas de la corona" de las características de Python.

Es una manera de generar listas de una manera concisa, compuesta por una
expresión seguida de uno a más **for** y una condicionalidad al final

La lista ** [i for i in range(1000) if (i % 3 == 0 or i % 5==0)]** se
lee así: crear una lista con todos los elementos (expresión i) en el
rango de 0 a 999 (for) cuyo resto de dividirlo por 3 o 5 sea 0 (if).
