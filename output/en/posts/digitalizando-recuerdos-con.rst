Para el Mundial del 2006, compré, como tantos otros que no tenían
televisor pero sí computadora, una plaquita sintonizadora de TV: una
Kozumi con el chip sintonizador BT878, uno de los más genéricos y
bastante bien soportado en linux.

Tuvo poca utilidad en aquel 2006, primero porque argentina no duró
demasiado y segundo y principal porque un vecino reclamó potestad sobre
la señal del cable coaxil que alimentaba mi chip y mis ilusiones
mundialistas.

Quedó cajoneada en algun rincón, hasta que rescaté del olvido la
videofilmadora de la familia, una vieja y noble JVC , con un montón de
casetitos Compact VHS (que es el formato con el que funciona).

Así que después de mucho patear la tarea, decidí conectar los cables y
encontrar la forma de convertir en bytes los recuerdos archivados en
esos casettes polvorientos.

Lo que hice
~~~~~~~~~~~

Primero, configurar la placa. El chip bt878 se usa en muchísimas
sintonizadoras que tienen configuraciones diferentes. Para asignarle los
correctos, se pasa un código ``card`` que se obtiene de `esta
lista <http://www.mjmwired.net/kernel/Documentation/video4linux/CARDLIST.bttv>`_.
En mi caso, para una Kozumi ktv-01c, el código es 151. El comando
completo con el que configuro el módulo es:

::

    sudo modprobe bttv card=151 pll=1 tuner=38 radio=1 bttv_verbose=1 gbuffers=4

Luego, el supercomando mencoder:

::

    mencoder tv:// -tv driver=v4l2:device=/dev/video0:input=1:width=480:height=360:norm=ntsc:alsa:adevice=hw.0:amode=1:audiorate=44100:forceaudio:forcechan=1:buffersize=300 -oac mp3lame -lameopts cbr:br=96:mode=3 -af volume=-6:0,channels=1 -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=5000:keyint=125:mbd=2 -vf yadif,crop=464:352:8:2  -o salida.avi

Algunos detalles:

|-| tv:// indica que se va a capturar video, y se le pasan paramétros
luego del flag -tv: driver **v4l2**, un tamaño de 480x360 (aunque
después se recorta), preconfigurado para ntsc (29.97 fps).
|image1| Un aspecto importante son los flags referidos al audio: se
captura el audio **alsa**, indicando la placa de sonido, el modo y la
calidad (mono a 44100hz de ancho de banda)
|image2| El audio se comprime con **lame** a mp3 de 96kps constante.
|image3| con **-af volume** le bajo el volumen 6db, porque de otra
manera me salía saturado (estoy capturando desde el microfono). El
parametro **forceraudio** fuerza la captura aunque la entrada esté
silenciada en la mezcladora. También se fuerza a grabar un solo canal
con **forcechan=1**.
|image4| Con -ovc lavc se usa **libavcodec** (ffmpeg), comprimiendo en
mpeg4 a un bitrate de 5000.
|image5| Se aplican 2 filtros de video al vuelo: **yadif** que es el
mejor filtro desentralazador (necesario para captura analógica) y un
**crop** que recorta 8 pixeles de los costados, 2 de arriba y 6 de
abajo, para evitar la distorción que producen los cabezales con las
cintas viejas.

El resultado es un video de unos 250kb/s de calidad más que aceptable.

Por ejemplo, el casamiento de mi hermano Juan, en 1998:

.. |-| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image1| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image2| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image3| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image4| image:: local/cache-vignettes/L8xH11/puce-32883.gif
.. |image5| image:: local/cache-vignettes/L8xH11/puce-32883.gif
