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

.. attention:: articulo en borrador

Estas son notas de lo que he ido logrando hasta el momento, para armar un entorno
de desarrollo y empaquetamiento (en lo posible, libre) de software multiplataforma basado en Python y Fortran.

El "San Valentín" de esta pareja es f2py_, una biblioteca que genera los wrappers
necesarios para convertir subrutinas (o funciones) de Fortran en módulos binarios (bibliotecas) importables desde Python.

No abordo acá cómo usar f2py (aunque `este <http://websrv.cs.umt.edu/isis/index.php/F2py_example>`_ es un buen ejemplo), sino como conseguir instalarlo y usarlo para un caso no trivial.


1. Instalar Anaconda_, de Continuum Analytics.

   Anaconda es una distribución de Python y una amplia colección de paquetes
   y bibliotecas para computación científica, que se pueden instalar con el gestor
   ``conda`` (análogo a ``pip + virtualenv``) que viene incluído.

   Este *framework* grautuito simplifica muchísimo la instalación de un entorno
   de computación científica en Windows.

   La versión Miniconda_ instala sólo Python y conda. Luego podemos instalar paquetes
   desde la consola (``cmd.exe``). Por ejemplo::

      $ conda install ipython numpy mingw32

2. Configurar gfortran

   A través de ``conda`` puede instalarse MinGW, el conjunto herramientas GNU
   para tener un entorno de compilación basado en GCC en Windows. Esto incluye, entre otros, gfortran_.

   Anaconda wrappea ``gfortran.exe`` con el archivo batch ``c:/Anaconda/Scripts/gfortran.bat``.
   Modificarlo para que linkee estáticamente con *libgcc* y *libgfortran*. Quedaría así::

        @echo off
        %~f0\..\..\MinGW\bin\gfortran.exe -static-libgcc -static-libgfortran %*

3. Instalar lapack y blas

   Aun cuando la única virtud de Fortran es ser rápido para operaciones basadas en arrays,
   `no trae`_ una biblioteca estándar incorporada de "alto nivel".

   Para no tener que reinventar (*copypastear*) subrutinas todo el tiempo, se linkea con bibliotecas de terceros que, en general, utilizan una API común. [3]_

   Lapack_ es la más completa y mantenida biblioteca libre para algebra lineal, incluyendo rutinas de resolución de sistemas de ecuaciones lineales, factorización de matrices,
   etc. Esta se basa a su vez en BLAS
   que implementa las rutinas de más bajo nivel como rotación y producto de matrices.

   Todo código numérico no trivial utiliza alguna subrutina de Lapack/BLAS.

   Compilarlas en Windows es un lio, pero por suerte ya
   `lo hicieron otros <http://icl.cs.utk.edu/lapack-for-windows/lapack/index.html#libraries>`_.

   Hay que bajar ``libblas.dll`` y ``liblapack.dll`` (las que correspondan para tu arquitectura) y copiarlas en
   ``c:\Anaconda\MinGW\i686-w64-mingw32\lib`` y ``c:/windows/system32``

   Tambien bajar ``libblas.lib`` y ``liblapack.lib`` y ponerlas en
   ``c:\Anaconda\libs``


4. dlls en ``c:/windows/system32``


   Además de las bajadas, para que el programa se pueda ejecutar hace falta que Lapack encuentre las librerias de las que depende (ya que no está compilado de manera estática)

   Hace falta bajar `gcc-core-4.4.0-mingw32-dll.tar.gz <http://sourceforge.net/projects/mingw/files/MinGW/Base/gcc/Version4/Previous%20Release%20gcc-4.4.0/gcc-core-4.4.0-mingw32-dll.tar.gz/download>`_, descomprimirlo y copiar ``libgcc_s_dw2-1.dll``
   a ``c:/windows/system32``.

   También habrá que copiar allí algunas dll que ya vienen
   en la instación de MinGW (buscarlas en ``c:\Anaconda\MinGW\i686-w64-mingw32\lib``)::

     libgcc_s_sjlj-1.dll
     libgfortran-3.dll
     libquadmath-0.dll


5. Bajar libmsvcr90.a

   Desde `acá <https://github.com/enthought/vendor-mingw/blob/master/msvcrt/libmsvcr90.a?raw=true>`_ y ponerlo en la carpeta ``c:/Anaconda/libs/``

6. Compilar

    $ f2py --compiler=mingw32 -llapack -m hello -c hello.f90

7. Importar desde python y usar
8. Brindar.

.. _f2py: http://www.f2py.com
.. _no trae: http://www.nsc.liu.se/~boein/f77to90/a5.html
.. _Anaconda: https://store.continuum.io/cshop/anaconda/
.. _Miniconda: http://repo.continuum.io/miniconda/index.html
.. _gfortran: http://en.wikipedia.org/wiki/Gfortran
.. _Lapack: http://netlib.org/lapack
.. _otro: http://www.textosypretextos.com.ar
.. _Machinalis: http://machinalis.com
.. _Phasety: http://phasety.com
.. _deuda técnica: http://es.wikipedia.org/wiki/Deuda_t%C3%A9cnica
.. _fomentando: http://phasety.com/1/blog/article/curso-taller-python-para-ciencia-e-ingenieria




.. [1] o "terminé de dejar", porque estaba part-time desde septiembre de 2012.
.. [2] lo de "empresa pythónica", no
.. [3] La `MLK`_ de Intel es una biblioteca matemática optimizada para procesadores
       de esta firma. En la parte de algebra lineal utiliza la misma API de Lapack, pero
       no es libre y sale 500 verdes :).

.. _MLK: http://software.intel.com/en-us/intel-mkl


