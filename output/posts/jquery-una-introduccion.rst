.. link:
.. description:
.. tags:
.. date: 2012/11/02 16:20:21
.. title: Jquery, una introducción
.. slug: jquery-una-introduccion

jQuery, una librería javascript ligera y sumamente útil, desarrollada
por el talentoso programador `John Resig <http://ejohn.com>`_.

Como se explica en el `sitio web <http://jquery.com/>`_:

    jQuery es una biblioteca javascript ligera y concisa que simplifica
    como atraviesas tus documentos HTML, manejas eventos, realizas
    animaciones, y agregas interacción Ajax a tus páginas web. **jQuery
    está diseñada para cambiar la manera en que escribes JavaScript**

¿Necesitamos otra biblioteca?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El `Toolkit Dojo <http://dojotoolkit.org/>`_ está maduro e incluye hasta
el los hielos del whisky. Es ampliamente popular y muchas interfaces
`UI <http://es.wikipedia.org/wiki/Interfaz_de_usuario>`_ fueron
construidas sobre este toolkit, incluyendo
`script.aculo.us <http://script.aculo.us>`_,
`Rico <http://openrico.org>`_, y otros. Por supuesto, no podemos dejar
afuera a `mootools <http://mootools.net>`_. Su biblioteca UI,
`moo.fx <http://moofx.mad4milk.net/>`_, puede apoyarse sobre Prototype
si lo deseas. Tambiñen está `Y!UI the Yahoo! User Interface
library <developer.yahoo.com/yui/>`_. Y tenemos
`ExtJs <http://extjs.com>`_, un robusto framework de interfaz que se
basa en Y!UI, Prototype, o jQuery.

jQuery
~~~~~~

Lo que nos trae a... jQuery. Sí, otro framework JavaScript. jQuery, sin
embargo, es a mi criterio el más rápido y elegante del montón. Soporta
CSS3, detección del navegador, encadenamiento de métodos, plugins, Ajax,
selectores flexibles, y efectos UI basicos. Todo en menos de 30Kb.

Pues bien, engolosinemos los ojos un poco. Hacé `click
acá </blog/jQuery-una-introduccion#>`_ para ver lo que jQuery puede
hacer con un par de líneas de código.

Wow! Jquery en acción. ¿Lo ves?
Ese efecto se logra con este sencillo código:

::

    $("a.intro").click( function() {
        $("div.introtarget").toggle(100);return false;

