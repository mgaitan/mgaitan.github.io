    **UPDATE** Hay una nueva versión con interfaz gráfica
    `acá <blog/article/cuevanalinks-ahora-para-seres>`_

Parece que se me hizo hobby `chupar links de
cuevana.tv <blog/article/yendo-a-las-fuentes-de-cuevana-tv>`_ y el
experimento ahora tiene su versión pythonica:
`Cuevanalinks <http://pypi.python.org/pypi/CuevanaLinks>`_ .

Es un pequeño proyecto que permite "conseguir links" de contenidos
ofrecidos en cuevana, sirviendo estos como fuentes a manejadores de
descargas como `Tucan <http://www.tucaneando.com/>`_ o
`JDownloader <http://jdownloader.org/>`_.

Más allá de los resultados, me ha tenido entretenido algunas horas y me
permitió aprender (o al menos resolver) algunas cosas: cómo se usa
mercurial (y en particular un merge conflictivo con Meld), cómo se
escribe un setup.py, como se distribuye via PyPi, etc.

También, por supuesto, me permitió usar dos utilidades que me gustan
mucho: `PyQuery <http://pyquery.org>`_ y
`plac <http://pypi.python.org/pypi/plac>`_.

La aplicación tiene dos módulos/componentes:

#. Una `biblioteca que intenta funcionar como
   API <https://bitbucket.org/tin_nqn/cuevanalinks/src/943b329f3da5/cuevanalinks/cuevanaapi.py>`_
   de `Cuevana <http://www.cuevana.tv>`_ y es la encargada de
   *scrappear* la web en busca de la info interesante.

#. Una `interfaz de línea de
   comandos <https://bitbucket.org/tin_nqn/cuevanalinks/src/943b329f3da5/cuevanalinks/cuevanacli.py>`_
   que permite buscar links y bajar subtitulos de contenidos específicos

.. figure:: local/cache-vignettes/L510xH296/2011-04-09-173503_562x326_scrot-1fb6b.png
   :align: center
   :alt: 
Para qué sirve
~~~~~~~~~~~~~~

Por ejemplo, para bajar la temporada 4 completa de Mad Men, con
subtitulos, se podría hacer esto:

::

    $ cuevanalinks 'mad men' s04 -s > madmen.txt && tucan -d -i madmen.txt

Instalación
~~~~~~~~~~~

Para instalarlo, basta con usar `pip <http://www.pip-installer.org>`_

::

    $ sudo pip install cuevanalinks

O con
`easy\_install <http://packages.python.org/distribute/easy_install.html>`_:

::

    $ sudo easy_install cuevanalinks

O bien, bajar `el
paquete <http://pypi.python.org/pypi/CuevanaLinks#downloads>`_ y
ejecutar :

::

    $ tar xvfz CuevanaLinks-0.1.tar.gz
    $ cd CuevanaLinks-0.1
    $ sudo python setup.py install

Algunas posibilidades de la API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El CLI por ahora sólo expone una parte pequeña de la API, pero hay
varias posibilidades. Por ejemplo:

::

    >>> from cuevanalinks import cuevanaapi
    >>> api = cuevanaapi.CuevanaAPI ()
    >>> house = api.get_show ('house')
    >>> house.plot
    u'El doctor Gregory House, especialista en el tratamiento de enfermedades infecciosas, trabaja en un hospital universitario de Princetown, donde dirige una unidad especial encargada de pacientes afectados por dolencias extrañas y en la que colabora con un selecto grupo de aventajados ayudantes.'
    >>> house7x1 = house.get_episode (7, 1)
    >>> house7x1.title
    'Now What?'
    >>> house7x1.cast 
    ['Hugh Laurie',
     'Lisa Edelstein',
     'Omar Epps',
     'Jesse Spencer',
     'Jennifer Morrison',
     'Robert Sean Leonard',
     'Olivia Wilde',
     'Peter Jacobson']
    >>> house7x1.sources 
    ['http://www.megaupload.com/?d=DM58TA0J',
     'http://www.filesonic.com/file/36841721/?',
     'http://bitshare.com/?f=67z435xm',
     'http://www.filefactory.com/file/caf85b9']
    >>> house7x1.subs
    {'ES': 'http://www.cuevana.tv/download_sub?file=s/sub/7888_ES.srt'}

Lo que falta
~~~~~~~~~~~~

Si bien es lo más prolijito que he hecho, todavía está lejos de ser un
trabajo completo, tanto en funcionalidades como en
`SQA <http://en.wikipedia.org/wiki/Software_Quality_Assurance>`_

Un aspecto esencial es hacer test (perdón Nati Bidart ;-) ), para lo
cual tengo que aprender a usar
`nose <http://code.google.com/p/python-nose/>`_ y
`minimock <http://blog.ianbicking.org/minimock.html>`_.

Respecto a funciones, algo importante es definir cómo resuelve el CLI el
manejo de múltiples resultados para una búsqueda. Actualmente devuelve
el resultado "más relevante" sin anoticiar al usuario de otras opciones.

También falta documentación! Veremos la próxima.

Comentarios, sugerencias, bugs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Todo aporte (ideas, código, etc.) es bienvenido. Si encuentran
problemas,
`reportenlos <https://bitbucket.org/tin_nqn/cuevanalinks/issues>`_.

No estoy seguro cuánto puede durar esto funcionando, ya que depende de
que el funcionamiento del sitio no cambie o yo tenga mucho tiempo y
ganas de andar parchando detrás. Por eso, si hay más interesados y
usuarios, seguramente podremos hacerlo durar más.
