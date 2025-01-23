<!--
.. title: SVG animados para tus demos de programas CLI
.. slug: svg-animados-para-tus-demos-de-programas-cli
.. date: 2025-01-23 16:02:18 UTC-03:00
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text
-->

¿Querés mostrar lo piola que es tu programa de línea de comandos con una demo de un uso real? ¿Querés evitar que la demo quede desactualizada facilmente? ¿Querés incluir la demo en sitios que no permiten videos ni javascript como los `README` de Github o Pypi? 

¡Los SVG animados generados programáticamente son la solución! Se incrustan como una imágen normal pero son más livianos que los GIFs, se reproducen automáticamente en la misma página, no requieren javascript y mantienen el texto nítido sin importar el zoom. 

Además, automatizar tus demos te permite tener control total y regenerar el resultado visual de manera programática cuando la CLI cambie o quieras hacer cambios. 


Como ejemplo, acá la demo un programita que hice hace poco llamado [cuitonline](https://github.com/mgaitan/cuitonline) que luce así para su versión 0.1: 

<p align="center">
<img width="90%" src="https://raw.githubusercontent.com/mgaitan/cuitonline/refs/tags/0.1/demo/usage.svg" />
</p>

## ¿Cómo lo hacemos?

Vamos a utilizar las siguientes herramientas, todas open source. 

**[tuterm](https://github.com/veracioux/tuterm)**: Es una herramienta bash para crear demos de programas CLI. Se define un "script" (en el mejor sentido de la palabra) que permite controlar los comandos que se ejecutan (¡de verdad!) en la consola, que comentario mostrar y qué otros comandos auxiliares ejecutar. 


- **uvx**: Es el equivalente a `pipx` de [uv](https://github.com/astral-sh/uv). Lo usamos para ejecutar `asciinema` gestionando las dependencias e instalandolo en un entorno virtual automáticamente. 

- **[asciinema](https://docs.asciinema.org/manual/cli/)**: Graba sesiones de terminal y las guarda en un formato de texto. Por defecto estos archivos se suben y se comparten a traves de [asciinema.org](https://asciinema.org/), que es genial pero el reproductor requiere javascript lo que limita su uso. Por eso lo convertimos a SVG.  
  
- **[svg-term-cli](https://github.com/marionebl/svg-term-cli)**: Convierte grabaciones de asciinema en SVGs animados. 

## Paso a paso


### 1. Escribe el script

Siguiendo el ejemplo de `cuitonline` mostrado arriba. El script de `tuterm` lo llameé `usage.tutorial` con el siguiente contenido:

```bash
# file: > cuitonline_usage
prompt() {
 echo -ne "\033[1;35m\$ \033[0;33m"
}
configure() {
 DELAY=0.02
 DELAY_PROMPT=0.2
 COLOR_MESSAGE='1;32'
}

run() {
 M "Buscar por CUIT"
 c cuitonline 20-22293909-8
 sleep 3
 M "Buscar por DNI"
 c cuitonline 10433615
 sleep 3
 M "Busca por nombre"
 c cuitonline "messi lionel andres"
 sleep 3
 clear
 M "Obtiene la página 2 de los resultados"
 c cuitonline "juan jose gonzalez" -p2
 sleep 3
}
```

Las líneas que empiezan por `M ` son los comentarios. `c ` son comandos que se van a ver, y el resto son comandos que se van a ejecutar pero no se muestran tipeados. 


### 2. Graba la sesión de la terminal

Utiliza asciinema para grabar la sesión mientras tuterm ejecuta tu demo:

```bash
uvx asciinema rec --overwrite -c 'tuterm usage.tutorial --mode demo' usage.cast
```

### 3. Convierte la grabación en un SVG animado

Con svg-term-cli definimos el aspecto de la "consola" y convertimos la grabación en un SVG animado:


```bash
svg-term --window --width 75 --height 24 --padding 1 --in usage.cast --out usage.svg
```

### 4. Añade el SVG generado en tu archivo `README.md`

Por ejemplo si lo subis a `/demo/usage.svg` de tu repo, 

````markdown
<p align="center">
<img width="90%" src="https://raw.githubusercontent.com/<user>/<repo>/refs/heads/main/demo/usage.svg" />
</p>
````


¡Y listo! Ahora tenés una demo animada, nítida y mantenible programáticamente para tu programa CLI directamente en tu README de GitHub. 😎
