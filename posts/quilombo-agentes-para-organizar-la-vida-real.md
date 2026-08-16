<!--
.. title: Quilombo: agentes para organizar la vida real
.. slug: quilombo-agentes-para-organizar-la-vida-real
.. date: 2026-08-15 12:06:35 UTC-03:00
.. status: draft
.. tags: agentes, mcp, django, LLM, inventario, okf
.. category: projects
.. link:
.. description: Una memoria agentica para encontrar, ordenar y cuidar las cosas del taller, la biblioteca y el mundo físico.
.. type: text
.. author: Martín Gaitán
-->

Mi profesión consiste, en buena medida, en ordenar cosas con ordenadores. Datos en tablas,
funciones en módulos, tareas en issues, cables invisibles entre servidores. Puedo pasar una tarde
discutiendo el nombre exacto de una variable y después entrar a mi taller y no encontrar una mecha
de 8 milímetros aunque estoy seguro de que tengo tres.

La cajonera tiene ocho cajones. Cada cajón, veinticuatro compartimientos. Es decir: ciento noventa y
dos oportunidades de guardar una cosa en un lugar perfectamente lógico que voy a olvidar media
hora después.

Mi profesión son los ordenadores. Mi taller es un quilombo. **Quilombo**, entonces, es el nombre
inevitable de este proyecto: una memoria para organizar las cosas del mundo físico y poder
conversar con ellas a través de un agente.

La idea no es abrir una planilla para informar solemnemente que moví siete tornillos. Quiero decirle
a ChatGPT o Claude «guardé los tornillos FIX de 35 mm en el cajón de arriba, junto a los tarugos» y,
otro día, preguntar desde el teléfono «¿dónde había tornillos para madera?».

El ordenador, por fin, ordenando.

<!-- TEASER_END -->

## El test Oscar

Mi suegro Oscar tiene un tallercito y le gusta conversar con la inteligencia artificial. No sabe
qué es una API, un MCP o una clave foránea y no tiene ningún motivo para aprenderlo. Si para usar
Quilombo tiene que modelar una base de datos, fracasamos.

Oscar debería poder mostrar un cajón en una videollamada y decir:

> Acá tengo tornillos, unas pilas y esa cajita azul tiene arandelas. Anotá más o menos, después lo
> acomodamos.

El agente que ve o escucha traduce esa conversación a datos. Quilombo no mira la foto ni ejecuta un
modelo de inteligencia artificial: guarda hechos, cantidades, ubicaciones y la referencia que el
cliente quiera dejar, por ejemplo «cambios inferidos de una foto procesada el 15 de agosto». La
foto queda donde estaba. La inteligencia también.

Esta separación es bastante importante. Quilombo puede ser una base de datos aburrida, predecible
y barata. El agente puede ser tan listo como permita el modelo de turno, pedir confirmación antes
de escribir y entender que «los fix largos» probablemente son los tornillos FIX de 35 mm. Cada uno
hace su trabajo.

