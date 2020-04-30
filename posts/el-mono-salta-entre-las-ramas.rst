.. title: El mono salta entre las ramas. El desarrollador también
.. slug: el-mono-salta-entre-las-ramas
.. date: 2020-04-30 01:59:00 UTC-03:00
.. tags:
.. category:
.. link:
.. description:
.. type: text


Cuando laburamos con git, necesitamos frecuentemente cambiar
de rama, sea porque estamos haciendo un feature mientras esperamos
que alguien haga review de otra cosa y eventualmente pide algo,
sea porque somos nosotros los que *checkouteamos* el branch
de un compañero para probar algo.

Ir y volver entre ramas es fácil porque basta usar `-` que es
un alias del branch previo.

.. code-block:: bash

    $ git checkout master
    Switched to a new branch 'master'
    $ git checkout -
    Switched to branch 'writing'

``git checkout -`` es equivalente a la forma general ``git checkout @{-1}``
y si cambiamos el -1 por -N volveremos al enésimo branch en que estuvimos.

El problema es que si no nos acordamos el nombre del branch, mucho menos
podriamos acordarnos el orden cronológico en el que lo usamos.

.. TEASER_END

Así que tomando ideas de aqui y allá, hice este scriptcito en Python
al que bauticé ``git-recent-branches`` que basicamente te lista las ramas
en las que venis trabajando (las 10 últimas por defecto o ``-n N``)
y checkoutear la que querés rapidamente pasando el índice.

En mi día a día lo uso un montón asi que quizas les sirve.

.. gist:: https://gist.github.com/mgaitan/ba1e4e252b90a7fd4a4eb9e1742e94fb

