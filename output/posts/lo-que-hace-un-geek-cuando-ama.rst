Mi computadora de escritorio, la primera que compré trabajando como
desarrollador de software, es del 2005. La "morocha", una AMD64 con
placa madre `Asus
K8N <http://www.asus.com/Motherboards/AMD_Socket_754/K8N>`_ que se la
sigue bancando.

|image0|
Aquel año me enamoré, no por primera vez, pero sí mucho. Aunque resultó
una `historia
complicada <http://www.textosypretextos.com.ar/Hurgando-en-el-Gmail>`_,
es lindo recordar cuanto uno es capaz de amar y ser amado. Y reirse,
también, de cuán estúpido se puede ser en ese estado.

El tatuaje digital
~~~~~~~~~~~~~~~~~~

Hay `gestos de amor <http://www.ascodevida.com/amor/42152>`_ que no
miden consecuencias y son dificiles de comprender. Yo, por ejemplo,
decidí "hackear" la BIOS de mi maquina recién comprada y poner una foto
de aquella mujer amada omo pantalla de splash, esa que se muestra apenas
se enciende la computadora, mucho antes de cargar cualquier sistema
operativo.

Si bien por entonces ya usaba linux, para hacer esto usé una aplicación
oficial de Asus que venía en el Windows instalado, que pronto, a falta
de espacio en disco y necesidad, desapareció.

La historia siguió, por supuesto. Aquel amor terminó pero esa imagen
quedó allí, tatuada. Mientras vivía solo mucho no me importaba, quizas
porque reiniciaba muy poco la computadora, quizas porque uno naturaliza
una cicatriz hasta volverse indiferente.

Cuando un amor nuevo llegó y más tarde la convivencia, encender la
Morocha cada mañana empezó a hacerse un momento gracioso pero incómodo.
Para colmo, aun estando dispuesto a reinstalar Windows con este único
propósito, aquel programita de Asus se me hizo inconseguible .

Hasta que hoy, seis años despues, me animé a la cirugía.

Si no podés cambiar el tatuaje, cambiá de piel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Encontré un `firmware
actualizado <http://dlcdnet.asus.com/pub/ASUS/mb/sock754/K8N/K8n1011.zip>`_
para la BIOS. Aunque no hubiera problemas con la que tenía, actualizarlo
traería el splash original de Asus.

El problema, felación habitual a Microsoft de las fabricantes de
hardware, es que `la utilidad para actualizar
BIOS <http://dlcdnet.asus.com/pub/ASUS/mb/flash/AFUDOS211.zip>`_ es para
D.O.S.. WTF!

La
`solución <http://www.linuxinsight.com/how-to-flash-motherboard-bios-from-linux-no-dos-windows-no-floppy-drive.html>`_
es usar `FreeDOS <http://www.freedos.org/>`_

::

    # obtener una imagen booteable de freeDOS y montarla en un directorio
    wget http://www.fdos.org/bootdisks/autogen/FDOEM.144.gz
    gunzip FDOEM.144.gz
    mkdir /tmp/floppy
    mount -t vfat -o loop FDOEM.144 /tmp/floppy

    # obtener la herramienta para actualizar el bios y la imagen, y moverlos 
    wget http://dlcdnet.asus.com/pub/ASUS/mb/flash/AFUDOS211.zip
    unzip AFUDOS211.zip
    mv AFUDOS.exe /tmp/floppy
    wget http://dlcdnet.asus.com/pub/ASUS/mb/sock754/K8N/K8n1011.zip
    unzip K8n1011.zip
    mv 1011.rom /tmp/floppy

    # desmontar 
    umount /tmp/floppy

    # crear una ISO y grabar a un disco virgen 
    # (tambien se podría grabar a un pendrive)
    mkisofs -o bootcd.iso -b FDOEM.144 FDOEM.144
    cdrecord -v bootcd.iso

Reinciar, bootear el CD de FreeDOS y ejecutar

::

    afudos /i1011.rom

.. |image0| image:: /images/1110133923_20ebd-30987.jpg
