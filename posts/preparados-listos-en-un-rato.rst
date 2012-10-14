Hace aproximadamente dos meses que estoy trabajando en lo que será mi
proyecto final, para recibir el título de `ingeniero en
computación <http://computacion.efn.uncor.edu>`_.

El proyecto es una aplicación de uso "científico y académico"
implementada en Python que sirve para obtener diagramas de equilibro
termodinámico entre fases fluidas de sistemas binarios. Toda la batahola
está en `este repo <http://code.google.com/p/gpec2010>`_.

En concreto, el proyecto se circunscribe a la generación y [análisis
sintáctico] de archivos de texto con el que la aplicación se comunica
con los programas que implementan los algoritmos de cálculo, que están
implementados en Fortran, y son, literalmente, unas cajas negras.
[`1 </blog/article/preparados-listos-en-un-rato#nb1>`_]. Se procesan
esos archivos para obtener arrays con los que se plotean las distintas
curvas.

Utilizo principalmente `wxPython <http://wxpython.org>`_,
`Matplotlib <http://matplotlib.sourceforge.net>`_ y
`Numpy <http://numpy.sourceforge.net>`_. Vale destacar, ya que mucho de
un trabajo final es documentación, que escribo en
`restructuredText <http://docutils.sourceforge.net/rst.html>`_,
renderizando con `Sphinx <http://sphinx.pocoo.org/>`_ y el genial
`rst2pdf <http://code.google.com/p/rst2pdf/>`_
