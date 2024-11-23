.. title: Deploy de Django con Circus, Chaussette y Nginx
.. slug: deploy-de-django-con-circus-chaussette-nginx
.. date: 06/12/14 12:45:13 UTC-03:00
.. tags: python, devop, tutorial, django, circus
.. link:
.. description:
.. type: text

Aunque hay un pequeño mito al respecto, poner en producción una aplicación web hecha en Python no es tan complejo. Esa facilidad se debe a la estandarización de la pasarela WSGI_, que define cómo se comunica (o se debería comunicar) una "app" (sea hecha con un framework o no) con un servidor web.

.. TEASER_END

Si bien Nginx, el servidor web que está `desplazando a Apache como el más popular <http://w3techs.com/blog/entry/nginx_just_became_the_most_used_web_server_among_the_top_1000_websites>`_ tiene `un módulo <http://wiki.nginx.org/NgxWSGIModule>`_ que implementa el estándar WSGI de manera nativa, la arquitectura más típica es utilizarlo como `proxy reverso <http://en.wikipedia.org/wiki/Reverse_proxy>`_, conectado a un servidor WSGI especializado como Gunicorn_ que interactua con la aplicación web (posiblemente a través de multiples instancias o *workers*). Como queremos que nuestra app funcione permanentemente, el proceso WSGI y otros que sean necesarios (por ejemplo Redis) se demonizan de manera que sepan restaurarse automáticamente si mueren y sea posible monitorearlos: para eso suele usarse supervisor_.

.. figure:: https://raw.githubusercontent.com/mozilla-services/circus/dff6cf3a348fecc0b58bd08cae91b1508aed14c2/docs/source/classical-stack.png

    La arquitectura de deployment más común para una aplicación web Python

Si bien esta arquitectura está bastamente probada, hay una opción mejor.

.. image:: https://circus.readthedocs.org/en/0.11.1/_images/circus-medium.png
   :align: center

El circo y el soquete
---------------------

Circus_ y Chaussette_ son proyectos desarrollados por `Tarek Ziadé <http://ziade.org/>`_ y el equipo de `Mozilla Sevices <https://blog.mozilla.org/services/>`_.

.. tip::

    Tarek es un pythonista francés, core committer de Python y muchos proyectos relacionados. Recibió el `reconocimiento de la PSF <https://www.python.org/community/awards/psf-awards/#april-2011>`_ por sus aportes y es autor del gran libro `Expert Python Programming <http://www.packtpub.com/expert-python-programming/book>`_

Una arquitectura de producción análoga a la descripta arriba, pero basada en Circus, se ve así:

.. image:: https://raw.githubusercontent.com/mozilla-services/circus/dff6cf3a348fecc0b58bd08cae91b1508aed14c2/docs/source/circus-stack.png
   :align: center

Circus maneja procesos demonizados igual que Supervisor, pero además puede bindear **sockets** y manejarlos de la misma manera. Este desacople de la gestión de sockets del webserver WSGI permite muchas posibilidades, tanto en la gestión como en la escalabilidad de la arquitectura.

La capa WSGI en este esquema la aporta Chaussette, que tiene la particularidad que, en vez de abrir un socket nuevo, utiliza el que Circus abrió (y controla) para el worker. Además, aunque trae una implementación de WSGI *built-in*, `puede usar muchos backends <http://chaussette.readthedocs.org/en/latest/index.html#backends>`_ más eficientes o con características particulares como `meinheld <http://meinheld.org/>`_, `gevent <http://www.gevent.org/>`_, `gevent-socketio <http://gevent-socketio.readthedocs.org/en/latest/>`_, entre muchos otros.

A diferencia de Supervisor que se basa en el protocolo XML-RPC para inspeccionar los procesos que controla, Circus utiliza un canal pub/sub basado en el mucho más moderno ZeroMQ_ (lo mismo que usa IPython Notebook) que permite un monitoreo realtime y una `API de plugins <https://circus.readthedocs.org/en/0.11.1/for-devs/#extending-circus>`_ mucho más simple. Otra diferencia, nada menor, es que **Circus funciona con Python 2 o 3** (supervisor no es compatible con Python 3).

