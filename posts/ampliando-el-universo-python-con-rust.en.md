<!--
.. title: Expanding the Python universe with Rust
.. slug: expanding-the-python-universe-with-rust
.. date: 2025-12-07 14:15:23 UTC-03:00
.. tags: python, rust, maturin, pyo3, bindings
.. category: development
.. link:
.. description: How I packaged a Rust crate as a Python wheel using PyO3 and maturin, and what I learned along the way.
.. type: text
-->

My wife Natalia, among many [other talents she has](https://www.instagram.com/natinadibuja/), is a German-to-Spanish translator and, besides freelancing, works as a researcher and lecturer at the Universidad Nacional de Córdoba, Argentina.

Probably because foreign languages are almost as hard for me as dancing or singing (sorry to my colleagues who have had--and will have--to suffer through my spoken English), I have deep admiration for polyglots. Not for the mere ability to swap words or produce more vowel sounds, but for the power to know and feel different universes. That is what [Jorge L. Borges was complaining about](https://borgestodoelanio.blogspot.com/2017/01/jorges-luis-borges-el-oficio-de-traducir.html) when someone mangled one of his tales with a translation:

> According to dictionaries, languages are repertoires of synonyms, but they are not. Bilingual dictionaries make you believe that every word in one language can be replaced by another word in a different language. The mistake is ignoring that each language is a way of feeling the universe.

I extrapolate that admiration for polyglotism--the art of widening your vital universe--to people who know many programming languages deeply. They bring ideas from one universe to the next, bursting bubbles, prejudices, blind spots. They propose new ways and limits, taking inspiration from here to create over there. Python would not exist without that kind of people. Long live those "Marco Polos" who connect universes.

Since I'm ambitious (but not quite dedicated enough) to open a small window into the Rust universe, I compensate for my slowness and distraction with tools and shortcuts.

This is a simple way to expand my Python universe with a "Marco Polo" who knows the Rust world and can open a window to that [other realm full of possibilities](https://crates.io/).

<!-- TEASER_END -->

## Bridging universes: maturin and PyO3, crates as Python packages

Rust is famous for performance and safety. Python for versatility, simplicity, and pragmatism. Why not take high-performance Rust libraries and use them from Python? Writing the minimal amount of "glue" that lets you reuse software from one language in another is called a [binding](https://en.wikipedia.org/wiki/Language_binding), and for this pair of languages it's pretty straightforward thanks to [maturin](https://www.maturin.rs/) and [PyO3](https://pyo3.rs/latest/).

Maturin is a CLI tool and a "Python builder" (think uv_build or setuptools) that takes a Rust library (a crate) and packages it into a wheel you can import from Python. PyO3 is the glue library you add to the target crate: it provides the APIs to expose Rust functions, classes, and types as if they were Python objects.

Sound like a big challenge if you barely know Rust? Turns out it isn't that hard, so let me share an example. I forked a crate called [astral-tl](https://github.com/astral-sh/astral-tl) (itself a fork of [tl](https://github.com/y21/tl)), an HTML parser comparable to the ubiquitous [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) or [pyquery](https://pypi.org/project/pyquery/). It's the library [uv](https://github.com/astral-sh/uv/) uses when you pass [--find-links](https://docs.astral.sh/uv/reference/settings/#find-links) to locate URLs for packages that aren't on PyPI.

If you want to skip the details, the Pythonized result is [here](https://github.com/mgaitan/tl-parser), and [this is the full diff](https://github.com/astral-sh/astral-tl/compare/v0.7.11...mgaitan:tl-parser:python-v0.7.11) I added.

## Preparing the crate for PyO3/maturin

### 1. PyO3 behind a feature flag

In `Cargo.toml` (Rust's equivalent of `pyproject.toml`) I added PyO3 as an optional dependency and gated it behind a `python` feature flag, so everything I added is only compiled when passing `-F python` to Cargo/maturin.

```toml
[features]
python = ["pyo3"]

[dependencies]
pyo3 = { version = "0.27.2", optional = true, features = ["extension-module"] }

[lib]
crate-type = ["rlib", "cdylib"]
```

In `crate-type`, `rlib` is the default static library Rust produces, which is all the crate originally defined. I added `cdylib`, indicating that it can also produce a shared library, which is what Python loads as an extension module.

### 2. Metadata for maturin

Here's the tricky part. The library is named `tl` and I wanted to keep that namespace (`import tl`), but there is already [a package with that name on PyPI](https://pypi.org/project/tl/). So I needed to differentiate them: the wheel is called `tl-parser`, but once installed you still `import tl`.

That distinction lives in your metadata files:

```toml
# Cargo.toml
[package.metadata.maturin]
name = "tl-parser"
python-source = "python"

# pyproject.toml
[tool.maturin]
features = ["python"]
python-source = "python"
module-name = "tl"
python-packages = ["tl"]
```

There's also a tiny bit of Python glue in `python/tl/__init__.py` that re-exports the native `tl` module (the compiled binary), so in Python we can simply `import tl`.

### 3. Define the Python-facing API

This is the "laborious" part: you have to write a bit of Rust, but thankfully our LLM friends (Skynet, remember I called you friend when the day arrives) can help a lot.

The trick is to use the [macros PyO3 provides](https://pyo3.rs/latest/macros.html), which generate code at compile time.

- `#[pymodule] pub(crate) fn tl(...)` creates the native `tl` module.
- `#[pyclass(module = "tl", name = "DOM")]` and `#[pyclass(module = "tl", name = "Element")]` expose structs.
- `#[pymethods]` on each struct defines their Python methods.

A trimmed-down version of [`src/python.rs`](https://github.com/mgaitan/tl-parser/blob/python-v0.7.11/src/python.rs):

```rust
#[pymodule]
pub(crate) fn tl(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse, m)?)?;
    m.add_class::<PyDom>()?;
    m.add_class::<PyElement>()?;
    Ok(())
}

#[pyfunction]
fn parse(html: &str) -> PyResult<PyDom> { }

#[pyclass(module = "tl", name = "DOM")]
struct PyDom { dom: Arc<VDomGuard> }

#[pymethods]
impl PyDom {
    fn get_element_by_id(&self, id: &str) -> Option<PyElement> { /* ... */ }
    fn get_elements_by_class_name(&self, class_name: &str) -> Vec<PyElement> { /* ... */ }
    fn query_selector(&self, selector: &str) -> PyResult<Vec<PyElement>> { /* ... */ }
    fn children(&self) -> Vec<PyElement> { /* ... */ }
    fn outer_html(&self) -> String { /* ... */ }
}

#[pyclass(module = "tl", name = "Element")]
struct PyElement { dom: Arc<VDomGuard>, handle: NodeHandle }

#[pymethods]
impl PyElement {
    fn inner_text(&self) -> PyResult<String> { /* ... */ }
    fn inner_html(&self) -> PyResult<String> { /* ... */ }
    fn outer_html(&self) -> PyResult<String> { /* ... */ }
    fn name(&self) -> PyResult<Option<String>> { /* ... */ }
    fn get_attribute(&self, name: &str) -> PyResult<Option<String>> { /* ... */ }
    fn children(&self) -> PyResult<Vec<PyElement>> { /* ... */ }
}
```

To expose more APIs you just repeat the pattern: wrap each public Rust method you want to expose in a PyO3 function/method that performs the necessary type and lifetime conversions.

Conventions I followed: I prefixed the exposed structs with `Py` (`PyDom`, `PyElement`) so the Rust names don't collide with the internal types (`VDom`, `Node`). The `module = "tl"` attribute pins the namespace Python sees. And the `#[cfg(feature = "python")] mod python;` in `lib.rs` ensures this module is only compiled when the feature flag is enabled.

### 4. Documentation for Python

PyO3 takes Rust doc comments (`///`) and automatically turns them into Python docstrings. You can use `#[pyo3(text_signature = "(self, arg)")]` to show a proper signature when people call `help()` in Python. For longer docs, keep the comments right above the Rust method--they end up in `__doc__`.

### 5. Build and install

To test the package locally you can build it in development mode:

```bash
uv run maturin develop -F python
```

And voilà, time to try it:

```python
In [1]: import tl

In [2]: dom = tl.parse('<div></div><p class="a b">hey</p><p></p>')

In [3]: element = dom.get_elements_by_class_name('a')[0]

In [4]: element
Out[4]: <Element id=1>

In [5]: element.inner_text()
Out[5]: 'hey'
```

## A workflow to automate wheel publishing

Rust and Python are both cross-platform, and maturin leans into that strength by letting you build wheels for every combination of Python versions, operating systems, architectures, and [ABIs](https://en.wikipedia.org/wiki/Application_binary_interface) (via [manylinux](https://github.com/pypa/manylinux)) that you care about. Think Python 3.14 on Linux x86_64, or Python 3.13 on macOS 11 arm64; lots of flavors for the same release!

To make that manageable without provisioning runners for each target, there's an [official GitHub Action](https://github.com/PyO3/maturin-action) that builds the desired matrix (configurable) and relies on [Rust cross-compilation](https://rust-lang.github.io/rustup/cross-compilation.html) and [manylinux's images](https://quay.io/organization/pypa) under the hood to produce every wheel.

The workflow lives at [`./github/workflows/python-wheels.yml`](https://github.com/mgaitan/tl-parser/blob/python-v0.7.11/.github/workflows/python-wheels.yml). It uses a matrix of Python 3.12–3.14 × {Linux, Windows, macOS x86_64/arm64}. Once the wheels are generated, they are uploaded as artifacts, and a follow-up job bundles them all and attaches them to a GitHub release.

I didn't push anything to PyPI (this is still an experiment and the Python API isn't feature-complete), but you can install straight from the release's static page via [--find-links](https://docs.astral.sh/uv/reference/settings/#find-links). For example:

```console
uv run --with=tl-parser --find-links=https://github.com/mgaitan/tl-parser/releases/expanded_assets/python-v0.7.11 python
```

## A quick benchmark (because why not)

While the goal here was to learn the toolchain to turn Rust crates into Python packages, I was curious about the resulting performance. If Astral's `uv` depends on this library--and they maintain it themselves--it must be blazing fast, right?

I asked Codex for a [basic benchmark](https://gist.github.com/mgaitan/0c4a49a16c825c1993a3ec3064035718) comparing `tl` with `BeautifulSoup` (default parser and `lxml`) and `pyquery`.

```
uv run https://gist.github.com/mgaitan/0c4a49a16c825c1993a3ec3064035718/raw/3eb295405f0cf71cadce856c018c94e3dd39dfe8/benchmark.py
```

The result surprised me:

<table class="table table-striped">
    <thead>
        <tr>
            <th>metric</th>
            <th>tl.parse</th>
            <th>BeautifulSoup (html.parser)</th>
            <th>BeautifulSoup (lxml)</th>
            <th>PyQuery</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>parse</td>
            <td>0.353 ms</td>
            <td>50.681 ms</td>
            <td>51.144 ms</td>
            <td>3.864 ms</td>
        </tr>
        <tr>
            <td>title_text</td>
            <td>0.033 ms</td>
            <td>0.011 ms</td>
            <td>0.013 ms</td>
            <td>0.057 ms</td>
        </tr>
        <tr>
            <td>class_lookup</td>
            <td>0.021 ms</td>
            <td>2.957 ms</td>
            <td>4.124 ms</td>
            <td>0.070 ms</td>
        </tr>
        <tr>
            <td>id_lookup</td>
            <td>0.007 ms</td>
            <td>0.029 ms</td>
            <td>0.038 ms</td>
            <td>0.064 ms</td>
        </tr>
        <tr>
            <td>css_query</td>
            <td>0.037 ms</td>
            <td>9.456 ms</td>
            <td>9.786 ms</td>
            <td>0.130 ms</td>
        </tr>
    </tbody>
</table>

The `tl` API isn't as complete as the others yet; it only lets you extract nodes and attributes (not mutate them), but if you're doing heavy web scraping it might already be useful. [PRs welcome](https://github.com/mgaitan/tl-parser)!