[![Flujo entre la observación, el agente y Quilombo](https://mermaid.ink/img/Zmxvd2NoYXJ0IExSOyBBW0ZvdG8gbyBjb252ZXJzYWNpw7NuXSAtLT4gQltBZ2VudGVdOyBCIC0tPiBDW1F1aWxvbWJvIE1DUF07IEMgLS0-IERbKFBvc3RncmVTUUwpXTsgRCAtLT4gQzsgQyAtLT4gQjsgQiAtLT4gRVtFbmNvbnRyYXIsIG1vdmVyLCByZXBvbmVyXQ?type=png)](https://mermaid.ink/)

## Un mapa que admite el desorden

Un lugar en Quilombo puede contener otros lugares. `taller` contiene `cajonera`; `cajonera`
contiene `cajon-1`; el cajón contiene `compartimiento-b4`. Si no hay etiquetas tan prolijas, también
se pueden registrar relaciones: este estante está arriba de aquel, la caja roja está a la izquierda
de la azul.

Un *workspace* no es el estante superior de esa jerarquía. Es una frontera de acceso: quién puede
ver y modificar un inventario. Dentro de `Home` puedo tener como ubicaciones de primer nivel el
taller, la biblioteca y el galpón, y buscar solamente dentro del taller. Si algún día comparto el
inventario de un club o una escuela, eso puede vivir en otro workspace con otras personas.

Los objetos, por su parte, tienen nombre, alias, categoría, descripción y atributos libres. La
descripción sirve para una pista humana: «caja roja, ancha, con letras blancas». Los atributos
permiten guardar algo más regular: color del lomo, material, medida, marca. Una existencia une ese
objeto con un lugar y agrega cantidad, unidad, aproximación y notas de esa copia concreta.

Esto evita confundir dos tipos de dato:

- *Quilombo*, el libro como obra o edición, puede tener autor, ISBN y editorial.
- Mi ejemplar puede tener una dedicatoria y una esquina mordida.

Cuando hay ISBN, el agente puede consultar [Open Library](https://openlibrary.org/developers/api),
mostrar un borrador con título, autores, editorial y páginas, y guardar sólo lo que resulte útil.
Más adelante se podría agregar otro proveedor, como Google Books. Una reseña no es bibliografía:
es mejor conservarla como nota propia o como referencia externa, con su procedencia clara.

## La biblioteca también es un quilombo

Supongamos que pregunto por un libro y Quilombo responde «segundo estante, a la izquierda». Voy,
miro y no está. O, más probablemente, miro sin verlo.

La ubicación sola no siempre alcanza. Una mejor respuesta sería:

> Está registrado en el segundo estante a la izquierda. Es una edición ancha, de lomo rojo y letras
> blancas. En ese mismo sector figura *Crónicas del Ángel Gris*, la edición de lomo azul.

La descripción visual ayuda a reconocer el objeto. Los vecinos funcionan como mojones. Si tampoco
aparece, el agente no debería insistir con la autoridad de un GPS: el registro puede estar viejo.
Puede proponer revisar el lugar, corregir la ubicación o actualizar lo que efectivamente hay.

La misma información sirve para ordenar. Si el primer cajón tiene mayormente tornillos pero quedaron
dos paquetes en otro cajón mezclados con pilas, el agente puede leer el inventario y sugerir una
reorganización. Quilombo no decide el movimiento: ofrece el estado; el agente razona, prepara un
plan y espera la confirmación antes de actualizarlo.

También quiero poder preguntar «¿qué me está faltando?». Para eso no hace falta futurología: cada
objeto puede tener una cantidad mínima y una cantidad objetivo. Si quedan tres tornillos y el mínimo
es diez, el sistema informa stock bajo y propone reponer hasta el objetivo. Predecir *cuándo* se van
a acabar requerirá historial de consumo. Todavía no tenemos esa bola de cristal.

Los préstamos son otra extensión natural. Un libro puede estar bien inventariado y, sin embargo,
no estar en ningún estante porque se lo presté a alguien cuyo nombre ya no recuerdo. Registrar
salida, persona y devolución esperada es bastante más honesto que declarar desaparecido al libro.

## Una wiki para el mundo físico

Mientras pensaba Quilombo me encontré con dos ideas vecinas. En
[llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), Andrej Karpathy
propone que un agente mantenga entre sesiones una wiki de conocimiento que se va condensando,
enlazando y corrigiendo. En vez de releer todas las fuentes crudas para cada pregunta, conserva una
memoria navegable que mejora con el uso.

El [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
(OKF) apunta a una representación mínima, legible por humanos y máquinas, con Markdown, metadatos,
enlaces, procedencia y ciclo de vida. Sirve para que el conocimiento no quede encerrado en una
aplicación opaca.

Quilombo no necesita guardar cada tornillo como una página Markdown. PostgreSQL es mejor para sumar
cantidades, aislar usuarios y hacer un lote de miles de cambios en una transacción. Pero el patrón
sí aplica: fuentes u observaciones relativamente inmutables, una memoria curada que se corrige con
el tiempo, enlaces espaciales y procedencia. OKF, además, puede ser un gran formato de
importación/exportación para que el inventario sea portable.

[![Relación conceptual entre fuentes, memoria agentica y Quilombo](https://mermaid.ink/img/Zmxvd2NoYXJ0IFRCOyBTW0Z1ZW50ZXMgeSBvYnNlcnZhY2lvbmVzXSAtLT4gQVtBZ2VudGUgcXVlIG1hbnRpZW5lIGNvbm9jaW1pZW50b107IEEgLS0-IFFbUXVpbG9tYm86IGhlY2hvcyBkZWwgbXVuZG8gZsOtc2ljb107IFEgLS0-IFJbQ29uc3VsdGFzIHkgYWNjaW9uZXNdOyBLW2xsbS13aWtpIC8gT0tGXSAtLiBwYXRyw7NuIGRlIG1lbW9yaWEsIGVubGFjZXMgeSBwcm9jZWRlbmNpYSAuLT4gQQ?type=png)](https://mermaid.ink/)

## La parte aburrida que lo hace posible

[Quilombo](https://github.com/mgaitan/quilombo) es por ahora un monolito Django con PostgreSQL. Es
multiusuario, separa los datos por workspace y expone una API HTTP y un servidor MCP con OAuth. La
interfaz web existe para crear una cuenta, buscar inventario y conectar agentes, pero el camino
principal es conversar.

MCP permite que ChatGPT, Claude u otro cliente descubra herramientas como buscar, leer una vista
general del inventario, mover existencias o hacer *upserts* masivos. Las escrituras son
transaccionales e idempotentes: si una observación contiene cuarenta libros, se guardan todos o no
se guarda ninguno; si el cliente reintenta la misma operación, no duplica el taller.

Hay además una *skill*, una pequeña guía para el agente. Allí vive la política conversacional:
buscar antes de afirmar, diferenciar «no registrado» de «no existe», mostrar un borrador antes de
modificar y no fingir que Quilombo vio una foto que nunca recibió. La API, en cambio, hace lo que se
le ordena. Storage y criterio están separados hasta en la documentación.

## ¿Y qué sigue?

La primera versión ya deja guardar ubicaciones anidadas, relaciones relativas, objetos, cantidades
y procedencia; buscar dentro de una ubicación; y conversar vía MCP. Estoy trabajando en las pistas
visuales, el enriquecimiento de libros por ISBN y los avisos de faltantes. Después vendrán los
préstamos, los códigos QR y una forma conversada de inventariar por primera vez sin convertir el
domingo en una carga de datos.

El desafío interesante no es construir otra aplicación de inventario. Es conseguir que actualizar
el inventario cueste menos que volver a perder las cosas. Por eso Oscar es el test: mostrar,
conversar, corregir. Si él puede usarlo en su taller sin enterarse de que detrás hay Django, OAuth y
un protocolo con siglas, quizás hayamos inventado un ordenador de verdad.

Y quizás encuentre por fin las otras dos mechas de 8.
