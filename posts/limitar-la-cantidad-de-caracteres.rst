Si Twitter funciona con 140 caracteres los comentarios a nuestros
artículos podrían tener 200, ¿no?

Hay una forma fácil de limitar el largo permitido en un campo de texto
mediante jQuery, que vaya mostrando de manera interactiva la cantidad de
caracteres restantes.

Por ejemplo, esto limita el tamaño de un comentario en SPIP.

::

    
     $(document).ready(function () {  
         
         $("#texte").before("<div id='chars' style='float:right;font-weigth:strong;margin-right:5px;'></div>");
    
    $(function(){
        $('#texte').keyup(function(){
            limitChars('texte', 200, 'chars');
        })
        });
     });  
     
    function limitChars(textid, limit, infodiv) {
         var text = $('#'+textid).val(); 
         var textlength = text.length;
         if(textlength > limit) {
             $('#' + infodiv).html('No puede ingresar m&aacute;s de '+limit+' caracteres');
             $('#'+textid).val(text.substr(0,limit));
             return false;
         } else {
             $('#' + infodiv).html('Restan '+ (limit - textlength) +' caracteres.');
             return true;
         }
    }

Intrucciones para SPIP
~~~~~~~~~~~~~~~~~~~~~~

#. Copiar el código
#. Pegarlo luego de la baliza #INSERT\_HEAD de tu cabecera
#. (opcional) Cambiarle el límite (el número 200),

¡Listo!

Intrucciones generales
~~~~~~~~~~~~~~~~~~~~~~

Es igual al anterior, sólo debes asegurarte que tiene en jquery en la
página. Luego cambia el selector ``#texte`` por el que corresponda al
campo que querés limitar.

Ejemplo
~~~~~~~

