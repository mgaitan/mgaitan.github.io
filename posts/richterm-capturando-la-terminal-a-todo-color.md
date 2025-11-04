<!--
.. title: richterm, capturando la terminal a todo color
.. slug: richterm-capturando-la-terminal-a-todo-color
.. date: 2025-11-03 22:26:32 UTC-03:00
.. tags: cli, rich, terminal
.. category: projects
.. link:
.. description:
.. type: text
-->

Siempre estoy haciendo programitas de línea de comando y siempre quiero mostrar como se ve el resultado de algun comando. Si bien es texto que puedo copiar y pegar, muchas veces prefiero tomar capturas de pantalla de la terminal para mostrar como se ve el resultado, especialmente si tiene colores o algun formato especial.

Cuando estaba escribiendo [este post](https://mgaitan.github.io/posts/un-cheatsheet-automatico-para-tu-cli-typer/) necesitaba una captura, y encontré una manera de hacerlo:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Tired of taking manual screenshots for CLI examples?<br>Try this:<br><br>$ alias rich-capture=&#39;uvx rich-codex --no-search --skip-git-checks --use-pty --no-confirm --img-paths cli_$(date -I).svg --command&#39;<br><br>Then use it as a wrapper of your command. Eg. <br>$ rich-capture &quot;uv run -m rich&quot; <a href="https://t.co/U18Dr7p2Df">pic.twitter.com/U18Dr7p2Df</a></p>&mdash; Martín Gaitán ⭐⭐⭐ (@tin_nqn_) <a href="https://twitter.com/tin_nqn_/status/1983986531972116685?ref_src=twsrc%5Etfw">October 30, 2025</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>x.com//1983986531972116685

El truco que propuse ahí es usar [rich-codex](https://ewels.github.io/rich-codex/) pero, a decir verdad, la CLI de esta herramienta es un bastante complicada para este caso súper común: sólo quiero ejecutar un comando y quedarme con un SVG listo para incrustar en un post o en la documentación.

Así que me armé una mini herramienta más simple: [**richterm**](https://github.com/mgaitan/richterm).

<!-- TEASER_END -->

### ¿Qué hace?

Ejecutás `richterm <comando>` y te genera `rich_term_<timestamp>.svg` con la salida ANSI, respetando todos los colores. También escribe la salida en `stdout` así el flujo normal de la terminal no se rompe.

En su caso más trivial, no tenés que acordarte de ninguna opción exótica. Ejemplo rápido:

```bash
uvx richterm python -m rich.tree
```

Listo, SVG fresquito en el directorio actual. Se ve así:

<object data="/images/rich_term_20251103_222031.svg" type="image/svg+xml" width="80%" title="rich.tree"></object>

Tip: Para incrustar en markdown/html, en vez de una etiqueta `<img>` preferí, si podés, usar `<object data="<path>" type="image/svg+xml"></object>` así las referencias inline de fuentes del svg funcionan, resolviendo las ligaduras.

Si preferís instalarlo:

```bash
uv tool install richterm
```

Opciones mínimas:

- `-o archivo.svg` si querés controlar el nombre.
- `--prompt` para tunear el prompt con markup de Rich. Por ejemplo:

  ```
  uvx richterm --prompt "[bold green]λ " git status --short
  ```
- `--hide-command` si querés ocultar la línea de comando del render.

## richterm como extensión de Sphinx

Además del CLI funciona como una extension de Sphinx, agregando la directiva `richterm::`.

En [la docu](http://mgaitan.github.io/richterm) uso la extensión incluída. En `conf.py` agregás `"richterm.sphinxext"` y listo. Después en cualquier página podés poner:

````rst
```richterm:: uv run -m rich
```
````

O su equivalente markdown si usás [myst-parser](https://myst-parser.readthedocs.io/en/latest/):

````md
```{richterm} uv run -m rich
```
````

Cuando compiles tu proyecto Sphinx ejecutará el comando e incrustará el SVG resultante en el HTML. Cero esfuerzo.

### ¿Cómo funciona?

Usa subprocess para ejecutar el comando y capturar la salida. Luego rich's [`from_ansi()`](https://rich.readthedocs.io/en/stable/reference/text.html#rich.text.Text.from_ansi) para interpretar potenicales códigos ANSI y [export_svg()](https://rich.readthedocs.io/en/stable/reference/console.html#rich.console.Console.export_svg) para guardar el svg.

El repo es [github.com/mgaitan/richterm](https://github.com/mgaitan/richterm). Feedbacks, issues, PRs ¡todo bienvenido! 🎨

PS: Si querés algo un poquito más sofisticado (¡svg animados!) fijate [este otro post](
https://mgaitan.github.io/posts/svg-animados-para-tus-demos-de-programas-cli/)
