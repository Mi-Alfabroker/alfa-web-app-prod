debemosimplementar en este proyecto los rubros faltantes, en este sistema ya tenemos la logica para el rubro de Copropiedades, que es el rubro mas complicado, debemos complementarlo con los rubros faltantes, en esa carpeta de propuestas faltantes esta el csv con cada uno de los elementos

los generales son los aspectos pertenecientes a ese rubro y las opciones de seguro son las opciones pre cargadas que se van a configurar por cada aseguradora, aseguradora.py en models tiene el ejemplo de como van en copropiedad, la idea es que esos elementos van en esa tabla, para que al configurar la aseguradora la podamos configurar para todos los rubros

por el momento debemos ignorar las entregas de las polizas, ya que aun no hemos desarollado nada de eso, por ahora centremonos en los aspectos que nos piden generar las propuestas

tambien debemos generar los diccionarios que ya esta implementados para las propuestas puesto a que estos nos serviran para poder poner esos elementos en el excel, en el de cooprpiedades ya tenemos el ejemplo de los diccionarios, pero cada rubro maneja cosas diferentes y debemos generar un diccionario por los rubros faltantes

el boton que genera la propuesta debera generar la propuesta usando el excel correspondiente en la ruta donde esta la carpeta plantillas_xlsx, esto permitira usar la plantilla apropiada para las propuestas, cada una tiene su nombre correspondiente y el script que reemplaza los valores puede usar cualquier excel