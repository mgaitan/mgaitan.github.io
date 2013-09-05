.. link:
.. description:
.. tags:
.. date: 2013/09/04 20:38:44
.. title: Un procesador de reStructuredText
.. slug: un-procesador-de-restructuredtext

Siempre me gustó escribir_. Pero, desde que recuerdo, casi siempre lo hice en un teclado de computadora. Salvo garabatos_ cuando tengo que pensar algo difícil o cuando me aburro en una reunión/clase, casi no escribo en papel.

En la compu escribo mucho y, sin embargo, tampoco uso procesadores de texto, ni siquiera los open source: aunque "lo que se ve" es "lo que se obtiene", (me)sucede demasiado seguido que lo que veo no es lo que quiero.

Por ese motivo (y porque casi siempre sigo los consejos de `Roberto Alsina <http://ralsina.com.ar/>`_) escribo texto plano, usando el formato reStructuredText_. Y así escribo todo: este blog, las charlas_, mi `tesis de grado`_, la documentación de `mis proyectos`_ , notas rápidas en una `wiki`_, `cartas de amor`_, etc.

reST es un lenguaje de marcado sencillo y potente, que a diferencia de LaTex fue pensado para que el contenido sea legible en formato fuente, es decir, en texto plano. Escribiendo con un simple **editor** de texto nos concentramos en lo importante (el contenido) y no en luchar contra el formato de la tabla, la sangría o el tipo de letra de un encabezado. Además, es más útil cuando se usa con un sistema de control de versiones, porque se pueden visualizar los cambios claramente.

Si bien su sintaxis es algo más verborrágica [1]_ que la de Markdown_ (el markup liviano más difundido en la web), reST es muchísimo más potente y orientado a tener múltiples formatos de salida (html, ebooks, pdf, etc.). De hecho se han escrito libros y toda la `documentación oficial de Python`_ de esta manera.

Pero tampoco hace falta ser un asceta: si un software nos puede ayudar a escribir y a formatear lo escrito mejor y más fácilmente, ¿por qué no usarlo?

Eso hace `rst-completions`_ el plugin para SublimeText_ del que soy el principal desarrollador [2]_. Acá una demo de los que se puede hacer.


.. raw:: html

    <iframe width="640" height="360" src="//www.youtube.com/embed/otM_tjIi_vY" frameborder="0" allowfullscreen></iframe>

Por ahora tiene:

- Atajos de directivas y formatos: links, admoniciones, código, etc.
- Encabezados: autocompletado, navegación, cambio de nivel, folding
- Tablas: autoformato, ajuste con ancho fijo o variable, fusión de celdas lindantes
- Notas al pie: inserción automática al final del documento, salto entre referencia y nota,
- Listas: detección automática del patrón, autonumeración.
- Output: generación de html, pdf, etc. (usando pandoc, rst2pdf o rst2html)

Lo hice para SublimeText porque es el editor que uso y, sobre todo, porque su API de plugins está basada en Python [2]_. Pero tengo la idea de separarlo como una biblioteca agnóstica, permitiendo hacer plugins como wrappers delgados para cualquier editor.

¿Qué opinás? ¿Te sumás a colaborar?


.. note::

    ¿Por qué está en el github de `otro tipo <https://github.com/dbousamra>`_? Simplemente porque él lo empezó. Luego me dió permisos de escritura y yo `me cebé un poco <https://github.com/dbousamra/sublime-rst-completion/contributors>`_.


.. _charlas: http://mgaitan.github.io/charlas.html
.. _SublimeText: https://www.sublimetext.com/
.. _rst-completions: https://github.com/dbousamra/sublime-rst-completion
.. _documentación oficial de Python: http://docs.python.org/
.. _escribir: http://textosypretextos.com.ar
.. _garabatos: http://es.wikipedia.org/wiki/Garabato_%28dibujo%29
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _wiki: http://waliki.nqnwebs.com
.. _tesis de grado: http://gpec2010.googlecode.com/svn/trunk/docs/_build/html/index.html
.. _mis proyectos: http://github.com/mgaitan/
.. _Markdown: http://en.wikipedia.org/wiki/Markdown
.. _cartas de amor: http://www.textosypretextos.com.ar/Cartas-de-amor-efimero-


.. [1] En las funcionalidades básicas
       `son muy parecidos <https://gist.github.com/dupuy/1855764>`_

.. [2] Aunque su documentación apesta