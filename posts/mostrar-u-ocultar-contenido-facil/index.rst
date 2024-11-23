Adrian León consultó en la lista
`spip-es <http://listes.rezo.net/mailman/listinfo/spip-es>`_:

    Estoy intentado poner balizas de este tipo:

    #BOUTON\_BLOCK

    #DEBUT\_BLOCK

    Desde el editor del sitio privado en el texto de un artículo. No
    conozco la forma de que funcione desde ahí (sale escrito como texto
    en la página resultante. ¿Hay alguna manera de hacerlo?

Estaba intentando, me enteré después, usar `este
plugin <http://www.spip-contrib.net/Block-deplier-replier>`_

Al otro día yo contesté:

    Hola Adrián. Desconocía de qué hablabas hasta que Marina mandó el
    link. Me parece que en el algunas ocasiones los plugins están
    opacando las soluciones más eficientes e ingeniosas, esas que
    buscabamos antes de que todo fuese "enchufable". **¡Spip se está
    wordpressisando!**

    Lo que quiero decir es que me parece que hay formas mejores de hacer
    eso. Yo tengo `un ejemplo para
    darte <http://www.lavozdelanzarote.com/Carlos-Espino-cree-que-los>`_

    Andá al pie del artículo, y hacé click en Opinar: despliega (u
    oculta, depende del estado) el formulario de comentarios.

    Es, sin balizas ni plugins, lo que parece que hace esa contrib.

Y el código es de risa: un pelín de jQuery (con su efecto
`toggle() <http://docs.jquery.com/Effects/toggle>`_ )

El `esqueleto del ejemplo que
propongo <http://www.lavozdelanzarote.com/squelettes/inc_article.html>`_
es bien sencillo. El formulario aparece encerrado en una ``div`` y
escondido con la propiedad CSS ``display:none``. De manera simplificada
[`1 </blog/article/mostrar-u-ocultar-contenido-facil#nb1>`_] :

::

        [(#FORMULAIRE_FORUM)]

Y el link que produce el efecto mostrar/ocultar (en este caso «opinar»
)tiene este código.

::

    Opinar

En perfecto argentino se diría: ¡una papa!

Breve explicación: Al hacer click sobre el link, se ejecuta el evento
Onclick, que mendiante jQuery (que ya se encuentra en todo sitio SPIP si
existe la baliza #INSERT\_HEAD en el ``<head>`` de los esqueletos), se
busca la el bloque con ID «form-comment» (o sea, el ``div`` contenedor
del formulario), y se aplica ``toggle()``, que es una funcion que si el
bloque está oculto, lo muestra, y se está visible lo oculta. Simple y
efectivo.

Permitiendo el uso desde la redacción
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hasta aquí el reemplazo al plugin, que no da una solución completa a la
consulta de Adrían, porque esta solución también está programado en los
esqueletos del sitio. Pero, con simples modificaciones, se puede usar
dentro del texto de los artículos.

El truco es este: la balizas no se pueden usar en el texto, pero **los
modelos** sí. Y como spip respeta el HTML, tenemos solución: generamo el
link interruptor a través de `un
modelo <http://www.spip.net/es_article3609.html>`_
[`2 </blog/article/mostrar-u-ocultar-contenido-facil#nb2>`_].

Creamos un modelo dentro de *modeles/toggle.html* (dentro de la carpeta
de nuestros esqueletos) con el siguiente código:

::

    #ENV{texto}

¡Y listo!

Para usarlo, en el cuerpo del artículo se invocaría al modelo con dos
parámetros: el identificador del contenedor, y el texto de link
controlador.

Donde se quiera mostrar el link escribimos:

::

y donde queramos que vaya el contenido oculto:

::

    Hola amigos, esto es una astucia para el compañero Adrian!
    </div>

Sólo hay que asegurarse de que el ID del contenedor sea el mismo que el
parametro *div* que pasamos a nuestro modelo. Por supuesto, esto permite
tener múltiples bloques ocultos y link controladores.

El resultado
~~~~~~~~~~~~

`esto
funciona? </blog/article/mostrar-u-ocultar-contenido-facil#oculto>`_

¡Hola amigos, esto es una astucia para el compañero Adrian!
