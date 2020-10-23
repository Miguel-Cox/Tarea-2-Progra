# Tareas-Progra# Tarea 02: DCCafé
##
## Consideracion generales
* Respecto al funcionamiento del programa, se logró hacer la gran mayoria de los requerimientos.
* Falla en la correcta aparición de los clientes en los mesones, en donde se superponen. (No logre arreglar este error) Producto de esto, hay fallas en la finalización del programa y la implementación de la ventana post ronda y las funciones ligadas al avance del juego a medida que se van pasando las rondas. Las demas funcionalidades funcionan de forma correcta. (pd: La ronda debiese de terminar cuando pones salir o cuando clientes_rondas == clientes_atendidos + clientes_perdidos)
* Al iniciar un juego nuevo las mesas y chef se les asigna un lugar aleatorio, si choca con otro: se le vuelve a asignar un nuevo lugar. (Lo mismo ocurre si se hace una compra de algunos de estos y se intenta poner sobre otro label)
* Si el chef quema uno de sus platos, no se indica en la consola que se ha quemado. Solamente desaparece.
* El drag and drop, lo implemente netamente con Mouse Events.
* Los objetos creados en el programa los agregaba en diccionarios.
* Algunas señales estan implementadas en los archivos ui, otras no.

## Ejecución
El módulo principal de la tarea es _"Main.py"_.
## Librerías
1. random.randint()
2. time
3. Pyqt5 --> QtCore (Qt, QtPoint, Qrect, QThread, pyqtSignal, QObject), QtWidgets (QApplication, Qlabel, Qwidget), QtGui (QPixmap, QDrag, QPainter, QCursor)
4. a.intersects(b)
## Funciones

1. Las funciones por lo general se entienden lo que cumplen en base al nombre que se les indica.
2. La funcion **mover_mesero** se ejecuta con KeyPressEvent y este envia una señal para definir la posicion del mesero por medio de un retorno. (Es importante esta función porque permite que al iniciar el programa se actualice inmediatamente la posicion inicial del mesero al movimiento)
3. **Objetos.limites** / **ajustar_colision** / **intersectan** --> Dichas funciones definen los Qrect de los objetos creados, y evaluan que no intersectan. De Intersectar, cambia sus posiciones.
## Supuestos y consideraciones adicionales
* Las probabilidades las definí por medio del uso de if y random.randint.
* No hice uso de layouts al fijar las ventanas a un cierto tamaño.
* Mi trabajo esta hecho en pyCharm y al momento de cargar los archivos .ui, no se cargaban los Pixmap. Frente a esto, gracias a una respuesta en issues logre solucionarlo cambiando los archivos internos .ui. Esto genera que en el juego se carguen de forma correcta. Pero si se quiere cargar el archivo, para visualizarlo nuevamente en QtDesigner, **no se cargarán**.
## Referencias a codigo externo
* [Codigo para eliminar fondo de los labels --> setStyleSheet("border: 0px; background-color:rgba(0,0,0,0%);")](https://stackoverflow.com/questions/56327000/qlabel-removing-border-and-background)

