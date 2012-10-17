Hace 5 años que laburo en `una
organización <http://www.agrupacionmazamorra.com.ar>`_ de trabajo
barrial. Como no recibimos aportes privados y rara vez del Estado (a
veces presentamos proyectos a programas) siempre andamos buscando formas
de sostener económicamente nuestras actividades.

Un recurso, no por viejo en desuso, es el del *"bono contribución"*, que
muchas veces incluye un sorteo con algún premio.

Además de la algo ingrata tarea de venderlos, hay que hacerlos. Alguno
tiene uno de esos sellos numeradores (un mecanimismo que va
incrementando el contador automáticamente ) pero igual cualquiera se
vuelve un burócrata (más cuando hay que sellar dos veces - el bono y
talón -).

Así que ayer, en 20 minutos hice *Bonito*, un programa feo pero
efectivo.

Primero hice una plantilla en `Inkscape <http://inkscape.org>`_ donde
entran 6 de estos bonitos en un A4.

.. figure:: local/cache-vignettes/L500xH117/bonito2-ccc74.png
   :align: center
   :alt: 
Como el SVG es XML que es TEXTO, la marca XXXX se puede reemplazar
fácilmente por el número que corresponda. Yo quería que me quedaran así:

.. figure:: local/cache-vignettes/L400xH436/bonito-8305a.png
   :align: center
   :alt: 
De esta manera, simplemente tengo que meter 6 broches a la izquierda y
recortar, ya quedan ordenados para repartir entre los compañeros y
compañeras.

Para algunas cosas, Inkscape se puede usar por línea de comandos, por
ejemplo para convertir entre los formatos que soporta. Así paso el SVG
con los números reemplazados a un PDF. Después concateno todos los PDF
de una tanda (por ejemplo agrupados de a 10, como en el dibujo) con
Ghostscript.

Acá el código:

::

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    #
    #       bonito.py
    #       
    #       Copyright 2010 Martin Gaitán <gaitan(at)gmail.com>
    #       
    #       This program is free software; you can redistribute it and/or modify
    #       it under the terms of the GNU General Public License as published by
    #       the Free Software Foundation; either version 2 of the License, or
    #       (at your option) any later version.
    #       
    #       This program is distributed in the hope that it will be useful,
    #       but WITHOUT ANY WARRANTY; without even the implied warranty of
    #       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    #       GNU General Public License for more details.
    #       
    #       You should have received a copy of the GNU General Public License
    #       along with this program; if not, write to the Free Software
    #       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
    #       MA 02110-1301, USA.

    import sys, os
    import subprocess
    import glob

    def markToNum(content, num, mark='XXXX'):
        num_as_string = '0' * (4 - len(str(num))) + str(num)
        return content.replace(mark, num_as_string, 2)

    def main():
        
        if len(sys.argv) <= 1:
            print "Modo de uso:"
            print sys.argv[0] + " archivo.svg"
            sys.exit(1)
        else:
            with open(sys.argv[1]) as input:
                svg_content = input.read()
            
            index_from = int(raw_input('Desde [0]') or 0)
            number_by_page = int(raw_input('Num por pagina [6]') or 6)
            grouped_by =  int(raw_input('agrupar de a [20]') or 20)
            planchas = int(raw_input('Planchas [1]') or 1)

            
            for plancha in range(planchas):
                counter_from = index_from + plancha*number_by_page*grouped_by

                for pagina in range(grouped_by):
                    page_content = svg_content
                    for bono in range(number_by_page):
                        num_remplazo = counter_from + bono*grouped_by + pagina
                        page_content = markToNum(page_content, num_remplazo)
            
                    with open('temp.svg', 'w') as output_svg:
                        
                        output_svg.write(page_content)

                    subprocess.call(["inkscape", "-f", 'temp.svg', '--export-dpi=150', '-A', 'temp%s.pdf' % ("0"*(4 - len(str(pagina))) + str(pagina)) ])

                generator = ['gs',
                             '-q',
                             '-sPAPERSIZE=a4',
                             '-dNOPAUSE',
                             '-dBATCH',
                             '-sDEVICE=pdfwrite',
                             '-sOutputFile=%s-%i-%i.pdf' % (sys.argv[1][:-4], counter_from, num_remplazo),] + \
                            ['temp%s.pdf' % ("0"*(4 - len(str(pagina))) + \
                                str(pagina)) for pagina in range(grouped_by)]

                subprocess.call(generator)

                for temp in glob.glob('temp*'):
                    os.remove(temp)

    if __name__ == '__main__':
        main()

Nada que no se pueda hacer con Bash, cierto, pero mucho más fácil de
escribir (y de leer).

De paso, acá está la plantilla, por si a alguno le sirve.
