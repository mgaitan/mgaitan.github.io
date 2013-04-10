.. title: pip, apurate por favor
.. slug: pip-apurate-por-favor
.. date: 2013/04/10 01:17:55
.. tags: pip, python
.. description:

`pip <http://pip-installer.org/>`_  es una herramienta esencial
para el trabajo diario de un programador python: es el manejador
de paquetes de nuestro entorno de trabajo (¡`virtual <http://www.virtualenv.org/en/latest/>`_ por favor!),
con el que instalamos, actualizamos o eliminamos las dependencias de nuestro proyecto
(y, recursivamente, las dependencias que estas pudieran tener).

Conceptualmente es similar a los manejadores de paquetes de sistema como ``apt-get``,
diferenciándose en que, por defecto, *consulta cada vez* a una `base de
datos online <https://pypi.python.org/pypi/>`_ si el paquete solicitado existe y de dónde
puede bajar la última versión o la específica que se haya pedido.

Responder "qué, cuál y de dónde" es una tarea lenta porque dicha base de datos no es
más que una página html por cada paquete con links que funcionan como un índice (como
`este <https://pypi.python.org/simple/lxml/>`_  que pip
`debe parsear <https://github.com/pypa/pip/blob/f1fb4b4fda127529e24b71a4e03bb0b5df484ef6/pip/index.py#L141>`_
comparar y elegir la mejor opción para bajar (a veces incluso debe parsear la homepage
del proyecto en busca de links de descarga, puaj!).

Por eso (y porque muchas veces la infraestructura se satura) el uso estándar de pip es lento.
Pero hay algunas maneras de que lo sea menos. Veámoslas.


No bajes dos veces lo mismo
---------------------------

El funcionamiento básico de pip es instalar un paquete con ``pip install <paquete>``: busca, baja e
instala el paquete. El flag ``--download_cache=<path>`` evita repetir el paso del medio,
cosa tediosa cuando tenemos que instalar frecuentemente (por ejemplo en distintos virtualenvs)
la misma dependencia o cuando el uso de ancho de banda es limitado.

Por ejemplo instalamos por primera vez `lxml <http://lxml.de/>`_ y vemos cuanto tarda.

.. code-block:: bash

    (test)tin@traful:~/lab/test$ time pip install lxml --download-cache=~/.pip_download
    Downloading/unpacking lxml
      Downloading lxml-3.1.1.tar.gz (3.3MB): 3.3MB downloaded
      Storing download in cache at /home/tin/.pip_download_cache/https%3A%2F%2Fpypi.python.org%2Fpackages%2Fsource%2Fl%2Flxml%2Flxml-3.1.1.tar.gz
      Running setup.py egg_info for package lxml
        Building lxml version 3.1.1.

        [... compilación]


    Successfully installed lxml
    Cleaning up...

    real    2m58.276s
    user    0m38.822s
    sys 0m0.676s
    (test)tin@traful:~/lab/test$

¡3 minutos! Y eso que estoy en una conexión bastante rápida.

.. tip::

   Cualquier flag que pip acepta en su linea de comando se puede configurar como una
   `variable de entorno`_. Entonces podemos setear flag por defecto en nuestro ``.bashrc``,
   por ejemplo.. code-block: bash

        export PIP_DOWNLOAD_CACHE=~/.pip_download_cache


Pero sigamos: una vez cacheado, las siguientes veces que queramos instalar la misma versión de lxml
no bajará **el archivo** de nuevo

.. code-block:: bash

    (test2)tin@traful:~/lab/test2$ time pip install lxml --download-cache=~/.pip_download

    Downloading/unpacking lxml
      Using download cache from /home/tin/.pip_download_cache/https%3A%2F%2Fpypi.python.org%2Fpackages%2Fsource%2Fl%2Flxml%2Flxml-3.1.1.tar.gz
      Running setup.py egg_info for package lxml
        Building lxml version 3.1.1.

        [... compilación]

    Successfully installed lxml
    Cleaning up...

    real    2m30.624s
    user    0m38.966s
    sys 0m0.504s


Mejoró realmente poco. ¿que clase de caché es esta?
Chusmeemos que hay en el directorio.

.. code-block:: bash

    (test)tin@traful:~/lab/test$ ls ~/.pip_download_cache/ | grep lxml
    https%3A%2F%2Fpypi.python.org%2Fpackages%2Fsource%2Fl%2Flxml%2Flxml-3.1.1.tar.gz
    https%3A%2F%2Fpypi.python.org%2Fpackages%2Fsource%2Fl%2Flxml%2Flxml-3.1.1.tar.gz.content-type

¿Caché de urls? ``-download-cache`` no evita todo el laburo de averiguar de dónde bajar,
sino simplemente no baja si la url resultante ya existe (como nombre de un archivo)
en este directorio.

Lo explica simple `Carl Meyer <https://github.com/pypa/pip/issues/680#issuecomment-8773509>`_:

    La función ``--download-cache`` no apunta a prevenir la búsqueda en la red del archivo
    correcto a bajar: todo lo que hace es guardarlo una vez que lo encontró.
    Si de verdad te interesa instalar tus depedencias desde tu compu (sin salir a la red)
    usá ``--download`` primero y luego ``--find-links`` (apuntando al path de descarga) con
    ``--no-index``.

Una caché sin salir a la red
----------------------------

Sigamosle la corriente al bueno de `@carljm <https://twitter.com/carljm>`_:

.. code-block:: bash

    (test3)tin@traful:~/lab/test3$ time pip install --download=~/.pip_packages lxml
    Downloading/unpacking lxml
      Using download cache from /home/mgaitan/.pip_download_cache/https%3A%2F%2Fpypi.python.org%2Fpackages%2Fsource%2Fl%2Flxml%2Flxml-3.1.1.tar.gz
    Saved /home/mgaitan/.pip_packages/lxml-3.1.1.tar.gz
        [...]

    Successfully downloaded lxml
    Cleaning up...

    real    2m8.969s
    user    0m1.008s
    sys 0m0.136s

¡Uff, 2 minutos en copiar un archivo que ya tenía bajado! (evidentemente lo que demora mucho
es *averiguar* la versión del archivo a bajar)

.. tip::

   se puede inspeccionar el berenjenal de redirecciones y parseos que suceden hasta que pip
   da con el paquete lxml a bajar haciendo el comando más verborrágico con
   ``pip install lxml -vvv``


En este caso, el caché es directamente el archivo:

.. code-block:: bash

    (test)mgaitan@traful:~/lab/test$ ls ~/.pip_packages/ | grep lxml
    lxml-3.1.1.tar.gz

Por suerte, una vez cacheado el paquete de esta manera no tendremos
que consultar el índice online las siguientes veces.

.. code-block:: bash

    (test3)mgaitan@traful:~/lab/test3$ time pip install --no-index --find-links=~/.pip_packages lxml
    Ignoring indexes: https://pypi.python.org/simple/
    Downloading/unpacking lxml
      Running setup.py egg_info for package lxml
        Building lxml version 3.1.1.

        [...]


    Successfully installed lxml
    Cleaning up...

    real    0m38.944s
    user    0m38.338s
    sys 0m0.564s

Ok, ya va mejor.

Haciendo que la cosa vuele: no recompiles la rueda
--------------------------------------------------

pip 1.4 (en desarrollo) trae `soporte integrado <https://github.com/pypa/pip/commit/5d02b5207a305543ad6ef19d6e6596ffa45b99e5>`_ para el nuevo formato de paquetes
wheel_ (superador del viejo *egg* y basado en los estándares actuales)
que es muchísimo más rápido que instalar desde fuentes (sobre todo en casos
que se debe compilar, como lxml)

.. _wheel: http://wheel.rtfd.org/,

Para usar wheel el paquete a bajar tiene que existir en dicho formato y todavía no abundan
en PyPi asi que podemos armarlos localmente con el propio pip

.. code-block:: bash

    pip wheel --wheel-dir=./pip_packages lxml

Eso es similar a usar ``--download`` pero además compila y empaqueta como
un archivo ``.whl``

Para que pip acepte instalar estos archivos hay que usar ``--use-wheel``
y para que los busque localmente haremos:

.. code-block:: bash

    pip install --use-wheel --no-index --find-links=~/.pip_packages lxml

¡Lo que tardó menos de 2 decimas de segundo! Un speedup del 90mil veces respecto al primer
y canónico ``pip install lxml``

.. code-block::

    (test)tin@morochita:~/lab/test$ time pip install --use-wheel --no-index --find-links=. lxml
    Ignoring indexes: https://pypi.python.org/simple/
    Downloading/unpacking lxml
    Installing collected packages: lxml
    Successfully installed lxml
    Cleaning up...

    real    0m0.180s
    user    0m0.152s
    sys 0m0.024s

Asi que ya sabés: todos esos paquetes que instalás en cada entorno (quizas ipython,
django, whatever) me los haces rodar para que pip vuele.


.. _variable de entorno: http://www.pip-installer.org/en/latest/configuration.html#environment-variables
