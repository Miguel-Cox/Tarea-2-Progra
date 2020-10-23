import sys
from PyQt5 import uic
from PyQt5.QtCore import (QObject, pyqtSignal)
from PyQt5.QtWidgets import QApplication
from math import floor

window_name, base_class = uic.loadUiType("ventana_post_ronda.ui")

class Ventana_post_ronda(window_name, base_class):

    senal_continuar = pyqtSignal()
    senal_empezar = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)


    def iniciar_ventana(self, datos):
        self.label_post_perdidos.setText(str(datos["perdidos"]))
        self.label_7.setText(str(datos["atendidos"]))
        self.label_8.setText(str(f"{datos['reputacion']}/5"))
        self.label_post_dinero.setText(str(datos["dinero"]))
        self.calculo_reputacion(datos)
        self.show()


    def salir_juego(self):
        sys.exit()

    def guardar_partida(self):
        # Aqui ya esta implementada la señal interna.
        pass


    def continuar_partida(self):
        pass

    def calculo_reputacion(self, datos):
        nueva_reputacion = max(0, min(5, int(datos["reputacion"]) + floor(4 * (int(datos["perdidos"])/(datos["total"])) - 2)))

        if nueva_reputacion <= 0:
            print("Lo siento, haz perdido el juego")
            self.salir_juego()