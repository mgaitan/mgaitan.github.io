.. title: Ext4 superblock failure y la cola del Diablo
.. slug: ext4-superblock-failure-y-la-cola-del-diablo
.. date: 2012/10/26 02:24:46
.. tags:
.. link:
.. description: e

Domingo, ciudad de Guayaquil, todo dispuesto para salir a
conocer una ciudad que en las guías de viaje suena intererante y bonita.
Se me ocurre prender la compu para ver si ese email que mandé la noche
anterior, recién llegado después de 14 horas de viaje
(5 de espera en el aeropuerto de Santiago) y deseando únicamente
ducha y colchón, había sido contestado.

*"No pusheé"*, fué lo primero que pensé, o me lo dije, en voz inaudible,
como eufemismo de un gran insulto y síntesis de *"Martincito querido,
ya sabés que el booteo está tardando mucho, el material para el taller_ que
tenés que dar mañana está en esa computadora y tiene al menos 10 horas
de trabajo offline que está en la última versión online: no podés ser tan
pelotudo y tener tan mal orto a la vez*". Mi voz interior sí que sabe
resumir.

Por suerte, no perdí la calma. Apreté el 1 en el teléfono: *"sí señor",  el
Bussiness Center queda en el 4 piso"*. Ahí fui y habia computadoras con
las que pude contactarme con Houston.

Grulic, `Perrito <https://twitter.com/perrito666>`_,
`Mariano <http://verdumariano.com.ar/>`_, Rudi, y especialmente
`mi cuñado que trabaja en Ontrack <http://blog.ontrackdatarecovery.es/conoce-al-ingeniero-ernesto-lobo/>`_
y era algo así como un Messi sentado en mi banco de suplentes
para este partido que yo no hubiese querido jugar, fueron los primeros
con quienes me comuniqué.

Mandé este mensaje:

    Gente, les mando una de Murphy y el diablo y toda la mala leche junta.
    Estoy en Ecuador invitado a dar un curso-taller de Python y Django.

    Rodo venía fantastico , hasta que hoy enciendo la laptop y no y no entra el sistema operativo!.

    Entro en modo recuperacion (ubuntu 11.10) y se clava en el ``fsck``
    hasta que me aparece un menucito que me deja entrar a una consola root.
    Lo peor sucedió ``/home/`` no monta , pero el ``/``
    parece estar sano. Ambas son una particion ``ext4``

    Si intento montar a mano o un fsck, el output dice muchas cosas que
    suenan mal pero no tengo puta idea qué significan::

        STATUS { DRDY }
        ERROR { UNC }
        configured for UDMA/133
        failed command READ DMA
        exception Emask 0x0 Sact 0x0 Serr 0x0 action 0x0
        res 51/40... Emask 0x9 (media error)


    Por favor, iluminenmé sobre cómo proceder.


Ernesto contestó. Primero intentar hacer un un live-usb con algunas
herramientas de diagnostico: `Ubuntu-rescue-remix <http://ubuntu-rescue-remix.org/>`_
podría funcionar, pero las maquinas del Bussiness center no me dejan
instalar algun `programita <http://www.pendrivelinux.com/universal-usb-installer-easy-as-1-2-3/>`_
para pasar la ISO al pendrive.

Empiezo a deseperar ya pensar si no conviene aprovechar el tiempo que me llevará
intentar un salvataje con alta probabilidad de fracaso para rehacer el
trabajo inaccesible.

Desactivar journal, no. Forzar montado, no. No se qué otra cosa, no.

Ernesto pregunta si me animo a ir por el camino duro.

    Cómo estás de fresco ara leer hexadecimal ? ``hexdump`` y ``dd``, la navaja suiza.
    que necesitamos

Intentamos algunas cosas, calculadora en mano,
pero la mayoría de los intentos de acceso al disco
caen en el mismo bucle de errores horribles. Mucho calor en Guayaquil.

Le digo a Ernesto (domingo, dia de descanso) que no se preocupe, que intentemos
eso último que se le ocurrió pero que si no funciona voy a ponerme a trabajar
de nuevo. Mientras tanto, el Dios en el que no creo me pone
`este link <http://linuxexpresso.wordpress.com/2010/03/31/repair-a-broken-ext4-superblock-in-ubuntu/>`_
en el camino de resultados de Google.

"Ernesto, prabamos esto?" y no alcanzó a contestar
antes de que esté poniendo los primeros comandos

.. code-block:: bash

    $ sudo mke2fs -n /dev/sda3

    Superblock backups stored on blocks:
    32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208

Me la juego con el primer backup:

.. code-block:: bash

    sudo e2fsck -b 32768 /dev/sda3

Cientos de  ``Y`` ``Enter`` para mensajes estilo *"está roto, desea repararlo?"*
(no había una opción "Sí a todo", como si uno fuese capaz de arrepentirse
a mitad de camino)

Anduvo. Uff. Dos simples comandos.
El Ingeniero Lobo festeja desde Londres, Skype mediante,
que podía volver a limpiar su moto sin quedar mal con su cuñado con mala
pata. Me dijo antes:

    Si no hubiese sido una situadion del tipo *mañana
    ya no me sirven los datos* yo te hubiera  recomendado en contra
    de herramienta como ``e2fsck``. Esos programas sólo se encargan
    de asegurar que el filesystem esté íntegro, pero si para eso tienen
    que cortarlo a la mitad lo hacen sin dudar.
    Son como doctores de guerra: te dejan vivo, pero sin una pierna y un
    brazo.

Querido Guayaquil: prometo visitar tu Malecón la próxima,
**push** por adelantado.



.. _taller: http://github.com/mgaitan/curso-django
