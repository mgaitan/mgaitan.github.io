.. title: Mi plantilla personalizada para proyectos Python
.. slug: plantilla-personalizada-proyectos-python
.. date: 2025-12-08 18:30:00
.. tags: python, tooling, copier, uv, ci, docs
.. category: development
.. description: Un template Python moderno y mantenible con Copier, uv, ruff, ty, pytest, documentación en markdown y releases automáticos.
.. author: Martín Gaitán


Python, como el lenguaje pragmático que es, no exige mucho para empezar. Un archivo de texto con código válido, que por convención lleva la extensión `.py` y constituye un "módulo" en la jerga *pythónica*, ya es un pequeño programa (un *script*); lo ejecutamos con `python <archivo>` y a cobrar. Pero cuando esa simple pieza de código necesita crecer a más archivos o merece ser distribuida, quizás porque será dependencia de otro proyecto o simplemente porque consideramos que a alguien le servirá, entonces necesita algo de estructura y metadatos. 

Esto no es algo exclusivo de Python: cuando se comienza un proyecto de software siempre hay una serie de archivos y estructuras básicas que sirven como punto de partida; el conjunto mínimo de archivos y carpetas, configuraciones y código "básico" que se necesita cuando se desea compartir el código como una aplicación o biblioteca: el *boilerplate* de un proyecto. El boilerplate no define lógica, pero sí establece la base técnica, muchas veces basada en convenciones y otras en gustos personales, sobre la cual se construirá todo lo demás. 

