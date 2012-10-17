A lo largo de esta vida he amado, he llorado y reído, me han salido
canas y dí algunas charlas y talleres.

Me gusta la docencia, probable herencia de `una
grosa <blog/article/grosa>`_. Me gusta compartir lo que sé, instarme a
aprender para compartir con otros y aprender cuando enseño. Educación
horizontal, educación popular.

+-----------------------------------------+
| `|image1| </images/chino-garce.jpg>`_   |
+-----------------------------------------+

El viernes pasado, en la
`PyConAr <blog/article/pyconar-2010-el-orgullo-de>`_ debía dar una de
las primeras charlas, *`IPython, la interactividad al
poder <http://ar.pycon.org/2010/conference/schedule/event/91/>`_* .
Entró al cronograma en una segunda tanda de selección, con más sorpresa
que el chino Garcé a Sudáfrica 2010. El problema es que para cuando me
invitaron yo ya había descartado mi participación en PyCon y aceptado
dar `una en mi facu <blog/article/charla-python-a-los-bifes>`_, también
sobre Python pero otra. Ergo, ¡tenía que preparar 2 charlas!

En el medio, solucionar horribles bugs de
`GPEC <http://code.google.com/p/gpec2010/>`_ para la release de la
semana que viene, un casamiento a 1500 km de mi casa (por suerte no
mío), aprender a `diseñar
hardware <http://article.gmane.org/gmane.comp.python.myhdl/1536/>`_,
malabarear estres con las `remeras de
PyAr <http://python.org.ar/pyar/RemerasV3>`_ y terminar el
`poster <blog/article/gpec-2010-el-poster>`_ que se me ocurrió
presentar.

El contexto no favoreció a preparar la charla con anticipación. De
hecho, pude hacerme lugar el jueves de 0:05 a 4 am para leer el manual y
escribir lo poco que escribí. Mucha audacia teniendo en cuenta que
algunas de las cosas que quería (de alguna manera debía) mostrar, no las
uso/aba realmente (eso de *instarme a aprender* es posta) y más aun,
considerando que las presentaciones con "demo" incluída son una fiesta
orgiástica para `Murphy <http://en.wikipedia.org/wiki/Murphy's_law>`_

Por eso, para descompimir la ansiedad y la casi certeza de que algo
podía salir mal, lo primero que hice fue echarle la culpa a John Lenton,
que fue el que
`incitó <http://permalink.gmane.org/gmane.org.user-groups.python.argentina/38170>`_
a la vergüenza. La charla comienza con este disclaimer:

::

    Disclaimer
    -----------------
    
    Todo lo que sigue es culpa de John Lenton:
    
        
        2010/7/28 John Rowland Lenton :
        > Hola!
        >
        > Estamos organizando PyConAr. Viste? La conferencia de Python en
        > Argentina (...) te vas a dar cuenta cuando
        > estés acá en Córdoba que podrías haber presentado tu charla, y te vas
        > a sentir muy zonzo.

Para colmo de riesgos, descubrí algo que supongo que es un bug (TODO:
check and report this) con la utilidad ``Demo`` de IPython que usé, en
la versión estable (0.10) y la que está en desarrollo (0.11). Por eso
tuve que hacer un downgrade a la 0.9, que no tiene algunas cosas
interesantes que quería mostrar (%paste, por ejemplo).

Por supuesto, Murphy vino y se divirtió, pero no se burló
sarcasticamente. Hasta que alguien me muestre un video y me ponga rojo
de vergüenza voy a quedarme con la idea de que no estuvo tan mal. Alguno
seguro no descrubrió nada nuevo, pero `otros parecieron
satisfechos <http://twitter.com/#!/martinvol/status/27447006335>`_ y
probablemente jueguen un ratito con IPython.

Archivos / Descarga
~~~~~~~~~~~~~~~~~~~

Como es una presentación interactiva, no hay "diapositivas". O sí, pero
es un módulo python.

Todo lo que usé (con nimios retoques respecto a lo mostrado el viernes)
se puede bajar (o forkear) de
`GitHub <http://github.com/nqnwebs/IPython-interactive-talk>`_ .

::

    git clone git@github.com:nqnwebs/IPython-interactive-talk.git

O desde este Zip

.. |image0| image:: /images/chino-garce-55977-54acc.jpg
.. |image1| image:: /images/chino-garce-55977-54acc.jpg
