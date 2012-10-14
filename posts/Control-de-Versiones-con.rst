Xab, compañero de la lista
`spip-es <http://listes.rezo.net/mailman/listinfo/spip-es>`_ me propone
un trato:

    abro una cuenta con magoya en picasa y testeo el
    `plugin <blog/article/spicasa-adjunta-fotos-de-picasa-a>`_, y a
    cambio vos "hacés (o recomendás)" un how-to subversion aplicado a
    spip

Como tenía unos materiales de una charla que dí en la facu, lo comparto
con el pueblo spipero.

Subversion, un software de control de versiones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Subversion <http://subversion.tigris.org/>`_ es el software de control
de versiones más popular de la actualidad. Es robusto, fácil de usar,
multiplataforma, libre y gratuito.

Aquí las diapositivas (un tanto frías sin nuestra explicación) que
presentamos.

La pregunta del novato: **¿Para qué sirve?**. Bueno, para llevar total
control del desarrollo de un software (u otros contenidos). Muchos lo
hemos hecho manualmente:

— Bueno, hasta aqui funciona. Hago una carpeta nueva, copio los
archivos, y sigo.

Así, al cabo de una semana de trabajo, tenemos 10 carpetas con versiones
distintas, archivos repetidos, y no sabemos realmente cual es la version
en curso. Más complicado aun, si se trabaja desde distintos equipos (por
ejemplo, la notebook y la PC de escritorio).

Pero además, sumemos la complicación de trabajar con colegas.

— Ey, Martín, acá te mando la última versión del esqueleto de portada.
— ¡Pero cómo! si te avisé que había modificado la portada completamente!

Trabajar en equipo es casi inviable a la vieja usanza. Imaginen
proyectos de software grandes, como SPIP. Imposible. Hace falta ayuda:
Subversion.

¿Cómo funciona?
~~~~~~~~~~~~~~~

Es una aplicación cliente-servidor. El cliente se instala en nuestra/s
computadoras y el servidor está, generalmente, online. A este servidor
online se le denomina **repositorio**. A la copia local de los archivos,
**copia de trabajo**. A cada cambio que el repositorio recibe se le
llama **revisión**.

|-| Para Windows, el mejor cliente es
`TortoiseSVN <http://tortoisesvn.tigris.org/>`_
|image1| Para GNU/Linux, basta **subversion**, la versión para línea de
comandos, o **RapidSVN**, una versión gráfica para entornos GTK.

El proceso de trabajo es más o menos así:

|image2| Si no existe en el repositorio nuestro código, hacemos un
**import** (enviar por primera vez nuestro código al repositorio.
|image3| Para empezar a trabajar, necesitamos hace un **checkout**, es
decir, decirle a Subversion que convierta nuestra carpeta de código (o
la cree si no existe) en copia de trabajo.
|image4| Ya preparados, el trabajo cotidiano: lo comandos más frecuentes
son tres. **update**, para actualizar la copia local con las ultimas
revisiones; **commit** para enviar nuestras modificaciones locales al
repositorio y crear una nueva revisión y **add** para agregar un archivo
que hemos creado, y aun no existe en el repositorio.

Un ejemplo con SPIP-Zone
~~~~~~~~~~~~~~~~~~~~~~~~

`Spip-zone <http://zone.spip.org>`_ tiene un servidor subversion
(asociado al software `Trac <http://trac.edgewall.org/>`_ que es un
gestor integral de proyectos de software) donde se puede alojar
cualquier contenido libre que tenga que ver con SPIP. Es abierto para
lectura (podés hacer checkouts y updates anonimamente) pero necesitás
ser usuario para hacer commits. Podés pedirle un user y pass a
`Fil <mailto:fil@nospam--.rezo.net>`_.

**Paso 0**

Suponiendo que sos usuario con clave y password y querés compartir el
desarrollo de tus squeletos, los *squelettes\_maslindos* que están en la
carpeta squelettes local (por poner un ejemplo).

La dirección del repositorio, arbitraria pero recomendada, sería esta

::

    svn://zone.spip.org/spip-zone/_squelettes_/maslindos

Desde **Tortoise**, con el boton derecho sobre la carpeta de esqueletos,
le damos a la opción **Import** y ponemos la dire del repo donde la
pide.

Desde línea de comandos sería

::

    $ svn import ./squelettes  svn://zone.spip.org/spip-zone/_squelettes_/maslindos -m "importacion de los squeletos más lindos"

Si la importación salió bien, debería poder ver tus archivos en la
siguiente dirección
`http://zone.spip.org/trac/spip-zone... <http://zone.spip.org/trac/spip-zone/browser/_squelettes_/maslindos>`_

**Paso 1** Este es el paso inicial para aquellos que quieren probar algo
que está en el repositorio, pero sin intenciones de enviar
modificaciones (sólo lectura). Tambien deben hacerlo aquellos que sí lo
van a hacer, porque la importación no implica que se haya creado una
copia de trabajo.

Así que hay que hacer el **checkout**. Si hiciste el paso anterior, para
evitar complicaciones, lo mejor es borrar la carpeta que importaste.

Entonces sí, sobre la carpeta raiz (donde queremos que se cree la otra),
hacemo checkout a la dire del repo, definiendo que la copia local será
``./squelettes`` (si no, nos creará una que se llamará *maslindos*)

La dire del repo es la siempre:

::

    svn://zone.spip.org/spip-zone/_squelettes_/maslindos

Por línea de comandos sería así:

::

    $ svn checkout svn://zone.spip.org/spip-zone/_squelettes_/maslindos ./squelettes  

**Pasos 2 y 3 **

Listo, tenemos nuetra copia de trabajo. Cada vez que queramos actualizar
a la ultima versión, parados sobre la carpeta, hacemos **update**

::

    $ svn  update

Si somos desarrolladores, y queremos enviar nuestras modificaciones, hay
que hacer **commit**

::

    $ svn  update

En caso de agregar archivos, hay que indicarselo a Subversion.

::

    $ svn  add archivo1 archivo2 *jpg

Un video vale más que mil palabras
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un ejemplo de flujo de trabajo por línea de comandos

Y otro ejemplo usando TortoiseSVN sobre Windows.

.. |-| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image1| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image2| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image3| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image4| image:: local/cache-vignettes/L8xH11/puce-32883.gif
