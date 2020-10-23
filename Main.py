import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from Ventana_inicial import Ventana_inicio
from Ventana_principal import Ventana_principal
from Ventana_post_ronda import Ventana_post_ronda
from Clases import Mesero, Objetos
from Reloj import Crear_reloj
import Parametros

app = QApplication([])
ventana_inicial = Ventana_inicio()
ventana_principal = Ventana_principal()
ventana_post_ronda = Ventana_post_ronda()


ventana_inicial.senal_empezar.connect(ventana_principal.iniciar_juego)
ventana_inicial.senal_continuar.connect(ventana_principal.continuar_partida)

objetos = Objetos()

ventana_principal.senal_moverse.connect(ventana_principal.mover_mesero)

ventana_principal.senal_crear_mesa.connect(ventana_principal.crear_mesa)
ventana_principal.senal_crear_chef.connect(ventana_principal.crear_chef)
ventana_principal.senal_crear_mesero.connect(ventana_principal.crear_mesero)
ventana_principal.senal_limites.connect(objetos.limites)
objetos.senal_ajustar_label.connect(ventana_principal.mover_label)
objetos.senal_enviar_objetos.connect(ventana_principal.recibir_objetos)
ventana_principal.senal_pausar.connect(ventana_principal.pausar_juego)
ventana_principal.senal_abrir_post_ronda.connect(ventana_post_ronda.iniciar_ventana)


ventana_inicial.show()
sys.exit(app.exec_())