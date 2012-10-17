Cuando decidí dar el salto desde Subversion a un DVCS estuve leyendo
muchos posts comparativos entre las dos opciones más relevantes, Git y
Mercurial. Había que elegir entre `Mc Gyver o James
Bond <http://importantshock.wordpress.com/2008/08/07/git-vs-mercurial/>`_
decía uno, entre `Denzel Washington y Wesley
Snipes <http://www.ericsink.com/entries/hg_denzel.html>`_ y la
comparación jocosa entre estos dos grandes softwares se volvió una
especie de meme tácito.

Sabía que, a fin de cuentas, tenía que probarlos y ver cual encajaba
mejor para mis necesidades de "solo developer". En el medio leí `Hg
Init <http://hginit.com/>`_ del gran divulgador Joel Spolsky y, víctima
de semejante labia, me sumergí para ese lado.

Mi flujo de trabajo era bastante básico pero suficiente y superador de
subvesion. Comparado con lo que había probado de Git era mucho menos
verbósico (no podía entender la necesidad de Git hacer ``add`` cada vez
que quería commitear un archivo modificado) y
`Bitbucket <http://bitbucket.org>`_ daba no sólo hospedaje gratuito para
repositorios públicos sino también para potenciales desarrollos privados
(cosa que GitHub, su equivalente — siendo benévolo con bitbucket — para
Git, no daba).

Con el tiempo empecé a compatir `algunos
proyectitos <https://bitbucket.org/tin_nqn/cuevanalinks>`_ con otros
desarrolladores y mi inexperiencia en Mercurial me empezó a jugar en
contra. Y justo cuando necesitaba ponerme a aprender más profundamente
Hg, entre a laburar, muy a gusto, en
`Machinalis <http://machinalis.com>`_ (qué vago, nunca conté nada por
acá) donde usamos Git para el control de versiones de los proyectos,
implementando `esta política de ramificación y
mezcla <http://nvie.com/posts/a-successful-git-branching-model/>`_.

Resultó entonces que en poquito tiempo ya sabía mucho más de Git que de
Mercurial (con la ventaja de tenerlo a Daniel Moisset cerca para apagar
algunos incendios que encendí las primeras semanas).

Para más señales, Atlassian, la empresa detras de Bitbucket y principal
referente de Mercurial (junto con Selenic, la creadora), comenzó a
ofrecer Git (sin descartar mercurial) como sistema DVCS (comiéndose
alguna que otra gastada porque alguna vez comunicó una noticia parecida
como broma del dia de los inocentes).

Asi que llegó el dia que decidí mudar un proyecto en Mercurial a Git.
Atenti: las razones no son técnicas. No tengo suficiente conocimiento de
Mercurial (ni de Git) para decir que uno es mejor que el otro por tales
razones. Sólo es \*mi experiencia\*, que vino un poco por obligación. Y
sí, también, siguiendo un poco a la manada. Proyectos de la envergadura
de Django han migrado a Git (y, particularmente, a GitHub)

La limpieza
~~~~~~~~~~~

Soy de esos que se mudan seguido. "¿Asi que si te renuevo contrato me
aumentas 30 % el alquiler e igual te tengo que pagar comisión sin que
hagas nada? ¡Andá a cagar!" puedo imaginarme dialogando con algun agente
inmobiliario.

Esta no era la excepción y debía mudar un repositorio mercurial que a su
vez había sido mudado (en realidad, exportado desde el último commit, y
arrancando de 0) desde
`subversion <http://code.google.com/p/gpec2010/>`_.

El detalle es que el repositorio original, y por ende el nuevo en
mercurial, tenia un montón de datos de documentación que era,
basicamente, todos los fuentes y muchos de los archivos generados del
reporte escrito de mi tesis.

El primer changeset en el flamante mercurial consistió en borrar todo
esa información innecesaria, pero que seguía allí, en el historial (uno
110Mb de datos que no necesitaba).

Así que ya que ahora iba a mudarme de nuevo, queria tirar a la basura
todas esas cajas de papeles que había metido en un caja y, si bien no la
veía, me ocupaban el placard.

Despues de darle vueltas, `encontré una
punta <http://stackoverflow.com/questions/2684898/mercurial-remove-history#8819813>`_
usando la extensión `hg convert para obtener un subconjunto de repo
original <http://mercurial.selenic.com/wiki/ConvertExtension#Converting_from_Mercurial>`_,
por ejemplo, partiendo de un determinado cambio.

1. Primero, activar la extensión editando ``~/.hgrc``::

    [extensions]
    convert =

2. ¡Tirar las cajas del placard! ::

    $ hg convert --config convert.hg.startrev=1 repo_hg_orig/ repo_hg_liviano/

En mi caso yo queria todo desde la revision 1. **Atenti**: como explica,
esto genera un repo totalmente nuevo, con ids distintos para los
changesets, de modo que no se puede mantener "sincronizados" ambos con
el mismo cambio (al menos no de manera directa).

La mudanza
~~~~~~~~~~

Contra todo pronóstico fruto de mi prejuicio y desidia, migrar a git fue
extremadamente fácil usando
`hg-fast-export <http://repo.or.cz/w/fast-export.git>`_.

1. Obtener los scripts ::

   $ git clone git://repo.or.cz/fast-export.git

2. Convertir! ::

   $ mkdir repo_git
   $ cd repo_git
   $ git init 
   $ ~/fast-export/hg-fast-export.sh -r ~/repo_hg_liviano/ --force

¡Charánnnn...!

El flag ``--force`` era necesario en mi caso porque, como explica el
`readme.txt <http://repo.or.cz/w/fast-export.git/blob_plain/master:/hg-fast-export.txt>`_
*"hg-fast-export supports multiple branches but only named branches with
exaclty one head each..."*.

El resultado fue un repo git que ocupa el 5% (5.6mb) que el mercurial
original que sin perder la historia útil.

Parafraseando a Lito, *si la historia la escriben los que ganan* ...
¿ganamos ? 

.. youtube:: 3mkhn6oiqCM