Este artículo detalla las decisiones que hice para la plantilla e inicialización automatizada (el "bootstrapping") que uso para mis proyectos, basada en la herramienta [Copier](https://copier.readthedocs.io/en/stable/). 

Si querés probar, la plantilla está en [mgaitan/python-package-copier-template](https://github.com/mgaitan/python-package-copier-template) y podés crear un proyecto nuevo a partir de ella así:

```console
uvx --with=copier-template-extensions copier copy --trust "gh:mgaitan/python-package-copier-template" /path/to/your/new/project
```

Lo destacado:

- 🐍 Paquete Python moderno (+3.12) con configuración centralizada en `pyproject.toml`. 
- 📦 Build y gestión de dependencias con [uv](https://astral.sh/uv), distinguidas por grupos (dev/qa/docs). 
- 🧹 Linter y formateado vía [Ruff](https://docs.astral.sh/ruff/) con un conjunto amplio de reglas habilitadas.
- ✅ Type checking vía [ty](https://github.com/astral-sh/ty).
- 🧪 Tests con [pytest](https://docs.pytest.org/en/stable/), [coverage.py](https://coverage.readthedocs.io/en/latest/) y otras extensiones
- 📚 Documentación con [Sphinx](https://www.sphinx-doc.org/en/master/), [MyST](https://myst-parser.readthedocs.io/en/stable/) y algunas extensiones, desplegada en [GitHub Pages](https://pages.github.com/)
- 🤖 Automatización de la creación de proyecto en GitHub vía [GitHub CLI](https://cli.github.com/)
- ⚙️ Workflow de CI en [GitHub Actions](https://github.com/features/actions)
- 🚀 Workflow para releases automáticos vía [Trusted Publishing](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/)
- 🧠 Defaults vía introspección para minimizar las decisiones durante el cuestionario inicial 
- 🛠️ Makefile con algunos atajos para tareas comunes
- 📄 Generación de documentos genéricos como LICENSE/CODE_OF_CONDUCTS/AGENTS.md, etc. 
- 🌀 Setup inicial del entorno de desarrollo y repositorio git
- ♻️ Proyectos actualizables con [`copier update`](https://copier.readthedocs.io/en/stable/updating/)

Y muchos más detalles que me estoy olvidando ahora. 


<!-- TEASER_END -->

## Un bootstrapping mínimo en Python

Empezemos por dar algo de contexto. Un boilerplate mínimo para un proyecto Python actual, instalable y distribuible se puede crear con `[uv init](https://docs.astral.sh/uv/concepts/projects/init/#packaged-applications)` (que está fuertemente inspirado en `cargo init` para Rust):

```console
$ uv init demo-project --package 
Initialized project `demo-project` at `/home/tin/lab/demo-project`
```

Lo que resulta en esto

```console
$ tree demo-project/
demo-project/
├── pyproject.toml
├── README.md
└── src
    └── demo_project
        └── __init__.py

3 directories, 3 files
$ cat demo-project/pyproject.toml 
[project]
name = "demo-project"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
authors = [
    { name = "Martín Gaitán", email = "gaitan@gmail.com" }
]
requires-python = ">=3.14"
dependencies = []

[project.scripts]
demo-project = "demo_project:main"

[build-system]
requires = ["uv_build>=0.9.9,<0.10.0"]
build-backend = "uv_build"
```

Este boilerplate declara `demo-project` como CLI, asociado a la función `main` que es un placeholder para reemplazar con tu código. 

```console
$ cd demo-project/
$ cat src/demo_project/__init__.py 
def main() -> None:
    print("Hello from demo-project!")

$ uv run demo-project
Using CPython 3.14.0
Creating virtual environment at: .venv
Installed 1 package in 6ms
Hello from demo-project!
```

Si instalaras tu programa con `uv tool install .` desde el directorio del proyecto podrás ejecutar `demo-project` desde cualquier lado. 

## Un boilerplate a medida 

Como dije, eso es **lo mínimo**. Cualquier proyecto que se precie define tests unitarios (y cómo ejecutarlos), declara dependencias auxiliares para desarrollo, configura uno o más linter con reglas de estilo, idealmente tiene documentación, incluye algún workflow de integración continua, se versiona con git, y hasta se le ponen "badges" en la cabecera del README. ¿Qué framework de tests usamos? ¿Con qué generamos la documentación? ¿El proyecto estará en un [layout src/ o flat](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)? 

Son un montón de decisiones a tomar (que eventualmente pueden cambiar) y un montón de trabajo implementarlas a mano. Más aún, cuando nos acostumbramos a una manera, muchas veces queremos lo mismo en todos los proyectos. 

Acá es cuando entra el concepto de *scaffolding*, que es generar el boilerplate a partir de plantillas editables de manera centralizada. Quizás la manera más genérica y trivial de hacer estas plantillas para proyectos sea la de [marcar un repositorio en GitHub como "template"](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository) de modo que cuando uno inicia un proyecto, en vez de empezar con el repositorio vacío se inicia desde el estado `HEAD` del repositorio template (pero sin ser un fork de este). 

Pero iniciar un proyecto no es solo crear el boilerplate, sino también preparar el entorno de desarrollo, inicializar el repo, crear el proyecto en GitHub y quizás pushear un primer commit, revisar que el nombre que elegimos para el paquete no está ya registrado, etc. Todo ese "bootstrapping" de un proyecto también implica tareas repetitivas y consumidoras de tiempo. ¡Automatizémoslas!

En Python la herramienta más conocida de scaffolding+bootstrapping es [cookiecutter](https://cookiecutter.readthedocs.io/). Aunque es una herramienta hecha en Python (los templates se definen con [Jinja](https://jinja.palletsprojects.com/en/stable/)), no se limita a crear boilerplate para proyectos Python ¡Está lleno de [templates cookiecutter para cualquier tipo de proyecto](https://github.com/search?q=cookiecutter&amp%3Btype=Repositories&type=repositories)!

`cookiecutter` es genial, pero sólo se ocupa del bootstrapping inicial de un proyecto. ¿Qué pasa cuando las convenciones cambian o adoptamos una nueva preferencia? Por ejemplo yo hace mucho [usaba Nose](https://mgaitan.github.io/posts/metiendose-cosas-en-la-nariz/) como framework y runner de testing, y ahora uso Pytest. Python mismo reemplazó el viejo formato `setup.py` por `pyproject.toml`. Y así un montón de cosas. 

De nuevo, si tenemos muchos proyectos, cambiar lo mismo en muchos lados es un trabajo aburrido y repetitivo. 

Por ese motivo mi plantilla se basa en [copier](https://copier.readthedocs.io/en/stable/) que es en muchos aspectos igual a cookiecutter (acá hay una [tabla comparativa](https://copier.readthedocs.io/en/stable/comparisons/)) pero soporta [actualizaciones](https://copier.readthedocs.io/en/stable/updating/) de los proyectos generados, es decir que cualquier proyecto que se inició con la plantilla puede aplicar las novedades con un simple comando. 


## Mi <strike>cuerpo</strike> plantilla, mi decisión

El template asume Python 3.12+ con layout `src/` y configuración unificada en el `pyproject.toml`. El backend para build 
es [uv_build](https://docs.astral.sh/uv/concepts/build-backend/) que es más que suficiente para proyectos "python puro" (sin extensiones compiladas). Se declara un script (opcional) como entrypoint que usa [`argparse`](https://docs.python.org/3/library/argparse.html) e incluye `--version` y `--help`. Si bien muchas veces prefiero [typer](https://typer.tiangolo.com/) como framework para CLIs (especialmente por su autocomplete), mejor [dejarlo simple](https://en.wikipedia.org/wiki/KISS_principle) por defecto. 

Obviamente uso `uv` para gestionar las dependencias y el entorno. Si bien el proyecto inicial no declara dependencias productivas (porque no se define ninguna "lógica de dominio" [^1] ) sí declaro varios [`dependency-groups`](https://github.com/mgaitan/copier-uv/blob/6751063f461775b31514ef86dc595d0774cf126f/project/pyproject.toml.jinja#L98-L120), un mecanismo definido en la [PEP 735](https://peps.python.org/pep-0735/) que organiza dependencias en conjuntos separados según su propósito --por ejemplo, test, docs, etc-- evitando mezclar todo en las dependencias principales y facilitando instalaciones parciales según el entorno o la tarea. Esto permite, por ejemplo, que cuando instalamos dependencias para compilar la documentación no tengamos que instalar las dependencias de tests (ahorrando precioso tiempo de CI cuando se ejecutan), o cuando verificamos QA con ruff no hagan falta herramientas exclusivas para desarrollo como ipdb. Cuando `uv` instala o sincroniza las dependencias (por ejemplo, mediante `uv sync`) busca por defecto el grupo `"dev"`, que en mi template es un metagrupo que incluye dependencias de test, qa y otras cosas. 


[^1]: Así como en los últimos años hemos ido [revisando y politizando el lenguaje](https://www.xataka.com/aplicaciones/se-acabaron-terminos-como-esclavo-lista-negra-linux-desarrolladores-tendran-que-usar-lenguaje-inclusivo) en nuestra industria evitando (o tratando de evitar) el lenguaje sexista, esclavista o belicista, también deberíamos dejar de pensar siempre en términos estrictamente capitalistas al software. Te estoy mirando a vos, "lógica de negocio". 

[ruff](https://docs.astral.sh/ruff/), ya que lo mencioné, es el linter canónico 
en la actualidad. De los mismos creadores de uv (y también hecho en Rust) es realmente un misterio cómo logran semejante performance. Cubre lint (reemplazando a flake8, isort y decenas de plugins) y formateo (reemplazando al adelantado [black](https://black.readthedocs.io/en/stable/)) con un límite de 120 caracteres por línea (porque los 79 [recomendados en PEP 8](https://pep8.org/#maximum-line-length) me resultan escasos para las resoluciones actuales) con un [conjunto amplio de reglas activadas](https://github.com/mgaitan/copier-uv/blob/6751063f461775b31514ef86dc595d0774cf126f/project/pyproject.toml.jinja#L39-L65), la mayoría de las cuales tienen autofix (y cuando no, los agentes se encargan) así mantiene un estilo pythónico consistente que minimiza bugs. Quizás a futuro active aún [más reglas](https://docs.astral.sh/ruff/rules/#flake8-errmsg-em): si es gratis, automático y rápido, las quiero todas. 

El paquete incluye tipado "inline" e incluye el archivo `py.typed` ([PEP 561](https://peps.python.org/pep-0561/)). Los chequeos de tipos se ejecutan con [ty](https://github.com/astral-sh/ty), otra de las herramientas de Astral que aún está en alpha, pero ya es usable para los fines de un proyecto nuevo. 

El stack de **pruebas unitarias** usa el estándar de facto, [pytest](http://pytest.org/), y [coverage.py](https://coverage.readthedocs.io/en/7.13.0/) vía [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/readme.html) (configurado con un threshold del 100%) con plugins para [mocks genéricos](https://pytest-mock.readthedocs.io/en/latest/index.html) y de [fechas](https://github.com/pytest-dev/pytest-freezer). Si bien perfectamente se podría usar [`mock`](https://docs.python.org/3/library/unittest.mock.html) incluido en la stdlib de Python, me gusta el fixture `mocker` porque no fuerza a usar context managers en el patching. Como [dice el Zen](https://pep20.org/#flat), "Flat is better than nested". 

Para un proyecto inicial que aún no define su finalidad puede pensarse que no hay mucho para documentar (y quizás basta con el `README`), pero tener el andamiaje preparado facilita que cuando haya algo sea trivial hacerlo. Por eso la plantilla incluye una carpeta `docs/` con la estructura inicial. Acá podría haber usado [mkdocs](https://www.mkdocs.org/) que es una opción cada vez más popular, pero me mantuve en el clásico [Sphinx](https://www.sphinx-doc.org/) usando [myst-parser](https://myst-parser.readthedocs.io/) para escribir en **Markdown** (solía [gustarme reStructuredText](https://mgaitan.github.io/posts/un-procesador-de-restructuredtext/) pero sé reconocer al [campeón](https://ia.net/topics/markdown-and-the-slow-fade-of-the-formatting-fetish)). Incluyo un par de extensiones mías ya configuradas: [sphinx-mermaid](https://github.com/mgaitan/sphinxcontrib-mermaid) para diagramas y [richterm](https://github.com/mgaitan/richterm) para incluir "capturas". 

Luego de crear el código, [ejecutamos algunas tareas](https://github.com/mgaitan/copier-uv/blob/6751063f461775b31514ef86dc595d0774cf126f/copier.yml#L15-L20). Por ejemplo se hace el primer `sync` (que instala dependencias de desarrollo), y se crea un primer commit con `git`. Luego, si [GitHub CLI](https://cli.github.com/) está instalado, se crea el repo en GitHub, se pushea y se lanza el primer workflow sin pasos manuales. 

Los tests creados así como los chequeos para que no se está infringiendo QA (ruff/ty) se verifican en un **workflow de CI** que se ejecuta en cada push o PR y corre los tests en todas las versiones de Python en una matriz. Las herramientas que lo soportan están configuradas para generar salidas de errores o warnings en formato de [anotaciones de GitHub](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands#setting-an-error-message) de modo de poder navegarlos en el contexto del código. 

Otro workflow es el encargado de realizar los releases. El flujo típico de un release es `make bump` + `make release` (incrementar la versión y commitear e iniciar un release de GitHub). El Workflow detecta este evento, arma los wheels (vía `uv build`) que adjunta al release en GitHub y además usa el mecanismo de [Trusted Publishing](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/) para subir la nueva versión directamente a PyPI. Además, se compila y se actualiza la documentación que se sirve desde GitHub Pages (si el repo es público). 

El mecanismo tradicional para subir paquetes a PyPI implicaba usar herramientas como [twine](https://github.com/pypa/twine) que requieren un token o un usuario y contraseña. El protocolo Trusted Publishing en cambio gestiona dinámicamente esta autenticación (usando el protocolo [oidc](https://openid.net/developers/how-connect-works/)), por lo que no hay que gestionar (ni rotar) estos secretos. 
Como lamentablemente este paso aún no se puede automatizar porque la API de PyPI no expone endpoints para este registro, lo único que hay que hacer de manera manual, por única vez, es registrar [el paquete y el workflow asociado](https://docs.pypi.org/trusted-publishers/adding-a-publisher/). En mi caso el workflow es `cd.yml` y el environment lo dejo en blanco. 

Cuando se ejecuta copier con una plantilla se lanza un cuestionario: nombre del paquete, autor, usuario de GitHub, esas cosas. Todo lo que pude automatizar aquí para ofrecer defaults con sentido lo hice, para que respondas lo mínimo imprescindible. Por ejemplo el nombre del proyecto se infiere del directorio que se pasa como argumento, el nombre e email del autor se obtienen de git y el usuario de GitHub desde la API vía GitHub CLI. 

Un detalle fruto de la experiencia: muchas veces me sucedió que ideo un nombre para un proyecto y a la hora de publicarlo me percaté de que el nombre ya está ocupado (mi reciente [textual-tetris](https://mgaitan.github.io/posts/textual-tetris/) se llamaba "textris" originalmente, pero [alguien me ganó de mano](https://pypi.org/project/textris)). Por eso el wizard se encarga de validar que el nombre que le queremos dar al paquete está disponible haciendo una simple consulta web a PyPI, y en caso de que esté ocupado nos propone un sufijo. 

En el proyecto generado definí un `Makefile` con una serie de atajos para "el día a día". Por ejemplo, si querés compilar la documentación localmente en `epub`, no tenés que acordarte los argumentos para Sphinx sino `make docs-epub` (y viene con un `make help` para más INRI). Si bien hay herramientas más modernas como [just](https://github.com/casey/just) o [mise](https://github.com/jdx/mise) (también existe [invoke](https://www.pyinvoke.org/) pero lo aborrezco) el cincuentón `make` es ubicuo y suficiente para estos humildes fines. Targets como `qa`, `test`, `docs` y `release` encapsulan los comandos largos y dejan una interfaz uniforme para tareas recurrentes.

Además de código se generan los documentos que típicamente son "copy & paste" como `LICENSE` y `CODE_OF_CONDUCT.md` (copiado de [Contributor Covenant](https://www.contributor-covenant.org/)). No creé por ejemplo un archivo de `CHANGELOG` porque aprovecho directamente la página de release de Githubs. 

Por otro lado, qué tiempos modernos, definí un [AGENTS.md](https://agents.md/) con instrucciones básicas para que los agentes de código se ubiquen en el contexto donde meteran sus múltiples manos robóticas. 

### Actualizaciones con Copier

Quizás la feature más interesante de Copier es que puede actualizar los proyectos ya creados, porque todo programador/a que se precie tiene sus principios, pero con el tiempo los cambia por otros. 

Recomiendo la entrevista a Jairo Llopis (uno de los mantenedores de Copier) en este [podcast](https://www.pythonpodcast.com/episodepage/project-scaffolding-that-evolves-with-your-software-using-copier) donde define a Copier como una "project life cycle management tool" (en contraposición con un gestor de scaffolding tradicional). 

Cuando todo está listo en el proyecto generado, copier deja un archivito `.copier-answers.yml` con metadatos con la información básica del template que se usó y las variables (las respuestas del cuestionario inicial) usadas. Si hay novedades en el template (por defecto busca tags), ejecutar `uvx copier update` basta para que se apliquen (o al menos se intente) al proyecto, aún cuando este haya mutado. 

El mecanismo que usa para esto no es trivial, implica un proceso de extracción y aplicación de diff (hay que recordar que el template y el proyecto son repositorios totalmente distintos que no comparten historia). Se resume en este diagrama que [obtuve de la documentación](https://copier.readthedocs.io/en/stable/updating/#how-the-update-works)

[![](https://mermaid.ink/img/pako:eNqlVcuOmzAU_RXL1UgTlWSSTF4w1WyabVftqqWqPHAhNGAjY6rSJP_ea2wnQFGldrwA-_qc--IYn2gkYqABTSUrD-TTPuQhv7sjHK0Vmf73CLmCosyZgm8SSnEfUrcmel1lSsgmpJMOLqqlBK4Q-qCK8sHZ373I53u7RxRLJ32WflTjJLN144S8lOI7RApTSoE7jjW2lERCdfCIC_cDZJUJbuiOfMvTwexOD3VgeYIQ_SJFht1VEOsQY9i6jPU2wu1s1CMryzwbQ7WZx1mSEAvp55vUeY4k_WqIpWoK4_E1s17AkBvUFxfJ9aOTP8n4FDsdmU6jsShVxtOJXr4lsubY9upYEZayjIf0a8gjhDCpndoZUYKkoIjOvEXo7Bvcb983c8j1FCswlolVKMTpKxVK7OgpFT0-k3OaKRLlgsOZDPX5zzwjQ511n-XUY4jAQX8Jor_KtX1n0lOsCz1QYuvBNvVvkLNpbClhar47SrsTQkv1Vlwv8FiEDqYVuYYYuTjEoAMjiOuwOtOIwaEYQp14NLQVxNAVac3tflvvsCPu8PwBuA3Tp24y9mANfVlzr7uiUqPt1efPSrdSTQ6vkm6Us6raQ0Je8AweX4SMQaJbKY4QvJnP508W4trlmao9k2OH9EQ9WoAsWBbjJXDSBeKv-gAFhDTAaQwJq3P8L4T8glBWK_Gx4RENlKzBo1LU6YEGCcsrXJkg-4xh9YWDlIx_FqK7pMGJ_qTBcrmcPe4ed6vVeudv5_7Kow0NFtvZFlfrjb_119v18uLRXy19PvOXi9V242_mi91ysfN9Dy8tnbaNjjrHgt6LmivtBt1BrK-ZD-aCa--5y2-R6D_y?type=png)](https://mermaid.live/edit#pako:eNqlVcuOmzAU_RXL1UgTlWSSTF4w1WyabVftqqWqPHAhNGAjY6rSJP_ea2wnQFGldrwA-_qc--IYn2gkYqABTSUrD-TTPuQhv7sjHK0Vmf73CLmCosyZgm8SSnEfUrcmel1lSsgmpJMOLqqlBK4Q-qCK8sHZ373I53u7RxRLJ32WflTjJLN144S8lOI7RApTSoE7jjW2lERCdfCIC_cDZJUJbuiOfMvTwexOD3VgeYIQ_SJFht1VEOsQY9i6jPU2wu1s1CMryzwbQ7WZx1mSEAvp55vUeY4k_WqIpWoK4_E1s17AkBvUFxfJ9aOTP8n4FDsdmU6jsShVxtOJXr4lsubY9upYEZayjIf0a8gjhDCpndoZUYKkoIjOvEXo7Bvcb983c8j1FCswlolVKMTpKxVK7OgpFT0-k3OaKRLlgsOZDPX5zzwjQ511n-XUY4jAQX8Jor_KtX1n0lOsCz1QYuvBNvVvkLNpbClhar47SrsTQkv1Vlwv8FiEDqYVuYYYuTjEoAMjiOuwOtOIwaEYQp14NLQVxNAVac3tflvvsCPu8PwBuA3Tp24y9mANfVlzr7uiUqPt1efPSrdSTQ6vkm6Us6raQ0Je8AweX4SMQaJbKY4QvJnP508W4trlmao9k2OH9EQ9WoAsWBbjJXDSBeKv-gAFhDTAaQwJq3P8L4T8glBWK_Gx4RENlKzBo1LU6YEGCcsrXJkg-4xh9YWDlIx_FqK7pMGJ_qTBcrmcPe4ed6vVeudv5_7Kow0NFtvZFlfrjb_119v18uLRXy19PvOXi9V242_mi91ysfN9Dy8tnbaNjjrHgt6LmivtBt1BrK-ZD-aCa--5y2-R6D_y)


## No hay bala de plata

Tengo muchos años de Python encima, los últimos especificamente en el área de "[developer experience](https://en.wikipedia.org/wiki/Developer_Experience)", y vi cómo fueron cambiando las convenciones y evolucionando las herramientas. En particular el packaging en Python siempre fue un trastorno por el cual muchas otras comunidades técnicas se burlaron de nosotros socarronamente. Por suerte en la actualidad se lograron estandarizaciones robustas y la aparición de `uv` parece haber terminado el debate. 

Más allá de que espero que no deba cambiar eso en particular, como se ha visto, hay un montón de otras decisiones tomadas que de acá a un tiempo quizás deba revisar. 

Si te interesa usar esta plantilla como base porque te gustan muchas de estas decisiones pero otras no te cierran y no te basta con resolverlas directamente en el proyecto generado (supongamos que no te interesa el `Makefile` porque usas Windows y te da fiaca: borrás el archivo y listo) entonces el camino es hacer un fork y hacer tus propios cambios. Estrictamente es lo que hice yo: todo comenzó como un fork de [este template](https://github.com/pawamoy/copier-uv). 

Espero que te sirva y ¡que viva el software libre!
