<!--
.. title: Automatic dependencies management for Python scripts with autopep723
.. slug: dependencias-automaticas-scripts-python-autopep723
.. date: 2025-07-25 8:00:00 UTC-03:00
.. tags: python, uv, pep723, dependencies, automation
.. category: tools
-->

Have you ever wished you could run a Python script without worrying about installing its dependencies first?

We've all been there. You need to hack a small piece of code, maybe your LLM friend gives you a useful Python script you want to try, or you found something on Stack Overflow (God rest its soul) or gist. But if you try to run it directly:

```python
ModuleNotFoundError: No module named 'your_experiment_dependency'
```

Then begins the bureaucracy of checking which packages you need, with the aggravating factor that many times the name with which it is installed does not correspond to the name that is imported, dealing with version conflicts and overloading your environment.

If everyone agrees that Python is a pragmatic and elegant language that's ideal for scripts, why does this part have to be complicated?

<!-- TEASER_END -->

Consider a data analysis script

```python
import httpx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

response = httpx.get("https://api.github.com/users/octocat")
data = pd.DataFrame([response.json()])
# ... analysis
```

The old-school way (booh!) involves setting up a virtual environment, activating it, and manually installing each dependency:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install httpx pandas matplotlib seaborn scikit-learn
python script.py
```

Of course, the situation has improved a lot since the appearance of the glorious [uv](https://docs.astral.sh/uv/) with which you can run your script in an implicit virtualenv [with dependencies](https://docs.astral.sh/uv/guides/scripts/#running-a-script-with-dependencies) in a single line:

```bash
uv run --with httpx --with pandas --with matplotlib --with seaborn --with scikit-learn script.py
```

However this does not scale for non trivial cases and every time you want to run your script you will have to remember all the packages you need. That is, the script is not self-contained.

A better step is to include a comment in the header of the script in the format of [PEP 723](https://peps.python.org/pep-0723/) that `uv run` supports, so that the script itself declares its dependencies:

```python
# /// script
# requires-python = ">=3.12"
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
...
```

But there is a more elegant solution: simply **run your scripts using [autopep723](https://github.com/mgaitan/autopep723)**

```bash
uvx autopep723 script.py
```

No `--with`, no specially crafted comments, just plain Python imports as if the whole PyPI package ecosystem were the standard library.

Since `uv run` can execute remote scripts (technically, downloading them to a temp directory before executing), `autopep723` can do the same, so let's try it with a real example
<script src="https://gist.github.com/mgaitan/7052bbe00c2cc88f8771b576c36665ae.js"></script>

```bash
uvx autopep723 https://gist.githubusercontent.com/mgaitan/7052bbe00c2cc88f8771b576c36665ae/raw/cbaa289ef7712b5f4c5a55316cce4269f5645c20/autopep723_rocks.py
```

<img width="1122" height="722" alt="autopep8" src="https://gist.github.com/user-attachments/assets/b1413418-4ce7-4b04-9452-d69de3af3d82" />


**An extra tip?** Use `autopep723` directly as the shebang of your script

```python
#!/usr/bin/env -S uvx autopep723
import httpx
...
```

After marking the script as executable you can simply run `./script.py`. Dependencies are automatically detected and installed in an ephemeral environment. Share this script with anyone with `uv` installed and it will just work on their machine too!

## How it works

Behind the scenes, `autopep723` parses your script using AST to detect third-party imports, handles complicated cases where import names differ from package names (e.g., `import PIL` → `pillow`), then runs your script using `uv run` passing the necessary `--with` automatically. Everything happens in a clean, ephemeral environment thanks to `uvx`'s isolation capabilities.

In my humble opinion, this approach solves several pain points that plague Python script distribution. Scripts simply work immediately with zero setup friction, while `uvx` ensures no environment pollution as dependencies are installed in isolation. Each script gets its own clean environment, avoiding version conflicts, making scripts truly portable with no installation instructions. `uv`'s speed makes this practical for daily use rather than just a clever demo.

By the way, you can also use `autopep723` to add PEP 723 metadata to existing scripts:

```bash
autopep723 add script.py  # Adds PEP 723 to the file
```

and then simply use `uv run script.py`

## The future

To be honest, I wish this package didn't exist, but was a built-in feature of uv.

I tweeted about this idea asking for a `--with-auto` flag that does its best attempt to satisfy missing dependencies:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">how about a --with-auto that does its best attempt to satisfy missing deps? <a href="https://t.co/yYvYXGKZnM">https://t.co/yYvYXGKZnM</a></p>&mdash; Martín Gaitán (@tin_nqn_) <a href="https://twitter.com/tin_nqn_/status/1825970796478738940?ref_src=twsrc%5Etfw">August 21, 2024</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Here is my [open proposal](https://github.com/astral-sh/uv/issues/6283). Until then, `autopep723` closes the gap, making Python scripts as easy to run as shell scripts.
