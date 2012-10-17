Un típico uso de un ``ListCtrl`` es usarlo para mostrar un Log de la
aplicación que muestra mensajes al usuario, similar a lo que puede hacer
la barra de estada, pero con la ventaja (complementaria, si se quiere),
de mantener un historial de los eventos ocurridos.

.. figure:: local/cache-vignettes/L510xH114/log-4afe3.jpg
   :align: center
   :alt: 
En tal caso, primero, hay una decisión de diseño que hacer: ¿los nuevos
mensajes se agregan al inicio (como un blog) o al final de la lista
(como los comentarios) ?

No sé si existe una respuesta canónica a la cuestión, pero infiriendo
(de los pelos) el sentido de lectura occidental (de izquierda a derecha
y de arriba hacia abajo) decidí que "un nuevo contenido" debe estar
abajo del anterior.

Eso trae aparejado un nuevo problema: si se agrega un nuevo item a
ListCtrl al final y ya hay más de los que caben en el espacio visible
del control, el último (el más importante) no se verá en pantalla y el
usuario debería hacer un scroll hasta el final para verlo. Es decir,
para un panel de Log, el scroll vertical siempre debería mantenerse
abajo.

Por suerte no hay que liarse con generar eventos programaticamente, ni
manipular el scroll, ni obtener dimensiones del widget. He aquí una
solución *"fits your brain"*: el método
`EnsureVisible(index) <http://www.wxpython.org/docs/api/wx.ListCtrl-class.html>`_

Por ejemplo:

::

        def OnAppendLog(self, msg):
            ico = self.icon_map[msg.data[0]]
            message = msg.data[1]
            index = self.list.InsertImageStringItem(sys.maxint, message, ico)
            self.list.SetStringItem(index, 1, time.strftime('%H:%M:%S'))
    
            self.list.EnsureVisible(index) #keep scroll at bottom

