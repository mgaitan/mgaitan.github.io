<!--
.. title: Analizando la migración intraprovincial en Córdoba
.. slug: analizando-la-migracion-intraprovincial-en-cordoba
.. date: 2025-11-18 13:57:13 UTC-03:00
.. tags: padrones electorales, LLM, inteligencia artificial, data science, ETL, visualización, Sankey
.. category: 
.. link: 
.. description: 
.. type: text
-->

Charlando hace poco con Facundo Cruz, sociólogo investigador del Equipo de Investigación Política de la Revista Crisis ([EdIPo](https://www.investigacionpolitica.com/)), le conté sobre un estudio "en joda" que hice una vez, el [padronazo cordobés](https://mgaitan.github.io/posts/el-padronazo-cordobes/), y recordé un trabajo más útil que supimos hacer desde [Open Data Córdoba](https://www.opendatacordoba.org/) y que suele ser un tema de interés en la [prensa local](https://www.lavoz.com.ar/ciudadanos/cuales-son-las-localidades-de-cordoba-que-mas-estan-creciendo-en-habitantes-ahora/): **analizar migraciones dentro de la provincia de Córdoba basado en los cambios de domicilio, según los padrones electorales**. Como Facu se emocionó cuando le explicaba, le prometí que, si me conseguía el último padrón, se lo actualizaría.  Así que empecemos por el final. Quedó así: 

<!-- TEASER_END -->
<iframe src="https://mgaitan.github.io/migraciones-padron-cordoba/index.html" width="111.11%" height="1160px" frameborder="0" style="transform: scale(0.9); transform-origin: top left;"></iframe>


## Cómo lo construimos (los LLMs y yo)

Andrés Vázquez, gran amigo y colega de ODC, conserva de forma obsesiva todo dato electoral que le pase cerca, mientras más crudo mejor. Por ejemplo, tenía en un backup los _tar.gz_ de varios padrones (algunos provinciales, otros nacionales) de 2011, 2013, 2015 y 2017 ya formateados en CSV o TSV (aunque no súper normalizados y hasta algunos sin cabeceras, pero _a dataset regalado no se le miran los headers_).  

Algunos días después, Facu me envió un link con el padrón de Córdoba de la última elección (2025) que había conseguido moviendo contactos. El problema: **no era un CSV**, ni una base de datos, ni siquiera el "aplicativo para Windows" (supongo que hecho por INDRA, habitual licitador de elecciones) que solía distribuirse en DVD hasta bien entrados los 2010s. Esta vez **eran cientos de PDFs de varias paginas con tablas**, uno por mesa. Es decir, el padrón que los partidos imprimen para que sus fiscales "punteen" cuántos (y quiénes) votaron durante la elección.

Así que este fue el primer trabajito: extraer texto a partir de esos PDFs, y con ese texto limpiar y reconstruir (via [expresiones regulares](https://es.wikipedia.org/wiki/Expresi%C3%B3n_regular)) un CSV homogéneo con las mismas columnas que los históricos: nombre, clase, DNI, dirección, sección, circuito, mesa, número de orden. 
Un trabajo similar al que hice [acá](https://mgaitan.github.io/posts/scrapping-de-pdf-con-ipython-y-pdftotext/). 

Para no tener que bajarme los varios gigas de PDFs que estaban en un Drive compartido, [lo hice directamente en Google Colab](https://colab.research.google.com/drive/1cvm7I-MfS_y28gtO9m42hSsn92n-A_cr?usp=sharing), pidiéndole todo al agente Gemini integrado. Que bajara los archivos, convitiera a texto (usó [pymupdf](https://pymupdf.readthedocs.io/en/latest/)), generara las expresiones regulares para extraer los datos de cada columna, y luego los uniera en un único CSV para todas las mesas. Cuando estuvo listo me subí el CSV de nuevo a GDrive y despues los bajé todos a mi compu. 

Ya con todos los CSVs, quería unificar todo en una sola base de datos. Recurrí entonces a la ayuda de [Codex de OpenAI](https://openai.com/es-419/codex/) (uno de los LLMs que tengo integrado a mi IDE actual, [Zed](https://www.zed.dev/) via [ACP](https://agentclientprotocol.com/))

La pedí algo así al agente: 

```
A partir de los datasets del directorio actual, quiero crear una base de datos SQLite con tres tablas: `personas`, `elecciones` y `secciones`. La tabla `personas` guarda los datos intrínsecos a de cada persona (por ejemplo clase, DNI, nombre), la tabla `elecciones` registrará el año de elección y en qué sección, circuito y mesa aparece una persona en ese año, y la tabla `secciones` cataloga los nombres oficiales de secciones y circuitos. 

Tené en cuenta que no los datasets no son homogéneos y algunos no tienen headers, vas a tener que inferirlos a través de algunos valores. 
  
Creá un script python anotando los requerimientos en formato PEP723 y ejecutalo con `uv run <script>`. 
```

Esto es, básicamente, un tipo de proceso conocido como [ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load) y habitualmente la etapa más costosa (y muchas veces la más divertida) en el procesamiento y análisis de datos. 


Cuando Codex comenzó, me di cuenta de un problema operativo: como los datasets eran tan grandes, cuando el LLM intentaba leerlos, colapsaba. Entonces se me ocurrió hacer unas muestras, manteniendo la estructura pero de un tamaño manejable. Pedí versiones con solo las primeras 10 filas de cada archivo y me devolvió un bucle que ejecuta el comando `head -n 10` por cada archivo. 

```
for f in *.csv *.tsv; do
    [ -e "$f" ] || continue
    head -n 10 "$f" > "muestras/$f"
done
```

Ahí sí, con las muestras, creó un script Python `build_sqlite.py` que ejecutó y modificó algunas veces por su cuenta hasta que obtuvo un flamante `padrón.sqlite` que dió por listo. Yo verifiqué un par de datos a modo de sanidad y entonces le indiqué dónde estaban los datasets completos (¡le advertí que no los leyera!) para que volviera a ejecutar el script. Tardó un rato (me fui a ver el segundo tiempo de Boquita contra Tigre en el interín) pero cuando volví ya estaba mi nuevo `padron_full.sqlite` (de 1.8GB)

¿Qué se puede hacer con esta base de datos? Mucho. Desde las preguntas obvias (“¿cuántos electores hay en cada sección en 2015?”) hasta la más interesante que le había prometido a Facu: ¿cuántos DNI cambiaron de una sección a otra en cada eleccion? ¿Entre cuáles secciones?. 

Lo imaginé como un [diagrama de Sankey](https://es.wikipedia.org/wiki/Diagrama_de_Sankey) que explicara las migraciones entre secciones a lo largo del tiempo: columnas por elección, alto proporcional al tamaño de la sección y ancho de los flujos igual a la cantidad de electores que migran o permanecen. 

El prompt a la IA fue justamente ese: 

```
Tenés acceso a padron_full.sqlite. Quiero hacer el análisis de migraciones que habíamos charlado: visualizar la cantidad de electores que se muda de una seccion a otra (por ejemplo de CAPITAL a CALAMUCHITA) entre elección y elección. 

Quiero visualizarlo en un diagrama sankey: veremos cada "columna" que se corresponde con una eleccion, 2011, 2013, ... 2025.  Esas columnas estarán compuestas por segmentos que representan secciones electorales (usar nombres) en un alto proporcional a la cantidad de electores de esa seccion en la eleccion.  

El ancho del "flujo" (arco) desde cada segmento "A" de una columna a un segmento "B" de columna siguiente representa la migracion entre A y B.  

Quiero poder filtrar por secciones electorales y por un umbral para la cantidad de migrantes. 

Usar vega o d3.js para la visualización. 
```
  
# Qué programó Codex

Como había comenzado una sesión nueva, primero se puso a investigar la estructura de la base de datos. Si bien el `.sqlite` tiene la misma info que todos los CSVs originales, no hace falta leer todo para hacer queries, por lo que ya no tendría el problema de memoria al querer leer datos. 

Cuando supo qué tipo de consultas debía hacer, comenzó el script python que se centraba en las consultas SQL para generar un par de CSVs con los datos agregados, necesarios para el Sankey. Lo importante: 

- En qué años hubo elecciones, ordenados de menor a mayor. Esto determina la cantidad de columnas/pasos en el diagrama. 
- Qué cantidad de votantes hay por cada combinación de año y sección en la tabla 'elecciones'. Esto sirve para representar los segmentos de secciones en cada columna.  El [resultado es un CSV](https://github.com/mgaitan/migraciones-padron-cordoba/blob/main/seccion_sizes.csv) con la siguiente estructura:

```CSV
year,seccion,seccion_nombre,total
2011,1,CAPITAL,990289
2011,13,RIO CUARTO,192137
2011,3,COLON,164492
2011,20,SAN JUSTO,161216
2011,12,PUNILLA,135804
...
```

- Y por último, la query más costosa y valiosa. Qué número de votantes aparecen entre diferentes secciones electorales a lo largo de dos años específicos consecutivos. Es decir, cuántas personas votaron en una sección 'A' en el primer año y luego votaron en una sección 'B' en la elección siguiente. Esta query se ejecuta por cada "par" de años (2011, 2013), (2013, 2015), ..., (2017, 2025). 

En terminos de SQL: 

```sql
SELECT
    e1.seccion AS from_seccion,
    e2.seccion AS to_seccion,
    COUNT(*) AS count
FROM elecciones e1 INDEXED BY idx_elecciones_dni_anio
JOIN elecciones e2 INDEXED BY idx_elecciones_dni_anio
    ON e1.dni = e2.dni AND e2.anio = ?
WHERE e1.anio = ?
GROUP BY e1.seccion, e2.seccion
ORDER BY count DESC
```

Esa función produjo [este otro csv](https://github.com/mgaitan/migraciones-padron-cordoba/blob/main/migration_links.csv)

Finalmente escribió el dashboard en un único archivo HTML basado en [d3-sankey](https://github.com/d3/d3-sankey). 

Le fui pidiendo algunos ajustes menores (podés ver [el historial de git](https://github.com/mgaitan/migraciones-padron-cordoba/commits/main)) y quedó [aquí](https://mgaitan.github.io/migraciones-padron-cordoba/). 

## Un cambio de era 

Esto no es un trabajo académico. Ni siquiera aspira a ser ejemplo de mis habilidades técnicas. 

Es más, puede que tenga errores. Por ejemplo Andrés observó que sería bueno revisar la incorporación de los "mayores de 16" al padrón nacional y que no están en el padrón de Córdoba (y explicaría el cambio de tamaño de algunas secciones que aumentaron y disminuyeron en sucesivas elecciones). 

**Es, en cambio, un trabajo de divulgación**, pero no sobre el análisis "demográfico" en sí, ni siquiera sobre una visualización de datos en particular. En lo que **quiero hacer énfasis es en el *modus operandi***: construí esta pequeña aplicación en un par de tardes, sin prestarle mucha atención. Sólo sabía lo que quería y que era posible con los datos "crudos" con los que contaba, pero **no escribí ni una línea de código por mi cuenta** y esta vez tampoco revisé exhaustivamente, simplemente porque no es **tan** importante. 

Personas "no técnicas" como los amigos de EdIPo, que comprenden un dominio sobre el que tienen preguntas inteligentes que se pueden contestar con datos y gráficos, tienen hoy estos agentes (virtualmente gratuitos) de los que pueden obtener resultados sin tener que invertir el tiempo (¡a veces años!) en aprender un lenguaje de programación. 

Pero a la vez sin tener que invertir ese mismo tiempo en dominar herramientas específicas que prometen facilitar, a través de interfaces gráficas y trabajo manual, algunas tareas cuyos resultados, en el mejor de los casos, quedan "atrapados" en el programa o bien quedan limitados en funcionalidades. Ejemplos: PowerBI, qgis, Tableau, Excel, etc. 

Realizar todo un proceso de ETL y visualización de datos a través de un agente de programación supera a cualquier software específico porque **casi nada es más fácil que escribir en lenguaje natural** y el ecosistema tecnológico en el que te podés basar (por ejemplo con lenguajes como Python o Javascript, excelentemente dominados por los LLMs) es cuasi infinito. ¡Ya ni siquiera hace falta *promptear* en buen inglés o con [contorsiones especiales en la redacción](https://en.wikipedia.org/wiki/Prompt_engineering)!

Sociólogxs del mundo, periodistas de investigación, filósofxs, politólogxs, ¡uníos! Esperamos sus dashboards interactivos para explicar sus hallazgos con datos.
