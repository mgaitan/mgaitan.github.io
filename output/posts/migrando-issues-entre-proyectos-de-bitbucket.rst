.. title: Migrando issues entre proyectos de Bitbucket
.. slug: migrando-issues-entre-proyectos-de-bitbucket
.. date: 2012/11/10 0:09:24
.. tags: python, migraciones, scripts
.. link:
.. description:

Hace un tiempo conté `como migré un repositorio Mercurial a Git`_ .
Se trataba de un proyecto hospedado en Bitbucket_ y para cambiar
de DVCS tuve que crear un proyecto nuevo, que tambien hospedamos 
allí porque somos pobretones y nos da repos privados gratis. 
En la mudanza se me quedaron varios *issues* que necesitaba migrar. Y `no era el único`_.

Buscando un rato encontré scriptcitos para migrar desde_ o hacia_ GitHub 
pero no había para migrar entre proyectos de Bitbucket, algo bastante común 
desde que empezaron a ofrecer soporte Git.

Decidí entonces que debía hacer mi propio scriptcito migrador. La cosa se 
complicaba porque `el <https://github.com/Sheeprider/BitBucket-api>`_ 
`par <https://github.com/ericof/python-bitbucket>`_ de bibliotecas python 
que interactuan con la API de Bitbucket no tenian, hasta el momento, soporte
para "postear" *issues*

Pero no hay darse por vencido: se me ocurrió mirar el par de forks de cada 
proyecto y encontré `justo lo que estaba buscando <https://github.com/davidmpaz/BitBucket-api/commit/e7d727f0a340ca9f2c131b04bd72d7cf5e4960dc>`_. 

.. _no era el único: https://bitbucket.org/site/master/issue/1642/allow-moving-tickets-over-to-another
.. _desde: https://github.com/sorich87/github-to-bitbucket-issues-migration
.. _hacia: https://gist.github.com/3778347

Entonces bastó con instalar el fork de David Paz Reyes

.. code-block:: bash

    $ pip install git+https://github.com/davidmpaz/BitBucket-api.git

he hice un script que migra todo los issues en estado *new*
del repo original (``gpec``) al nuevo (``gpec``) y los potenciales comentarios que tenga. 
Como el autor  se pierde (dado que el nuevo quedará publicado con mi usuario)
agrego un comentario avisando que es un *issue migrado*. 

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from bitbucket import bitbucket

    gpec = bitbucket.Bitbucket('tin_nqn', '***', 'gpec')
    gpec3 = bitbucket.Bitbucket('tin_nqn', '***', 'gpec3')

    # request original ISSUES
    _, result = gpec.get_issues()

    for issue in result['issues'][:]:
        original_id = issue['local_id']
        if issue['status'] != 'new':
            continue

        # and post to the new repo
        ok, new_issue = gpec3.add_issue(**issue)

        if not ok:
            print 'Fail migrating #%d' % original_id
            continue

        new_id = new_issue['local_id']

        print 'Migrated #%d as #%d in the new project' % (original_id, new_id)

        # add a comment to mark the migration
        who = issue.get('reported_by', None)
        who = who['username'] if who else 'anonymous'
        gpec3.add_issue_comment(new_id, content="Issue migrated from the original repo. "
                "Was #%d reported by %s" % (original_id, who))

        # migrate comments
        result, comments = gpec.get_issue_comments(original_id)
        for c in comments:
            if not c['content']:
                continue
            gpec3.add_issue_comment(new_id, **c)



¡Disfruten!

.. _como migré un repositorio Mercurial a Git: /posts/de-mercurial-a-git-limpieza.html
.. _Bitbucket: http://bitbucket.org
