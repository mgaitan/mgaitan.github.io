<!--
.. title: Easter-eggs en tu código con texto invisible
.. slug: easter-eggs-con-texto-invisible
.. date: 2025-10-31 17:18:17 UTC-03:00
.. tags: humor, easter-egg, gist
.. category: scripts
.. link:
.. description:
.. type: text
-->

Según Wikipedia en español, [un "easter egg" es ](https://es.wikipedia.org/wiki/Huevo_de_Pascua_(virtual)) ...

> un mensaje o capacidad oculta contenido en películas, series de televisión, ..., programas informáticos o videojuegos. Entre los programadores, parece haber una motivación en dejar una marca personal, casi un toque artístico sobre un producto intelectual, el cual es por naturaleza estándar y funcional. Actualmente, los huevos de Pascua tratan de entretener, buscar nuevos trabajos potenciales, pagar tributo a los ejecutivos o divertir a los programadores.

No sé a quien le hizo creer eso de que un software es "estándar y funcional" al crédulo wikipedista,
pero es verdad que la pulsión por poner huevos de pascua en el software es casi tan vieja como el software mismo.

Acá les traigo una técnica que yo descubrí hace varias décadas, en el jardín de infantes cuando dibujabamos con jugo de limón en una hoja en blanco para que más tarde, mágicamente, se revelara el garabato al calor del encendedor de la seño que seguramente había estado fumando en el rincón de las maderitas un rato antes.

Veamos entonces como escribir mensajes en texto (digital) invisible: jugo de limón en su versión unicode.

<!-- TEASER_END -->

## ¿Qué son los caracteres *zero-width*?

Hay un conjunto de caracteres Unicode especiales que no se ven.
Los más comunes son:

| Código | Nombre | Descripción |
|:-------|:--------|:-------------|
| `U+200B` | Zero Width Space (ZWSP) | se comporta como un espacio “invisible” |
| `U+200C` | Zero Width Non-Joiner (ZWNJ) | evita unir caracteres en ciertos idiomas |
| `U+200D` | Zero Width Joiner (ZWJ) | hace lo contrario: une caracteres |

Estos caracteres "de ancho cero" (o "no imprimibles") se usan por ejemplo en sistemas de composición tipográfica como caracteres de control o para hacer ligaduras en alfabetos como el persa o árabe.

Pero podemos abusar de su invisibilidad y darle otro uso: usarlos como bits para codificar los caracteres de nuestro texto.

Si tomamos un texto cualquiera, lo convertimos a bytes (UTF-8), luego a bits, y finalmente reemplazamos cada bit por el carácter correspondiente, obtendremos una tira de caracteres invisibles.
Al volver a decodificar, recuperamos el mensaje original. Podemos definir por ejemplo que

- ZWSP → `0`
- ZWNJ → `1`

De esa manera, podemos **incrustar mensajes invisibles** en comentarios, strings, o al final de archivos sin romper nada. Es una modesta técnica de [estenografía](https://es.wikipedia.org/wiki/Esteganograf%C3%ADa)

## Ejemplo mínimo en Python 🐍

Este snippet muestra cómo convertir texto → secuencia de caracteres invisibles → texto otra vez:

```python
ZW0 = "\u200b"  # Zero Width Space -> bit 0
ZW1 = "\u200c"  # Zero Width Non-Joiner -> bit 1

def encode_to_zw(text: str) -> str:
    return ''.join(f"{byte:08b}" for byte in text.encode()).translate(
        str.maketrans("01", ZW0 + ZW1)
    )

def decode_from_zw(zw_text: str) -> str:
    bits = zw_text.translate(str.maketrans(ZW0 + ZW1, "01"))
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8)).decode("utf-8", errors="ignore")

secret = "🎵 Música oculta"
payload = encode_to_zw(secret)
print("Invisible payload:", payload)   # se ve vacío
print("Recovered:", decode_from_zw(payload))
```

Salida:

```
Invisible payload: ​‌​​‌‍​‌‍‌​‍​‌‍​‍‍‍‌‍‍​‌‍‍‍‍‍​
Recovered: 🎵 Música oculta
```

Entonces, ¿cómo usarlo como “easter egg”?

1. Generá tu payload invisible con el snippet anterior.
2. Pegalo al final de un comentario o línea inocente en tu código:
   ```python
   # NOTE: nothing to see here. ​‌‍‌​​‌‍‌​‍‍​‍‌‍‍‍‍‍‍
   ```
3. Solo quien sepa el truco, haga la ingeniería inversa o lea este blog podrá recuperarlo con el script decodificador.

## Hacerlo a lo grande

El método manual está bien para jugar, pero si querés esconder mensajes en varios archivos o buscarlos en todo un repositorio, conviene un script más potente.

Entonces le pedí a mi LLM <strike>amigo</strike> pasante que me haga un script para inyectar o decodificar mensajes invisibles. Acá el [gist](https://gist.github.com/mgaitan/53c3b2988b7e6e7a7c2215e0bee8138b)

- Inyecta mensajes invisibles en uno o más archivos (`zw_secret inject -m "mensaje"`).
- Los decodifica desde archivos o directorios completos (`zw_secret decode path/`).
- Usa `re` y `concurrent.futures` para escanear rápidamente grandes bases de código.

Te dejo como tarea decodificar este inocente mensaje:

<script src="https://gist.github.com/mgaitan/53c3b2988b7e6e7a7c2215e0bee8138b.js?file=example.txt"></script>

```console
wget https://gist.githubusercontent.com/mgaitan/53c3b2988b7e6e7a7c2215e0bee8138b/raw/e253f635f65d97de72d856ad240b45c3192438b4/example.txt
uv run https://gist.githubusercontent.com/mgaitan/53c3b2988b7e6e7a7c2215e0bee8138b/raw/e253f635f65d97de72d856ad240b45c3192438b4/zw_secret.py decode example.txt
```

PS: Esto es más bien un chiste (o una técnica para hacerlos). No abuses poniendo mensajes largos en un proyecto de tu laburo porque vas a meter ruido y aumentar mucho el tamaño de los archivos.
