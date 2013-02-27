.. title: Cómo funciona Cuevana
.. slug: como-funciona-cuevana
.. date: 2013/02/26 22:17:55
.. tags: draft
.. link:
.. description:

Estimando cuanto trabajo significa actualizar `Cuevana sources <http://userscripts.org/scripts/show/98017>`_
y/o `Cuevanalib <https://bitbucket.org/tin_nqn/cuevanalib>`_
investigué cómo funciona la nueva versión de cuevana.

Estas notas son el resultado de lo que fui observando.

Una vez que se elige un contenido, un iframe apunta a una URL de este formato
http://www.cuevana.tv/player/sources?id=4773&tipo=pelicula

En código javascript inline define las fuentes disponibles para ese contenido

.. code-block:: javascript

    var plugin_ver = 5, plugin_rev = 0;
    var actual_ver, actual_rev;

    var sources = {
        "2": {
            "360": ["uptobox", "uploadcore", "vidbull", "bayfiles", "filebox", "cramit", "zalaa"],
            "720": ["uploadcore", "vidbull", "bayfiles", "cramit"]
        }
    }, sel_source = 0;

La primer clave (en este caso ``2``, inglés) es el idioma del audio,
y la segunda la calidad del video

Luego define diferentes constates:

.. code-block:: javascript

    var label = {
        '360': 'SD (360p)',
        '480': 'SD (480p)',
        '720': 'HD (720p)',
        '1080': 'HD (1080p)'
    };
    var labeli = {
        "1": "Espa\u00f1ol",
        "2": "Ingl\u00e9s",
        "3": "Portugu\u00e9s",
        "4": "Alem\u00e1n",
        "5": "Franc\u00e9s",
        "6": "Coreano",
        "7": "Italiano",
        "8": "Tailand\u00e9s",
        "9": "Ruso",
        "10": "Mongol",
        "11": "Polaco",
        "12": "Esloveno",
        "13": "Sueco",
        "14": "Griego",
        "15": "Canton\u00e9s",
        "16": "Japon\u00e9s",
        "17": "Dan\u00e9s",
        "18": "Neerland\u00e9s",
        "19": "Hebreo",
        "20": "Serbio",
        "21": "\u00c1rabe",
        "22": "Hindi",
        "23": "Noruego",
        "24": "Turco",
        "26": "Mandar\u00edn",
        "27": "Nepal\u00e9s",
        "28": "Rumano",
        "29": "Iran\u00ed",
        "30": "Est\u00f3n",
        "31": "Bosnio",
        "32": "Checo",
        "33": "Croata",
        "34": "Fin\u00e9s",
        "35": "H\u00fanagro",
        "36": "Persa",
        "38": "Indonesio"
    };
    var labelh = {
        'filebox': 'Filebox',
        'uptobox': 'Uptobox (NUEVO)',
        'uploadcore': 'Uploadcore (NUEVO)',
        'vidbull': 'Vidbull (NUEVO)',
        'zalaa': 'Zalaa',
        'cramit': 'Cramit',
        '180upload': '180upload',
        'bayfiles': 'Bayfiles'
    };

El usuario selecciona mediante un menú donde se define ``audio``, ``quality`` y ``source``
que se ofrencen en links con el formato ::

.. code-block::

    <a class="sel" data-type="quality" data-id="360">SD (360p)</a>

Donde ``data-type`` es el tipo de variable, ``data-id`` el valor para esa opción
y ``class="sel"`` determina si esa es la opción seleccionada.

Cuando se aprieta el botón Play se invoca la URL:

    http://www.cuevana.tv/player/source_get?def=**quality**&audio=**audio**&host=**source**&id=4773&tipo=pelicula

Por ejemplo:

    http://www.cuevana.tv/player/source_get?def=360&audio=2&host=bayfiles&id=4773&tipo=pelicula

Esta página presenta el captcha, que una vez superado redirige a la URL:

    http://go.cuevana.tv/?*URL_DESTINO*

Por ejemplo:

    http://go.cuevana.tv/?http%3A%2F%2Fbayfiles.com%2Ffile%2FvIsf%2FkTvfNj%2Fthe.apparition.2012.bdrip.xvid-sparks.mp4%3Fcid%3D4773%26ctipo%3Dpelicula%26cdef%3D360

Que a su vez redirige a *URL_DESTINO* que es la URL del servicio donde el video está hosteado
con parámetros extra: ``?cid=4773&ctipo=pelicula&cdef=360``. En el ejemplo anterior:

    http://bayfiles.com/file/vIsf/kTvfNj/the.apparition.2012.bdrip.xvid-sparks.mp4**?cid=4773&ctipo=pelicula&cdef=360**

Aquí entra en juego el "plugin de cuevana". Se puede bajar por ejemplo
la versión para Firefox desde http://www.cuevana.tv/player/plugins/cstream-5.0.xpi
Descomprimirlo con unzip y abrir el archivo ``content/cuevanastream.js``

La presencia de los parámetros ``cid``y ``ctipo`` y una url de alguno de los servicios
que usa Cuevana hace que se inyecte un javascript en la URL del servicio.

.. code-block:: javascript

    var loc = (window.location.href.match(/cid=/i) && window.location.href.match(/ctipo=/i));
    if (window.location.href.match(/^http:\/\/(www\.)?bayfiles\.com/i) && loc) {
        addScript('bayfiles');
    }

        // más servicios

      else if (window.location.href.match(/^http:\/\/(www\.|beta\.)?cuevana\.(com|co|tv|me)/i)) {
        var n = document.createElement('div');
        n.id = 'plugin_ok';
        n.setAttribute('data-version', '5');
        n.setAttribute('data-revision', '0');
        document.body.appendChild(n);
    }

    function addScript(id) {
        var s = document.createElement('script');
        s.setAttribute('type', 'text/javascript');
        s.setAttribute('src', 'http://sc.cuevana.tv/player/scripts/5/' + id + '.js');
        document.getElementsByTagName('head')[0].appendChild(s);
    }

En ese caso se inyecta el javascript:

    http://sc.cuevana.tv/player/scripts/5/bayfiles.js

Que es el encargado de parsear html para obtener la url real de descarga,
resolver/exponer el captcha si existiera, esperar el tiempo de guarda
del servicio y redirigir al reproductor de cuevana::

    window.location.href = 'http://www.cuevana.tv/#!/' + tipo + '/' + id + '/play/url:' + encodeURIComponent(a) + '/def:' + vars['cdef'];

Donde tipo es ``series`` o ``peliculas``, ``id`` es el identificador del contenido,
def es ``360`` o ``720`` y ``a`` es la url final del archivo mp4

    http://www.cuevana.tv/#!/' + tipo + '/' + id + '/play/url:' + encodeURIComponent(a) + '/def:' + vars['cdef'];

El reproductor carga el subtitulo desde la siguientes URL.

Para series:

    http://sc.cuevana.tv/files/s/sub/**ID**_**LANG**.srt

Donde ``ID`` es el identificador del contenido y ``LANG`` es el código
del idioma en 2 letras mayúsculas (ES, EN, etc.)

Para contenidos HD se agrega el sufijo *_720*

    http://sc.cuevana.tv/files/s/sub/**ID**_**LANG**_720.srt

Para peliculas es análogo pero un nivel más arriba.

    http://sc.cuevana.tv/files/sub/**ID**_**LANG**.srt

Y eso es todo lo que necesitamos saber.
