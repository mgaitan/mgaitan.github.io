Como sabemos, el desarrollo de SPIP se realiza a través del sistema de
control de versiones Subversion.

A través de Subversion, podemos obtener la ultima version de desarrollo
considerada estable

::

    svn checkout svn://trac.rezo.net/spip/branches/spip-2.0/  carpeta_destino

Una de las ventajas de obtener SPIP a través de SVN, es que luego es muy
fácil de actualizar.

::

    cd  carpeta_destino
    svn update

Subversion asigna un numero de revision a cada cambio realizado al
conjunto de archivos. Así, cuando los desarrolladores lo evaluan
pertinente, en un determinado momento del desarrollo se empaqueta una
nueva version "oficial"

Por ejemplo, la revisión
`13982 <http://trac.rezo.net/trac/spip/browser/branches/spip-2.0?rev=13982>`_
es la version 2.08 de Spip.

Podemos obtener una revision específica con el parámetro -r. Por
ejemplo, el siguiente comando obtendría una copia de SPIP 2.08

::

    svn -r 13982 checkout svn://trac.rezo.net/spip/branches/spip-2.0/  carpeta_destino

Genial, pero para para asegurarnos estar en una revision que se
corresponda con una "version oficial" tenemos que saber el número de ID.

En el `Trac de Spip <http://trac.rezo.net/trac/spip/wiki>`_ se mantiene
una tabla donde se especifica esta correspondencia para cada nueva
version, pero a decir verdad, es un engorro tener que ingresar sólo para
averiguar un número. Mejor hagámoslo automático!

Automatizando la obtención de un SPIP oficial por SVN
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    #!/bin/bash
    #script para una instalacion de spip a traves de svn

    if [ $# -lt 1 ]
    then
    echo "Debe indicar al menos un parametro:"
    echo "$0 destino [rev]"
    echo 
    exit 1
    fi


    if [ $# -eq 2 ]
    then
    REV=$2
    else
    echo "Averiguando revision de la ultima release..."
    REV=$(svn info svn://trac.rezo.net/spip/archivelist.txt | sed -n '9p' | cut -d' ' -f5)
    fi


    echo "Recuperando la version $REV de SPIP"
    svn checkout -r `echo $REV` svn://trac.rezo.net/spip/branches/spip-2.0/ $1 1>/dev/null
    echo "Configurando permisos..."
    cd $1
    chmod 657 IMG local tmp config
    echo "Lanzando el navegador para continuar la instalacion..."
    firefox http://localhost/~tin/$1/ecrire

Este script hace el trabajo aburrido por nosotros. Averigua cuál fue la
última modificación de *archivelist.txt* que es un archivo que se
modifica en cada nuevo lanzamiento de paquete. ¡Es el dato que nos hacía
falta!

Una solución más genuina
~~~~~~~~~~~~~~~~~~~~~~~~

**Atención**: Ya me hicieron caso. `Ver
actualización </blog/article/ultima-version-de-spip-por-svn#update>`_

Aunque el hacking (como este) es sano y divertido (y a veces también
útil), la solución más genuina sería que los desarrolladores de SPIP
mantengan un **tag** por cada nuevo empaquetamiento y uno que apunte
siempre al último.

Por ejemplo, con el siguiente comando deberiamos obtener la version 2.05
(sin saber a qué numero de revision corresponde)

::

    svn checkout svn://trac.rezo.net/spip/tags/2.05

y con este otro obtener la **última** versión

::

    svn checkout svn://trac.rezo.net/spip/tags/lastest-version

Esto, por ahora, no está implementado, pero ya hice llegar mi propuesta
a *l’equipe* de SPIP, y `lo están
discutiendo <http://article.gmane.org/gmane.comp.web.spip.devel/53503>`_

Actualización
~~~~~~~~~~~~~

Gracias a `Gilles <http://my.opera.com/tech-nova/blog/>`_ el Dev Team
adoptó mi propuesta y ahora existen Tags en el arbol SVN de spip. En
particular,

::

    svn co svn://trac.rezo.net/spip/tags/spip-2-stable

