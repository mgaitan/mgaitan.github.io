Hace algunos días, en
`spip-es <http://listes.rezo.net/mailman/listinfo/spip-es>`_ se planteó
la duda de cómo controlar una cabecera diferente para algunas secciones
en particular.

`Xabi
aportó <http://archives.rezo.net/spip-es.mbox/200903.mbox/%3C29008.88.7.114.173.1236164746.squirrel@correo.nodo50.org%3E>`_
la solución canónica, que es crear esqueletos ad-hoc para cada sección
difente, valiendose de los esqueletos con forma *rubrique-X.html* (donde
X es el ID de la sección).

Esto se describe en el apartado "`Para ir más
lejos <http://www.spip.net/es_article2257.html>`_" de la documentación.

En este caso particular, sólo se quería mostrar el logo en la cabecera
para algunas secciones. El problema es que las secciones "diferentes"
serían iguales entre sí, pero invocando distintos esqueletos. Esto
contradice el `principio DRY <http://es.wikipedia.org/wiki/DRY>`_
siempre deseable en todo desarrollo de software.

Una forma sencilla, pero a la vez parcial de resolver esto, es hacer un
`enlace duro <http://es.wikipedia.org/wiki/enlace_duro>`_ entre los
esqueletos que son iguales.

Por ejemplo, la sección 2, la 4 y la 6, tendrán el mismo esqueleto.
Entonces creamos el rubrique-2.html y definimos rubrique-4.html y
rubrique-6.html como enlaces duros al primero. Desde la línea de
comandos:

::

    $ ln rubrique-2.html rubrique-4.html
    $ ln rubrique-2.html rubrique-6.html

Esta solución funciona, pero es sólo para servidores *\*nix* y teniendo
acceso a la consola (por `SSH <http://es.wikipedia.org/wiki/SSH>`_, por
ejemplo). Además, hay que documentar bien qué se está haciendo, porque
da lugar a errores cuando dos esqueletos "linkeados" intentan ser
iguales.

Por suerte, hay varias otras maneras de resolver esto,

Filtros de condición o filtro match
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Esta
solución <http://archives.rezo.net/spip-es.mbox/200903.mbox/%3C516299.21618.qm@web90607.mail.mud.yahoo.com%3E>`_,
es la que aportó `Juan Pablo
Portugau <http://www.graciasdenada.com.ar/>`_.

Lo que plantea, es usar la baliza #ID\_RUBRIQUE (que obviamente,
devuelve el número de la sección) con filtros de comparación. Es,
hablando en geek, un simple **if**: *Si es la sección 2, mostrar el
logo. Sino, nada*:

En código SPIP:

::

    [(#ID_RUBRIQUE|=={2}|?{'#LOGO_RUBRIQUE',''})]

La limitación de esta solución se da cuando son múltiples los valores
posibles. En nuestro caso, se debe mostrar el logo cuando se trata de la
sección 2, de la 4 o de la 6. Juan Pablo propone anidar esta estructura.

::

    [(#ID_RUBRIQUE|=={2}|?{'#LOGO_RUBRIQUE',[(#ID_RUBRIQUE|=={4}|?{'#LOGO_RUBRIQUE',[(#ID_RUBRIQUE|=={6}|?{'#LOGO_RUBRIQUE',''})]})]})]

Aunque es sintácticamente correcto, el código resultante es bastante
inmantenible para un ser humano con cerebro normal y el monito parseador
de SPIP queda agitado.

Para eso existe el filtro
`match <http://www.spip.net/fr_article901.html#match>`_, que se vale de
las `expresiones regulares <http://www.regular-expressions.info/>`_ para
que hagamos nuestro festín.

Lo de arriba, puede reducirse a esto:

::

    [(#ID_RUBRIQUE|match{^(2|4|6)$}|?{'#LOGO_RUBRIQUE',''})]

El filtro devuelve **VERDADERO** si el valor de #ID\_RUBRIQUE empieza
con 2, 4 o 6 y termina con nada. Que es, dicho de otra manera, lo que
queremos.

Y aún más claro: bucles como filtros
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Las expresiones regulares *no son moco de pavo*, diría mi abuela. Super
potentes, pero poco escalables en la curva complejidad-comprensibilidad.

Hay una solución que es muy útil, sencilla pero no trivial: usar un
bucle como filtro.

::

La explicación es de la lógica de conjuntos: los criterios de un bucle
funcionan como condiciones AND. Deben cumplirse todas. En este caso, el
primer criterio ``{id_rubrique IN (1,2,4)}`` exige que el id\_rubrique
sea 1, 2 o 4. En el segundo ``{id_rubrique}``, se exige que sea el que
viene en contexto. Por lo tanto, este bucle sólo funcionará (mostrará el
logo) si el id\_rubrique *del contexto* es 1, 2 o 4. En lógica, es una
operación `O
exclusiva <http://es.wikipedia.org/wiki/Disyunción_lógica>`_

Funciona, es más legible que cualquiera de las otras soluciones y además
permite una clausula *ELSE* mucho más accesible, simplemente usando la
estructura completa del bucle.
