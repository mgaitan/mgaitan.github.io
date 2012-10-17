Muchas balizas SPIP generan código HTML como salida (las balizas
#LOGO\_\* y los filtros \|image\_\* son los más notorios) y
frecuentemente necesitamos o queremos modificar este código autogenerado
en nuestros esqueletos. Hay diversos filtros para ayudarnos a esto
(`inserer\_attribut <http://www.spip.net/en_article2465.html#inserer_attribut>`_
para insertar atributos y
`extraire\_attribut <http://www.spip.net/en_article2465.html#extraire_attribut>`_
para extraer el valor de uno generado) pero son particularmente largos y
tediosos de tipear.

Más allá de eso, aunque uso estos filtros bastantes seguido para
implementar cosas como galerías de imágenes, todavía pienso lo difícil
que es escribir las palabras en francés sin equivocarme. Por suerte, un
pequeño wrapper, puede suavizar este inconveniente.

Cuando se trata de acceder y modificar atributos de valores de atributos
nada, en mi opinión, llega tan lejos como `la API de atributos de
jQuery <http://docs.jquery.com/Attributes>`_. El `método de jQuery
*attr* <http://docs.jquery.com/Attributes/attr>`_ por sí solo, permite
leer y escribir el valor de cualquier atributo en cualquier nodo. Recibe
uno o dos parámetros, el nombre del atributo, y opcionalmente, el valor.

Si sólo se especifica el nombre, entonces *attr* extrae y devuelve el
valor de ese atributo. Si ambos parámetros son pasados al método,
entonces attr modifica el objeto configurando el atributo en cuestión
con el valor dado. Es jerga de Programación Orientada a Objetos, es un
estilo de interfaz "polimórfica" — cuando un solo método tiene dos
comportamientos complementarios que son distinguidos por el número y/o
el tipo de los argumentos dados — que está por todos lados en jQuery y
es una de las razones por las que este framework es tan conciso y
productivo.

Considerandola como la mejor estructura para este tipo de interfaces que
conozco (y también, que uso diariamente), decidí ue mi wrapper tendría
que copiarlo. Así fue como el *attr* nació.

Como el método de jQuery, el filtro *attr* de SPIP toma uno o dos
parámetros (y un objeto "implícito", pero lo ignoraremos por el
momento). Si sólo pasamos uno, este lo remite como entrada a
*extraire\_attribut* para obtener el valor correspondiente. Si se lo
llama con dos parámetros, entonces llama a *inserer\_attribut* para
modificar el objeto.

Como la idea, el código es razonablemente sencillo; la únca

Like the idea, the code is reasonably straightforward; quizas lo único
un poco inusual el uso de
`func\_get\_args <http://php.net/func_get_args>`_ para obtener el
conjunto de los argumentos pasados a la función llamada. Con ese array
podermos usar `count <http://php.net/count>`_ para saber cuantos
argumentos se pasaron y decidir qué se debe hacer. Esto es más seguro
que especificar y evaluar valores por defecto (FALSE o NULL, por
ejemplo) porque algunos usuarios genuinamente podrían querer usar esos
valores (supongamos que NULL signifique eliminar el atributo en una
futura versión).

::

    include_spip("inc/filtres");
    
    /**
     * The `attr` function allows the user to get and set the attributes of an HTML tag.
     * It is intended to be used as a SPIP filter and depends on existing SPIP functionality.
     *
     * @param $tag
     *     The HTML code.
     * @param $name
     *     The name of the attribute.
     * @param $val...
     *     The new value for the attribute $nom. Optional.
     * @return
     *     If $val was given, the code for tag with $name=$val
     *     Otherwise, the value for the $name attribute in $tag.
     */
    function attr($tag, $name){
            $args = func_get_args();
    
            if (count($args) > 2) {
                    // SET
                    return  inserer_attribut($tag, $name, $args[2]);
            } else {
                    // GET
                    return extraire_attribut($tag, $name);
            }
    }

Simplemente copia el código en mes\_fonctions.php (Mira "Agregar
funciones propias" en la documentación sobre `filtros de
spip <Agregar%20funciones%20propias>`_) y luego usa el filtro attr en
tus esqueletos:

::

Hay algunos cambios que se puede hacer a esta función: pasar $args
directamente a inserer\_attribut y extraire\_attribut en vez de las
variables individuales, agregar un parámetro $value=FALSE que sólo sirva
para la claridad de la documentación , y el mencionado, eliminar
atributos cuando se pase por ejemplo NULL como parámetro.
