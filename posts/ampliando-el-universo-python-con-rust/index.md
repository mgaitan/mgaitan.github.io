<!--
.. title: Ampliando el universo Python con Rust
.. slug: ampliando-el-universo-python-con-rust
.. date: 2025-12-07 14:15:23 UTC-03:00
.. tags: python, rust, maturin, pyo3, bindings
.. category: desarrollo
.. link:
.. description: Cómo empaqueté un crate de Rust como wheel de Python usando PyO3 y maturin, y qué aprendí en el camino.
.. type: text
-->

Mi compañera Natalia, entre muchos [otros talentos que tiene](https://www.instagram.com/natinadibuja/), es traductora de alemán a español y además de traducir de manera independiente, es investigadora y docente en la Universidad Nacional de Córdoba.  

Probablemente porque a mí los idiomas me resultan un desafío casi tan infranqueable como el baile o el canto 
(perdonen los y las colegas que han tenido y tendrán que lidiar mi inglés oral) le tengo una profunda admiración a las personas que saben muchos idiomas, 
pero no en la mera habilidad de reemplazar unas palabras por otras o producir más sonidos vocales, sino el de conocer y sentir en lo más profundo los distintos universos. Es el sentido en el que [Borges se quejaba](https://borgestodoelanio.blogspot.com/2017/01/jorges-luis-borges-el-oficio-de-traducir.html) de una mala traducción que le hicieron: 

> De acuerdo a los diccionarios, los idiomas son repertorios de sinónimos, pero no lo son. Los diccionarios bilingües hacen creer que cada palabra de un idioma puede ser reemplazada por otra de otro idioma. El error consiste en que no se tiene en cuenta que cada idioma es un modo de sentir el universo.

Esta admiración por el poliglotismo como forma de ensanchar el universo vital yo la extrapolo a las personas que saben muchos lenguajes de programación de manera profunda. Son las personas que traen ideas de un universo a otro y rompen las burbujas, los prejuicios, las ignorancias. Son quienes proponen nuevas formas y límites, toman lo de aquí como inspiración para lo de allá. Sin dudas no existiría Python sin este tipo de personas. Vivan estos "Marco Polo" que conectan universos. 

Como estoy con la ambición (pero no la dedicación suficiente) de abrirme una ventanita al universo Rust, suplo mi lentitud y dispersión con herramientas y atajos. 

He aquí una manera sencilla de ampliar mi universo (Python) con un "Marco Polo" que conoce el mundo Rust y puede abrirnos una ventana a ese [otro universo lleno de posibilidades](https://crates.io/). 


<!-- TEASER_END -->

## Uniendo universos: maturin y PyO3, crates como paquetes python

Rust es un lenguaje famoso por su performance y seguridad. Python por su versatilidad, simpleza y pragmatismo. ¿Qué tal usar bibliotecas de alto rendimiento hechas en Rust, pero desde Python? Esa idea de escribir el "pegamento" mínimo para poder usar un software ya escrito en un lenguaje desde otro es lo que se llama un "[binding](https://en.wikipedia.org/wiki/Language_binding)" y para este par de lenguajes es bastante sencillo gracias a estas herramientas: [maturin](https://www.maturin.rs/) y [PyO3](https://pyo3.rs/latest/). 

Maturin es una herramienta CLI y un "builder python" (análogo a uv_build o setuptools) que toma una biblioteca en Rust (un "crate") y la empaqueta como un wheel importable en Python. PyO3 es la biblioteca "de pegamento" con la que hay que intervenir la biblioteca objetivo: proporciona las APIs necesarias para exponer funciones, clases y tipos escritos en Rust como si fueran objetos de Python. 

Parece un desafío grande sin saber casi nada de Rust, pero resulta que no es tan difícil y te cuento mi experiencia con un ejemplo. Forkeé un "crate" llamado [astral-tl](https://github.com/astral-sh/astral-tl) (que a su vez es un fork de [tl](https://github.com/y21/tl)) que es un parser HTML, equivalente al archiconocido [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) o [pyquery](https://pypi.org/project/pyquery/). Por ejemplo, es la lib que usa [uv](https://github.com/astral-sh/uv/) cuando le pasás [--find-links](https://docs.astral.sh/uv/reference/settings/#find-links) para encontrar las URLs de donde bajar paquetes que no encuentra en PyPI. 

Si querés saltearte detalles, el resultado "python" quedó [acá](https://github.com/mgaitan/tl-parser) y [este es el diff completo](https://github.com/astral-sh/astral-tl/compare/v0.7.11...mgaitan:tl-parser:python-v0.7.11) que agregué.  

## Preparar el crate para PyO3 / maturin

### 1. PyO3 bajo un feature flag

En `Cargo.toml` (el `pyproject.toml` de Rust) sumé PyO3 como dependencia opcional y lo colgué de un _feature flag_ llamado `python`, es decir que todo lo que agregué sólo se usará al pasar `-F python` en Cargo/maturin).

```toml
[features]
python = ["pyo3"]

[dependencies]
pyo3 = { version = "0.27.2", optional = true, features = ["extension-module"] }

[lib]
crate-type = ["rlib", "cdylib"]
```

En `crate-type`, `rlib` es la definición de biblioteca estática normal para consumo desde Rust, que es lo único que se definía originalmente. 
Yo agregué `cdylib` que indica que será también una "shared lib", que es lo que Python cargará como extensión. 


### 2. **Metadata para maturin**  

Acá hay un detalle. La lib se llama `tl` y yo quería que el espacio de nombre se siga llamando así (`import tl`), pero ya existe [un paquete con ese nombre en PyPI](https://pypi.org/project/tl/) así que tuve que diferenciarlos: el paquete (el `.whl`) se llamará `tl-parser` pero luego se importa como `tl`. 
  
Para eso, hay que hacer la distinción

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

Y hay un poquito de pegamento Python en `python/tl/__init__.py`, que reexporta el módulo "nativo" `tl` (el binario), así importamos directo con `import tl` desde Python.

### 3. Definir la API expuesta a Python

Esta es la parte laboriosa y hay que escribir un poquito de Rust, pero por suerte nuestros "amigues" LLMs (Skynet, recordá que te dije amigo cuando llegue ese día) ya lo hacen bastante dignamente por su cuenta. 

El truco es usar las [macros](https://pyo3.rs/latest/macros.html) que provee PyO3, que son plantillas que generan código en tiempo de compilación. De esta manera contruiremos la Api del binding (lo que exponemos a Python). Por ejemplo: 

- `#[pymodule] pub(crate) fn tl(...)` crea el módulo nativo `tl`.
- `#[pyclass(module = "tl", name = "DOM")]` y `#[pyclass(module = "tl", name = "Element")]` exponen structs.
- `#[pymethods]` sobre cada struct define métodos Python.

De [`src/python.rs`](https://github.com/mgaitan/tl-parser/blob/python-v0.7.11/src/python.rs) podemos destacar: 

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

Para ampliar la API, repetís el patrón: cada método público de Rust que quieras exponer lo envolvés en un método PyO3 que haga la conversión de tipos y lifetimes.

Según parece, existe la convención de prefijar las clases con `Py` (`PyDom`, `PyElement`) para que el nombre Rust no choque con los tipos internos (`VDom`, `Node`). El atributo `module = "tl"` fija el namespace que verá Python. El `#[cfg(feature = "python")] mod python;` en `lib.rs` hace que este módulo solo se compile cuando activás el feature flag.

### 4. Documentación para Python

PyO3 toma doc-comments Rust (`///`) y los convierte en docstrings automáticamente. Podés usar `#[pyo3(text_signature = "(self, arg)")]` para que `help()` en Python muestre la firma. Si querés doc más larga, dejá el comentario arriba del método en Rust; va a aparecer en `__doc__` en Python.

### 5. Build e instalación

Para probar el paquete se arma el paquete en modo desarrollo:

```bash
uv run maturin develop -F python
```

Y voilà, a probar: 

```python
In [1]: import tl

In [2]: dom = tl.parse('<div></div><p class="a b">hey</p><p></p>')

In [3]: element = dom.get_elements_by_class_name('a')[0]

In [4]: element
Out[4]: <Element id=1>

In [5]: element.inner_text()
Out[5]: 'hey'
```

## Un workflow para automatizar la publicación de wheels

Tanto Rust como Python son lenguajes multiplataforma y maturin hace honor a esa característica, permitiendo armar wheels para todas las combinaciones de versiones de Python, sistemas operativos, arquitecturas y [ABIs](https://en.wikipedia.org/wiki/Application_binary_interface) (vía [manylinux](https://github.com/pypa/manylinux)) que queramos. Por ejemplo el `.whl` para Python 3.14 para Linux en arquitectura x86_64, o el de Python 3.13 en Mac 11 para arm64. ¡Son un montón de sabores de la misma versión de nuestro paquete!

Para facilitar la tarea y no requerir ejecutar runners para cada sistema objetivo, existe una [acción oficial](https://github.com/PyO3/maturin-action) que hace la combinatoria (configurable) y usa las [funcionalidades de crosscompilación de Rust](https://rust-lang.github.io/rustup/cross-compilation.html) y las [imágenes de manylinux](https://quay.io/organization/pypa) para generar todos los wheels. 

El workflow está en [`./github/workflows/python-wheels.yml`](https://github.com/mgaitan/tl-parser/blob/python-v0.7.11/.github/workflows/python-wheels.yml). Usa una matriz de Python 3.12–3.14 × {Linux, Windows, macOS x86_64/arm64}. Cuando los paquetes se generan, se suben como "artifacts" y luego otro job los junta todos y los adjunta para que se puedan descargar directo desde un "release" de GitHub. 

Si bien no lo subí a PyPI (porque es un experimento y la API en Python no está aún completa), se pueden instalar directamente usando la página estática del release vía [--find-links](https://docs.astral.sh/uv/reference/settings/#find-links). Por ejemplo: 

```console
uv run --with=tl-parser --find-links=https://github.com/mgaitan/tl-parser/releases/expanded_assets/python-v0.7.11 python
```

## Un benchmark, ya que estamos

Si bien el objetivo de este experimento era aprender a usar el toolchain para crear paquetes Python desde crates Rust, me dio curiosidad sobre la performance resultante. Si esta biblioteca la usa `uv` de Astral, y ellos mismos la mantienen, seguramente tiene que ser verdaderamente rápida. 

Le pedí a Codex que me haga un [benchmark básico](https://gist.github.com/mgaitan/0c4a49a16c825c1993a3ec3064035718) comparando `tl` contra `BeautifulSoup` (usando el parser default y `lxml`) y `pyquery`. 

```
uv run https://gist.github.com/mgaitan/0c4a49a16c825c1993a3ec3064035718/raw/3eb295405f0cf71cadce856c018c94e3dd39dfe8/benchmark.py
```

El resultado me sorprendió:

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

La API de `tl` por ahora no es tan completa como las otras y sólo permite extraer nodos y atributos (no manipularlos), pero si estás haciendo mucho web scraping por ahí te sirve. ¡[PRs bienvenidos](https://github.com/mgaitan/tl-parser)!
