from PyQt5 import uic
from PyQt5.QtCore import (QObject, pyqtSignal)

window_name, base_class = uic.loadUiType("ventana_inicio.ui")

class Ventana_inicio(window_name, base_class):

    senal_continuar = pyqtSignal()
    senal_empezar = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Inicio")

    def continuar_partida(self):
        self.senal_continuar.emit()
        self.hide()

    def empezar_nueva_partida(self):
        self.senal_empezar.emit()
        self.hide()

