<!--
.. title: Un cheatsheet automático para tu CLI Typer
.. slug: un-cheatsheet-automatico-para-tu-cli-typer
.. date: 2025-10-30 19:18:39 UTC-03:00
.. tags: cli
.. category:
.. link:
.. description:
.. type: text
-->

[Typer](https://typer.tiangolo.com/) es gran framework de CLIs del mismo autor que creó [FastAPI](https://fastapi.tiangolo.com/). Permite crear interfaces de línea de comandos robustas e intuitivas basándose en anotaciones sobre los argumentos de funciones. Sin hacer mucho esfuerzo te ofrece autocompletado y ayuda en línea de comandos, que de paso se ve muy bonita al estar basada en [rich](https://rich.readthedocs.io/).

También permite facilmente registrar grupos de comandos y subcomandos, lo que facilita la organización y mantenimiento de aplicaciones grandes. Pero, ¿qué pasa cuando tu aplicación crece, con múltiples subcomandos, grupos y opciones anidadas?

Para los usuarios (¡o incluso para vos mismo después de un tiempo!), puede ser un desafío recordar todos los comandos disponibles, sus funciones y cómo interactúan. La ayuda integrada y la documentación son clave, pero **¿no sería fantástico tener un "mapa" en vivo de tu aplicación, accesible directamente desde la terminal?**

¡Acá es donde entra [typer-cheatsheet-command](https://github.com/mgaitan/typer-cheatsheet-command)!

<!-- TEASER_END -->

 `typer-cheatsheet-command` es una pequeña biblioteca que escribí que te permite agregar un subcomando `cheatsheet` a tu programa basado en Typer. Este comando instrospecciona la aplicación y genera una  representación en formato de árbol de todos tus comandos y subcomandos.

Por ejemplo, una aplicación Typer llamada `typer-cheatsheet-demo` tiene algunos comandos y subcomandos:

```python
import typer

app = typer.Typer(name="demo", help="demo")

users_app = typer.Typer(help="Manage users in the system.")

@users_app.command("add")
def add_user(username: str):
    """Adds a new user."""
    print(f"Adding user: {username}")

@users_app.command("delete")
def delete_user(username: str):
    """Deletes an existing user."""
    print(f"Deleting user: {username}")

app.add_typer(users_app, name="users")

@app.command()
def generate_report(month: str):
    """
    Generates a monthly report.
    """
    print(f"Generating report for {month}...")

@app.command()
def configure():
    """
    Configure application settings.
    """
    print("Configuring application...")

# Register the cheatsheet command
register_cheatsheet_command(app)

```

Gracias a la última linea, al ejecutar tu aplicación, el comando `cheatsheet` estará disponible:

```bash
typer-cheatsheet-demo cheatsheet
```

Verás una salida similar a esta:

![Cheatsheet](/images/cli_2025-10-30.svg)

¿Tenés comandos ocultos que quieres ver? Simplemente agregá la opción `--show-all`:

Por defecto, el comando se registra como `cheatsheet`. Si querés usar un nombre diferente para el subcomando, podés definir explícitamente:

```python
register_cheatsheet_command(app, command_name="cheat")
```

## Cómo funciona

Una función de registro recibe la app y el nombre del comando, y luego registra el comando provisto en la aplicación. La función instrospecciona los comandos y subcomandos registrados en la aplicación y genera una representación en formato de árbol, usando el widget [Tree de rich](https://rich.readthedocs.io/en/latest/tree.html).
