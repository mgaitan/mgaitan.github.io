`SimpleCart <http://simplecartjs.com/>`_ es un sistema para e-commerce
muy sencillo íntegramente desarrollado en javascript. Permite realizar
ventas mediante PayPal o Google Checkout y es muy extensible para
implementar otros sistemas.

En este domingo de procrastinación, decidí integrarlo a SPIP
[`1 </blog/article/simplecart-js-para-spip#nb1>`_]. Lo usaré, espero que
pronto, para vender los productos del `taller de serígrafía de
Mazamorra <http://www.agrupacionmazamorra.org.ar/taller-de-serigrafia-30>`_.

Cómo funciona
~~~~~~~~~~~~~

Se instala como un plugin común y se configura mediante el plugin CFG.
Por ahora sólo soporta PayPal como medio de pago, pero incluiré otros.

SimpleCart usa simples señaladores html, que yo he convertido en
balizas.

Baliza
Descripción
#SIMPLECART\_QUANTITY
Indica la cantidad de productos
#SIMPLECART\_ITEMS
Muestra los items en el carrito según las cabeceras definidas en la
página de configuración
#SIMPLECART\_TAX\_RATE
Indica la tasa impositiva indicada en la configuración
#SIMPLECART\_TAX\_COST
Indica el total de impuestos
#SIMPLECART\_SHIPPING\_COST
Indica el costo de envío en función de la configuración definida
#SIMPLECART\_TOTAL
La suma del precio de los productos en el carrito (Subtotal)
#SIMPLECART\_FINAL\_TOTAL
Total considerando impuestos y envío
#SIMPLECART\_CHECKOUT
Genera el botón para finalizar compra (redirige al sistema de pago)
#SIMPLECART\_EMPTY
Genera el botón para vaciar el carrito
Con estas balizas puedes armar el carrito en cualquier lado. Los datos
del carritos son persistentes usando cookies (incluso se conservan
durante un tiempo aunque se abandone la página).

Por ejemplo, este puede ser tu carrito .

::

    <:simplecart:your_cart:> (#SIMPLECART_QUANTITY items)

    #SIMPLECART_ITEMS


    <:simplecart:subtotal:>: #SIMPLECART_TOTAL<:simplecart:tax_cost:> (#SIMPLECART_TAX_RATE): #SIMPLECART_TAX_COST <:simplecart:shipping_cost:>:  #SIMPLECART_SHIPPING_COST <:simplecart:final_total:>: #SIMPLECART_FINAL_TOTAL 

    #SIMPLECART_CHECKOUT
    #SIMPLECART_EMPTY

Cómo agregar productos
~~~~~~~~~~~~~~~~~~~~~~

Muy simple. Se sube una imágen como documento definiendo su título y
descripción y se la incrusta con el modelo *item*. El precio se indica
con el parámetro *price*.

Por ejemplo, el documento 111 se vuelve un item si se lo incluye así

``<item111|price=23.4>``

Un atajo más
~~~~~~~~~~~~

El código para el carrito de arriba lo incluí como un modelo para poder
incrustarlo directamente desde la redacción de un artículo con
``<cart1> ``.

Demostración
~~~~~~~~~~~~

Si alguien completa la transacción, lo interpretaré como una donación
:D.

Descarga
~~~~~~~~

El plugin está en desarrollo sobre
`spip-zone <http://svn.spip.org/trac/spip-zone/browser/_plugins_/simplecart>`_.
Podés hacer un ckeckout SVN
