#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
import urllib
import csv
import subprocess
from pyquery import PyQuery

SITE = 'http://nqnwebs.com/'
TARGET_SITE = 'http://mgaitan.github.com/'
POST_PATH = os.path.join(os.path.dirname(__file__), 'posts')
IMG_PATH = os.path.join(os.path.dirname(__file__), 'images')
DOWNLOADS_PATH = os.path.join(os.path.dirname(__file__), 'downloads')


HTML_PLAN = """
<ul>

    <li><a href="blog/article/apuntes-del-pycamp-2011">Apuntes del PyCamp 2011</a></li>

    <li><a href="blog/article/auto-podcast">Auto Podcast </a></li>

    <li><a href="blog/article/backup-selectivo-de-tablas-mysql">Backup selectivo de tablas Mysql</a></li>

    <li><a href="blog/article/bonito-feito-pero-efectivo">Bonito, feito pero efectivo</a></li>

    <li><a href="blog/article/cdpedia-0-7-disponible">CDPedia 0.7 disponible</a></li>

    <li><a href="blog/article/charla-ser-freelance-como-trabajar">Charla "Ser Freelance: Cómo trabajar en ojotas desde el living de tu casa"</a></li>

    <li><a href="blog/article/charla-myhdl-de-python-al-siliicio">Charla: MyHDL, de Python al silicio</a></li>

    <li><a href="blog/article/charla-python-a-los-bifes">Charla: Python a los bifes</a></li>

    <li><a href="blog/article/como-volver-a-compartir-desde">Cómo volver a compartir desde Google Reader</a></li>

    <li><a href="blog/article/compartiendo-documentacion-de">Compartiendo documentación de paquetes Python</a></li>

    <li><a href="blog/Control-de-Versiones-con">Control de Versiones con Subversion</a></li>

    <li><a href="blog/article/covertura-de-los-oscars-2011">Covertura de los Oscars 2011</a></li>

    <li><a href="blog/article/cuevanalinks-ahora-para-seres">Cuevanalinks, ahora para seres humanos</a></li>

    <li><a href="blog/article/de-mercurial-a-git-limpieza">De mercurial a git, limpieza mediante</a></li>

    <li><a href="blog/article/de-otra-galaxia">De otra galaxia</a></li>

    <li><a href="blog/article/deja-que-el-servidor-trabaje-por">Deja que el servidor trabaje por tí con GNU Screen</a></li>

    <li><a href="blog/article/digitalizando-recuerdos-con">Digitalizando recuerdos con mencoder</a></li>

    <li><a href="blog/article/disqus-para-spip">Disqus para SPIP</a></li>

    <li><a href="blog/article/django-dash-hace-una-aplicacion">Django Dash: hacé una aplicación web en 2 dias</a></li>

    <li><a href="blog/article/el-numero-mi-primer-juego">El Número, mi primer juego</a></li>

    <li><a href="blog/article/el-quijote-del-software-libre">El Quijote del Software Libre</a></li>

    <li><a href="blog/article/esqueletos-accion">Esqueletos Acción</a></li>

    <li><a href="blog/Esqueletos-de-aten-org-ar">Esqueletos de aten.org.ar</a></li>

    <li><a href="blog/article/gpec-2010-el-poster">GPEC 2010: El poster</a></li>

    <li><a href="blog/article/grosa">Grosa</a></li>

    <li><a href="blog/article/hemisferio-derecho">Hemisferio derecho</a></li>

    <li><a href="blog/article/integracion-de-dineromail-en">Integración de DineroMail en SimpleCart (js) </a></li>

    <li><a href="blog/article/ipython-la-interactividad-al-poder">IPython, la interactividad al poder</a></li>

    <li><a href="blog/jQuery-una-introduccion">jQuery, una introducción</a></li>

    <li><a href="blog/article/la-academia-las-practicas-agiles-y">La academia, las prácticas ágiles y el UML</a></li>

    <li><a href="blog/article/la-sanguijuela-de-cuevana">La sanguijuela de cuevana</a></li>

    <li><a href="blog/article/learning-python-4th-edition">Learning Python, 4th Edition</a></li>

    <li><a href="blog/article/limitar-la-cantidad-de-caracteres">Limitar la cantidad de caracteres de los comentarios</a></li>

    <li><a href="blog/article/lo-que-hace-un-geek-cuando-ama">Lo que hace un geek cuando ama</a></li>

    <li><a href="blog/article/lorem-ipsum-para-spip">Lorem Ipsum para Spip</a></li>

    <li><a href="blog/article/mantener-el-scroll-vertical-de-wx">Mantener el scroll vertical de wx.ListCtrl abajo</a></li>

    <li><a href="blog/article/me-cago-en-vos-afip">Me cago en vos, AFIP</a></li>

    <li><a href="blog/article/me-recibi-el-mes-pasado">Me recibí (el mes pasado)</a></li>

    <li><a href="blog/article/modelos-de-negocio-floss-la">Modelos de negocio FLOSS, la universidad, el sector privado y el Estado</a></li>

    <li><a href="blog/article/monetizar-pagos-virtuales-en">Monetizar pagos virtuales en Argentina sin costo </a></li>

    <li><a href="blog/article/mostrar-u-ocultar-contenido-facil">Mostrar u ocultar contenido, fácil</a></li>

    <li><a href="blog/article/pep-20-el-zen-del-barca">Pep 20: El Zen del Barça</a></li>

    <li><a href="blog/article/personalizar-el-texto-de">Personalizar el texto de #INTRODUCTION</a></li>

    <li><a href="blog/article/piccola-radiolina">Piccola Radiolina</a></li>

    <li><a href="blog/article/preparados-listos-en-un-rato">Preparados, listos... en un rato</a></li>

    <li><a href="blog/article/principios-para-un-freelancear">Principios para un "freelancear" exitosamente</a></li>

    <li><a href="blog/article/project-euler-problema-2">Project Euler, Problema #2</a></li>

    <li><a href="blog/article/pyconar-2010-el-orgullo-de">PyConAr 2010, el orgullo de pertenecer</a></li>

    <li><a href="blog/article/referenciar-figuras-por-numero-en">Referenciar figuras por número en Sphinx / Latex</a></li>

    <li><a href="blog/article/resolviendo-project-euler-con">Resolviendo Project Euler con Python</a></li>

    <li><a href="blog/article/revista-orsai-no-3-en-cordoba">Revista Orsai Nº 3 en Córdoba</a></li>

    <li><a href="blog/article/simplecart-js-para-spip">SimpleCart(js) para SPIP</a></li>

    <li><a href="blog/article/spicasa-adjunta-fotos-de-picasa-a">Spicasa: adjuntá fotos de picasa a un artículo</a></li>

    <li><a href="blog/SPIP-el-Gestor-de-Contenidos">SPIP, el Gestor de Contenidos</a></li>

    <li><a href="blog/article/suscribirse-a-los-comentarios-por">Suscribirse a los comentarios por RSS</a></li>

    <li><a href="blog/article/ultima-version-de-spip-por-svn">Ultima versión de Spip por SVN</a></li>

    <li><a href="blog/article/un-gran-lenguaje-una-gran">Un gran lenguaje, una gran comunidad</a></li>

    <li><a href="blog/article/un-spip-para-muchos-sitios">Un SPIP para muchos sitios</a></li>

    <li><a href="blog/article/una-introduccion-a-python">Una introducción a Python</a></li>

    <li><a href="blog/article/una-mejor-manera-de-controlar-los">Una mejor manera de controlar los atributos en SPIP</a></li>

    <li><a href="blog/article/usando-pubsub-para-una-panel-de">Usando PubSub para un panel de mensajes</a></li>

    <li><a href="blog/article/variar-o-no-variar-esa-es-la">Variar o no variar, esa es la cuestión</a></li>

    <li><a href="blog/article/veinteanero">Veinteañero</a></li>

    <li><a href="blog/article/video-sis-771-671-en-ubuntu">Video SIS 771/671 en Ubuntu</a></li>

    <li><a href="blog/article/voto-electronico-e-ingenieros">Voto electrónico e ingenieros analógicos</a></li>

    <li><a href="blog/article/yahoo-pipes-como-por-un-tubo">Yahoo! Pipes como por un tubo</a></li>

    <li><a href="blog/article/yendo-a-las-fuentes-de-cuevana-tv">Yendo a las fuentes de cuevana.tv</a></li>

    <li><a href="blog/article/basta-de-ie6">¡Basta de IE6!</a></li>

    <li><a href="blog/article/c-automatico">&copy; automático</a></li>

</ul>
"""

