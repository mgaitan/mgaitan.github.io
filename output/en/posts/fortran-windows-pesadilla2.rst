.. link:
.. description:
.. tags:
.. date: 2013/08/24 11:11:45
.. title: Fortran + Windows = pesadilla^2
.. slug: fortran-windows-pesadilla2


Hace bastante que no escribo en este blog y no es porque tengo otro_, sino, principalmente, porque estoy con muchísimo trabajo.

Hace casi un mes dejé [1]_ de trabajar en Machinalis_, una de las empresas más pythónicamente grosas del mundo mundial [2]_, en la que inevitablemente aprendí muchísimo
(y eso que me esforcé ;-)), hice amigos y laburé en proyectos de una escala y complejidad a la que nunca podría haber aspirado como un "freelance *che pibe* programador".

Ahora laburo fulltime (o sea: el triple) en Phasety_, el proyecto que estamos creando junto a Martín Cismondi, director de mi proyecto integrador de grado hace algunos años ("ingeniero en computación", dice el pelpa) y hoy socio. Cismondi es doctor en ingeniería
química y uno de los especialistas más reputados a nivel mundial en el área "equilibro de fases", que es, básicamente, modelar el comportamiento termodinámico de un fluido mediante algoritmos numéricos.

Un poco por cierta "inercia cultural" del mundo científico (en particular en las área de química computacional) y otro poco porque sigue siendo increíblemente eficiente para rutinas de cálculo, Fortran es el lenguaje predominante en el que los tipos
como Cismondi programan. A lo que si le sumás Windows, las bibliotecas privativas y un flujo de trabajo atado al IDE que aprendieron a "clickear" (en general, Visual Studio),
es todo un problema.

Así que parte de mi laburo es sumergirme en este escabrozo mundo y meter ingeniería de software allí donde nunca la hubo.

Por suerte existe Python, pisando cada vez más fuerte en el mundo de la ciencia y la ingeniería (http://scipycon.com.ar/, como ejemplo). Pero, mientras seguimos minimizando
la `deuda técnica`_ fomentando_ esta tecnología, hay que hacerlas convivir.

f2py, gfortran y lapack en Windows
----------------------------------

Estas son notas de lo que he ido logrando hasta el momento en el intento de armar un entorno de desarrollo y empaquetamiento (en lo posible, libre) de software multiplataforma basado en Python y Fortran.

Como se sabe, el "San Valentín" de esta pareja es f2py_, una herramienta que genera los wrappers necesarios para convertir subrutinas (o funciones) de Fortran en módulos binarios (bibliotecas) importables desde Python.

No abordo acá los detalles de cómo usar f2py (aunque `este <http://websrv.cs.umt.edu/isis/index.php/F2py_example>`_ es un buen ejemplo), sino cómo conseguir que funcione para un ejemplo no trivial en windows, compilando con gfortran y linkeando con la biblioteca Lapack.


1. Instalar Anaconda_, de Continuum Analytics.

   Anaconda es una distribución de Python y una amplia colección de paquetes
   y bibliotecas para computación científica, que se pueden instalar con el gestor
   ``conda`` (análogo a ``apt-get + pip + virtualenv``) que viene incluído.

   Este *framework* gratuito simplifica muchísimo la instalación de un entorno
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


.. tip::

    podés bajar todos los archivos mencionados desde el paso 3 al 5
    (para 32bits) desde `este zip <https://docs.google.com/file/d/0Bx300vaUNYn1cDVva0FGaEFQTFE/edit?usp=sharing>`_


3. Instalar lapack y blas

   Aún cuando la única virtud de Fortran es ser eficiente para operaciones basadas en arrays, `no trae`_ una biblioteca estándar incorporada de "alto nivel".

   Para no tener que reinventar (*"copypastear"*) subrutinas todo el tiempo, se linkea con bibliotecas de terceros que, en general, utilizan una nomenclatura común para las
   signaturas. [3]_

   Lapack_ es la más completa y mantenida biblioteca libre para álgebra lineal, incluyendo rutinas de resolución de sistemas de ecuaciones lineales, factorización de matrices,
   etc. Se basa a su vez en la biblioteca BLAS
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


6. Listo! Si todo salió bien, ya podés compilar en windows modulos python
   implementados en fortran


Como ejemplo,  podés probar con esta subrutina que hace lo mismo que
``numpy.linalg.solve`` (resolver un sistema lineal Ax=b), basada en la rutina ``SGESV``
de lapack (para simple precisión).

.. code-block:: fortran

    subroutine solve(A, b, x, n)
        implicit none

        ! solving the matrix equation A*x=b using LAPACK
        ! declarations, notice single precision
        real, dimension(n,n), intent(in) :: A
        real, dimension(n), intent(in) :: b
        real, dimension(n), intent(out) :: x

        integer :: i, j, pivot(n), ok

        integer, intent(in) :: n

        ! find the solution using the LAPACK routine SGESV
        call SGESV(n, 1, A, n, pivot, b, n, ok)

        ! copy the vector x
        x = b

    end subroutine

Lo guardamos en un archivo llamado ``linalg.f90`` y compilamos::

    $ f2py --compiler=mingw32 -llapack -m linalg -c linalg.f90

Se creeará un archivo ``linalg.pyd`` que es importable desde Python.

.. code-block:: python

    In [1]: from linalg import solve

    In [2]: solve?
    Type:       fortran
    String Form:<fortran object>
    Docstring:
    solve - Function signature:
      x = solve(a,b,[n])
    Required arguments:
      a : input rank-2 array('f') with bound
      b : input rank-1 array('f') with bound
    Optional arguments:
      n := shape(a,0) input int
    Return objects:
      x : rank-1 array('f') with bounds (n)

    In [3]: import numpy

    In [4]: A = numpy.array([[1, 2.5], [-3, 4]])

    In [5]: b = numpy.array([1, 2.5])

    In [6]: solve(A, b)

    Out[6]: array([-0.19565217,  0.47826087], dtype=float32)


Que es lo mismo que

.. code-block:: python

    In [7]: numpy.linalg.solve(A, b)
    Out[7]: array([-0.19565217,  0.47826087])


¡Salud!

.. note:: por supuesto, queda resolver lo del IDE (especialmente el debugger)
          sin el cual los cientificosprogramadores Fortran se quedan rengos.
          Cualquier recomendación es bienvenida.


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
.. [2] lo de "empresa pythónica", lo digo `en serio <http://www.python.org/dev/peps/pep-0020/>`_
.. [3] La `MLK`_ de Intel es una biblioteca matemática optimizada para procesadores
       de esta firma. En la parte de algebra lineal utiliza la misma API de Lapack, pero
       no es libre y sale 500 verdes :).

.. _MLK: http://software.intel.com/en-us/intel-mkl


