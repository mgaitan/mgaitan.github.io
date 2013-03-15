.. title: Desambiguando un hash en Git
.. slug: desambiguando-un-hash-en-git
.. date: 2013/03/14 18:02:01
.. tags:
.. link:
.. description:

Soy vago. Por eso me llevo bien con Git, que permite reconocer un changeset con un `pedacito de
su hash sha1 <http://git-scm.com/book/ch6-1.html>`_ :

    Git is smart enough to figure out what commit you meant to type if you provide the first few characters, as long as your partial SHA-1 is at least four characters long and unambiguous — that is, only one object in the current repository begins with that partial SHA-1.

Pero a veces soy demasiado vago, y Git deja de llevarse bien conmigo: Estaba en una rama con varios commits y quería volver al pasado, deshaciendo commits, pero llevando uno. Fácil: ``reset`` + ``cherry-pick``. Pero copié muy pocos caracteres del hash que quería *cherrypickear*:

.. code-block:: bash

    (cpi)tin@morochita:~/cpi$ git reset --hard 772dad9a775
    HEAD is now at 772dad9 making aqueous migration script more robust
    (cpi)tin@morochita:~/cpi$ git cherry-pick c4396
    error: short SHA1 c4396 is ambiguous.
    error: short SHA1 c4396 is ambiguous
    fatal: ambiguous argument 'c4396': unknown revision or path not in the working tree.
    Use '--' to separate paths from revisions
    (cpi)mgaitan@gutemberg:~/laburo/cpi/code/cpi_mrp$

Recórcholis.

Un poquito de bash y *git plumbing* al rescate:

.. code-block:: bash

    (cpi)tin@morochita:~/cpi$ for hash in c4396{{0..9},{a..f}}; do git cat-file -e $hash && git rev-parse $hash; done 2>/dev/nul
    c4396586273b2a9ea5eae46c4ab2d98e236e7792
    c4396a2d64214a28791e4ba5a4a4017bdd9d14d6

Ahora tenemos el conjunto de hash con igual prefijo, y podemos revisarlos para ver cual era el que queriamos:

.. code-block:: bash

    (cpi)tin@morochita:~/cpi$ git show c4396586273b2a9ea5eae46c4ab2d98e236e7792

Y ese era el que quería.
