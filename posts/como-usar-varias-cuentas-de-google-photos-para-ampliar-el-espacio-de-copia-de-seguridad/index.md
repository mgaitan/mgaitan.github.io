<!--
.. title: Cómo usar varias cuentas de Google Photos para ampliar el espacio de copia de seguridad
.. slug: como-usar-varias-cuentas-de-google-photos-para-ampliar-el-espacio-de-copia-de-seguridad
.. date: 2026-07-23 09:50:40 UTC-03:00
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text
-->

En [El termo](https://textosypretextos.pages.dev/blog/el-termo/), un cuento que publiqué en mi otro blog, decía:

> Mi viejo lleva el termo en las manos. Lo quiero, lo deseo, pero no lo necesito en absoluto. Siento un placer que acepto tonto en encontrar cosas o recuperarlas. Claro que me resulta más tranquilizador y satisfactorio cuando es evidente que fue un despojo deliberado, como esa vez que recogí dos valijas impecables (sólo debí cambiarles una rueda) en una vereda de Oxford. La ecología que abrazamos los ratas: gustar de las mercancías sin tener que pagarlas; consumir, pero si son sobras en oferta; capitalismo, pero sólo la puntita porque duele. Podría pedir el termo ahora mismo desde el celular y el señor Bezos en persona me lo llevaría en su camioncito Prime mañana a primera hora, pero no tendría gracia alguna. Y cuántos litros de combustible que ha de gastar ese hombre, ¿cierto?

Soy esa especie de [frigano](https://es.wikipedia.org/wiki/Friganismo) tercermundista con particular enconno con las corpo, cuyos productos igual usufructo. Pero me resisto a darles un mango de más. 

Aquí uno de mis hacks ratas.

<!-- TEASER_END -->

## Backupear fotos en Google sin ponerla

Google Photos permite configurar una sola cuenta como destino activo de la copia de seguridad en cada dispositivo Android. Sin embargo, es posible distribuir las fotos entre varias cuentas de Google y compartirlas todas con una cuenta principal.

Por ejemplo, se puede utilizar una estructura como esta:

- `gaitan@...`: cuenta principal, desde la que se consultan todas las fotos.
- `gaitan.archivo@...`: primera cuenta de almacenamiento.
- `gaitan.archivo2@...`: segunda cuenta de almacenamiento.
- `gaitan.archivo3@...`: tercera cuenta de almacenamiento.

Cada cuenta secundaria utiliza su propio espacio gratuito de Google. Cuando una se llena, se cambia manualmente la cuenta utilizada para las nuevas copias de seguridad.

## Cómo funciona

La configuración combina dos funciones de Google Photos:

1. Una cuenta secundaria se utiliza para hacer la copia de seguridad de las fotos del teléfono.
2. Esa cuenta comparte automáticamente todas sus fotos con la cuenta principal mediante la función **Compartir con colaborador**.

De esta manera, las fotos quedan almacenadas en las distintas cuentas secundarias, pero aparecen juntas en la biblioteca de la cuenta principal.

Google Photos no cambia automáticamente de cuenta cuando se agota el espacio. Cuando una cuenta se llena, es necesario seleccionar manualmente otra cuenta como destino de la copia de seguridad.

## 1. Agregar la nueva cuenta a Android

Abrir los ajustes del teléfono y entrar en:

**Ajustes → Contraseñas y cuentas → Añadir cuenta → Google**

La ruta puede variar según la marca del teléfono. También puede aparecer como:

- **Ajustes → Cuentas**
- **Ajustes → Usuarios y cuentas**
- **Ajustes → Administrar cuentas**

Iniciar sesión con la nueva cuenta, por ejemplo:

`gaitan.archivo3@...`

Es importante agregarla al perfil personal de Android. Si se agrega dentro de un perfil de trabajo, una Carpeta Segura, un segundo espacio o un usuario diferente, la aplicación principal de Google Photos podría no verla.

## 2. Hacer que la cuenta aparezca en Google Photos

Abrir Google Photos y tocar la imagen de perfil, en la esquina superior derecha.

Después:

1. Tocar la flecha situada junto al correo electrónico actual.
2. Buscar la nueva cuenta.
3. Cambiar temporalmente a esa cuenta.
4. Esperar unos segundos para que Google Photos la inicialice.

Luego entrar en:

**Foto de perfil → Configuración de Fotos → Copia de seguridad**

La nueva cuenta debería aparecer como opción para la copia de seguridad.

Si no aparece, probar lo siguiente:

1. Cerrar completamente Google Photos y volver a abrirlo.
2. Comprobar que la cuenta figure en los ajustes de cuentas de Android.
3. Verificar que la sincronización de la cuenta esté habilitada.
4. Actualizar Google Photos desde Play Store.
5. Ir a **Ajustes → Aplicaciones → Google Photos → Almacenamiento** y borrar solamente la caché.

No es recomendable borrar los datos de la aplicación como primera medida.

## 3. Cambiar la cuenta de copia de seguridad

Dentro de Google Photos, entrar en:

**Foto de perfil → Configuración de Fotos → Copia de seguridad**

Buscar la opción correspondiente a la cuenta utilizada para la copia de seguridad y seleccionar la nueva cuenta.

Solo puede haber una cuenta de copia de seguridad activa a la vez.

Antes de cambiarla, conviene comprobar que la cuenta anterior indique:

**Copia de seguridad completa**

También es recomendable revisar:

- La calidad de la copia de seguridad.
- Las carpetas del dispositivo incluidas.
- La copia de seguridad de WhatsApp, capturas de pantalla y otras carpetas.
- El espacio disponible en la nueva cuenta.

## 4. Compartir todas las fotos con la cuenta principal

Con la nueva cuenta secundaria seleccionada en Google Photos, entrar en:

**Foto de perfil → Configuración de Fotos → Compartir → Compartir con colaborador**

Seleccionar:

- La cuenta principal como destinataria.
- La opción para compartir todas las fotos.
- Una fecha de inicio, si fuera necesaria.

Por ejemplo:

`gaitan.archivo3@...` comparte todas las fotos con `gaitan@...`.

Después hay que abrir Google Photos con la cuenta principal, aceptar la invitación y activar la opción:

**Guardar en tu cuenta → Todas las fotos**

Así, las fotos almacenadas en la cuenta secundaria también aparecerán en la biblioteca principal.

## 5. Evitar que se vuelvan a subir todas las fotos del teléfono

Al cambiar la cuenta de copia de seguridad, Google Photos puede detectar como pendientes todas las imágenes que todavía estén físicamente almacenadas en el dispositivo.

Esto puede provocar que la nueva cuenta se llene con copias de fotos que ya estaban respaldadas en la cuenta anterior.

Para reducir ese riesgo:

1. Confirmar que la cuenta anterior tenga la copia de seguridad completa.
2. Verificar algunas fotos desde la versión web de Google Photos.
3. Usar la función **Liberar espacio en este dispositivo** desde la cuenta anterior.
4. Cambiar la copia de seguridad a la nueva cuenta.
5. Sacar una foto de prueba.
6. Comprobar que aparezca en la cuenta secundaria y en la principal.

No se deben eliminar las fotos del teléfono antes de verificar que la copia de seguridad anterior esté completa.

## 6. Qué sucede cuando una cuenta se llena

Cuando la cuenta secundaria se queda sin espacio:

1. Google Photos deja de realizar nuevas copias de seguridad.
2. Las fotos anteriores continúan almacenadas en esa cuenta.
3. Hay que agregar otra cuenta de Google.
4. Se configura esa nueva cuenta como destino de las próximas copias.
5. Se activa nuevamente **Compartir con colaborador** hacia la cuenta principal.

La cuenta anterior no debería eliminarse, porque sigue siendo la propietaria de las fotografías que se guardaron allí.

Con esta configuración, cada cuenta secundaria almacena una parte de las fotografías:

- `gaitan.archivo@...`: fotos más antiguas.
- `gaitan.archivo2@...`: siguiente período.
- `gaitan.archivo3@...`: fotos nuevas.
- `gaitan@...`: biblioteca principal donde se visualizan todas.

Desde la cuenta principal es posible consultar las fotos compartidas, realizar búsquedas, ver recuerdos y navegar por la biblioteca sin tener que cambiar constantemente de cuenta.

La principal limitación es que el cambio entre cuentas de copia de seguridad no es automático. Cada vez que una cuenta se llena, hay que configurar manualmente la siguiente.
