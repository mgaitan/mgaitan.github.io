Un comando muy práctico para hacer backups de una base de datos MySQL es
*mysqldump*.

::

    mysqldump -h SERVIDOR -u USUARIO -pPASSWORD base_de_datos > backup.sql

Eso hace un backup completo de la base *base\_de\_datos* (incluyendo la
creación de todas las tablas.

Para restaurar ese backup se hace directamente inyectando el sql al
interprete de mysql.

::

    mysql -h SERVIDOR -u USUARIO -pPASSWORD base_de_datos 

Respaldar sólo algunas tablas de la base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A menudo tenemos multiples sistemas instalados sobre la misma base de
datos, Si sólo queremos respaldar algunas tablas bastaría enumerar las
tablas luego del nombre de la base de datos

::

    mysqldump -h SERVIDOR -u USUARIO -pPASSWORD base_de_datos  tabla1 tabla2 > backup.sql

Pero si estas tablas son muchas, es engorroso definirlas una por una.
Por suerte, en general, un prefijo asocia todas las tablas de un
sistema.

En ese caso, se puede usar el siguiente compando que respalda todas las
tablas con un prefijo, En este ejemplo, las que comienzan con "spip\_":

::

    mysql -h SERVIDOR -u USUARIO -pPASSWORD base_de_datos  -e 'show tables like "spip_%"' | grep -v Tables_in | xargs mysqldump -h SERVIDOR -u USUARIO -pPASSWORD base_de_datos > backup.sql

