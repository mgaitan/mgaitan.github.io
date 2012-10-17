Continuando con el `artículo
anterior <blog/article/simplecart-js-para-spip>`_ hay tener en cuenta
que cuando decimos "sistema de e-commerce **simple**" implica que tiene
que ser simple también para el comprador.

En Argentina (y varios otros paises de latinoamérica) PayPal o
GoogleCheckout no son de uso masivo, porque el e-commerce no es una
práctica común y desde nuestro país es realmente imposible "poner" plata
en una cuenta de esas — salvo que sea un pago efectuado desde el
extranjero — , y es bastante engorroso sacarla. Además, quizas lo más
importante, no aceptan pagos la mayoría de las monedas locales
latinoamericanas.

+----------------------------------------------+
| `|image1| </images/dineromail_pagos.jpg>`_   |
+----------------------------------------------+

Por eso he integrado a `SimpleCart (js) <http://simplecartjs.com/>`_ el
sistema de pagos virtuales `Dineromail.com <http://dineromail.com/>`_
que es similar a los otros pero orientado al mercado latinoamericano. Se
puede utilizar desde Argentina, Brasil, Chile, México y (al parecer)
próximamente Colombia, pagando en moneda local de cada país o en
dólares.

La implementación está integrada al código original en javascript, no
sobre SPIP, por lo que puede ser útil para usarlo independientemente o
integrarlo con otro CMS.

El código está `disponible en
GitHub <http://github.com/nqnwebs/simplecart-js>`_

Instalación rápida
~~~~~~~~~~~~~~~~~~

Obviamente, se incluye el código javascript en la cabecera de la página
HTML.

::

y se definen, al menos, las variables requeridas:

::

    </root>

¡Listo! Al hacer Checkout, el contenido del carrito será enviado a
DineroMail para procesar el pago.

Otros parámetros
~~~~~~~~~~~~~~~~

El carrito de DineroMail tiene muchísimos parámetros opcionales que en
su mayoría he omitido. Mirá el `manual de
integración <https://ar.dineromail.com/content/Integración-AR.pdf>`_
para conocer la API completa. Sin embargo, algunas variables opcionales
las tuve en cuenta. Acá listo todas las implementadas:

Variable JS
Descripción
dmMerchantId
Número de cuenta de DineroMail (los primeros 7 digitos sin el dígito
verificador /X). **(requerido)**
dmCountryId
Código de país del vendedor. 1: Argentina, 2: Brasil, 3: Chile, 4:
México. **(1 por defecto)**
dmSellerName
Leyenda que el vendedor quiere mostrar en lugar de su email.
dmHeaderImage
URL de la imagen a mostrar en el Header
dmCurrency
Moneda de pago. Puede ser **USD** (dolares) . Si no se define, se usar
la **moneda local** del país del vendedor.
dmOkUrl
URL donde se re direcciona al comprador en caso de transacción exitosa
dmErrorUrl
URL donde se re direcciona al comprador en caso de transacción errónea
dmPendingUrl
URL donde se re direcciona al comprador en caso de transacción
pendiente.
dmPaymentMethods
Cadena de medios de pago permitidos. Por defecto elige todos los medios
disponibles para el país, pero se puede configurar específicamente. Por
ejemplo para permitir Pago Fácil, Rápipago y Visa en 1, 3 y 6 cuotas:
``ar_dm;ar_pagofacil;ar_rapipago;ar_visa,1,3,6``
**Nota:** Todas las variables son atributos del objeto ``simpleCart``,
por ejemplo ``simpleCart.dmSellerName = "Vendedor Loco";``

Además se puede asignar un código de producto al item.

::

El valor ’X18A’ se envía a DineroMail para futuros controles del
vendedor.

Es todo por ahora. ¡A vender!

Actualización
~~~~~~~~~~~~~

Agregué unos selectores asociados al evento "click" para permitir
cambiar dinámicamente el método de pago, de manera de darle más libertad
al comprador.

Basta con declarar un elemento que acepte el evento ``onclick `` y
asociarlo a alguna de estas clases

class
descripción
simpleCart\_to\_paypal
Activa PayPal como medio de pago
simpleCart\_to\_googlecheckout
Activa Google Checkout como medio de pago
simpleCart\_to\_dineromail
Activa Google Checkout como medio de pago
Un ejemplo de uso podría ser:

::

    Elija su método de pago

.. |image0| image:: /images/dineromail_pcdb0-b0476-b18ef.jpg
.. |image1| image:: /images/dineromail_pcdb0-b0476-b18ef.jpg
