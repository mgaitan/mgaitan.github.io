El viernes presenté el draft para la revisión final de mi `proyecto
integrador <blog/article/preparados-listos-en-un-rato>`_ (a.k.a. tesis).
Tentativamente (¡a esta altura y todavía no es seguro!) se titula
*"Software para graficación de digramas termodinámicos"* y se puede
chusmear
`acá <http://gpec2010.googlecode.com/svn/trunk/docs/_build/html/index.html>`_.

Como verán, lo hice con `Sphinx <http://sphinx.pocoo.org/>`_, generando
LaTeX y compilando luego a PDF. Estoy más que satisfecho del resultado.

Sin embargo, un problema de Sphinx/Docsutils (y esto viene a ser el
verdadero tema de este post) es es que si bien están llenos de pulentez
y se la bancan mil, no están "pensados" para escribir tesis sino
documentación/manuales de software. Esto se nota, sobre todo, en la
subutilización de recursos de LaTeX a los que "no se accede" desde
restructuredText.

El caso paradigmático es la referenciación de figuras. En las versiones
"imprimibles" que se generan con LaTeX suele pasar que una figura no
quepa en una página y el compilador, al medir y darse cuenta, la manda a
una página siguiente. Esto hace indispensable ser preciso en la
referencia ya que un mensaje como *"en la siguiente figura"* puede estar
seguido de toda una página sin figuras.

Para hacer una referenciar una figura en Sphinx hay que declarar un
target

::

    .. _ok:
    
    .. figure:: ok.png
    
       Una imágen

y luego usar el rol ``:ref:``. Por ejemplo:

::

    Referenciando la figura :ref:`ok` se evidencia el problema.

El problema es que el LaTeX generado por Sphinx no hace exáctamente una
referencia a la figura, sino un hipervínculo (hyperref). Como texto de
ese hipevinculo usa el epígrafe de la figura, lo cual es horrible e
inútil para textos cientificos/académicos. El issue, `está reportado
hace más de 2
años <https://bitbucket.org/birkenfeld/sphinx/issue/76/proper-references-to-figures-code-tables>`_.

Con el estilo gronchohacker que se me está volviendo costumbre, hice
unos cambiecitos para que funcaran las referencias como tienen que ser,
por número. La directiva es particularmente fácil en LaTeX: ``~\ref{}``.
En concreto, el "gronchohackeo" se trata de cambiar
``{\hyperref[label]{\emph{epigrafe}}}`` por ``~\ref{label}``.

Para garantizar compatibilidad con los que les gusta que el título de la
referencia sea el epígrafe y no el número, lo hice opcional: toda
referencia a un destino con sufijo ``-num`` usa una referencia númerica
en vez de un hipervinculo con texto.

Acá el patch (para la versión 1.1 —en desarrollo— )

+-----------------------------------------------+
| `|image1| </downloads/sphinx-issue76.txt>`_   |
+-----------------------------------------------+
| Diff Parche para el Issue #76 de Sphinx       |
+-----------------------------------------------+

Y acá un ejemplo del problema y la gronchosolución

+---------------------------------------+
| `|image3| </downloads/prueba.pdf>`_   |
+---------------------------------------+

El código del ejemplo es este:

::

    Ejemplo
    *******
    
    Referenciando la figura :ref:`ok` se evidencia el problema. Aplicando mi 
    rústico parche en cambio, se puede referenciar a la Figura :ref:`ok-num`.
    
    .. _ok:
    
    .. figure:: ok.png
    
       Una imágen
    
    .. _ok-num:
    
    .. figure:: ok.png
    

.. |image0| image:: /images/txt-56069.png
.. |image1| image:: /images/txt-56069.png
.. |image2| image:: /images/pdf-eb697.png
.. |image3| image:: /images/pdf-eb697.png