Y de yapa: Circus se puede usar como una `biblioteca de muy alto nivel <https://circus.readthedocs.org/en/0.11.1/for-devs/library/>`_  para la gestión no bloqueante de procesos. Se puede pensar con un wrapper de ``subprocess`` y/o ``multiprocess``, que aporta información de monitoreo y estadísticas, control de flujo, una `capa de señales (hooks) <https://circus.readthedocs.org/en/0.11.1/for-devs/writing-hooks/>`_ muy completa y más.

Desplegando Django
------------------

Para ejemplificar, voy utilizar un proyecto Django que estoy desarrollando (muy lentamente): nikolahub_.

Circus se configura con un archivo con formato ``.ini``. El mio, que bauticé ``circus.ini`` quedó así:

.. code-block:: ini

    [circus]
    check_delay = 5
    endpoint = tcp://127.0.0.1:5555
    pubsub_endpoint = tcp://127.0.0.1:5556
    stats_endpoint = tcp://127.0.0.1:5557

    [socket:nikolahub]
    host = 127.0.0.1
    port = 8080

    [watcher:nikolahub]
    cmd = /virtualenvs/nikolahub/bin/chaussette --fd $(circus.sockets.nikolahub) nikolahub.wsgi.application
    use_sockets = True
    numprocesses = 3

    [env:nikolahub]
    PYTHONPATH = /projects/nikolahub

La sección ``watcher`` indica lanza el comando a controlar, en este caso levantando 3 workers de la aplicación -django.  Notar que como tengo instalado Chaussette dentro del virtualenv, uso el path absoluto al ejecutable. El fragmento ``--fd $(circus.sockets.nikolahub)`` se expande implícitamente asignando el pid que obtuvo el fork (el proceso hijo) de circus.

Si quisieramos usar otro servidor web, sólo hay que indicar cual con el parámetro ``--backend`` Por ejemplo:

.. code-block:: ini

    cmd = /virtualenvs/nikolahub/bin/chaussette --backend gevent --fd $(circus.sockets.nikolahub) nikolahub.wsgi.application

Podemos probar si todo funciona:

.. code-block:: bash

    (nikolahub)tin@morochita:$ circusd circus.ini
    2014-06-12 04:36:16 circus[1141] [INFO] Starting master on pid 1141
    2014-06-12 04:36:16 circus[1141] [INFO] sockets started
    2014-06-12 04:36:16 circus[1141] [INFO] Arbiter now waiting for commands
    2014-06-12 04:36:16 circus[1141] [INFO] nikolahub started
    2014-06-12 04:36:16 circus[1141] [INFO] circusd-stats started
    2014-06-12 04:36:17 circus[1150] [INFO] Starting the stats streamer
    2014-06-12 04:36:17 [1149] [INFO] Application is <django.core.handlers.wsgi.WSGIHandler object at 0xa06f60c>
    2014-06-12 04:36:17 [1149] [INFO] Serving on fd://5
    2014-06-12 04:36:17 [1149] [INFO] Using <class chaussette.backend._wsgiref.ChaussetteServer at 0x9f2d6ec> as a backend
    2014-06-12 04:36:17 [1148] [INFO] Application is <django.core.handlers.wsgi.WSGIHandler object at 0x939b60c>
    2014-06-12 04:36:17 [1148] [INFO] Serving on fd://5
    2014-06-12 04:36:17 [1148] [INFO] Using <class chaussette.backend._wsgiref.ChaussetteServer at 0x92596ec> as a backend

Tendremos la aplicación servida en el puerto 8080 de localhost. Demonizarlo es sólo un flag:

.. code-block:: bash

    (nikolahub)tin@morochita:$ circud --daemon circus.ini



Para implementar nginx como proxy reverso armé un archivo ``nginx.conf``:

.. code-block:: javascript

    server {
        listen 80;
        server_name nikolahub.nqnwebs.com;

        location /static/ {
                alias /projects/nikolahub/static/;
        }

        location /media/ {
            alias /projects/nikolahub/media/;
        }

        location / {
            proxy_pass http://localhost:8080/;
            proxy_pass_header Server;
            proxy_set_header Host $host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_connect_timeout 600;
            proxy_send_timeout 600;
            proxy_read_timeout 600;
        }
    }

