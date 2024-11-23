.. title: Notas rápidas de una mudanza
.. slug: notas-rapidas-de-una-mudanza
.. date: 2012/10/14 19:23:44
.. tags: nikola, spip, migration tools
.. link: 
.. description:

Hace unos días abría este espacio prometiendo migrar contenidos y 
tratar de que se vea un poco más bonito. 

Este post incluye algunas notas sobre lo que he hecho hasta el momento.

Github ♥ Nikola 
---------------

Este blog que estás leyendo está hospedado en `Github Pages`_ ,
el servicio de hosting gratuito de contenido estático que ofrece Github.

A diferencia de cuando se usa Gh-pages para proyectos, donde se sirve
el contenido del branch *gh-page* del proyecto en cuestión, 
para usar gh-pages por usuario hay que crear
un repo llamado *<username>*.github.com (donde *<username>* es el tuyo)
y lo que sirve en http://<username>.github.com es directamente el branch 
*master* (`referencia <https://help.github.com/articles/user-organization-and-project-pages>`_)

Por este motivo creé otro branch (que sin mucha imaginación denominé
`writing <https://github.com/mgaitan/mgaitan.github.com/tree/writing>`_ )
donde tengo todo el mi "proyecto" hecho con Nikola

Allí escribo, intento mejorar mi theme_, y corro ``nikola build``. 

El branch master es el de deploy y sirve todo lo que haya en la carpeta
``output/`` del branch ``writing``. Para hacer esto_ hay que ir a *master*,
borrar todo y leer desde el árbol del otro branch con ``read-tree`` ::

    git checkout master
    git rm *    # sólo la primera vez
    git read-tree writing:output
    git commit -m 'deploying last build'
    git push

Migrando desde Spip
-------------------

Uno de los motivos que me llevaron a migrar desde Spip_ es que el markup
que usa es *ad hoc* y muy feo. Algo así ::

  {{{ Un intertítulo }}}

  Esto es {{negrita}} y este [mi twitter->http://twitter.com/tin_nqn_]

Hasta ahí no se ve tan mal, pero es muy limitado cuando se trata de mostrar
código, necesario en todo blog mas o menos técnico.

Para migrar esquivé la idea de convertir el markup de spip y opté por un
scrapping, limpieza y conversión a restructuredText usando el mágico
Pandoc_ (y la ayuda de PyQuery)

El script que hice está 
`acá <https://github.com/mgaitan/mgaitan.github.com/blob/writing/tools/spip_converter.py>`_
. No es perfecto, pero está lo importante: contenidos, imágenes, adjuntos,
convertido a restructuredText bastante decente que mejoraré poco a poco
a mano.

Estilos
--------

Es mentira que a los ñoños no nos gustan las cosas (los blogs, entre otras)
que se ven bonitos. Sucede, en realidad, que la mayoría de las veces no
venimos con *esa* habilidad y el esfuerzo que nos implica intentarlo
preferimos ponerlo en otra cosa. No gusta, pero no es lo más importante.

No obstante, yo quiero que este espacio sea lindo y legible. Y como hay
muchos otros ñoños con sitios lindos y legibles que son tan amables de
compartir sus estilos (y existe bootstrap_, claro) voy a ir intentándolo,
incrementalmente. 

Por ahora tomé ideas y CSS de stevelosh.com_ [1]_ y de la documentación
de Flask_ [2]_ basado en el theme *Readable* de bootswatch.com_

Disqus
-------

El blog viejo usaba Disqus_, con un plugin_ que hice hace algun tiempo.
Para migrar los comentarios utilicé el método de subir un CSV con
el formato que genera el mismo script de migración:: 

    URL_POST_X_OLD, URL_POST_X_NEW
    URL_POST_Y_OLD, URL_POST_Y_NEW

En cuestión de minutos los (pocos) comentarios estaban migrados.

Redirección
------------

Como mantuve el slug de los viejos artículos, una redirección 301
via .htaccess redirige del viejo blog al nuevo::

    # nqnwebs.com blog rules
    RewriteCond %{HTTP_HOST} ^nqnwebs [nc]
    RewriteRule ^blog[/]?$ http://mgaitan.github.com/ [R=301]
    RewriteRule ^blog/article/(.*)$ http://mgaitan.github.com/posts/$1.html [R=301]



¿Cómo se va viendo? 



.. [1] https://bitbucket.org/sjl/stevelosh/src/6432040d5154/LICENSE?at=default
.. [2] https://github.com/mitsuhiko/flask-sphinx-themes/blob/master/LICENSE

.. _Disqus: http://disqus.com
.. _plugin: http://mgaitan.github.com/posts/disqus-para-spip.html
.. _Github Pages: http://pages.github.com
.. _bootswatch.com: http://bootswatch.com/
.. _Flask: http://flask.pocoo.org/docs/
.. _stevelosh.com: http://stevelosh.com
.. _Pandoc: http://johnmacfarlane.net/pandoc
.. _esto: http://stackoverflow.com/a/10591668
.. _theme: https://github.com/mgaitan/mgaitan.github.com/tree/writing/themes/custom
.. _Spip: http://www.spip.net
.. _bootstrap: http://twitter.github.com/bootstrap 
.. _PyQuery: http://pypi.python.org/pypi/pyquery



