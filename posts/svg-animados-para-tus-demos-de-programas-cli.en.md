<!--
.. title: Animated SVGs for your CLI program demos
.. slug: animated-svgs-for-your-cli-program-demos
.. date: 2025-01-23 16:02:18 UTC-03:00
.. tags:
.. category:
.. link:
.. description:
.. type: text
-->

Want to show off how cool your command-line program is with a demo of real-world usage? Want to avoid your demo easily becoming outdated? Want to include the demo on sites that don't allow videos or JavaScript, like GitHub or Pypi `README` files?

Animated SVGs generated programmatically are the solution! They are embedded like a normal image but are lighter than GIFs, play automatically on the same page, don't require JavaScript, and keep the text sharp regardless of zoom.

Plus, automating your demos gives you total control and lets you programmatically regenerate the visual result when the CLI changes or you want to make changes.

As an example, here's a demo of a little program I made recently called [cuitonline](https://github.com/mgaitan/cuitonline) which looks like this for its 0.1 version:

<p align="center">
<img width="90%" src="https://raw.githubusercontent.com/mgaitan/cuitonline/refs/tags/0.1/demo/usage.svg" />
</p>

## How do we do it?

We're going to use the following tools, all open source.

**[tuterm](https://github.com/veracioux/tuterm)**: It's a bash tool for creating demos of CLI programs. You define a "script" (in the best sense of the word) that lets you control the commands that are executed (for real!) in the console, what comment to show, and what other auxiliary commands to run.

- **uvx**: It's the equivalent of `pipx` for [uv](https://github.com/astral-sh/uv). We use it to run `asciinema` managing dependencies and installing it in a virtual environment automatically.

- **[asciinema](https://docs.asciinema.org/manual/cli/)**: Records terminal sessions and saves them in a text format. By default, these files are uploaded and shared through [asciinema.org](https://asciinema.org/), which is great, but the player requires JavaScript, which limits its use. That's why we convert it to SVG.

- **[svg-term-cli](https://github.com/marionebl/svg-term-cli)**: Converts asciinema recordings into animated SVGs.

## Step by step

### 1. Write the script

Following the example of `cuitonline` shown above. I named the `tuterm` script `usage.tutorial` with the following content:

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

Lines that start with `M ` are the comments. `c ` are commands that will be seen, and the rest are commands that will be executed but are not shown being typed.

### 2. Record the terminal session

Use asciinema to record the session while tuterm runs your demo:

```bash
uvx asciinema rec --overwrite -c 'tuterm usage.tutorial --mode demo' usage.cast
```

### 3. Convert the recording into an animated SVG

With svg-term-cli we define the appearance of the "console" and convert the recording into an animated SVG:

```bash
svg-term --window --width 75 --height 24 --padding 1 --in usage.cast --out usage.svg
```

### 4. Add the generated SVG to your `README.md` file

For example, if you upload it to `/demo/usage.svg` of your repo,

````markdown
<p align="center">
<img width="90%" src="https://raw.githubusercontent.com/<user>/<repo>/refs/heads/main/demo/usage.svg" />
</p>
````

And that's it! Now you have an animated, sharp, and programmatically maintainable demo for your CLI program directly in your GitHub README. 😎