Luego agregamos el sitio:

.. code-block:: bash

    $ ln -s /etc/nginx/sites-available/nikolahub nginx.conf
    $ ln -s /etc/nginx/sites-enable/nikolahub nginx.conf
    $ sudo service nginx restart

.. image:: http://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Reverse_proxy_h2g2bob.svg/400px-Reverse_proxy_h2g2bob.svg.png
   :align: right

Esto pone a nginx como "frontend" de la aplicación, sirviendo los directorios con contenido estático y pasando el resto de las peticiones al puerto 8080 que administra Circus.

Ya tenemos nuestro sitio en producción.

El dueño del circo y los monitos
--------------------------------

De ahora en más, podremos usar las herramientas que provee Circus.

``circusctl`` es el dueño del circo. Puede parar, reiniciar, cambiar la cantidad de workers, abrir una consola ipython para interactuar o inspeccionar y mucho mas. Se puede usar como subcomandos (``circusctl <subcmd> <watcher>``) o usar la consola interactiva.

Por ejemplo, si quisiera ver cuantos procesos workers tengo y agregar uno más, podría hacer así:

.. code-block:: bash

    (nikolahub)tin@morochita:$ circusctl numprocesses nikolahub
    3
    (nikolahub)tin@morochita:$ circusctl incr nikolahub
    ok
    (nikolahub)tin@morochita:$ circusctl numprocesses nikolahub
    4

Lo mismo y más se puede hacer desde una consola IPython.

.. code-block:: bash

    (nikolahub)tin@morochita:$ circusctl ipython
    Python 2.7.4 (default, Apr 19 2013, 18:32:33)
    Type "copyright", "credits" or "license" for more information.

    IPython 2.1.0 -- An enhanced Interactive Python.
    ?         -> Introduction and overview of IPython's features.
    %quickref -> Quick reference.
    help      -> Python's own help system.
    object?   -> Details about 'object', use 'object??' for extra details.

    In [1]: arbiter.numprocesses()
    Out[1]: 4


``circus-top`` es un monitor realtime, estilo top. Escucha las estadísticas
que produce ``circusd-stats``.

.. code-block:: bash

    (nikolahub)tin@morochita:$ circus-top

.. figure:: /images/circus-top.png

    circus-top en acción. Muestra los procesos watcher y los recursos que cosumen.

Todo esto puede verse y manejarse cómodamente a través de `circus-web <https://circus.readthedocs.org/en/0.11.1/for-ops/circusweb/>`_, un dashboard web que permite monitorear y
administrar circus, con gráficos realtime y muy fácil de usar.

.. image:: https://circus.readthedocs.org/en/0.11.1/_images/web-watchers.png
   :width: 100%
   :align: center

Desde las últimas versiones, ``circus-web`` se refactorizó para basarla en Tornado_ (originalmente usaba bottle_) y hay que instalarlo aparte.

.. code-block:: bash

   $ pip install circus-web

Conclusiones
------------

Circus_ es una herramienta que simplifica el stack de deployment de una aplicación web WSGI.
La API de alto nivel, una arquitectura mucho más moderna y simple y el aval de ser desarrollada (y usada exhaustivamente) por Mozilla, son avales poderosos para probarla.

Como `escribió el Marcos Luc <http://textosypretextos.com.ar/Bienvenidos-al-show>`_ *"la función ya debería empezar (...) Bueno nena, buena suerte, cada vez la red te teme más..."*


.. raw:: html

    <iframe width="709" height="390" src="//www.youtube.com/embed/AhfUfjLpNvI" frameborder="0" allowfullscreen></iframe>



.. _tornado: http://www.tornadoweb.org
.. _bottle: http://bottlepy.org/
.. _zeromq: http://zeromq.org/
.. _Circus: http://circus.readthedocs.org/
.. _Chaussette: http://chaussette.readthedocs.org/
.. _supervisor: http://supervisord.org/
.. _Gunicorn: http://gunicorn.org/
.. _WSGI: http://legacy.python.org/dev/peps/pep-3333/
.. _nikolahub: https://github.com/mgaitan/nikolahub