.. title: Miau: cuando el gato dice la verdad
.. slug: miau-cuando-el-gato-dice-la-verdad
.. date: 2018-05-09 16:36:18 UTC-03:00
.. tags:
.. category:
.. link:
.. description:
.. type: text

Cuando se cumplieron los primeros 7 meses de su gestión, el presidente Macri dió `una entrevista exclusiva <https://www.youtube.com/watch?v=Jp8_BXkTqXk>`_ a periodistas del canal Telefé. Horas después apareció este video en las redes, cuyo autor o autora desconozco:

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/C8e6Fibx0k0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

Ahí estaba el humor, el fruto más gozoso del ingenio popular, para salvarnos a carcajadas. No para evadirnos de la realidad sino, al contrario, para vencerla, para enfrentar la amargura que algunas certezas traen (ya sabíamos a esa altura, con devaluación a precios y tarifazos en curso, que las advertencias no habían sido una "campaña del miedo"). Pero era aún más: era un ejemplo de ese humor que enuncia verdades difíciles de escuchar de otra manera.

Simplemente me pareció genial. Me acordé, por supuesto, de la `entrevista a Homero <https://www.youtube.com/watch?v=Lz__bWnUMFQ>`_ en el capítulo de la Venus de jalea y también de un cortometraje español que ví hace mucho titulado "`Lo que tú quieras oir <https://www.youtube.com/watch?v=12Z3J1uzd0Q>`_", cuyo argumento se basa exáctamente en la creación de un *mash-up* de audio como alivio de una situación dramática.

Cada discurso o entrevista de Macri me parecía (me parece) un puesta en escena cínica, plagada de mentiras, floja de fonética y con pésimo acting. Necesitaba más de estos videos que le hagan decir la verdad.

.. TEASER_END

El maravilloso compositor Jorge Fandermole `escribió <https://www.letras.com/jorge-fandermole/946693/>`_


    *Canto, canto,*

    *tan débil soy que cantar es mi mano alzada y fuerte.*

    *Canto, canto,*

    *no sé más qué hacer en esta tierra incendiada*

    *sino cantar.*

Parafraseando (bastante lejos de esa belleza) yo podría decir:

.. code-block::

    print("programo, programo, programar es mi mano alzada y fuerte...")

Asi que ante la falta de talento natural para la edición audiovisual (entre todo el resto de las cosas), programé. Y así fue como hice un programita en Python que hace las ediciones por mí: `miau <http://github.com/mgaitan/miau>`_.

Sólo hay que darle la desgrabación del discurso original completo y el guión del discurso pretendido (basado en fragmentos textuales del original, en el orden que sea) y ``miau`` se encarga de encontrar, recortar y concatenar para armar un clip de video o un audio remixado.

Por ejemplo este en el que Macri reconoce las verdaderas razones que nos llevaran de vuelta a deberle al FMI.

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/axH1AUDZw_8" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

o este audio donde reconoce que niega los problemas

.. raw:: html

    <iframe width="100%" height="300" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/442231311&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true"></iframe>


O este otro en el acepta que están haciendo fantochadas y van a salir "para arriba" en cualquier momento:

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/YtY_CRiFKPY" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>



Agarrá la pala (o copiá y pegala)
---------------------------------

Si bien los excelsos discursos presidenciales suelen ser breves, ¿de verdad te fumás tener que desgrabar toda esa sarta de duranbarbaridades, Martincito?

Pues no, al menos para el caso específico de este felino doméstico. Gracias a que `casarosada.gob.ar <http://www.casarosada.gob.ar>`_ se toma el trabajo de conservar cada palabra de la retórica sublime, de estadismo profundo y condensado que será aplaudido por generaciones, de esas piezas de discurso político que interpelan hasta al más indiferente... Bueno, quiero decir, gracias a que guardan el txt de las 30 frases en distinto orden que le escriben, no hace falta desgrabar nada.

Alcanza con ir `acá <https://www.casarosada.gob.ar/informacion/discursos>`_, copiar un discurso y guardarlo en un txt, y luego `allá <https://www.youtube.com/user/casarosada/videos>`_ para bajarse el video que corresponda (por ejemplo, usando el genial `youtube-dl <https://rg3.github.io/youtube-dl/>`_), y ya tenemos todo el material de entrada necesario para mofarnos de estos fugadores un buen rato. Si a esos contenidos los guardamos, supongamos, como ``macri_gato.txt`` y ``macri_gato.mp4``, y a nuestro remix lo guardamos como ``remix.txt``, podemos hacer un *supercut* en mp3 así::

    $ miau macri_gato.mp4 macri_gato.txt -r remix.txt -o macri_gato_remixado.mp3

y casi lo mismo si queremos hacer un video::

    $ miau macri_gato.mp4 macri_gato.txt -r remix.txt -o macri_gato_remixado.mp4

.. tip:: te conviene siempre laburar primero generando audios y cuando estes conforme haces el video, ya que es mucho más rápido el recorte y concatenado.

Como la detección de fragmentos no es infalible, hay que meterle laburo de prueba y error y a veces hay que ajustar un poquito los tiempos detectados automáticamente (sobre todo cuando se recortan palabras sueltas o frases muy breves).

Eso se puede hacer de dos maneras:

- Reusar el json intermedio que se produce con `--dump`, editarlo a gusto y pasarlo a una nueva ejecución de miau en reemplazo del txt de remix a ``-r``. Este paso lo que hace justamente es saltearse la alineación automática y usar lo que le damos explícitamente.

