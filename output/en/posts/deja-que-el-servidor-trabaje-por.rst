Ya somos avispados usuarios de la línea de comandos y hacemos nuestros
pinitos administrando un servidor: movemos, bajamos y hasta compilamos
directamente en una maquina remota, muchas veces más potente y con más
ancho de banda que la nuestra.

Nuestra terminal cliente sólo ejecuta
`OpenSSH <http://www.openssh.com/>`_ (o
`Putty <http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html>`_
en Windows)

Pero cuando se trata de ejecutar un proceso largo y de nula
interactividad no tiene mucho sentido seguir conectados ¿Para qué gastar
tiempo y recursos (dejar la PC cliente prendida, por ejemplo) si el
trabajo sólo se hace en el servidor?

Este caso se da muchas veces, sobre todo (y aquí lo que me interesa)
cuando bajamos archivos muy pesados o hacer un mirror de un repositorio
completo.

Y aquí cómo resolverlo: usa `GNU
Screen <http://es.wikipedia.org/wiki/GNU_Screen>`_.

Screen es un multiplexor/virtualizador de terminales, y entre sus muchas
e interesantes características incluye el desacople de su proceso padre.

Esto significa que se puede ejecutar una terminal virtual con screen (en
una terminal remota por ssh, por ejemplo), ejecutar cualquier proceso en
ese entorno y desacoplarlo, pudiendo entonces desloguearse y cerrar la
conexión remota dejando el proceso en curso.

**Receta paso a paso**

-  ejecuta una consola virtual con screen
   ::

       $ screen

-  Ejecuta tu proceso largo. Por ejemplo, bajar la beta de Ubuntu Karmic
   Koala en DVD
   ::

       $ wget http://mirror.mcs.anl.gov/pub/ubuntu-iso/DVDs/ubuntu/9.10/beta/ubuntu-9.10-beta-dvd-i386.iso

-  Desacoplar el proceso con la combinación de teclas **Control+A D**
-  Desconectarse, tomar unos mates y volver cuando quieras

Para retomar el proceso

-  Conectarnos de nuevo al servidor mediante SSH
-  Listar las consolas virtuales para averiguar el PID
   ::

       $ screen -list

-  Traer a primer plano el proceso en cuestión con
   ::

       $ screen -r PID

y allí estará el proceso que dejamos corriendo (o al menos los rastros
que dejó en su paso).
