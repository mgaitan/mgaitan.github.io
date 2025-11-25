<!--
.. title: textual-tetris, un tetris en la terminal
.. slug: textual-tetris
.. date: 2025-11-24 22:38:00-03:00
.. tags: python, textual, juegos, terminal
.. category: proyectos
.. link:
.. description: Una autopsia amable de un port de Tetris hecho con Textual
.. type: text
-->

Como [sigo sin empleo](https://x.com/tin_nqn_/status/1978823177837912528) priorizando la búsqueda de salud mental, dedico mi tiempo ñoño a dos loables tareas: 

1. Colaborar con organizaciones que necesitan soluciones tecnológicas pero no tienen el presupuesto para competir con el mercado por mis conocimientos. 
2. La que compete a este post: aprender cosas nuevas implementando ideas viejas del `TO DO` permanente que [anoto acá](https://github.com/mgaitan/mgaitan/issues)), para las que rara vez encontraba el tiempo.    

Esta vez quería aprender un poco sobre [Textual](https://textual.textualize.io/) (hermano mayor de [rich](https://rich.readthedocs.io/en/stable/)), el gran framework en Python para hacer interfaces gráficas basadas en texto, las famosas [TUIs](https://en.wikipedia.org/wiki/Text-based_user_interface). 

Y ya que estaba, aprendí a hacer un Tetris que es bastante digno de jugar, no se ve taaan feo, y [actualmente tiene menos de 600 líneas](https://github.com/mgaitan/textual-tetris/blob/392744f6275160e5b8512e7f9f76b3a2e388fb4a/textris.py) contando los comentarios y se ve así:

![](/images/textual-tetris.png)

Pero una probadita vale más que mil capturas: abrí una terminal y si tenés [uv](https://docs.astral.sh/uv/) instalado (¡deberías!) ejecutá:

```console
uvx textual-tetris 
```

Y ya estás jugando Tetris!

<!-- TEASER_END -->

## Un paseo por mi implementación

Tetris no es un juego cualquiera. Es una ícono de la cultura popular, un producto que tuvo valor geopolítico (no se pierdan [este newsletter de Tomás Aguerre](https://cenital.com/la-invencion-del-tetris/) al respecto) y una pasión obsesiva para quienes lo juegan y lo programan. 

Hay [miles de versiones](https://github.com/search?q=tetris&type=repositories) en decenas de lenguajes de programación. Desde una versión [code golf](https://en.wikipedia.org/wiki/Code_golf) en Javascript que [entra completamente en 351 bytes](](https://blog.jay.vg/golf/tetris.html)), uno [en esamblador que bootea como sistema operativo)](https://github.com/programble/tetrasm) y hasta hay uno implemnentado [en un archivo PDF!](https://th0mas.nl/2025/01/12/tetris-in-a-pdf/). 

El que hice yo es mucho más clásico pero tiene algunos detalles de implementación que me gustaría comentar. 

Por ejemplo tomé [la idea de Ole Martin Bjørndalen](https://github.com/olemb/tetris/) de códificar los tetrominós en sus distintas posiciones posibles como un conjunto de coordenadas hexadecimales dentro de una malla 4x4.  

Acá armé un videito para explicarlo: 

<iframe width="560" height="315" src="https://www.youtube.com/embed/6b1sauBX35g" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

En el código se ve así:

```python
PIECES = {
    "O": {"color": "yellow", "codes": ["56a9", "6a95", "a956", "956a"]},
    "I": {"color": "cyan", "codes": ["4567", "26ae", "ba98", "d951"]},
    # ...
}

class TetrisPiece:
    ...

    @property
    def shape(self) -> list(tuple[int, int]):
        coords = []
        for char in self.code:
            value = int(char, 16)
            y, x = divmod(value, 4)
            coords.append((x, y))
        return coords

```


Esa `property` nos da coordenadas relativas de la pieza en la rotación dada por `self.code`, que luego se suman a una posición `x, y` de la pieza relativa al tablero para calcular la posición absoluta de las celdas a pintar. Si estas coordenadas caben en las dimensiones del tablero, entonces la celda pasa de mostrarse como dos espacios en blanco a dos "█" (full [block char](https://en.wikipedia.org/wiki/Block_Elements)) del color de la pieza. 

```python
      for board_x, board_y in self.current_piece.blocks:
          if 0 <= board_x < self.board_width and 0 <= board_y < self.board_height:
              display_board[board_y][board_x] = self.current_piece.color

      for row in display_board:
          for cell in row:
              if cell == 0:
                  text.append("  ")
              else:
                  text.append("██", style=f"bold {cell}")
```

Rotar una pieza es basicamente cambiar un código por el que le sigue y volver a empezar cuando se acaban. Es lo que se conoce como un "round-robin". 

Originalmente llevaba registro del índice de la rotación que se calcula como el módulo.

```python
    self.rotation = (self.rotation + 1) % len(self.codes)
```  

Luego cambie (simplifiqué?) a usar `collections.deque` que ya tiene los metodos de rotacion. 


```python
class TetrisPiece:
    def __init__(self, piece_type=None):
        ...
        self.codes = deque(PIECES[piece_type]["codes"])
        
    @property
    def code(self):
        return self.codes[0]

    def rotate(self):
        self.codes.rotate(-1)

    def undo_rotate(self):
        self.codes.rotate(1)
```

El `undo_rotate` es necesario porque cuando llega la directiva de rotar la pieza actual en el tablero, se calcula si hay colisiones antes de mostrarla, y si hay colisiones, se necesita revertir la rotación. Para quien juega esto es equivalente a "no se puede rotar" 

```python
def rotate_piece(self):
    """Rotate the current piece"""
    
    self.current_piece.rotate()

    # Check if rotation causes collision
    if self.check_collision():
        self.current_piece.undo_rotate()
        return False

    self.update_display()
    return True
```

El mismo criterio de intentar/deshacer si colisiona es para los movimiento.s   Así es `move_piece`: 

```python
def move_piece(self, dx, dy):
    old_x, old_y = self.current_piece.x, self.current_piece.y
    self.current_piece.x += dx
    self.current_piece.y += dy

    if self.check_collision():
        self.current_piece.x, self.current_piece.y = old_x, old_y
        if dy > 0:
            self.lock_piece()
        return False

    self.update_display()
    return True
```

Pero que es una colisión? Geometría discreta:

```python
def check_collision(self):
    for board_x, board_y in self.current_piece.blocks:
        if board_x < 0 or board_x >= self.board_width or board_y >= self.board_height:
            return True
        if board_y >= 0 and self.board[board_y][board_x] != 0:
            return True
    return False
```

Al bajar (`dy > 0`), si chocamos se llama a `lock_piece`: fija los colores en la grilla, limpia líneas completas y le avisa a la `App`. Eso contesta la clásica “¿por qué no puedo seguir bajando?”: porque la función probó el movimiento y chocó contra un borde o un bloque previamente fijado.


## Widgets, bindings y magia "Textual" 

Una app Textual se compone de [widgets](https://textual.textualize.io/widget_gallery/) (botones, inputs, options, etc.) que pueden agruparse en containers `Container`. Todos los widgets y los contenedores pueden estar asociados a un estilo de (pseudo) CSS. 

La compisición para este Tetris es bastante autoexplicativa 

```python
    def compose(self) -> ComposeResult:
        with Container(id="game-container"):
            yield Label("🎮 TETRIS 🕹", id="title")
            with Horizontal():
                with Container(id="board-container"):
                    yield TetrisBoard(id="board")
                    yield Static("GAME OVER\nPress R to restart", id="game-over-overlay")
                with Vertical(id="sidebar"):
                    with Container(id="next-piece-container"):
                        yield NextPieceWidget(id="next-piece")
                    with Container(id="score-container"):
                        yield ScoreWidget(id="score-widget")
                    with Container(id="controls"):
                        yield Label("CONTROLS", classes="section-title")
                        yield Label("↑/W: Rotate")
                        yield Label("←/A: Move Left")
                        yield Label("→/D: Move Right")
                        yield Label("↓/S: Move Down")
                        yield Label("Space: Drop")
                        yield Label("Ctrl+Q: Quit")
```

Todos los widgets "custom" que definí, `TetrisBoard`, `NextPieceWidget` y `ScoreWidget`,  heredan de `Static` que es el widget más básico, no "reactivo", pero que obviamente se puede renderizar multiples veces para actualizar su contenido. 

Esa actualización sucede en algunos eventos en este caso de teclado y de un timer que controla la caída automática de las piezas (textual tambien soporta eventos de mouse). El puente entre los eventos y la lógica está en `TetrisApp.BINDINGS`:

```python
BINDINGS = (
    ("left,a", "move_left", "Move Left"),
    ("right,d", "move_right", "Move Right"),
    ("down,s", "move_down", "Move Down"),
    ("up,w", "rotate", "Rotate"),
    ("space", "hard_drop", "Drop"),
    ...
)
```

Cada *binding* mapea combinaciones de teclas a `action_*`. Cuando Textual detecta el evento de una combinación, invoca `action_move_left`, `action_hard_drop`, etc. ¡Excelente API de desarrollo en mis libros!

Y hay un chiche. Cuando se pierde, además de hacer visible el cartelito de "Game over" (que en realidad está siempre pero oculto), el método a cargo tambien [desactiva varios bindings dinámicamente](https://textual.textualize.io/guide/actions/#dynamic-actions), asi no podes mover nada. Esta desconexión de eventos a acciones evita ensuciar los métodos con un chequeo (`if not self.game_over: ...`). 

Dicho sea de paso, la documentación de Textual es increíblemente buena, recomiendo leerla aun si todavía no tenés proyecto. 

## ¡Ponele los puntos!

Cuando una pieza ya no puede caer más (hay una colisión en un movimiento manual o automático hacia abajo), se llama al método `on_piece_locked`

```python
    if self.check_collision():
        # Revert move
        self.current_piece.x, self.current_piece.y = old_x, old_y
        # If we were moving down, lock the piece in place
        if dy > 0:
            self.lock_piece()
```

Este método es el que suma puntaje, calcula si se pasa de nivel, lo que a la su vez 
aumenta la velocidad de caída de las piezas.

```python
line_score = {1: 100, 2: 300, 3: 500, 4: 800}.get(cleared_lines, cleared_lines * 200)
self.score += line_score * self.level if cleared_lines else 10
self.lines_cleared += cleared_lines
self.level = max(1, 1 + self.lines_cleared // self.lines_per_level)
```

La duración de la pausa entre cada paso de descenso automático (a.k.a. velocidad de caída libre) es una funcion exponencial inversa del nivel 

<!--$$
t_{\text{drop}}(L) = \max\!\Bigl(0.02,\;\bigl(0.8 - 0.007(L-1)\bigr)^{\,L-1}\Bigr)
$$-->

![](https://quicklatex.com/cache3/71/ql_357031cd1c3bcd37e352da356333a171_l3.png)

que graficado se ve así:

![velocidad](/images/drop_interval_levels_xkcd.png)

¿De dónde saqué esa formula estrambótica?  De la [guía oficial de diseño de Tetris](https://archive.org/details/2009-tetris-variant-concepts_202201/2009%20Tetris%20Design%20Guideline/page/20/mode/2up), por supuesto. 

Si querés todas las recomendaciones de esa guía para tu Tetris clone, hay una [biblioteca Python que lo implementa en serio](https://pypi.org/project/tetris/). 

## ¿Y qué queda pendiente?

La UI es medio pelo, seamos sinceros. Muy copado Textual, pero acomodar las cosas en la pantalla sigue dependiendo de saber un poco de CSS y ya sabemos como somos los pythonistas con ese asunto. Y los LLMs [tampoco ayudan mucho con esto](https://x.com/ralsina/status/1991205490781573430). 

<div class="tenor-gif-embed" data-postid="12014506" data-share-method="host" data-aspect-ratio="1.33333" data-width="60%"><a href="https://tenor.com/view/family-guy-css-open-window-annoyed-pissed-gif-12014506">Family Guy Css GIF</a>from <a href="https://tenor.com/search/family+guy-gifs">Family Guy GIFs</a></div> <script type="text/javascript" async src="https://tenor.com/embed.js"></script>

El código probablemente se puede hacer un poco más prolijo. Por ejemplo hay algo de lógica repetida entre el render del tablero y el del widget de la pieza siguiente. 

La manera de recomenzar un juego es un poco bruta (lanza un nuevo proceso!). No hay acción para pausar. Y sobre todo, hace falta la posibilidad de repetir los boards para jugar de a dos (o más!) jugadoras/es, que es la más enérgica petición de mi más hábil usuaria, mi hija Ema de 10 años. 

¡Espero sus comentarios, sugerencias y pull requests!
