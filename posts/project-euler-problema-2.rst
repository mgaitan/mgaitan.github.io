El `problema nº
2 <http://projecteuler.net/index.php?section=problems&id=2>`_ pide
obtener la suma de todos los números impares pertenencientes a la
`sucesión de
Fibonacci <http://es.wikipedia.org/wiki/sucesión_de_Fibonacci>`_ menores
a 4 millones.

El código con el que lo resolví es este:

::

    def fibo(max):
            a, b = 0, 1
               n = a + b
               while n < max:
                    yield n
                    a, b = b, n
                    n = a + b
    
    sum([i for i in fibo(4000000) if i%2 == 0])

El resultado es 4613732.

Explicación
~~~~~~~~~~~

Fibonacci es el "hola mundo matemático" y Python luce su elegancia con
este problema.

El aspecto interesante de la función **fibo()** definida en el código de
arriba es que no se trata de una función común sino de un generador.
Sintácticamente la diferencia está en que no utiliza la sentencia
**return** sino
**`yield <http://docs.python.org/reference/simple_stmts.html#the-yield-statement>`_**
.

La definición de
*`yield <http://www.wordreference.com/definition/yield>`_*. en su
acepción de verbo, dice «end resistance, especially under pressure or
force;». Ceder, no oponer resistencia.

La diferencia sustancial entre un yield y un return es que el yield
devuelve el resultado parcial de cada iteración y hace una "marca de
entrada" desde donde se comenzará a ejecutar la próxima vez que la
función (el generador) sea invocado.

Esto permite una recursividad con "`evaluación
perezosa <http://en.wikipedia.org/wiki/Lazy_evaluation>`_", mucho más
eficiente en términos computacionales.
