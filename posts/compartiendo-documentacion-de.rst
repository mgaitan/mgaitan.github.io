Sabido es, aunque muchas veces se ignora, que un software sin
documentación está incompleto
[`1 </blog/article/compartiendo-documentacion-de#nb1>`_].

Si bien el manifiesto ágil
`proclama <http://agilemanifesto.org/iso/es/>`_ *"Software funcionando
sobre documentación extensiva"*, yo subrayaría extensiva como eufemismo
de documentación burocrática e inútil (opiné de esto
`acá <blog/article/veinteanero>`_) que evidentemente no es la que hace
falta. Pero la documentación (sobre todo la buena) es indispensable y
para `algunos <http://jacobian.org/writing/great-documentation/>`_, la
parte que más los enorgullece del proyecto (y con razón).

Desde el punto de vista técnico, escribir documentación (no `sólo para
Python <http://sphinx.pocoo.org/examples.html>`_!) es bastante fácil con
`restructuredText <http://docutils.sourceforge.net/rst.html>`_ (qué feo
el sitio de docutils, che!) que es `el markup estándar de los
pythonistas <http://www.python.org/dev/peps/pep-0287/>`_.

Sobre este markup funciona `Sphinx <http://sphinx.pocoo.org/>`_, el
generador de documentación más utilizado (por lejos) en el ecosistema de
Python. Es lo que usa la documentación de Python misma, la de Django y
casi todo proyecto conocido o por conocer.

Entonces usamos restructuredText, usamos Sphinx, pero para `nuestro
proyectito de morondanga <blog/article/la-sanguijuela-de-cuevana>`_ que
no tiene web propia ni nada, ¿dónde subimos la documentación generada?
Veamos.

Usando Readthedocs.org
~~~~~~~~~~~~~~~~~~~~~~

`Read the docs <http://readthedocs.org/docs/read-the-docs/en/latest/>`_
es un sitio para hospedar documentación realizada con Sphinx. Sólo se
necesita indicarle el repositorio público del proyecto (svn, git,
mercurial, bazaar), subir los fuentes .rst y contenido estático
(imágenes) aptos para Sphinx en una carpeta /doc o /docs y el sitio se
encarga de bajar los fuentes de documentación y renderizarlos a HTML a
través de Sphinx.

Estrictamente, usando rtfd.org (como le dicen `los
amigos <http://www.urbandictionary.com/define.php?term=RTFD&defid=2281638>`_)
ni siquiera hace falta tener Sphinx instalado localmente.

Más aun, por defecto actualiza diariamente, pero se puede utilizar un
"hook" para indicarle que actulice cuando "pusheamos" (o "commiteamos")
al repo, de manera de tener la documentación actualizada al instante.
Para usuarios de GitHub la activación del "web hook" se explica
`acá <http://readthedocs.org/docs/read-the-docs/en/latest/webhooks.html#github>`_
. Para `BitBucket.org <http://bitbucket.org>`_ es parecido:

#. Vas a tu proyecto , click en Admin -> Services
#. Agregás el servicio "POST"
#. Completás el campo de texto con la URL que te da ReadTheDocs en la
   página de descripción de tu proyecto (estándo logueado). Por ejemplo:

.. figure:: local/cache-vignettes/L295xH73/2011-04-10-221400_295x73_scrot-15220.png
   :align: center
   :alt: 
Y listo. Tu docu al instante.

Como el sitio genera el html en vez de servir una versión generada
previamente, la documentación que requiere introspección del código (
todas las directivas `` .. auto* :: `` de Sphinx) este debe poder
ejecutarse. Para eso el paquete debe ser instalable via ``setup.py`` y
hay marcar desde la página de configuración del proyecto en RTFD.org,
que instale en un virtualenv.

Para ver si hubo algún problema en la generación, podés fijarte en
"build" donde te muestra el stdout y el stderr de la corrida de Sphinx.

Subir la docu a PyPi
~~~~~~~~~~~~~~~~~~~~

