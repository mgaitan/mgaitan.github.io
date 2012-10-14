La aplicación que estoy desarrollando,
`GPEC <http://code.google.com/p/gpec2010>`_, genera muchos mensajes que
pueden ser útiles para el usuario.

En softwares con *GUI’s* sencillas suele utilizarse la barra de estado
para mostrar mensajes contextuales e información sobre el resultado de
una acción. Pero si estos mensajes son muchos y de diversa índole, este
espacio puede no bastar, sobre todo por la volatilidad de la información
que la barra de estado muestra.

Una solución posible es usar un panel con un ``ListCtrl`` de manera de
poder agregar los mensajes quedando un registro completo y cronológico;
un *log* propiamente dicho.

|image0|
Surge acá un detalle: si los mensajes se generan desde "cualquier parte"
del programa, todas esas "partes" deberían tener referencia de la
instancia del panel/widget de log.

Un ejemplo: todos las demostraciones de la aplicación de demo de
`wxPython <http://wxpython.org>`_ tienen la siguiente estructura:

::

    class TestPanel(wx.Panel):

        def __init__(self, parent, log):
            self.log = log
            wx.Panel.__init__(self, parent, -1)
            ...

            self.log.WriteText(' message ... ')

Esto vuelve la aplicación muy acoplada: la instancia ``log`` (que es un
caja de texto en el demo) se pasea por distintos *namespaces* para estar
disponible en todos lados.

Denotemos la falta de flexibilidad: ¿que pasa si queremos ’loggear’
mensajes desde un objeto donde no estaba previsto? ¿qué pasa si queremos
cambiar el widget que muestra los mensajes y el método para anexar
mensajes tiene otro nombre? ¿y si además de mostrarlos, con algunos los
mensajes queremos hacer alguna otra cosa (ejecutar un simple sonido de
alarma, por ejemplo) ?

PubSub
~~~~~~

Una manera más elegante y eficiente es utilizar
`PubSub <http://pubsub.sourceforge.net>`_ una implentación en Python del
paradigma de
`publicación-suscripción <http://en.wikipedia.org/wiki/Publish/subscribe>`_.

.. figure:: local/cache-vignettes/L510xH357/pubsub_concept-47f35.png
   :align: center
   :alt: 
Su implementación es trivial. Incluso viene incorporado dentro de
wxPython.

El ``Publisher`` (generalmente importado como ``pub``) envía mensajes
(cualquier objeto python) asociados a un tópico (una cadena)

::

    from wx.lib.pubsub import Publisher as pub

    pub.sendMessage('log', ('ok', 'Ready! You can send any message from anywhere.') )

En este ejemplo, el tópico, que elegí arbritrariamente, es ’log’, y el
mensaje es la tupla
``('ok', 'Ready! You can send any message from anywhere.')``

Del otro lado del mostrador, cualquiera puede suscribirse a los mensajes
con determinado tópico y asociarlos a un método/función.

::

    class LogMessagesPanel(wx.Panel):
        def __init__(self, parent, id):
            wx.Panel.__init__(self, parent, id)

            pub.subscribe(self.OnAppendLog, 'log')

        def OnAppendLog(self, msg):
            data = msg.data<img105|center>
            #do your things with the data!  

``pub.subscribe`` *bindea* los mensajes con tópico *’log’* al método
OnAppendLog pasando un objeto ``msg``. Nuestro mensaje real, la tupla
que enviamos, está en ``msg.data``

Nada impide que sean muchos los objetos que envien mensajes con tópico
*’log’* y muchos otros estén suscriptos a él. Y esto funciona sin
importar dónde ocurra cada cosa!
[`1 </blog/article/usando-pubsub-para-una-panel-de#nb1>`_].

Como ejemplo completo dejo el panel log. Podés probarlo creando otro
frame independiente que envie mensajes de log.

