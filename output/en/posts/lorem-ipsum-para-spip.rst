`Lorem ipsum <http://es.wikipedia.org/wiki/Lorem_ipsum>`_ es el texto
que se usa habitualmente en diseño gráfico en demostraciones de
tipografías o de borradores de diseño para probar el diseño visual antes
de insertar el texto final.

Cuando estamos desarrollando necesitamos ver cómo quedará el contenido,
y debemos recurrir a un *copy & paste* de caulquier cosa que tengamos a
mano.

La ventaja de un *Lorem Ipsum* sobre otros textos, es que este tiene una
distribución del largo de las palabras bastante natural de las palabras
lo que en textos largos queda mucho mejor que repetir un mismo fragmento
una y otra vez.

Hay muchos `generadores de texto Lorem Ipsum <http://www.lipsum.com/>`_
en internet, pero lo podemos hacer aún más fácil.

Un Lorem Ipsum automático
~~~~~~~~~~~~~~~~~~~~~~~~~

Con la ayuda del plugin `jQuery Lorem
Ipsum <http://sanderkorvemaker.nl/jquery/jLorem.php>`_ de Sander Korve
hice un modelo (instalable como plugin) que permite insertar un texto
del tamaño que queramos (por omisión, de 4 párrafos).

Podés bajarlo desde acá:

+-------------------------------------------+
| `|image1| </downloads/loremipsum.zip>`_   |
+-------------------------------------------+
| Lorem Ipsum Plugin version 0.2            |
+-------------------------------------------+

O por SVN:

::

    svn checkout svn://zone.spip.org/spip-zone/_plugins_/_test_/loremipsum

Instalación
~~~~~~~~~~~

La instalación es igual que con la de cualquier plugin: descomprimirlo
en la carpeta */plugins* y activarlo.

Requiere además que los esqueletos tengan la baliza ``#INSERT_HEAD``
dentro del header, ya que allí se incluirá el javascript necesario para
su funcionamiento.

Funcionamiento básico
~~~~~~~~~~~~~~~~~~~~~

La inclusión de un *Lorem Ipsum* se basa en el modelo *lorem.html*
incluído con el plugin, por lo que hay dos maneras de llamarlo:

|-| En el cuerpo (texto, descripción, etc) de un artículo: ``<lorem>``

|image3| Predefinido en un esqueleto: ``#MODELE{lorem}``

¡y listo!

Parámetros
~~~~~~~~~~

El modelo acepta algunos parámetros para configurar la longitud del
texto. Por ejemplo ``<lorem5>`` creará 5 párrafos.

Pero también se puede especificar más datos:

|image4| **type**: permite especificar que tipo de resultado se quiere.
Las opciones válidas son **paragraphs**, **words** o **characters** para
párrafos, palabras o characteres. Así: creará un texto de 25 palabras.
El valor por omisión es **paragraphs**.

|image5| **amount**: Es lo mismo que el ID pasado al modelo: es lo mismo
que . Por ejemplo ``[(#MODELE{lorem}{amount=5})]``
[`1 </blog/article/lorem-ipsum-para-spip#nb1>`_].

|image6| **ptags**: Permite agregar las etiquetas <code<>P<>/code>
alrededor de cada párrafo. Los valores aceptados son **true** o
**false**. Por omisión es **true**.

Una astucia
~~~~~~~~~~~

Una forma de mostrar contenido en un artículo (o cualquier elemento) sin
tener que editar cada artículo sólo para poner ``<lorem>`` es invocar el
modelo siempre y cuando no exista contenido en la baliza

Por ejemplo [`2 </blog/article/lorem-ipsum-para-spip#nb2>`_]:

.. |image0| image:: /images/zip-2bcd4.png
.. |image1| image:: /images/zip-2bcd4.png
.. |-| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image3| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image4| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image5| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image6| image:: local/cache-vignettes/L8xH11/puce-32883.gif