Una forma buenísima de compartir tu trabajo pythónico es a través del
Python Package Index, `pypi <http://pypi.python.org/pypi>`_, que es el
índice que usan las herramientas `pip <http://www.pip-installer.org>`_ e
easy\_install. Si bien no necesarimente los paquetes deben estar
hospedados allí (indicando en el setup.py la URL de descarga) es muy
común y fácil hacerlo con el comando ``upload`` del setup.py.

Lo que muchos no
`saben <http://packages.python.org/an_example_pypi_project/buildanduploadsphinx.html>`_
es que PyPi también ofrece `hostear la
documentación <http://packages.python.org/>`_. La forma canónica es ir a
la página de administración de tu proyecto en PyPi y adjuntar un .zip
con la documentación (que no necesariamente tiene que ser hecha con
Sphinx)

.. figure:: local/cache-vignettes/L510xH111/2011-04-10-223417_605x131_scrot-d5e1d.png
   :align: center
   :alt: 
Pero si usamos Sphinx hay una manera más fácil, manteniendosé en el
"ecosistema" de desarrollo: usar esta `extension de
setuptools <http://pypi.python.org/pypi/Sphinx-PyPI-upload/>`_ que
permite generar el html a través Sphinx y subirlo automáticamente. Se
instala, obviamente, vía pypi:

::

    $ easy_install sphinx-pypi-upload

Hay que condigurar un ``setup.cfg`` (ubicado al nivel raiz, junto con
``setup.py``) indicandole dónde está la docu fuente y dónde el
resultado. Más o menos así:

::

    [build_sphinx]
    source-dir = doc/source
    build-dir  = doc/build
    all_files  = 1

    [upload_sphinx]
    upload-dir = doc/build/html

Luego se usa:

::

    $ python setup.py build_sphinx
    $ python setup.py upload_sphinx

Y docu subida a la dire
*`http://packages.python.org/tu-proyecto <http://packages.python.org/tu-proyecto>`_*
. ¡`Charaaán <http://packages.python.org/CuevanaLinks/>`_!

Usando tu repositorio SVN
~~~~~~~~~~~~~~~~~~~~~~~~~

Si usas SVN y tu servidor lo permite, podés servir contenido estático
(html y todo lo que produce y necesita Sphinx) directamente desde el
repositorio.

Para que el servidor Subversion muestre el html renderizado en vez del
código (como texto plano) hay que indicarle el tipo ``mime`` de cada
archivo.

::

    $ svn propset svn:mime-type 'text/html' FILENAME
    $ svn propset svn:mime-type 'image/jpeg' FILENAME

Para que esto se haga automático, se puede modificar el archivo de
configuración ``~/.subversion/config ``

::

    [miscellany]
    enable-auto-props = yes

    [auto-props]
    *.html = svn:mime-type=text/html
    *.css = svn:mime-type=text/css
    *.js = svn:mime-type=text/javascript
    *.png = svn:mime-type=image/png
    *.jpg = svn:mime-type=image/jpeg
    *.gif = svn:mime-type=image/gif

Un ejemplo de esto es el `reporte de mi proyecto
integrador <http://gpec2010.googlecode.com/svn/trunk/docs/_build/html/index.html>`_
que está hospedado en Google Code

Aprovechándote de GitHub
~~~~~~~~~~~~~~~~~~~~~~~~

`GitHub <http://github.com>`_ hospeda `páginas
estáticas <http://pages.github.com/>`_, tanto del desarrollador/a como
de tus proyectos. Bien sirve eso para subir la documentación y eso hacen
mas o menos automáticamente estas opciones que no he probado pero las
dejo como referencia:

|-| `Hosting sphinx doc in
github <http://lucasbardella.com/report/hosting-your-sphinx-docs-in-github/>`_
de Luca Sbardella.
|image1| `Usando
github-tools <http://dinoboff.github.com/github-tools/overview.html#documentation-hosting>`_.

.. |-| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image1| image:: local/cache-vignettes/L8xH11/puce-32883.gif
