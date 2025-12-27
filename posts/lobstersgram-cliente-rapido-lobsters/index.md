.. title: Lobstersgram, un cliente rápido de lobste.rs en Telegram
.. slug: lobstersgram-cliente-rapido-lobsters
.. date: 2025-12-26 23:02:16
.. tags: telegram, lobsters, python, rss, github-actions, telegra.ph
.. category: projects
.. description: Un bot serverless que te manda posts de lobste.rs a Telegram con lectura limpia.
.. author: Martín Gaitán

Lobsters ([lobste.rs](https://lobste.rs)) es probablemente mi fuente principal[^1] de lecturas técnicas: es una curación hecha por humanos que prioriza la calidad de los contenidos, sin clickbaiting ladino, publicidad abusiva o comentarios hostiles. Si bien no soy miembro (requiere una [invitación](https://lobste.rs/about#invitations)), comulgo fuertemente con su [espíritu de la "vieja internet"](https://lobste.rs/about). 

[^1]: Otras partes de mi dieta informativa ñoña son el blog de [Simon Willison](https://simonwillison.net/) y los ["trending" de Github](https://github.com/trending). 

Ayer, mayormente desde ChatGPT en el teléfono, hice Lobstersgram, un bot que funciona como un cliente rápido de lobste.rs en Telegram. 

Cada cierto tiempo, si el bot detecta que hay artículos nuevos publicados en el sitio, te manda un mensajito con una intro y un link del artículo copiado a [telegra.ph](https://telegra.ph), además del link a la fuente original y al hilo de discusión en el foro. ¿Por qué republicar en telegraph? Porque soporta el modo [instant view](https://instantview.telegram.org/), que permite precargar el contenido con un estilo simple y unificado, ideal para leer desde el móvil.

Si tenés Telegram, podés probarlo en [@lobstersgram_bot](https://t.me/lobstersgram_bot)

Comandos:

- `/start` para suscribirte
- `/unsubscribe` para dejar de recibir

(Atención, solo funciona cada 2 horas, así que eventualmente te va a responder, pero no esperes inmediatez)

Acá una demo que grabé capturando la pantalla del celu (con notificación de un mensaje al grupo familiar incluida)

<iframe height="660" width="355" src="https://www.youtube.com/embed/wdzIBFYjJ3Y" title="Lobstergram demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<!-- TEASER_END -->

## Buscando una mejor experiencia de lectura

Lobsters ofrece un RSS de tipo "agregación" que contiene los links a los artículos que se comparten, pero no incluye el contenido de cada uno. Entonces no hay mucha diferencia entre un lector RSS tradicional y ver el sitio directamente en la web, que es muy sencilla, donde básicamente clickeás en los títulos de los artículos que te interesan. 

Si bien la mayoría de las veces son artículos de blogs que no tienen publicidad y son muy livianos, igual la experiencia de usuario tiene el costo cognitivo de leer en distintos estilos y tener que ir y volver entre las fuentes y lobsters. Por otro lado, para las conexiones malas que aún se tienen por estos lares (por ejemplo, cuando estás de viaje por la Patagonia, como yo ahora), no viene mal que las lecturas ya estén disponibles, cualesquiera sean las condiciones.  
 
Lobstersgram mejora esta experiencia de usuario principalmente para leer desde el teléfono. 

El flujo de lo que hace es el siguiente: 

- lee el RSS de Lobsters
- de cada link extrae el contenido principal, o sea un "scraping dinámico" [^2]. 
- Convierto el html a markdown
- Con el markdown hace un DOM de telegra.ph para crear un post programáticamente, creando la copia del artículo original. 
- Con ese link, recortando un cachito del markdown y el resto de las urls (original + foro) sacadas del RSS, mando un mensaje a cada suscriptor del bot. 

[^2]: Probé [trafilatura](https://trafilatura.readthedocs.io/) pero me quedé con el viejo [readability](https://github.com/buriy/python-readability) porque daba mejor resultado. 


## Mirá mamá, sin server y sin db (y gratis!)

Los bots de Telegram funcionan vía webhooks (el server hace un "push" del mensaje en tiempo real) o long polling, que es la que nos interesa: en vez de consultar constantemente si hay nuevos mensajes, el bot hace una petición al servidor que queda abierta un ratito esperando hasta que llegue un update o se acabe el tiempo, e inmediatamente o, **cuando puede**, vuelve a pedir otra.   

GitHub Actions nos da un server básico (como dicen en [Tiranos Temblad](https://www.youtube.com/@TiranosTembladTV), ¡Que viva lo gratis!) que alcanza lo más bien para correr un programita sin muchas pretensiones por pocos minutos. Y nuestro bot es eso: un script Python que no demora demasiado. 

La acción que dispara el workflow es un "cron" (schedule, en la jerga de github actions) y entonces cada 2 horas el bot se fija si tiene que actualizar la lista de susbcriptores (se agregaron / desagregaron) y si hay historias que enviar. 

Para que la cosa funcione tambien hace falta una minima persistencia de datos. ¿De donde va a sacar el bot la lista de usuarios que quieren recibir las novedades? ¿Y cuando se lee Lobsters, como sabe cuales articulos ya envió en corridas anteriores? 

Para eso hay un `state.json` y un `subscribers.json` cuyo fin, espero, no requieren explicación.  

Telegram no te deja enviar mensajes a chats que nunca interactuaron con el bot. Por eso el flujo es:

1. el usuario manda `/start`
2. el workflow corre en modo `--sync-subscribers`
3. se agregan los `chat_id` en `subscribers.json`
4. en el modo normal se manda cada post a esos chats

Si alguien quiere dejar de recibir, manda `/unsubscribe` y en la proxima corrida se lo elimina.

Acá un diagramita que resume el asunto:

[![](https://mermaid.ink/img/pako:eNq1kz1v2zAQhv_K4aYGtRTZom2JQ4B-APLQqbGXQAtNXWy2EqnyI2hq-L-XivLRVFk6VBPJ97l7j3fUCaVpCDnW2tGPQFrSZyUOVnS1hvj1wnolVS-0hx0IBzsXhFVmqm6rQd5SS29HV5tBr5TfhD18kF4Z7abUR-MH7IvZO092zDRSu-TqaltxuHQ-8uPZtkriabXhEPpGeIKedKNIexr1ahPlmJJDkrh7LRMX9k5atSf76B3FJyTemg4CBPwBpd-c0S9kRHccpNG3ynZCqkH728nJIzWhJZCiEbA4TnxaIvh6fQ3vQVoS4MeOpf0rcrgp6TslQJuhObEnrwp7uyvwTge6MxDGIV38vy6NPi_gpJ6gn8V_r2LiSq3qlBbQ0GQ6OMODVQ1ybwPNsKM4mWGLpyFLjf5IHdXI47IR9nsdX_o5xsTXdmNM9xRmTTgckd-K1sXdWOHjj_CMxHrJfjJBe-TlQwbkJ_yJPJ9n6SLLssVyzdiKZcV6hvfI52U6z_NVUa7YnK1ZucjPM_z1YJqlJcuWZcGKdbFkWZaX59_j-CEj?type=png)](https://mermaid.live/edit#pako:eNq1kz1v2zAQhv_K4aYGtRTZom2JQ4B-APLQqbGXQAtNXWy2EqnyI2hq-L-XivLRVFk6VBPJ97l7j3fUCaVpCDnW2tGPQFrSZyUOVnS1hvj1wnolVS-0hx0IBzsXhFVmqm6rQd5SS29HV5tBr5TfhD18kF4Z7abUR-MH7IvZO092zDRSu-TqaltxuHQ-8uPZtkriabXhEPpGeIKedKNIexr1ahPlmJJDkrh7LRMX9k5atSf76B3FJyTemg4CBPwBpd-c0S9kRHccpNG3ynZCqkH728nJIzWhJZCiEbA4TnxaIvh6fQ3vQVoS4MeOpf0rcrgp6TslQJuhObEnrwp7uyvwTge6MxDGIV38vy6NPi_gpJ6gn8V_r2LiSq3qlBbQ0GQ6OMODVQ1ybwPNsKM4mWGLpyFLjf5IHdXI47IR9nsdX_o5xsTXdmNM9xRmTTgckd-K1sXdWOHjj_CMxHrJfjJBe-TlQwbkJ_yJPJ9n6SLLssVyzdiKZcV6hvfI52U6z_NVUa7YnK1ZucjPM_z1YJqlJcuWZcGKdbFkWZaX59_j-CEj)

Tanto `state.json` como `subscribers.json` se autocommitean (si cambiaron) dentro del workflow desde GitHub Actions. Esta idea de usar git como storage de datos está un poco inspirada en la técnica de [Git scraping](https://simonwillison.net/2020/Oct/9/git-scraping/). 

Ejemplos de uso del CLI:

```console
uv run python main.py --sync-subscribers
uv run python main.py --max-items 1
uv run python main.py --url https://mgaitan.github.io/posts/ampliando-el-universo-python-con-rust/
```

El modo `--url` es interesante porque procesa una o más urls arbitrarias por fuera del RSS. Cuando el workflow de GitHub Actions se lanza manualmente (o vía API), se puede pasar una lista de urls y correrá en este modo, que llega igual, pero obviamente sin el link al foro: 

<img width="568" height="281" alt="image" src="https://gist.github.com/user-attachments/assets/d18e12fc-361c-475e-a1a3-7fd54ea3c835" />

De paso, si querés forzar que los mensajes te lleguen solo a vos cuando estás desarrollando, exportá esta variable de entorno que tendrá prioridad sobre el json:

```bash
export TELEGRAM_DEV_CHAT_ID=123456789
```

## ¿Y qué sigue?  

Probablemente nada, pero el repo está en [mgaitan/lobstersgram](https://github.com/mgaitan/lobstersgram) y es todo tuyo para hacer un fork. El convertidor de "markdown to telegra.ph" necesita algunas mejoras y, como me pidió mi amigo [Alvar Maciel](https://alvarmaciel.gitlab.io/), el archivo `subscribers.json` deberia estar encriptado (lo podemos hacer via [sops](https://github.com/nhedger/setup-sops)) para no exponer ninguna data.

En cuanto a funcionalidades potenciales, fácilmente se podría permitir que los subscriptores definan la lista de feeds que quieren consumir, haciendolo un lector de RSS/Atom en Telegram general. 

También podría funcionar como una app "read it later" minimalista y/o una comunidad de lectura: le enviamos una url al bot y este, cuando corre, procesa todo lo que le llegó en modo `--url`.

¿se te ocurre algo más?
