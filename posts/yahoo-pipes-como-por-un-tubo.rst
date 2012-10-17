`Yahoo! Pipes <http://pipes.yahoo.com>`_ es una una herramienta web
interactiva para agregar y manipular feeds RSS (y otras fuentes de
datos) a nuestro antojo de forma sencilla y asequible para cualquiera.

Es un entorno de programación visual online. La programación visual es
común para los ingenieros
(`Simulink <http://en.wikipedia.org/wiki/Simulink>`_ o
`LabVIEW <http://es.wikipedia.org/wiki/LabVIEW>`_) y también para los
viejos gamers (el glorioso `The incredible
Machine <http://en.wikipedia.org/wiki/The_Incredible_Machine>`_.

El concepto es simple: se conectan distintos módulos ("tubos", con una o
más salidas y entradas) según las necesidades, y se va probando el
resultado en una salida final.

En Y! Pipes, luego de toda nuestra manipulación, el resultado es un feed
personalizado que contiene únicamente lo que se quiera tener, por
ejemplo el resultado de mezclar y flitrar dos o más fuentes de
información.

Aplicandolo a SPIP
~~~~~~~~~~~~~~~~~~

Frecuentemente queremos ofrecer un canal RSS que provea tanto las breves
como los artículos. SPIP maneja estos objetos independientemente y es
muy dificil hacer un esqueleto que los mezcle (hay que trabajar con
pilas en PHP). Con Yahoo! Pipes es tan sencillo como mezclar los dos (o
más) feeds.

Esto lo hice en el sitio `Agrupación
Mazamorra <http://www.agrupacionmazamorra.com.ar>`_:

.. figure:: local/cache-vignettes/L510xH321/Pantallazo-90218.png
   :align: center
   :alt: 
El resultado puede verse (y clonarse) `desde
aquí <http://pipes.yahoo.com/mazamorra/rss_todo>`_

Más ejemplos
~~~~~~~~~~~~

Pero mezclar feeds no es la única posibilidad. De hecho, Pipes es tan
potente que permite obtener datos parseando un sitio web que no tenga un
canal RSS o Atom disponible (pero eso es un uso muy avanzado y lo
dejamos para otra oportunidad).

Un caso que sí está al alcance de esta breve introducción es filtrar el
contenido de un feed. Doy mi ejemplo en uso: me gusta leer a `Hernán
Casciari <http://nqnwebs.com>`_ que además de su blog, escribe una
columna en el diario argentino La Nación. Es un diario asquerosamente
oligarca y de derecha (¿redundante?) así que prefieron no leer nada más
que a este autor,

Fácil: Busco el feed de la sección donde se publican sus columnas,
filtro con la palabra clave ’Casciari’, y me libro de todo lo que no
quiero. `Aquí el resultado <http://pipes.yahoo.com/mazamorra/casciari>`_

.. figure:: local/cache-vignettes/L465xH360/pipes2-4a406.png
   :align: center
   :alt: 
Ejemplo en video
~~~~~~~~~~~~~~~~

Un screencast de `otro blog más <http://obm.corcoles.net>`_

    Un cierto blog no ofrece los RSS filtrados por categorías. O por
    autores. O por ‘tags’. O queremos el RSS de un sitio, eliminando,
    por ejemplo, todas las entradas que hablen de petanca o del chucho
    del autor. Vamos, que nos gustaría filtrar el RSS de acuerdo con
    algún criterio propio. Para eso (y para bastantes más cosas, pero
    centrémonos en esto) sirve Yahoo! Pipes. Para los interesados, un
    pequeño ’screencast’ que explica cómo recuperar las categorías (la
    de desarrollo web, en particular) que se ha cargado Feedburner…


