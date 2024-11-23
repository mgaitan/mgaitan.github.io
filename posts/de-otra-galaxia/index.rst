Si el sábado a la noche antes de rendir tu última materia en vez de
estar estudiando estás emborranchandote por ahí, sos un inconciente y/o
la tenés muy clara. Si en cambio no estás estudiando ni emborrachando,
pero te ponés a pensar ejercicios para el `curso de
python <https://github.com/nqnwebs/python-ingenieria>`_ que estás dando,
sos un nerd. Mereces un brindis de chocolatada a tu salud de todos los
de `este
foro <http://www.whatthefolk.net/forum/viewtopic.php?f=13&t=338>`_.

Si encima blogueas al respecto, sos un nerd intergaláctico. Te explico
por qué.

Resulta que tenés este `archivo de
datos <https://github.com/nqnwebs/python-ingenieria/raw/master/data/data.txt>`_.
Cada número representa la intensidad de luz de un punto y te informan
que la imágen es cuadrada. Se supone que son datos que te dió un
profesor una vez, para que resuelvas este mismo problema en
¡ensamblador!

Hacerlo en Python, con Numpy y Matplotlib, significa estas líneas

::

    import numpy as np
    import matplotlib.pyplot as plt
    
    data = np.fromfile ('data.txt', sep=' ')
    SIZE = int(len(data) ** .5)
    data.shape = SIZE, SIZE 
    plt.imshow (data)
    plt.show ()

Y se obtiene este resultado:

.. figure:: local/cache-vignettes/L510xH385/galaxy-efc45.png
   :align: center
   :alt: 
Se puede limitar los valores de luz a un valor entre 0 y 255 (truncando
valores de saturación extrema), haciendo :

::

    plt.imshow (data.clip(0,255) )

Obtenemos este resultado:

.. figure:: local/cache-vignettes/L510xH385/galaxy-2-e0bc7.png
   :align: center
   :alt: 

