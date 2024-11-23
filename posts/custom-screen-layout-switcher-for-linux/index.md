<!--
.. title: Screen layout switcher para Linux
.. slug: custom-screen-layout-switcher-for-linux
.. date: 2021-04-12 13:52:34 UTC-03:00
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text
-->

Mi setup de trabajo consiste en la laptop (Lenovo x1 del 2015), un monitor externo de 22" y un combo teclado + mouse inalambrico [del supermercado](https://www.cotodigital3.com.ar/sitios/cdigi/producto/-teclado-top-house-wireless-combo-mouse-kb592gcm/_/A-00484043-00484043-200). Actualmente estoy usando [Pop!_OS](https://pop.system76.com/)

El monitor está en un [brazo](https://www.oneboxsolutions.com.ar/producto/ob-lcd12/) que me permite acomodarlo y girarlo en cualquier posición. El brazo está en una pequeña alzada que me permite ganar unos 13cm de altura, de manera que puedo usarlo para hacer standup desk junto con mi mesita. 

<blockquote class="twitter-tweet"><p lang="es" dir="ltr">Hoy terminé mí mesita para trabajar parado. Con el brazo para monitor suplementado la altura queda bastante razonable y también puedo usarla con el tele vía chromecast <a href="https://t.co/O6RLKogCO7">pic.twitter.com/O6RLKogCO7</a></p>&mdash; Martín Gaitán (@tin_nqn_) <a href="https://twitter.com/tin_nqn_/status/1304951373482647553?ref_src=twsrc%5Etfw">September 13, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>


Trato de trabajar al menos la mitad del día parado y a veces me voy con la compu a otra parte de la casa. Así que todo el tiempo estoy cambiando la configuración de la/s pantalla/s. Hacer esta tarea a mano me llevaba mucho tiempo y además es dificilisima la motricidad con el mouse si la pantalla está girada.  

Dentro del soporte de "funciones avanzadas de teclado" de los linux modernos está "switch-monitor". Gnome mapea esta funcion con `<Super>+P` además de la tecla especial del teclado. 

```
$ gsettings get org.gnome.mutter.keybindings switch-monitor
['<Super>p', 'XF86Display']
```

El problema con esta funcionalidad es que los modos están predefinidos: monitores espejados, sólo externa, sólo integrada o ambas "unidas" pero asumiendo ambas horizontales y el monitor izquierdo a la derecha (y el mio queda a la izquierda de la laptop). 


[Pregunté en twitter](https://twitter.com/tin_nqn_/status/1380947297777901570) y varios amigos me apuntaron a la herramienta 
[arandr](https://christian.amsuess.com/tools/arandr/) que permite hacer las mismas configuraciones de pantallas que la herramienta de Gnome (de manera manual y visual) con la diferencia de que los modos definidos se pueden guardar como un comando de xrandr. Por ejemplo este setup de ambas pantallas encendidas y horizontales 

![arandr example](https://user-images.githubusercontent.com/2355719/114436452-b7c04780-9b9b-11eb-9b0f-1c7bc1c2da04.png)

se guarda desde arandr (¡y se puede abrir para editar!) como un script 

```
(blog) tin@pop-os:~/.screenlayout$ cat 2horizontal.sh 
#!/bin/sh
xrandr --output eDP-1 --mode 1920x1080 --pos 1920x283 --rotate normal --output DP-1 --off --output HDMI-1 --off --output DP-2 --off --output HDMI-2 --primary --mode 1920x1080 --pos 0x0 --rotate normal
```

Asi es que definí con esa herramienta los modos frecuentes que uso

```
~/.screenlayout$ ls *.sh
2horizontal.sh  ext-horizontal.sh  ext-vertical.sh  lapt-solo.sh
```

Lo que quería luego era un atajo de teclado que me permitiera rotar entre esos modos. Hice un script en python que lo dejé en la misma carpeta

```python
#!/usr/bin/env python3
import itertools
import subprocess
from pathlib import Path

folder = Path(__file__).absolute().parent
layouts = itertools.cycle(list(folder.glob('*.sh')))  # roundrobin over the layouts. 


try:
    # if there is a last used, move to the next one
    last = (folder / '.last').read_text()
    print("last found", last)
    layouts = itertools.dropwhile(lambda x: str(x) != str(last), layouts)
    next(layouts)   
except FileNotFoundError:
    pass 


current = next(layouts)
print(f"switching to {current.name}")
# write the last
(folder / '.last').write_text(str(current))

subprocess.call([str(current)])
```

Este `switcher.py` busca todos los archivos `.sh` en la misma carpeta y ejecuta el que sigue al ultimo ejecutado, que se guarda en un archivo `.last` (si no existe, el primer modo será el primero listado). 


Decidí deshabilitar el atajo por default 

```
$ gsettings set org.gnome.mutter.keybindings switch-monitor "['XF86Display']
```

y agregué un shortcut que ejecuta `~/.screenlayout/switcher` con `Ctrl + Super + P` (en gnome: Configuración -> Keyboard -> Combinación de teclas -> Customize Shortcuts -> Combinación Personalizada )

![image](https://user-images.githubusercontent.com/2355719/114437517-0a4e3380-9b9d-11eb-8847-1d6ebdd61f16.png)


Ahora puedo pararme cuando quiera, levantar y girar el monitor y apretar 
`Ctrl + Super + P` las veces necesarias hasta que quede como quiero. 