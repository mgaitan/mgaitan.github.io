.. title: Deploy de Django con Circus, Chausette y Nginx
.. slug: deploy-de-django-con-circus-chausette-nginx
.. date: 11/06/14 17:45:13 UTC-03:00
.. tags: draft
.. link:
.. description:
.. type: text

Aunque hay un pequeño de mito al respecto, poner en producción una aplicación web hecha en Django no es tan complejo. Esa facilidad se debe a la estandarización de la pasarela WSGI_, que define cómo se comunica (o se debería comunicar) una "app" (sea hecha con un framework o no) con un servidor web.

Si bien Nginx, el `servidor web que está desplazando a Apache como el más popular <http://w3techs.com/blog/entry/nginx_just_became_the_most_used_web_server_among_the_top_1000_websites>`_ tiene `un módulo <http://wiki.nginx.org/NgxWSGIModule>`_ que implementa el estándar WSGI de manera nativa, la arquitectura más típica es utilizarlo como `proxy reverso <http://en.wikipedia.org/wiki/Reverse_proxy>`_, conectado a un servidor WSGI como Gunicorn_ que interactua con la aplicación web (posiblemente a través de multiples instancias o *workers*). Como queremos que nuestra app funcione permanentemente, el proceso WSGI y otros que sean necesarios (por ejemplo Redis) se demonizan de manera que sepan restaurarse automáticamente si mueren y sea posible monitorearlos: para eso suele usarse supervisor_.

.. figure:: https://raw.githubusercontent.com/mozilla-services/circus/dff6cf3a348fecc0b58bd08cae91b1508aed14c2/docs/source/classical-stack.png

    La arquitectura de deployment más común para una aplicación web Python

Si bien esta arquitectura está bastamente probada, hay una opción mejor.

El circo y el soquete
---------------------

Circus_ y Chaussette_ son proyectos desarrollados por `Tarek Ziadé <http://ziade.org/>`_ y el equipo de `Mozilla Sevices <https://blog.mozilla.org/services/>`_.

.. tip::

    Tarek es un pythonista francés, core committer de Python y muchos proyectos relacionados. Recibió el `reconocimiento de la PSF <https://www.python.org/community/awards/psf-awards/#april-2011>`_ por sus aportes, y es autor del gran libro `Expert Python Programming <http://www.packtpub.com/expert-python-programming/book>`_

Una arquitectura de producción análoga a la descripta arriba, pero basada en Circus, se ve así:

.. image:: https://github.com/mozilla-services/circus/blob/dff6cf3a348fecc0b58bd08cae91b1508aed14c2/docs/source/circus-stack.png

Circus maneja procesos demonizados como Supervisor, pero además puede bindear sockets y manejarlos de la misma manera. Este desacople de la gesti
ón de sockets del webserver WSGI permite muchas posibilidades, tanto en la gestión como en la escalabilidad de la arquitectura.

A diferencia de Supervisor que se basa en el protocolo XML-RPC para inspeccionar los procesos que controla, Circus utiliza un canal pub/sub basado en el mucho más moderno ZeroMQ_ (lo mismo que usa IPython notebook) que permite un monitoreo realtime y una `API de plugins <https://circus.readthedocs.org/en/0.11.1/for-devs/#extending-circus>`_ mucho más simple. Además, Circus funciona en Python 3.







.. _zeromq: http://zeromq.org/
.. _Circus: http://circus.readthedocs.org/
.. _Chaussette: http://chaussette.readthedocs.org/
.. _supervisor: http://supervisord.org/
.. _Gunicorn: http://gunicorn.org/
.. _WSGI: http://legacy.python.org/dev/peps/pep-3333/