.. link:
.. description:
.. tags: preciosa, ideas
.. date: 2013/06/02 20:54:17
.. title: Hola Preciosa
.. slug: hola-preciosa

Mi propuesta_ sobre una aplicación para teléfonos inteligentes que facilite el relevamiento
de precios y ayude a encontrar mejores ofertas generó muchísimo debate en PyAr_, en la
`lista de Ingeniería`_  y en Twitter_ .

Hubo quienes desmerecieron la idea por "politizada_", otros que me `invitaron a no generar polémica`_ y llevar la discusión a otro lado [1]_, un par que no les gustó porque le quita *"la responsabilidad al gobierno que es el que genera inflación por su irresponsable emisión monetaria"*  y otros que directamente se `ofendieron feo`_ y me dijeron fascista.

.. raw:: html

    <blockquote class="twitter-tweet" data-conversation="none" lang="es"><p>@<a href="https://twitter.com/tin_nqn_">tin_nqn_</a> @<a href="https://twitter.com/damian_avila">damian_avila</a> por dios.eso es programar al gran hermano. Facismo en código</p>&mdash; JuanB. Cabral (@JuanBCabral) <a href="https://twitter.com/JuanBCabral/status/340955059607187457">1 de junio de 2013</a></blockquote>

    <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

Pero a la gran mayoría le pareció buena, de difundió bastante en facebook, muchos aportaron nuevas ideas para mejorarla y otros muchos se entusiasmaron en colaborar.

Así que de eso se trata este post: encauzar todas esas ideas y ganas que se generaron para diseñar e implementar el software. Se me ocurrió el nombre **Preciosa** [2]_, por **"Precios de Argentina"** [3]_, pero se puede cambiar más adelante.

¿Cómo empezamos(,) Preciosa?
----------------------------

Hice una lista de correos (`preciosa-devs@googlegroups.com <https://groups.google.com/forum/?fromgroups#!forum/preciosa-devs>`_.

Están invitados programadores/as, diseñadore/as, periodistas y todos y todas quienes tengan algo para aportar al proyecto. Es el lugar para discutir ideas de diseño, difusión e implementación, avisar de apps parecidas o útiles, etc.

También dí de alta el proyecto en Github: https://github.com/mgaitan/preciosa

Además del repositorio usaremos la Wiki_ para resumir los acuerdos de diseño y la `issue tracker`_ para listar las tareas y funcionalidades a implementar, pedir nuevas, reportar errores, etc.

Este será el proyecto padre y allí pondremos el código de la aplicación "servidor", es decir la que proveerá la API para que las aplicaciones móviles bajen y suban información de precios. Luego de que decidamos más o menos cómo
será esta API podemos crear un proyecto nuevo para cada una de las aplicaciones clientes de las distintas plataformas mobile (la prioridad debería ser Android y Blackberry, ¿no?).

Porque es lo que yo sé programar, porque es fácil aprenderlo y porque satisface (con creces) tecnológicamente el problema, la aplicación servidor la haremos en Django_.

¿Manos a la obra?

.. attention:

    Si sabés programar en python, web o cualquier tecnología mobile; sabes diseñar o maquetar css, o simplemente te gusta la idea, te esperamos en la nueva y preciosa lista_


.. [1] ¿esta actitud no es una "`burbuja de filtros`_", voluntaria? ¿No es *"reducir
       nuestra visión del mundo"* como dice Eli Pariser?
.. [2] Esteban Morales propuso "DeCompras", que es más explícito e internacionalizable
.. [3] o porque me inspiró su belleza_

.. _lista: https://groups.google.com/forum/?fromgroups#!forum/preciosa-devs
.. _Django: http://
.. _issue tracker: https://github.com/mgaitan/preciosa/issues
.. _Wiki: https://github.com/mgaitan/preciosa/wiki
.. _belleza: https://plus.google.com/photos/102449284377784435533/albums/5362561505342208481/5362561730845131554?pid=5362561730845131554&oid=102449284377784435533
.. _burbuja de filtros: http://www.ted.com/talks/lang/es/eli_pariser_beware_online_filter_bubbles.html
.. _propuesta: /posts/mirar-tu-smartphone-para-cuidar.html
.. _PyAr: http://listas.python.org.ar/pipermail/pyar/2013-June/thread.html#24966
.. _lista de Ingeniería: http://www.textosypretextos.com.ar/spip.php?page=recherche&recherche=limando+cantos
.. _Twitter: https://twitter.com/tin_nqn_/status/340839648798580736
.. _politizada: http://listas.python.org.ar/pipermail/pyar/2013-June/024967.html
.. _invitaron a no generar polémica: http://listas.python.org.ar/pipermail/pyar/2013-June/024977.html
.. _ofendieron feo: http://listas.python.org.ar/pipermail/pyar/2013-June/024988.html