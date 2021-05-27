.. title: #NoAlFraudeEnCórdoba. Ayudanos
.. slug: no-al-fraude-en-cordoba-ayudanos
.. date: 2013/10/30 15:17:55


#NoAlFraudeEnCórdoba. Ayudanos!
===============================

.. tip::

    Hay un nuevo artículo relacionado `acá </posts/no-al-fraude-en-cordoba-nuevo-analisis.html>`_

Mi nombre es Martín Gaitán y soy ingeniero  en computación. Quienes me
conocen saben que soy kirchnerista y fui fiscal de Carolina Scotto, pero
antes de eso soy ciudadano y como tal, mi deber cívico es defender la
democracia. En este caso, exigiendo un escrutinio transparente.

El domingo pasado, todas las boca de urna daban a Liliana Olivero,
candidata del Frente de Izquierda y los Trabajadores (FIT), como la 9na
diputada por Córdoba. Ese pronóstico se iba confirmando a lo largo del
escrutinio hasta alrededor de las 23hs, cuando la tendencia empezó a
cambiar en favor del tercer candidato de la UCR, Diego Mestre.

Al ser el margen tan estrecho
(`calculé <http://nbviewer.ipython.org/7206288>`_ que son menos de 1600, 0.06%) el partido de Olivero exige el recuento de los votos y `la justicia electoral se
niega <http://www.lavoz.com.ar/politica/desestiman-pedido-del-fit-para-abrir-todas-las-urnas>`_.

Aún sin el recuento voto a voto, se han encontrado mesas con votos al
FIT mal computados. Algunos ejemplos

-  `Mesa 2669, Cba
   Capital <http://www.resultados.gob.ar/telegramas/04/001/0013J/040010013J2669.htm>`_:
   no se computaron 33 votos del FIT (inferido)
-  `Mesa 611, Cba
   Capita <http://www.resultados.gob.ar/telegramas/04/001/0006E/040010006E0611.htm>`_:
   no se computaron 23 votos del FIT (inferido)
-  `Mesa 1064 <http://t.co/oahdUgFwEu>`_: se computaron 10 en vez de 40
   votos del Frente de Izquierda.

.. TEASER_END


El sistema de publicación de telegramas electorales
(www.resultados.gob.ar) es un gran progreso hacia la transparencia, pero
está muy incompleto. Por ejemplo, no sólo carece de buscador, sino que
no hay una validación entre la cantidad de votos computados (sumatoria
de votos a los partidos, más blancos, nulos y recurridos) con los votos
emitidos/cantidad de sobres que figura en el telgrama.

Más aun, los datos deberian estar no sólo visualizables sino en un
formato abierto para poder procesarlos con otras herramientas.

Cómo soy programador, realicé un simple programa para extraer los datos
de los resultados electorales de Córdoba (aunque bien serviría para
otros distritos), sistematizarlos en una base de datos y hacer una
búsqueda de mesas "sospechosas". Por ejemplo, aquellas en las que el FIT
obtuvo 0 voto (patrón de los 2 primeros ejemplos).

Si bien este proceso es automatizable, determinar cuándo ese dato es
realmente erroneo es mucho más complejo (en parte por la falta de datos
que menciono) y, dada la urgencia, es mejor hacerlo de forma manual,
colaborativamente. Por ello **necesito ayuda** para revisar: por ejemplo, para el primer listado, comparar la cantidad de votos emitios con el total computado.

.. tip::

    El software es libre (bajo licencia GPLv3), está realizado en Python
    y está autocontenido en un documento utilizando el entorno `IPython Notebook <http://ipython.org/notebook.html>`_. El código puede obtenerse `acá <https://gist.github.com/mgaitan/7237956>`_. En nbviewer se puede ver una `versión estática de su ejecución
    en IPython Notebook <http://nbviewer.ipython.org/7237956>`_.

    También se encuentra disponible la `base de datos <http://lab.nqnwebs.com/descargas/db.sqlite>`_.


.. attention::

    Si encontrás telegramas mal cargados o sospechosos, llená este formulario
    (o dejá un comentario al pie del artículo)


----


.. tip::

  Editado, mayo de 2021:

  Ver listados de "mesas sospechosas" en la `versión original del post
  <https://github.com/mgaitan/mgaitan.github.io/blob/b7ac5171018184a5693eda32848ac37fa29832ce/posts/elecciones_cba.rst#mesas-con-m%C3%A1s-de-5-votos-nulos-nuevo-listado>`_.