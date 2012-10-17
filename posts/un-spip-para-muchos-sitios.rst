Administrar muchos sitios SPIP tiene sus bemoles. Yo administro, fácil,
unos 30. Cuando hay que actualizar la versión (por cuestiones de
funcionalidad, o bien, como la semana pasada, por cuestiones de
seguridad), es un trabajo engorroso y aburrido hacer 30 veces lo mismo.
Y el trabajo se vuelve exponencial si hay que actualizar los plugins
para cada uno

Para evitar eso existe la
`Mutualización <http://www.spip-contrib.net/La-mutualisation-facile>`_,
que desde la versión 2 es realmente muy fácil.

El concepto es simple: un sólo núcleo de SPIP (/ecrire, /prive,
/squelettes-dist, /plugins) se comparte para motorizar diferentes
sitios, que tendrán los directorios con contenido propio (/squelettes,
/config , /IMG, etc), separado del resto

Así, a la hora de actualizar SPIP sólo tenemos que actualizar una sola
instalación, tarea que se vuelve trivial si además usamos
`svn <blog/article/ultima-version-de-spip-por-svn>`_.

Requisito
~~~~~~~~~

En general, la mutualización funciona sin muchos pormenores en un
servidor LAMP, pero nuestro servidor de hospedaje debe permitir apuntar
diferentes dominios a un mismo directorio publico.

Por ejemplo, mi sitio **textosypretextos.com.ar** apunta a
*/home/tin/public\_html/spip* y **nqnwebs.com** apunta también a
*/home/tin/public\_html/spip*.

Es una configuración simple, pero no todos los servicios de hosting lo
permiten.

Puesta en marcha
~~~~~~~~~~~~~~~~

+----------------------------------------------+
| `|image1| </downloads/mutualisation.zip>`_   |
+----------------------------------------------+
| plugin mutualisation                         |
+----------------------------------------------+

La "mutualización fácil" funciona a través de este plugin, pero que
particularmente **debe ser instalado en la raiz del sitio** y no en la
carpeta /plugins

Al descomprimirlo crea una nueva carpeta, */mutualisation*, en la raiz
de nuestro SPIP mutualizado

Además, incluye un archivo *mes\_options.php* de ejemplo, pero yo te
propongo este, que debe ser instalado en */config*

::

     true
         */ 
        # define ('_INSTALL_USER_DB_ROOT', 'mon_root');
        # define ('_INSTALL_PASS_DB_ROOT', '********');
     
        /*
         * Crear las bases de dato via un ping a una URL (metodo AlternC)
         *
         * Il suffit de renseigner l'option url_creer_base, en lui passant les bons parametres :
         * 'url_creer_base' => 'https://bureau.tld/admin/sql_doadd.php?username=USER&password=PASS&dbn='.prefixe_mutualisation($site)
         */
         
         
        /*
         * Transformar en las paginas publicas las URL de imagenes
         * /sites/mon_site/IMG/* -> /IMG/*
         * /sites/mon_site/local/* -> /local/*
         * 
         * - Necesita el mod_rewrite (reescritura de url) de apache
         * - Sólo funciona con nombres de dominio mutualización
         * ('http_host' : http://mi_sitio_mutualizado.com)
         * (por lo tanto, no funciona con un subdirectorio - http://mi_sitio_mutualizado.com/misitio/)
         * 
         * y añadir en la opción 
         * 'url_img_courtes' => true
         * 
         * Es posible generar los  .htaccess 
         * automaticamente en /IMG y /local
         * gracias a ?var_mode=creer_htaccess_img
         * 
         */
        
        /*
         * Indique aqui el nombre del sitio de administración de esta mutualización
         * (o varios, separados por oma)
         * (dpor ejemplo, 'scriibe.net' es el dominio de nivel maximo)
         * para autorizar todos los sitios no definir la constante ;
         * Si el propietario del sitio no se encuentra en los sites/ sino en la razi, 
         * escriba '' y agregue 'mutualisation' en $dossier_squelettes
         */
        define ('_SITES_ADMIN_MUTUALISATION', 'nqnwebs.com');

        
        demarrer_site($site,
            array(
                'creer_site' => true,        // Creer ou non le site s'il n'existe pas (defaut: false) 
                'creer_base' => false,        // Creer ou non la base de donnee si elle n'existe pas (false) 
                'creer_user_base' => false,  // Creer ou non un utilisateur pour la nouvelle base de donnee (false)
                'mail' => '',                // Adresse mail pour recevoir un mail lors d'une creation de site mutualise ('') 
                'code' => 'miclave',  // Code d'activation ('ecureuil') 
                'table_prefix' => true,     // Definir automatiquement le prefixe de table (false) ... mettre true si tous les sites dans la meme base 
                'cookie_prefix' => true,     // Definir automatiquement le prefixe de cookie (false)
                'repertoire' => 'sites',     // Nom du repertoire contenant les sites mutualises ('sites')
                'url_img_courtes' => true,   // Utiliser la redirection des URL d'images courtes dans la partie publique (false)
                # 'utiliser_panel' => false, // Utiliser une table externe pour recuperer des identifiants ... (code, user, pass) permettant a un utilisateur d'installer le site (false) 
                'url_creer_base' => ''       // Creer la base de donnees via une URL (methode AlternC)
            )
        );

        
    ?>

Este mes\_options.php (retocado por mi) permite que los sitios funcionen
con o sin ’www’. También apunta a una única base de datos, donde se
encargará de crear las tablas necesarias para cada sitio, diferenciadas
por un prefijo.

Sólo resta crear la carpeta */sites* en la raiz del sitio, donde irán
nuestros diferentes sitios mutualizados.

Al acceder via web a un dominio de un sitio sobre esta mutualización, lo
primero que aparecerá es una solicitud de contraseña, definida en array
de configuración de mes\_options.php (en el ejemplo, la contraseña es
*miclave*)

.. figure:: local/cache-vignettes/L510xH303/Pantallazo-2-d2b75.png
   :align: center
   :alt: 
Luego siguen dos etapas que nos crean la estructura de directorios para
este sitio dentro de */sites* y las tablas para este sitio en la base de
datos compartida. Lo que sigue es el proceso de instalación estándar de
SPIP.

**¡Listo!**

Hay que tener en cuenta que ahora los archivos para nuestro sitio
estarán dentro de */sites/dominio/* y es allí donde deberán subirse los
esqueletos y demás.

Mutualizar un sitio en producción
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

¿Qué pasa si el sitio que quiero mutualizar ya está funcionando sobre un
spip propio? No problem.

Basta indicar (desde el panel, o solicitando al administrador del
hosting) que nuestro dominio debe apuntar ahora a la carpeta donde
tenemos el spip mutualizado (en mi ejemplo */home/tin/public\_html/spip*
), crear el directorio **/sites/dominio** (donde dominio es la url del
sitio que queremos migrar) y mover alli las carpetas /config, /IMG,
/squelettes, /local y /tmp (o crear una /tmp nueva) del SPIP en uso al
nuevo directorio. [[Estas carpetas, bien podrian ser link simbólicos].
Magia!

Conclusión
~~~~~~~~~~

.. |image0| image:: /images/zip-2bcd4.png
.. |image1| image:: /images/zip-2bcd4.png
