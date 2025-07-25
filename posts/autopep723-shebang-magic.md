<!--
.. title: Depedencias automáticas en scripts Python con autopep723
.. slug: dependencias-automaticas-scripts-python-autopep723
.. date: 2025-07-25 8:00:00 UTC-03:00
.. tags: python, uv, pep723, dependencies, automation
.. category: tools
-->


¿Alguna vez has deseado poder ejecutar un script de Python sin preocuparte por instalar sus dependencias primero?

Todos hemos estado ahí. Necesitas hackear un pequeño fragmento de código, tu LLM amigo te da un script de Python útil o encontraste uno en Stack Overflow (Dios te tenga en la gloria) o Gist. Pero si lo intentas ejecutar directamente:

```
ModuleNotFoundError: No module named 'your_experiment_dependency'
```

Entonces comienza la burocracia de verificar qué paquetes necesitas, con el agravante de que muchas veces el nombre con el que se instala no corresponde con el nombre que se importa), lidiar con conflictos de versiones y sobrecargar tu entorno.

Si todo el mundo coincide en que Python es un lenguaje pragmático y elegante que resulta ideal para scripts, ¿por qué esta parte tiene que ser complicada?

<!-- TEASER_END -->

Considera este script de análisis de datos

```python
import httpx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

response = httpx.get("https://api.github.com/users/octocat")
data = pd.DataFrame([response.json()])
# ... análisis
```

La forma tradicional implica configurar un entorno virtual, activarlo e instalar manualmente cada dependencia:

```bash
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install httpx pandas matplotlib seaborn scikit-learn
python script.py
```

Por supuesto, la situación mejoró mucho desde la aparición del glorioso [uv](https://docs.astral.sh/uv/) con el que podés ejecutar tu script en un virtualenv efímero en una sola línea

```bash
uv run --with httpx --with pandas --with matplotlib --with seaborn --with scikit-learn script.py
```

Pero claramente esto no escala y cada vez que quieras ejecutar tu script tendrás que recordar todos los paquetes que necesitas. Es decir, el script no es autocontenido.

Un paso mejor es incluir un comentario de metadata en la cabecera del script en el formato de [PEP 723](https://peps.python.org/pep-0723/) que `uv run` soporta,
de modo que el propio script declare sus dependencias y sea "autocontenido".

```python
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "httpx",
#     "pandas",
#     "matplotlib",
#     "seaborn",
#     "scikit-learn",
# ]
# ///
import httpx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
```

Pero hay una solución más elegante: **ejecuta tus scripts usando autopep723**

```bash
uvx autopep723 script.py
```

Como `uv run` puede ejecutar scripts remotos (tecnicamente, bajarlos antes de ejecutarlos), también lo puede hacer
`autopep723`, así que probemos con un ejemplo real
<script src="https://gist.github.com/mgaitan/7052bbe00c2cc88f8771b576c36665ae.js"></script>

```bash
uvx autopep723 https://gist.githubusercontent.com/mgaitan/7052bbe00c2cc88f8771b576c36665ae/raw/cbaa289ef7712b5f4c5a55316cce4269f5645c20/autopep723_rocks.py
```

<img width="1122" height="722" alt="autopep8" src="https://gist.github.com/user-attachments/assets/b1413418-4ce7-4b04-9452-d69de3af3d82" />


**Un tip extra?** Usa `autopep723` directamente como el _shebang_ de tu script


```python
#!/usr/bin/env -S uvx autopep723
import httpx
...
```

Después de marcar el script como ejecutable (es decir, `chmod +x script.py`) simplemente podrás ejecutar `./script.py`. ¡Comparte este script con cualquiera y simplemente funcionará también en su máquina siempre que tenga `uv`!

## Cómo funciona

Entre bastidores, `autopep723` analiza tu script usando el módulo [ast](https://docs.python.org/3/library/ast.html) para detectar importaciones de terceros, maneja casos complicados conocidos donde los nombres de las importaciones difieren de los nombres de los paquetes (por ejemplo, `import PIL` → `pillow`), luego ejecuta tu script usando `uv run` pasando los `--with` necesarios automáticamente. Todo sucede en un entorno limpio y efímero gracias a las capacidades de aislamiento de `uvx`.

En mi humilde opinión, este enfoque resuelve varios puntos débiles que plagan la distribución de scripts de Python. Los scripts simplemente funcionan de inmediato con cero fricción de configuración, mientras que `uvx` garantiza que no haya contaminación del entorno, ya que las dependencias se instalan de forma aislada. Cada script obtiene su propio entorno limpio, lo que evita conflictos de versiones, lo que hace que los scripts sean verdaderamente portátiles sin instrucciones de instalación. La velocidad de `uv` hace que esto sea práctico para el uso diario en lugar de solo una demostración inteligente.

Por cierto, también podés usar `autopep723` para agregar metadatos PEP 723 a tus scripts existentes:

```bash
autopep723 add script.py  # Agrega PEP 723 al archivo
```

y luego simplemente usa `uv run script.py`

## El futuro

Para ser honesto, me gustaría que este paquete no existiera, sino que fuera una característica incorporada de uv.

Tuiteé sobre esta idea pidiendo un flag `--with-auto` que haga su mejor intento para satisfacer las dependencias faltantes:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">how about a --with-auto that does its best attempt to satisfy missing deps? <a href="https://t.co/yYvYXGKZnM">https://t.co/yYvYXGKZnM</a></p>&mdash; Martín Gaitán (@tin_nqn_) <a href="https://twitter.com/tin_nqn_/status/1825970796478738940?ref_src=twsrc%5Etfw">August 21, 2024</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Aquí está mi [propuesta abierta](https://github.com/astral-sh/uv/issues/6283). Hasta entonces, `autopep723` cierra la brecha, haciendo que los scripts de Python sean tan fáciles de ejecutar como los scripts de shell.