::

    #       Log Panel: example of PubSub implementation
    #       
    #       Copyright 2010 Martin Gaitán <gaitan(at)gmail.com>
    #       
    #       This program is free software; you can redistribute it and/or modify
    #       it under the terms of the GNU General Public License as published by
    #       the Free Software Foundation; either version 2 of the License, or
    #       (at your option) any later version.
    #       
    #       This program is distributed in the hope that it will be useful,
    #       but WITHOUT ANY WARRANTY; without even the implied warranty of
    #       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    #       GNU General Public License for more details.
    #       
    #       You should have received a copy of the GNU General Public License
    #       along with this program; if not, write to the Free Software
    #       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
    #       MA 02110-1301, USA.


    import wx
    from wx.lib.pubsub import Publisher as pub
    import time
    import sys

    from wx.lib.embeddedimage import PyEmbeddedImage

    icons = {}
    icons['ok'] = PyEmbeddedImage(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAAXNSR0IArs4c6QAAAK5QTFRF"
        "AAAA////2vO/+P3z+f31VJkEVJcEU5UEUpQEcc0GcMsGcMkGb8gGbcYGbcQGbMEGZLYFXKYF"
        "UJAET48ETo0ETYwEasAGddALd9ANeNERetETe9IVfdIXfdMZftMbf9Mci9cwlNpAlttElttF"
        "l9xHmtxLm91NnN1Pnd1Rnt5ToN9Xod9ZpuFhp+FjqOFlquJnr+RyseR0veiKwuqSy+2j4PTI"
        "9vzv9/zxidYs3fPCGN7g1AAAAAF0Uk5TAEDm2GYAAAABYktHRACIBR1IAAAACXBIWXMAAAsT"
        "AAALEwEAmpwYAAAAB3RJTUUH2gcMBC0Irn+MQAAAAINJREFUGNNjYCAJ6Bui8vXkpAxQ+LJa"
        "ylx6CL6utKYGJyszkGVpAuZLaahzsYH4phYKxgwMOpJqatzsID6ThbIGt5G+hKoKDweIz8Ai"
        "YaGtIiOnrMIrxAwxjJlXXl1VSYlPmBlmPLOAuLIivwgzwkJzQV4xUWZkJ5mzi7CgOtqMBbcH"
        "AVouCiZO5Tf/AAAAAElFTkSuQmCC")

    #----------------------------------------------------------------------
    icons['error'] = PyEmbeddedImage(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QAAAAAAAD5Q7t/AAAA"
        "CXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QsKCTIOk1O0sAAAAhpJREFUOMudk71Pk1EU"
        "xn/3bQvlo76gxBpNoGibArYLxJREh466MmnSgRH+IjsydGYjspBAWEQHMJIWmmhj+LAkpC1N"
        "Wyj2PcfhfUsQiRpPcnOTm/P8nuQ59xhuVA5SwDyQBsa95xKwDixlYOt6v7khfjscCi1MJpME"
        "w2F8AwOoKp2zM87LZYqFAtVmM5uBxd8AOXg3nUy+HJmZ4XJ7G+f0FBwHVUUMWEN38U9NUt3d"
        "5VOxuJqBVwC+rvN0Mvn6XixGe3MTbTRABFVBRUEEabboHHyjPxbDtqzoi2r1wTKsmBykhkOh"
        "98/m5rhYW0OdDqqKKqh6YgXFhakxBFMpPm9sUGu1Zi1gfjKR4HJnB3UcEFABFXEP6oEUVMFx"
        "uMjneTwWAZj3A+lg+D4/PnxERRkrf+dPtW/fQao1Ag8fAaT9wLjVP4iKG9jfSkRR7WB6AgDj"
        "FnCV9r8A8PpUBQA/UOrUzyYUg6rDl5ERt0HEvVE3PDdVRN0gtdkCKFnA+vnJCcYeuiL/Iu46"
        "iidWwRocpF2rAaxbwNL+3h6BeNwly3WRNzrtTkNQY/BHIpQODwGWrAxs1VqtbKWQp2fqqQu5"
        "5op3qygYQ080RuPggHq7nc3Alg9gGVaeVyqzts8XHUgkcBoN5KJ99RMVMHaI3vgEjXKZwvHx"
        "agbe3LpMdl/fwpPRUQK2jentRUVwmk069Tpfj466zou3buP/rPNPwkdmHrlYdncAAAAASUVO"
        "RK5CYII=")

    #----------------------------------------------------------------------
    icons['info'] = PyEmbeddedImage(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QAAAAAAAD5Q7t/AAAA"
        "CXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QMCBiAyOlCc9wAAADV0RVh0Q29tbWVudAAo"
        "YykgMjAwNCBKYWt1YiBTdGVpbmVyCgpDcmVhdGVkIHdpdGggVGhlIEdJTVCQ2YtvAAACq0lE"
        "QVQ4y5WSS0hUcRTGv//cO+O9OtdHJllqZlI+CEUiE8ShBiXUpKKQbGLKcGG0CBOyRcsQMapF"
        "j02ii4igAgMDJcgQSXQmSkrNijSVTJ1xdJy5d6739W/loDURfqtz4Pt+nHM4BBFUXNnUTCkc"
        "BiUpIISYiDHLEPq0/2Vr459edn1TVN6UwTCk72JtZVq5vQBxAg9VN+DxBVN7ej9cISbmLKV6"
        "SX9X69eIAJYlb++11G/fk7ljLBBSRmd9khJaVVlF06NtJflZ6enJe1tuPXYBiF/LMGtFSdXV"
        "2/Xnj5YVH8z5rKi6m7eYFQBEpyCqTg3vSmiWi+YQzXM7dSYlc3L8bScAmMIkhj1Xbi9AIKSO"
        "sSxDLWbGIIRQUBiabiiUwuganOwuKswBw3Kn1nJhwKpC4wUrD1nRV1XNSDQzpguJsZxzV7Lg"
        "yN+91QElkDrlEf08zyEgqVxtXYNpww0IIUTRdEiyajIMKiZYo+D1Sy5RCjErQUkbnpaGFUU3"
        "qaqxFuEBiGFADM9KXl8gRpRVy4qk+jOSYzH6w/deVHQ6tyQp7m+LHsFqSfD6g4gTeLWjrVnc"
        "sIKZ0QZ63gyDj2JzJ34tiwDw0yfqHye8/t7hmYUlUTZX7E+rGHKNwcph4q8bbBNCxzu7+uWZ"
        "6fnstCTroWvtAzfPHM665P4yH2JYkui0Z1X7F5dy3IMjqsD6SsOrr/+DY6cbq2QqPC8rLbIU"
        "HshGNM9B1XX4lkUMucbxzjWixXHS5SftNx5EBABAbV1DYohucQVkpDtOJDGEACwLdHXPBRnN"
        "v6+j7c4U/qeaGrvV6bRRz2IfFWUX/T75jDqdNhrJy/6DoQLA/bsPkZ2bjempaWxaTqeNzsy+"
        "MgLSEP00+sLY7AQAUFV98nqNIMQfWVhYeJ2XF/sokuk3Vkw2XnyKHQQAAAAASUVORK5CYII=")

    #----------------------------------------------------------------------
    icons['warning'] = PyEmbeddedImage(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAA"
        "CXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1gIQDictt+6SdwAAAehJREFUOMuVk8FKG2EU"
        "hb87mc40iTODEJlK7UZDxCCGQUqaMASCSGODdBe6ECJddOcwG/EJXBt0ZcBCwEVJVgWtr1AI"
        "PoBQXAQKhRZc1EBJMX831hLItPbAvYvL4Ttnc4UIhfDIgLcAA3jdgC/jfHoUwISjeXgOcAFH"
        "QHWcT4tI91KwWlhY0J6kUloKVkPw7g0wYS8NemJ3l0yzSRp0E/buBQihOAXFbLksej6Pns+T"
        "LZdlCoohFPmXdqB7AsNep6M8z1Oe56lep6NOYLgD3b82CGHFhaWM74vh+ziOg+M4GL5PxvfF"
        "haUQViIBJuxnwUgEAaJpWJaFZVmIppEIArJgmLA/FhDC+jSk5woFjFIJEcG2bWzbRkQwSiXm"
        "CgWmIR3C+gggBDGgsXibruk6IvKngQiarpMIAhbBMKARgsDtCuHVLLReLC8bk2dnEIuhlKLf"
        "7wOQTCYREbi54WptjQ/n54NLqDfgnYQQewxXT8GaPz7mYbWKUgqlFLVaDYB2u42IICL8OD3l"
        "YmODLnz/DJOawGYczJlcjnilcmcUEVzXxXXdkVu8UmEmlyMOpsCmbMPXl5CaPThgol6/S/89"
        "wAhARLhutbjc2uI9fJNDGD4DecD/6SfwEZT+CQ4H8GYi4i+idA3DHjR/AZfefQgctOETAAAA"
        "AElFTkSuQmCC")

    class LogMessagesPanel(wx.Panel):
        def __init__(self, parent, id):
            wx.Panel.__init__(self, parent, id)

            self.list = wx.ListCtrl(self, -1,  style=  wx.LC_REPORT|wx.SUNKEN_BORDER)

            self.setupList()
       
            sizer = wx.BoxSizer()
            sizer.Add(self.list, 1, wx.EXPAND)
            self.SetSizerAndFit(sizer)
        
            pub.subscribe(self.OnAppendLog, 'log')
            
        def setupList(self):
            """sets columns and append a imagelist """
            
             #setup first column (which accept icons)
            info = wx.ListItem()
            info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
            info.m_image = -1
            info.m_format = 0
            info.m_text = "Message"
            self.list.InsertColumnInfo(0, info)
            self.list.SetColumnWidth(0, 550)

            #insert second column
            self.list.InsertColumn(1, 'Time')   
            self.list.SetColumnWidth(1, 70)

            #setup imagelist and an associated dict to map status->image_index
            imgList = wx.ImageList(16, 16)
            
            
            self.icon_map = {}
            for key, bitmap in icons.iteritems():
                indx = imgList.Add( bitmap.GetBitmap() )
                self.icon_map[key] = indx
            self.list.AssignImageList(imgList, wx.IMAGE_LIST_SMALL)
            
        def OnAppendLog(self, msg):
            ico = self.icon_map[msg.data[0]]
            message = msg.data[1]
            index = self.list.InsertImageStringItem(sys.maxint, message, ico)
            self.list.SetStringItem(index, 1, time.strftime('%H:%M:%S'))

            self.list.EnsureVisible(index) #keep scroll at bottom

    class TestFrame(wx.Frame):
        def __init__(self, parent, id):
            wx.Frame.__init__(self, parent, id, "Log Panel demo")
            self.log = LogMessagesPanel(self, -1)
            self.SetSize((620,150))
            self.SetMinSize((620,150))

    if __name__ == "__main__":

        app = wx.PySimpleApp(0)
        wx.InitAllImageHandlers()
        main_frame = TestFrame(None, -1)
        app.SetTopWindow(main_frame)
        main_frame.Show()

        pub.sendMessage('log', ('ok', 'Ready! You can send any message from anywhere.') )
        pub.sendMessage('log', ('info', "Just import pubsub.Publisher and send a 'log' message") )
        pub.sendMessage('log', ('warning', "The message data is a tuple ('icon', 'message') ") )
        

.. |image0| image:: /images/mayavi2_logger-0f8f4.png
