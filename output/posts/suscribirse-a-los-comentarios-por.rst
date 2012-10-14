Con SPIP 2.0, más precisamente en la revisión
`13407 <http://trac.rezo.net/trac/spip/browser/spip/squelettes-dist/rss_forum_article.html?rev=13407>`_
se agregaron algunos esqueletos al juego de esqueletos estándar.

Unos muy interesantes son los que permiten suscribirse a los
comentarios.

::

    squelettes-dist/rss_forum_article.html
    squelettes-dist/rss_forum_breve.html
    squelettes-dist/rss_forum_rubrique.html
    squelettes-dist/rss_forum_syndic.html
    squelettes-dist/rss_forum_thread.html

Por ejemplo, en el foro de un articulo, podriamos incluir el siguiente
código, antes del bucle de comentarios de un artículo:

::

    [] Suscribite a los comentarios de este artículo 

Un código análogo, llamando al esqueleto correspondiente y pasando el
parámetro correcto, sirve para las breves, las secciones, los artículos
sindicados y los hilos de discusión (en foros con comentarios anidados).
