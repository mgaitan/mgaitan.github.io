Con un poco de coca-cola en la sangre, retomé esta madrugada un
proyectito que tenía: adjuntar fotos de un album de
`Picasa <http://picasaweb.google.com>`_ a un artículo.

El caso de uso, basado en mi propia necesidad, es el siguiente:

|-| Uso PicasaWeb para subir mis fotos. A veces son albumes públicos, a
veces no.
|image1| Al subir fotos, generalmente le pongo una descripción.
|image2| Algunas fotos las subo también a mi blog personal.

La complicación es que tengo que subir las fotos a picasa y tambien a mi
web (por ftp si son muchas). Obviamente es ineficiente, y además pierdo
los comentarios que hice en Picasa.

Con ustedes, Spicasa
~~~~~~~~~~~~~~~~~~~~

Spicasa intenta solucionar esto. Está basado en el plugin
`Flickr\_cc <http://plugins.spip.net/Flickr-CC>`_ pero utilizando la
excelente biblioteca `Lightweight PHP Picasa
API <http://cameronhinkle.com/blog/id/8585148182656068438>`_ de Cameron
Hinkle, para interactura con la `API de
Picasa <http://code.google.com/intl/es-AR/apis/picasaweb/overview.html>`_

Permite buscar fotos públicas en Picasa y asociarlas a un artículo, al
igual que Flickr\_cc lo hace con `Flickr <http://flickr.com>`_. Pero
además, permite ingresar a tu cuenta y adjuntar uno de tus albumes al
artículo. Todo con mucho AJAX y dulce de leche.

|image3|
Por supuesto, aunque cumple sus función básica, es un desarrollo
totalmente inacabado que necesita desarrollo y depuración.

Requerimientos
~~~~~~~~~~~~~~

|image4| Requiere SPIP 2.0 o superior
|image5| La biblioteca Lightweight PHP Picasa API está incluída. Sólo
requiere PHP5.

TODO y bugs conocidos
~~~~~~~~~~~~~~~~~~~~~

|image6| [STRIKEOUT:El tamaño máximo de las fotos descargadas es 800px]
|image7| [STRIKEOUT:No hace búsquedas de más de una palabra]
|image8| Hay que loguearse cada vez que se quiere adjuntar un álbum
nuevo
|image9| [STRIKEOUT:La ventana modal queda inaccesible si el scroll
vertical no está arriba. (bug heredado de Flickr\_cc)]

Descarga e instalación
~~~~~~~~~~~~~~~~~~~~~~

+---------------------------------------------+
| `|image11| </downloads/spicasa0.13.zip>`_   |
+---------------------------------------------+
| Spicasa 0.13                                |
+---------------------------------------------+

|image12| Descromprimilo en la carpeta */plugins* de tu sitio spip
|image13| Activalo desde el panel de administración
|image14| Al editar un artículo, te aparecerá un link con el logo de
Spicasa para adjuntar fotos.

.. |-| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image1| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image2| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image3| image:: /images/Pantallazo-1-3e61d.png
.. |image4| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image5| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image6| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image7| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image8| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image9| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image10| image:: /images/zip-2bcd4.png
.. |image11| image:: /images/zip-2bcd4.png
.. |image12| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image13| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image14| image:: local/cache-vignettes/L8xH11/puce-32883.gif