def write_meta(title, slug, date, tags=[]):
    with codecs.open(os.path.join(POST_PATH, slug + '.meta'), 'w', 'utf-8') as meta:
        meta.write(title + '\n')
        meta.write(slug + '\n')
        meta.write(date.replace('-', '/') + '\n')
        meta.write(', '.join(tags))


def retrieve_file(relative_url):
    """download a file from the site and return a relative local path"""
    basename = os.path.basename(relative_url)
    if basename[-3:].lower() in ('jpg', 'png', 'gif'):
        dest_path = os.path.join(IMG_PATH, basename)
        rel_path = '/images/' + basename
    else:
        dest_path = os.path.join(DOWNLOADS_PATH, basename)
        rel_path = '/downloads/' + basename
    if not os.path.exists(dest_path):
        urllib.urlretrieve(SITE + relative_url, dest_path)
    return rel_path


def retrieve_article(relative_url):

    slug = relative_url.replace('blog/article/', '')
    abs_url = SITE + relative_url
    html_path = os.path.join(POST_PATH, slug + '.html')
    rst_path = os.path.join(POST_PATH, slug + '.rst')
    print 'Migrating %s to %s...' % (abs_url, rst_path)
    with codecs.open(html_path, 'w', 'utf-8') as html_file:
        page = PyQuery(abs_url)
        date = page('span.date').attr('title')
        tags = [page(t).text() for t in page('a.tag')]
        title = page('.mititulo').text()

        write_meta(title, slug, date, tags)


        # cleanup html
        page('*').removeClass('spip spip_out')
        page('code.spip_code').removeAttr('class')     # inline code
        page('*[class=""]').removeAttr('class')

        # unwrap code blocks
        for code in page('.spip_code code'):
            code_tag = page(code)
            lang = code_tag.attr('class')
            code_content = code_tag.html().replace('<br /><br />', '\n').\
                                           replace('<br />', '').\
                                           replace('>&#13;', '')
            com_lang = '<!-- %s -->\n' % lang if lang else ''
            code_tag.parent('.spip_code').replaceWith(
                            u'%s<pre>%s</pre>' % (com_lang, code_content)
                        )

        # unwrap .cadre
        for code in page('textarea.spip_cadre'):
            code_tag = page(code)
            code_content = code_tag.text()
            code_tag.parents('form').replaceWith(u'<pre>%s</pre>' % code_content)

        # download docs
        for a in page('dl.spip_documents dt a'):
            a_tag = page(a)
            icon = a_tag.children()
            rel_path = retrieve_file(a_tag.attr('href'))
            icon_path = retrieve_file(icon.attr('src'))
            dl = a_tag.parents('dl.spip_documents')
            description = dl.text()
            if description:
                description_row =  "<tr><td>%s</td></tr>" % description
            else:
                description_row = ""
            my_tag = """<table>
                        <tr><td><a href="%s"><img src="%s"></a></td></tr>
                        %s
                      </table>""" % (rel_path, icon_path, description_row)
            dl.replaceWith(my_tag)

        # download and unwrap images
        for img in page('dl dt img'):
            img_tag = page(img)
            rel_path = retrieve_file(img_tag.attr('src'))
            my_tag = "<img src='%s' />" % rel_path
            img_tag.parents('dl').replaceWith(my_tag)

        body = page('div.body').children()
        html_file.write(body.html())

        # convert
        subprocess.call(['pandoc', html_path, '-o', rst_path])
        return (abs_url, '%sposts/%s.html' % (TARGET_SITE, slug))

def migrate_all():
    pq = PyQuery(HTML_PLAN)
    urls = pq('li a')
    disqus_file = open('disqus.csv', 'w')
    disqus = csv.writer(disqus_file)
    for url in urls[3:4]:
        relative_url = url.attrib['href']
        row = retrieve_article(relative_url)
        disqus.writerow(row)
    disqus_file.close()


if __name__ == '__main__':
    #retrieve_article('blog/article/disqus-para-spip')
    migrate_all()
