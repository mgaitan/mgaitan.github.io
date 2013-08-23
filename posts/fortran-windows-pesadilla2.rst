.. link:
.. description:
.. tags: draft
.. date: 2013/08/22 20:11:45
.. title: Fortran + Windows = pesadilla^2
.. slug: fortran-windows-pesadilla2

Hace muchísimo que no escribo en este blog y no es porque tengo otro_, sino, principalmente, porque estoy con muchísimo trabajo.

Hace casi un mes dejé [1]_ de trabajar en Machinalis_, una de las empresas más pythónicamente grosas del mundo mundial [2]_, en la que inenvitablemente aprendí muchísimo
(y eso que me esforcé ;-)), hice amigos y laburé en proyectos de una escala y complejidad a la que nunca podría haber aspirado como un "freelance *che pibe* programador".

Ahora laburo fulltime (o sea: el triple) en Phasety_, el proyecto que estamos creando junto a Martín Cismondi, director de mi proyecto integrador de grado hace algunos años ("ingeniero en computación", dice el pelpa) y hoy socio. Cismondi es doctor en ingeniería
química y uno de los especialistas más reputados en el área "equilibro de fases",
que es, básicamente, modelar el comportamiento termodinámico de un fluido mediante algoritmos numéricos.

Un poco por cierta "inercia cultural" del mundo científico (en particular en las área de química computacional) y otro poco porque sigue siendo increíblemente eficiente para rutinas de cálculo, Fortran es el lenguaje predominante en el que los tipos
como Cismondi programan. A lo que si le sumás Windows, las bibliotecas privativas y un flujo de trabajo atado al IDE que aprendieron a "clickear" (en general, Visual Studio),
es todo un problema.

Así que parte de mi laburo es sumergirme en este escabrozo mundo y meter ingeniería de software allí donde nunca la hubo.

Por suerte existe Python, pisando cada vez más fuerte en el mundo de la ciencia y la ingeniería (http://scipycon.com.ar/, como ejemplo). Pero, mientras seguimos minimizando
la `deuda técnica`_ fomentando_ esta tecnología, hay que hacerlas convivir.

f2py, gfortran y lapack en Windows
----------------------------------

Estas son notas de lo que he ido logrando hasta el momento, para armar un entorno
de desarrollo y empaquetamiento (en lo posible, libre) de software multiplataforma basado en python y fortran.

.. note:: work in progress.


.. _otro: http://www.textosypretextos.com.ar
.. _Machinalis: http://machinalis.com
.. _Phasety: http://phasety.com
.. _deuda técnica: http://es.wikipedia.org/wiki/Deuda_t%C3%A9cnica
.. _fomentando: http://phasety.com/1/blog/article/curso-taller-python-para-ciencia-e-ingenieria




.. [1] o "terminé de dejar", porque estaba part-time desde septiembre de 2012.
.. [2] lo de "empresa pythónica", no
