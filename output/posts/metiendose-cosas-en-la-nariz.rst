.. title: Metiéndose cosas en la nariz
.. slug: metiendose-cosas-en-la-nariz
.. date: 2013/02/26 22:17:55
.. tags:
.. link:
.. description:

nose_ es un excelente *framework* para testing en python. Es mucho más
que un *testrunner* inteligente: tiene un conjunto de extensiones y shortcuts
de aserciones de ``unittest``, soporta fixtures y setups/teardown
por paquetes, y viene con un montón de plugins incorporados.

    "nose extends unittest to make testing easier"

dice el eslogan y eso es lo que queremos: tests más fáciles de escribir,
más rápidos de ejecutar.

De plugins y opciones que potencian esta idea se trata este post.

nose-progressive
----------------

.. epigraph::

   Ah, beautiful dots

   -- `Erik Rose <http://blog.mozilla.org/webdev/2011/04/14/a-humane-python-test-runner/>`_

*"Puntito, puntito, puntito, puntito..."*, cuenta mi mente en standby
cuando los test van pasando, como ovejitas que saltan un cerco.
Pero, oh desdicha, una "efe", la oveja negra que falla, aparece
en la pantalla y la ansiedad por saber cuál nos invade.

El problema es que por default (con ``--verbose=1``), nose
pospone el detalle de errores y fallos hasta el final de la corrida.
En suites gigantes (que demoran más de 30 minutos en completarse,
por ejemplo) esto es un engorro.

nose-progressive_ reemplaza la interfaz de usuario por una mucho más
amigable y bonita. En vez de puntitos, una barra de progreso al pie de la
pantalla va indicando el progreso satisfactorio, y deja el resto de la pantalla
para mostrar errores y fallos *on the fly*.

.. image:: https://raw.github.com/erikrose/nose-progressive/master/in_progress.png

Como si fuera poco, te da shortcuts a la línea donde se produjo un fallo
(por ejemplo: ``vim +258 common/tests/test_guideplan.py``), simplifica los
tracebacks a la parte útil, e incluye colores usados con criterio
(basada en la genial biblioteca blessing_, del mismo autor).

Para instalarlo, lo de siempre:

.. code-block:: bash

    (env) $ pip install nose-progressive

Para usarlo, agregar ``--with-progressive`` como parámetros de ``nosetests``,
o bien, para usarlo siempre, configurarlo en ``.noserc`` o en la
variable ``NOSE_ARGS`` de django-nose_

django-nose
-----------

Si trabajás con Django esto quizas suene a perogrullada, pero django-nose_
es la vuelta de tuerca que faltaba para que la nariz brille en este entorno.
Con django-nose por defecto sólo se corren los tests del proyecto y no
los de todas las aplicaciones instaladas (que, se supone, tienen sus propios
tests).

Y entre otras opciones o, tiene  un modo de reuso de la base de datos,
(configurando ``REUSE_DB=1`` como variable de entorno), que nos evita la creación
de tablas en cada corrida, ahorrando unos cuantos segundos de setup en aplicaciones
como muchos modelos. Por supuesto, si la base de datos cambia (porque
se agregó un modelo o se se migró con South_) tenés que asegurarte
que la variable está en 0 para que cree la última version

with-id + failed
----------------

La opción `--with-id <https://nose.readthedocs.org/en/latest/usage.html?highlight=with-id#cmdoption--with-id>`_
(estrictamente el plugin ``TestId``, que viene en las baterías incluídas de nose)
le asigna un número único a cada test ejecutado,
y los guarda en el archivito ``.noseids`` junto con su path y el
resultado de la última corrida.

Lo bueno es que pasando ``--with-id --failed`` nose usa esa información
y ejecuta solamente los tests que fallaron en la última corrida,
permitiendo una rápida iteración *"falla/corrección"*.

nose-selecttests
----------------

Frecuentemente sucede que tenemos caso (una subclase de ``TestCase``)
con muchas pruebas (métodos) que están lógicamente agrupadas
porque comparten un setup, por ejemplo,
y sin embargo sólo queremos correr un subconjunto.

