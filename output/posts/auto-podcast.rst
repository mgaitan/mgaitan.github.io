`Efecto Tábano <http://www.efectotabano.com.ar>`_ es el programa radial
de mi amigo Fernando Barraza. Objetivamente, uno de los mejores
programas radiales de Argentina.

Lamentablemente, desde que me vine a Córdoba tuve que conformarme con
los fragmentos de entrevistas o especiales que Fernando subía a la web.
Pero ahora que la `Radio Calf-UNC <http://fm1037online.com/>`_ está
online, la alegría está completa.

El único problema que queda es que no todos los días tengo el tiempo de
escucharlo de 16 a 18hs, Necesitaba grabarlo para escucharlo offline.

Bien podría haber hecho esto localmente pero como al sitio lo administro
yo, dije... ¿por qué no grabar el programa directamente desde el
servidor, y que cualquiera pueda bajarlo cuando quiera?

Aquí está mi podcaster automático para Efecto Tábano.

La idea
~~~~~~~

Todo se basa en el glorioso `Mplayer <http://mplayerhq.hu>`_, Mplayer es
capaz de reproducir casi cualquier formato en streaming.

Por supuesto, no habrá sonido en esa "reproducción" sobre el servidor,
pero lo que queremos es la info para grabarla.

En vez de enviarla a la placa de sonidos, la información cruda (el
sonido WAV) lo enviamos a un archivo fifo desde donde
`lame <http://lame.sourceforge.net/>`_ obtendrá su fuente de datos para
comprimir a MP3 *on the fly*.

Todo esto, claro, se ejecutará al horario del programa (y durante el
tiempo que se indique, en este caso casi 2 horas) mediante una tarea
`cron <http://es.wikipedia.org/wiki/Cron_(Unix)>`_

Instalando lo necesario
~~~~~~~~~~~~~~~~~~~~~~~

Como anticipé, hace falta mplayer y lame. Estos programas en general no
se encuentran en el servidor (por ejemplo
`Dreamhost <http://www.dreamhost.com/r.cgi?150740>`_) así que hay que
instalarlos. Como tampoco somos root (la gran mayoría de las veces)
habrá que compilarlos desde las fuentes e instalarlos a nivel usuario.

primero crear, si no existiése, un directorio /bin donde irán nuestros
programas.

::

    mkdir bin
    chmod 775 bin

**Mplayer y mencoder**

::

    wget http://www3.mplayerhq.hu/MPlayer/releases/codecs/essential-20061022.tar.bz2
    bunzip2 essential-20061022.tar.bz2
    tar -xf essential-20061022.tar
    mv essential-20061022 $HOME/lib
    wget http://www3.mplayerhq.hu/MPlayer/releases/MPlayer-1.0rc1.tar.bz2
    bunzip2 MPlayer-1.0rc1.tar.bz2
    tar -xf MPlayer-1.0rc1.tar
    cd MPlayer-1.0rc1
    ./configure --prefix=$HOME --codecsdir=$HOME/lib/essential-20061022
    make
    make install

**LAME**

::

    wget http://nchc.dl.sourceforge.net/sourceforge/lame/lame-3.97.tar.gz
    tar -zxvf lame-3.97.tar.gz
    cd lame-3.97
    ./configure "--prefix=$HOME" "--enable-shared"
    make
    make install

Con eso ya tendríamos los programas necesarios en **./bin**

El script podcaster-efectotabano.sh
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    #!/bin/sh
    #
    # recorder — wrapper to pull remote audio stream and convert contents
    # to mp3
    
    # Path and arguments to lame (mp3 encoder)
    lame="$HOME/bin/lame -S -b 32 -m m"
    
    # Path and arguments to mplayer (stream decoder)
    mplayer="$HOME/bin/mplayer -quiet"
    
    # Where to put the output files
    odir="$HOME/efectotabano.com.ar/podcast"
    
    showname="efectotabano-`date +%Y-%m-%d`"
    duration="6660"
    url="http://78.159.108.83:8690/"
    
    fifo="${showname}_fifo"
    ofile="$odir/${showname}.mp3"
    
    #- end config ----------------------------------------------------
    
    mkfifo $fifo
    $lame $fifo $ofile &
    $mplayer  -vc null -vo null -ao pcm:file=$fifo $url &
    
    sleep 5
    pids=`ps auxww | grep $fifo | awk '{print $duration}'`
    
    sleep `echo ${duration} | bc`
    
    kill $pids
    rm $fifo

La primera parte permite configurar las rutas y parámetros de los
programas a usar, así como el formato y destino del mp3 de salida.

En este caso los parámetros de lame indican que se grabará a 32kbps en
mono.

Los mp3 de salida irán a `este
destino <http://www.efectotabano.com.ar/podcast/>`_

Este script se ejecuta de lunes a viernes a las 12:09 hora del servidor
(16:09 en argentina) y durante 6660 segundo, de modo que termina
tentativamente junto con la finalización del programa.

Para configurar la tarea en cron ejecutar **crontab -e**. La tarea a
agregar luce así:

::

    09 12 * * 1-5 ~/bin/podcaster-efectotabano.sh

Eso es todo. Todos los días, de lunes a viernes tendré mi programa para
descargar.

TO DO
~~~~~

Por supuesto, para que esto sea un
`podcast <http://es.wikipedia.org/wiki/podcast>`_ le falta la
sindicación. Por lo tanto, habría que agregar la tarea de injectar
información pertinente en una base de datos del cual generar el XML de
sindicación.