- Ponerle una metadata de ajuste al propio txt. La sintáxis que definí es un poco minimalista y se basa en ponerle signos ``+`` y ``-`` al final y/o al principio de cada linea, para estrechar o ensanchar el recorte. Cada símbolo equivale, por default, a 0.05s. Por ejemplo, si en el remix hay una línea que dice *"el único camino posible"* y nos damos cuenta que la detecta un instante tarde y la interrumpe antes de terminar, podemos corregirla poniendo un offset negativo al principio y uno positivo al final:

  .. code-block::

    --el único camino posible+++``

  Miau filtra la línea con una función que hace esto:

  .. code-block:: python

       >>> fine_tuning('--el único camino posible+++'):
       {'el único camino posible': {'start_offset': -0.1, 'end_offset': 0.15}}

En github fui dejando `algunos ejemplos <https://github.com/mgaitan/miau/tree/master/examples>`_ con los pasos y las fuentes con los que los hice.

Vale resaltar que esta herramienta **es software libre**, lo que quiere decir que no necesariamente tenés que usarla
para burlarte de gobiernos de derecha y podés hacer con ella lo que te plazca. ¡Hacele decir a la tía Berta eso que nunca dijo (o al menos no de esa textual manera) en Whatsapp!


Deconstruyendo el relato, con Python
------------------------------------

A este tipo de videos se le llaman "`supercuts <
https://en.wikipedia.org/wiki/Supercut>_" y hay distintas maneras de hacerlos.
De hecho, sin saberlo entonces, hace un tiempo hice `uno sobre Sergio Massa <http://mgaitan.github.io/posts/sergio-massa-y-lagente.html>`_, basado en fragmentos de los subtitulos automáticos de youtube. También hay una `herramienta en python <https://github.com/antiboredom/videogrep>`_ que permite hacer un "grep" en el video.

Yo quería algo un poquito más ambicioso, algo que permita la generación de cualquier edición posible y que sea más o menos fácil para cualquiera con ganas de hacerla.

Descubrí que existía software que se ocupa de la parte difícil: reconocer frases en un audio y generar las marcas de tiempo
de su ubicación. Es algo que se llama `forced aligment <http://linguistics.berkeley.edu/plab/guestwiki/index.php?title=Forced_alignment>`_ y hay una biblioteca en Python, hecha por un academico italiano, que anda al pelo: `aeneas <https://github.com/readbeyond/aeneas>`_. Anda tan bien que hasta acierta la mayoría de las veces con la dicción de Mauricio Macri, ¡imaginensé!. De yapa, soporta ("entiende") múltiples idiomas.

Si te dan un "buscador de audio" que te dice el inicio y final de una frase en un discurso, el resto es más o menos fácil. Sólo hay que saber recortar por la línea punteada, hacer una pila con los pedacitos y pegarlos unos con otros. Para eso `moviepy <https://github.com/Zulko/moviepy>`_ es mucho más que suficiente.

Sólo había una sutil complicación. ``aeneas`` requiere la desgrabación completa correspondiente al discurso a fragmentar, y en su forma de uso más general, asume que cada fragmento a encontrar es una linea del texto de entrada.

Por ejemplo, supongamos, que este es el "verso" original::

    Buenos días: ustedes saben que tengo un compromiso de decirles la verdad siempre;
    también que me metí en política y me postulé para la Presidencia para trabajar todos los días.

Si de allí quisiéramos pedirle a aeneas que recorte la frase "tengo un compromiso"  y *me postulé para la Presidencia*, habría que reformatear el texto completo separando en lineas de la siguiente manera::

    Buenos días: ustedes saben que
    tengo un compromiso
    de decirles la verdad siempre; también que me metí en política y
    me postulé para la Presidencia
    para trabajar todos los días.

Es decir, forzar que cada fragmento objetivo se encuentre textualmente en una fila independiente. El problema es que cabe la posiblidad de que queramos fragmentos que se solapan entre sí. Por ejemplo, si además de los anteriores quisiéramos *"me metí en política y me postulé"*, no tendríamos manera de cumplir con la regla de las filas independientes ya que *"me postulé"* debería estar repetido en dos renglones.

Por ese motivo ``miau`` hace tantas versiones de fragmentado del texto original como encuentre necesarias para salvar estos solapamientos. Esas son las *iteraciones* que se corresponden con sendas llamadas a aeneas.


Vermuth con software libre y ¡good show!
----------------------------------------

Aunque es divertidísimo (es decir, es totalmente redituable), mantener software de humor político tiene sus costos, sobre todo cuando tenés más de un laburo, una familia, algun@s amig@s y varios libros a los que tenés que dedicarle tiempo.

El tema es que ``miau`` anda masomenos. O como el culo, seamos sinceros. Y, saben, yo no puedo ni quiero pedirle un *stand-by* al Fondo Monetario, porque sé como termina esa ayudita. Por eso te pido a vos, programador/a, expert o wannabe, que me des una mano. Por ahora no son mucho más de 300 líneas de código en un solo módulo que `no hacen nada demasiado raro <import antigravity>`_, así que la zambullida para poder colaborar es accesible.

¿Y cómo? En este orden: usándolo, encontrando errores (que vamos anotando en el `issue tracker <https://github.com/mgaitan/miau/issues>`_), desculando por qué suceden y por último arreglándolos. También es indispensable tener pruebas unitarias, así no rompemos tanto nuevo cuando vamos arreglando lo viejo. Y hay funcionalidades que me gustaria completar, como la de permitir múltiples fuentes de entrada para hacer ediciones más complejas y ampliar la base de frases.

A futuro sería genial que tenga otras "atractividades" como una linda interfaz gráfica, que sea fácil instalarlo en cualquier sistema operativo (y particularmente en Windows) y, por qué no, que se convierta en el core de una app web (o la API REST para un app mobile) que permita usarlo directamente desde la nube.

Espero sus tickets y pull requests.

¡A maullar esos remixes!