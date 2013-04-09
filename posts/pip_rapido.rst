

Un ejemplo: instalar lxml
-------------------------

::

    (test)tin@traful:~/lab/test$ time pip install lxml
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

Una vez cacheado, las siguientes veces que queramos instalar la misma versión de lxml
no bajará **el archivo** de nuevo ::

    (test2)tin@traful:~/lab/test2$ time pip install lxml

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

Hmm, mejoró realmente poco. ¿que clase de caché es esta?
Chusmeemos que hay en el directorio:

    (test)tin@traful:~/lab/test$ ls ~/.pip_download_cache/ | grep lxml
    https%3A%2F%2Fpypi.python.org%2Fpackages%2Fsource%2Fl%2Flxml%2Flxml-3.1.1.tar.gz
    https%3A%2F%2Fpypi.python.org%2Fpackages%2Fsource%2Fl%2Flxml%2Flxml-3.1.1.tar.gz.content-type

¿Caché de urls?

Lo explica simple `Carl Meyer <https://github.com/pypa/pip/issues/680#issuecomment-8773509>`_:

    La función ``--download-cache`` no apunta a prevenir la búsqueda en la red del archivo
    correcto a bajar: todo lo que hace es guardarlo una vez que lo encontró.
    Si de verdad te interesa instalar tus depedencias desde tu compu (sin salir a la red)
    usá ``--download`` primero y luego ``--find-links`` (apuntando al path de descarga) con
    ``--no-index``.

Vamos por esa::

    (test3)tin@traful:~/lab/test3$ time pip install --download ~/.pip_downloads lxml
    Downloading/unpacking lxml
      Using download cache from /home/mgaitan/.pip_download_cache/https%3A%2F%2Fpypi.python.org%2Fpackages%2Fsource%2Fl%2Flxml%2Flxml-3.1.1.tar.gz
    Saved /home/mgaitan/.pip_downloads/lxml-3.1.1.tar.gz
        [...]

    Successfully downloaded lxml
    Cleaning up...

    real    2m8.969s
    user    0m1.008s
    sys 0m0.136s

Uff, 2 minutos en copiar un archivo que ya tenía bajado. Evidentemente lo que demora mucho
es *averiguar* la versión del archivo a bajar ()

En este caso, el caché es directamente el archivo::

    (test)mgaitan@traful:~/lab/test$ ls ~/.pip_downloads/ | grep lxml
    lxml-3.1.1.tar.gz


Una vez cacheado el paquete::

    (test3)mgaitan@traful:~/lab/test3$ time pip install --no-index --find-links ~/.pip_downloads lxml
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

Ok, esto suena mejor.