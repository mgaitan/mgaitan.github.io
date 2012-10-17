Desde la versión 1.4, SPIP tiene una baliza calculada ``#INTRODUCTION``
que como su nombre indica, sirve para presentar una introducción al
artículo completo.

En la `documentación explica <http://www.spip.net/es_article116.html>`_

    #INTRODUCTION: [SPIP 1.4] si el artículo contiene una descripción,
    esta se utiliza aquí; si no, SPIP muestra los 600 primeros
    caracteres del inicio del artículo (del epígrafe, y luego del
    texto).

En la versión 1.92 se incorporó otro atajo para indicar el largo del
texto mostrado (sobrecargando los 600 caracteres por omisión).

Así, ``#INTRODUCTION{150} `` mostrará la descripción, si existe, o los
primeros 150 caracteres del epigrafe y/o el texto.

Pero con la versión 2 llegó por fin un control más profundo para los
redactores. Es posible definir cual es el texto que se mostrará con
#INTRODUCTION encerrandolo entre la etiquetas ``<intro>...</intro>`` en
el cuerpo del artículo.
[`1 </blog/article/personalizar-el-texto-de#nb1>`_]

Así podemos redactar nuestro artículo con la siguiente estructura:

::

    Esta oración es la introducción al articulo. Y acá sigue mi artículo completo.

Suponiendo que la baliza #INTRODUCTION se muestra en el esqueleto de
seccion, allí se vería el texto

    Esta oración es la introducción al articulo.

Y donde esté la baliza #TEXTE:

    Esta oración es la introducción al articulo. Y acá sigue mi artículo
    completo.