Sabemos que como es inteligente y poco burocrático, nose no sólo ejecuta
tests definidos como subclases de ``unittest.TestCase`` sino
cualquier paquete, módulo, función o clase
que *matchee* una expresión regular, que por defecto es ``(?:^|[b_./-])[Tt]est``
Con el parámetro `-m  <https://nose.readthedocs.org/en/latest/usage.html?highlight=with-id#cmdoption-m>`_
se puede redefinir este patrón, pero igualmente no aplica a nivel
métodos.

Por eso existe nose-selecttests_, que permite filtrar pruebas con
determinada subcadena en el nombre del método.

Por ejemplo:

.. code-block:: bash

    $ djntest -v 2 common/tests/test_sequence_diff.py

    #2976 test_differ_in_fk (cpi_mrp.apps.common.tests.test_sequence_diff.TestInstanceDiff) ... ok
    #2977 test_differ_in_m2m (cpi_mrp.apps.common.tests.test_sequence_diff.TestInstanceDiff) ... ok
    #2979 test_multiple_diff (cpi_mrp.apps.common.tests.test_sequence_diff.TestInstanceDiff) ... ok
    #2980 test_only_compare_same_type (cpi_mrp.apps.common.tests.test_sequence_diff.TestInstanceDiff) ... ok

    ----------------------------------------------------------------------
    Ran 4 tests in 0.375s

En cambio:

.. code-block:: bash

    $ djntest --select-tests=differ -v 2 apps/common/tests/test_sequence_diff.py

    #2976 test_differ_in_fk (cpi_mrp.apps.common.tests.test_sequence_diff.TestInstanceDiff) ... ok
    #2977 test_differ_in_m2m (cpi_mrp.apps.common.tests.test_sequence_diff.TestInstanceDiff) ... ok
    ----------------------------------------------------------------------
    Ran 2 tests in 0.088s


django-tests-autocomplete
--------------------------

Esta herramienta no es estrictamente un plugin de nose, sino un helper
que aprovecha las posibilidades de bash para
`autocompletar <http://bash-completion.alioth.debian.org/>`_ usando la tecla
tab.

¿Para qué sirve? nose acepta un path (o muchos) para especificar qué test correr:

.. code-block:: bash

    $ nosetests path/to/test.py

Pero también permite afinar la puntería y "meterse" adentro del módulo:

.. code-block:: bash

    $ nosetests path/to/test.py:MyImportantTestCase

E incluso adentro del testcase:

.. code-block:: bash

    $ nosetests path/to/test.py:MyImportantTestCase.test_super_important

Desde el ``:`` en adelante estamos en Python y Bash ya no sabe autocompletar,
salvo que usemos esta herramienta que instrospecciona y "alimenta" el
autocompleter.

Lo hizo Javi Mansilla en Machinalis_ y
`busca ayuda <https://github.com/machinalis/django-test-autocomplete#future-features>`_
para mejorarlo y generalizarlo.

¿No sería buenísimo que esto estuviese built-in en nose? ¿Nos ayudarías?

nose-timer
----------

¿Cuánto tiempo insume cada test? Instalá nose-timer_ y activalo (con ``--with-timer``)
para saber la respuesta.

nose-ipdb
---------

nose tiene una opción ``--pdb`` (o la más estricta ``--ipdb-failures``)
que nos manda al debugger cuando un test falla o da error.

nose-ipdb_ lo imita, pero usando el más pulenta de los debuggers: ipdb_.


Suficiente por hoy. Pero ¿me estoy perdiendo alguna cosa interesante
para meter en mi nariz?


.. _nose: https://nose.readthedocs.org
.. _nose-progressive: https://pypi.python.org/pypi/nose-progressive/
.. _@ErikRose: https://twitter.com/ErikRose
.. _blessing: https://pypi.python.org/pypi/blessings
.. _django-nose: https://github.com/jbalogh/django-nose
.. _South: http://south.aeracode.org/
.. _nose-selecttests: https://github.com/iElectric/nose-selecttests
.. _Machinalis: http://machinalis.com
.. _nose-timer: https://github.com/mahmoudimus/nose-timer/
.. _nose-ipdb: https://github.com/flavioamieiro/nose-ipdb
.. _ipdb: https://pypi.python.org/pypi/ipdb
