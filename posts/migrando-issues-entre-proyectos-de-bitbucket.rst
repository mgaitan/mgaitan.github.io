.. title: Migrando issues entre proyectos de Bitbucket
.. slug: migrando-issues-entre-proyectos-de-bitbucket
.. date: 2012/11/09 13:09:24
.. tags: python, migraciones, scripts
.. link: 
.. description: 

$ pip install git+https://github.com/davidmpaz/BitBucket-api.git


.. code-block::

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from bitbucket import bitbucket

    gpec = bitbucket.Bitbucket('tin_nqn', '**', 'gpec')
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
