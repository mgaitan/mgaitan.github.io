# Guía de estilo del blog de Martín Gaitán

## Voz

- Escribir en primera persona, en español rioplatense y con voseo natural.
- Partir de una escena, necesidad o manía concreta. La explicación técnica aparece porque hace
  falta resolver algo, no como una demostración abstracta.
- Usar humor seco, autocrítica y juegos de palabras con moderación. No forzar chistes ni convertir
  el texto en publicidad.
- Mantener una voz curiosa y artesanal: contar qué se probó, por qué se eligió una solución y qué
  limitaciones siguen abiertas.
- Preferir palabras corrientes a jerga empresarial. Explicar la jerga técnica la primera vez que
  realmente sea necesaria.

## Estructura habitual

1. Abrir con una anécdota, observación personal o cita que contenga el problema.
2. Presentar pronto el artefacto o la idea y, cuando existe, una forma de probarlo.
3. Insertar `<!-- TEASER_END -->` después de que la promesa del artículo quede clara.
4. Desarrollar la motivación y luego el funcionamiento con subtítulos concretos.
5. Incluir ejemplos, comandos, capturas o diagramas cuando aclaren el flujo.
6. Contar decisiones y límites con honestidad; distinguir lo que funciona de lo que podría existir.
7. Cerrar con próximos pasos, preguntas abiertas o una invitación específica a usar o mejorar el
   proyecto.

## Ritmo y recursos

- Alternar párrafos narrativos con listas o pasos cuando el lector necesita actuar.
- Usar preguntas retóricas para acompañar el razonamiento, sin abusar.
- Los paréntesis y notas al pie pueden alojar desvíos graciosos o contexto lateral.
- En tutoriales, ser preciso y preventivo: señalar riesgos, verificaciones y caminos alternativos.
- En artículos de proyectos, incluir la arquitectura suficiente para que otra persona entienda o
  reproduzca la idea.
- Usar enlaces en contexto, no una bibliografía separada sin explicación.

## Convenciones del repositorio

- Los posts nuevos pueden escribirse en Markdown dentro de `posts/`.
- Incluir metadatos Nikola al comienzo: título, slug, fecha, tags, categoría, descripción y autor.
- Mantener `category: projects` para proyectos propios salvo una razón clara para otra categoría.
- Usar Mermaid mediante imágenes de `https://mermaid.ink/` cuando un diagrama explique mejor un
  flujo que varios párrafos.
- Conservar acentos y caracteres del español. Los ejemplos de código y claves técnicas deben usar
  el formato literal que corresponda.

## Evitar

- Entradas que comiencen con una definición genérica o un resumen de marketing.
- Superlativos, promesas infladas, lenguaje de startup y conclusiones fingidamente definitivas.
- Explicar cada línea de código o añadir secciones que no hagan avanzar la historia.
- Homogeneizar errores o giros históricos del archivo: esta guía orienta textos nuevos, no exige
  reescribir el pasado.
