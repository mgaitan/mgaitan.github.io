.. image:: /images/disqus-newlod23a-8b781.gif
   :align: right

Hace tiempo me interesa el servicio
`disqus.com <http://www.disqus.com>`_ que provee una plataforma de
comentarios muy poderosa y fácil de usar.

Comencé un `pequeño
plugin <http://zone.spip.org/trac/spip-zone/browser/_plugins_/disqus>`_
para integrar Disqus a `Spip <http://www.spip.net>`_.

+------------------------------------------------------------------+
| `Plugin Disqus para SPIP version 0.1 </downloads/disqus.zip>`_   |
+------------------------------------------------------------------+

Por ahora tiene dos componentes básicos:

#. Un esqueleto inc-forum.html que reemplaza el esqueleto por defecto de
   SPIP (y su formulario) por Disqus
#. Un esqueleto para exportar comentarios existentes (genera un XML
   importable a traves del panel de disqus)

La configuración se realiza a través de una página (requiere el `plugin
CFG <http://plugins.spip.net/CFG>`_) donde se define el *"Disqus
shortname"* (la identificación unica que asignamos al sitio donde
usaremos Diqus).

Para generar el XML con la exportación de comentarios preexistentes,
basta acceder a ``/?page=export_comments_to_disqus`` y luego importar
ese archivo desde el panel de Disqus (Tools -> Import/Export )
