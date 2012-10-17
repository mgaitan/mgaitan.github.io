.. important:: 

	El pipe tiene un problema con las fechas y quedó deactualizado
	cuando cambió en el html de G+. En su defecto hice este pequeño
	`scrapper <https://gist.github.com/2886591>`_ que es lo que uso
	en `Textos y Pretextos <http://www.textospretextos.com.ar>`_

Desde hace muchísimo tengo en `mi otro
blog <http://www.textospretextos.com.ar>`_ una sección que se llama *"De
por ahí, cosas que me parecieron interesantes"*. Es un feed de links a
contenidos de toda índole (política, literatura, cine, fotografía,
deportes, programación: intereses anchos) con un brevisimo extracto como
descripción que fui alimentando de diversas formas a lo largo del
tiempo: usé
`delicious <http://delicious.com/nqnwebs,%20use%20%20[esto%20%20-%3Ehttp://sourceforge.net/projects/linkwalla/>`_,
usé mi
`twitter <http://twitter.com/nqnwebs).%20Pero%20cuando%20[Google%20Reader-%3Ehttp://reader.google.com>`_
incorporó la opción de "Compartir" se convirtió en la manera por
defecto: si algo me gustaba, un click en compartir y listo. Eso permitia
que otros usuarios de Reader que me "seguian" pudieran ver mis posts
compartidos pero a la vez generaba un feed rss que alimentaba la sección
de mi blog.

Con la aparición de Google+ aquella simple y muy usada funcionalidad se
vió desplazada por el botón "+1" y por un "compartir" engañoso que sólo
permite compartir en Google+

Para colmo, cuando uno hace "+1" en algun contenido (dentro de Google
Reader o en cualquier lado donde esté el botón) se lista en una `página
publica <https://plus.google.com/102449284377784435533/plusones/p/pub>`_
pero que **no tiene feed RSS**! . Larry Page,
(`doblemente <https://twitter.com/#!/nqnwebs/status/154772127139102720>`_)
te odio.

Frustración colectiva
~~~~~~~~~~~~~~~~~~~~~

La bronca por los cambios en Reader no es sólo mia, sino que generó una
`petición <https://docs.google.com/spreadsheet/viewform?hl=en_US&formkey=dE16SFVla3JFZ1lwTkxGRWN2SkZtb2c6MA#gid=0>`_
firmada por más de
`13000 <http://www.bdkeller.com/2011/10/save-google-reader/>`_ usuarios
que manifiestan que "algunos ven estos cambios como un intento errado
para forzarnos a usar Google Plus, pero nosotros amamos la utilidad,
simplicidad y funcionalidades sociales limitadas que ofrece Google
Reader".

Mientras tanto, muchos
(`1 <http://www.theatlanticwire.com/technology/2011/10/how-survive-switch-google-reader-google/44069/>`_,
`2 <https://github.com/jtwebman/GooglePlusToRSSFeed>`_,
`3 <http://plus-one-feed-generator.appspot.com/>`_) intentan parchar el
atropello.

Mi solución
~~~~~~~~~~~

"¿Así que no me dejás compartir donde yo quiera, el algoritmo de tu
madre!?" vociferé, y no sin premeditación agarré `Yahoo!
Pipes <blog/article/yahoo-pipes-como-por-un-tubo>`_ (una genialidad, hay
que decirlo) para scrappearlos a puro golpe de mouse y sin salir del
navegador. El resultado fue `este
pipe <http://pipes.yahoo.com/pipes/pipe.info?_id=770fc166fd07a0f6e67fe63f513b05dc>`_
del que se puede obtener, por ejemplo, un `feed RSS 2.0 de mis
+1s <http://pipes.yahoo.com/pipes/pipe.run?_id=770fc166fd07a0f6e67fe63f513b05dc&_render=rss&google_plus_id=102449284377784435533>`_
. Podés obtener el feed de otros usuarios así:

``http://pipes.yahoo.com/pipes/pipe.run?_id=770fc166fd07a0f6e67fe63f513b05dc&_render=rss&google_plus_id=[GOOGLE_PLUS_ID] ``
donde ``[GOOGLE_PLUS_ID]`` es el numero de identificación del usuario en
cuestión.

.. figure:: local/cache-vignettes/L510xH139/google-plus-user-profile-id-f8dfc.png
   :align: center
   :alt: 

