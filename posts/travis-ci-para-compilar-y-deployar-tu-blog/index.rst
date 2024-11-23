.. title: Travis-CI para compilar y deployar tu blog estático
.. slug: travis-ci-para-compilar-y-deployar-tu-blog
.. date: 30/09/14 20:57:08 UTC-03:00
.. tags: devop
.. link:
.. description:
.. type: text


`Travis-CI <http://travis-ci.org/>`_ es un servicio de integración continua, gratuito para proyectos de 
software libre. Pero son gente tan copada que no se enojan si en vez de una suite de tests, corremos, por ejemplo, 
Nikola para compilar este blog y publicarlo automáticamente. 

.. TEASER_END


El flujo es así: 

1. Escribimos un post en el branch "fuente" (En mi caso ``writing``) y comiteamos. 
   Esto puede hacerse desde la propia compu, o usar el editor de Github :D

.. image:: http://i.snag.gy/U4hmv.jpg
   :width: 640px
   :align: center
   

2. Travis detecta el commit en el branch, clona el repo, instala las dependencias 
   y ejecuta un script que corre ``nikola build`` y lo necesario para pushear el resultado 
   (por ejemplo, la carpeta ``output``) al branch Github pages (en general ``gh-pages``, 
   ``master`` en mi caso)
   
3. Listo: Nikola desde la nube. For free. 


Permiso, soy el CI
-------------------

¿Cómo hace Travis para pushear de vuelta al repo? Bueno, hay que darle permiso. Para eso, necesitamos 
`crear un token <https://github.com/settings/tokens/new>`_ . Con un token, 
`se puede pushear a un repo <https://github.com/blog/1270-easier-builds-and-deployments-using-git-over-https-and-oauth>`_ 
via HTTPS sin que pida clave usando la url ``https://<token>@github.com/owner/repo.git``. 

Pero como el archivo para configurar Travis es público (y el token es información muy sensible), 
lo configuramos como una variable de entorno encriptada. 
Para eso necesitamos el utilitario (hecho en ruby) que provee la gente de Travis::


    $ sudo apt-get install ruby1.9.1-dev build-essentials
    $ sudo gem install travis
    
    $ travis encrypt GH_TOKEN=your_token

el resultado lo ponemos en el yaml:: 


  env:
    global:
      secure: dlAoq4D...
  

y con eso Travis tendrá una varible de entorno global llamada ``GH_TOKEN`` que podemos usarla en nuestro script. 


Podés ver el `.travis.yml <https://github.com/mgaitan/mgaitan.github.com/blob/writing/.travis.yml>`_ y 
el `script que compila y pushea de vuelta <https://github.com/mgaitan/mgaitan.github.com/blob/writing/travis_deploy.sh>`_ 

