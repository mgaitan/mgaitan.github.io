.. link:
.. description:
.. tags:
.. date: 2013/09/04 20:38:44
.. title: The reStructuredText processor
.. slug: the-reStructuredText-processor

I always liked to write_. As far as I remember, I always do it with a keyboard, in the computer. Except for some doodles when I'm thinking something hard or when I'm boring in a meeting or class, I never write in paper.

.. TEASER_END

In the computer I write a lot, but I not use text processors, neither the open-sources: althought "what you see" is "what you get", very frenquently what I see isn't what I want.

For that reason (and because I always follow the advices of  `Roberto Alsina <http://ralsina.com.ar/>`_) I write in plain text, using reStructuredText_. And I write everything: this blog, the slides of my talks_, my `thesis`_, the documentation of my `projects`_ , quick notes in a `wiki`_, `love letters`_, etc.

reST is a simple markup language designed to be readable in its source form. Writing in any text **editor**, we focus in the important part (the content), without fight against a table, the indentation or the header fonts. Morover, it's more useful under a version control system where the *diff* is easily viewable

Even when its syntax is a more verbose [1]_ than Markdown_ (the light markup more used in the web), reST is more powerful, supporting many output formats
(html, ebooks, pdf, etc.). In fact, there are books and the whole `official Python documentation`_ writing with this.

However, there is no need to be an ascetic: if a software could help us to write and to format a writing easier, why not to use it?

That is what does `rst-completions`_, a plugin for SublimeText_ I've developed [2]_. Here a demo of its capabilities.

.. raw:: html

    <iframe width="640" height="360" src="//www.youtube.com/embed/otM_tjIi_vY" frameborder="0" allowfullscreen></iframe>

At the moment it has:

- Shortcuts for links, admonitions, code blocks, etc.
- Headers: automcomplete, navigation, level changes, block folding
- Tables: autoformat, fixed or variable fitting, merge of cells
- Footnotes: automatic insertion at the bottom of the text, jump between the reference and definition
- Lists: automatic detection of the pattern (for ordered or unordered lists)
- Output: html, pdf, etc. (using pandoc, rst2pdf o rst2html)

I did it for SublimeText because it is the editor I currently use, among its extensions API is based on Python [2]_. But I have the idea to split as an agnostic library, allowing make light wrappers for any other editor.



.. _talks: http://mgaitan.github.io/charlas.html
.. _SublimeText: https://www.sublimetext.com/
.. _rst-completions: https://github.com/mgaitan/sublime-rst-completion
.. _official Python documentation: http://docs.python.org/
.. _write: http://textosypretextos.com.ar
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _wiki: https://github.com/mgaitan/waliki/
.. _thesis: http://gpec2010.googlecode.com/svn/trunk/docs/_build/html/index.html
.. _projects: http://github.com/mgaitan/
.. _Markdown: http://en.wikipedia.org/wiki/Markdown
.. _love letters: http://www.textosypretextos.com.ar/Cartas-de-amor-efimero-


.. [1] At a basic level, they are `very similar <https://gist.github.com/dupuy/1855764>`_

.. [2] Although its documentation sucks.