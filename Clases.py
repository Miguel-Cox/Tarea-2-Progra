import sys
import random
import time
from PyQt5.QtCore import QThread, QObject, pyqtSignal, QRect, QTimer, QMimeData, Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor
import Parametros


class Objetos(QObject):

    senal_ajustar_label = pyqtSignal(dict)
    senal_enviar_objetos = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.objetos = dict()

    def limites(self, dato):
        for u in dato.keys():
            if u[0:4] == "mesa":
                x = 35
                y = 60
            elif u[0:4] == "chef":
                x = 75
                y = 80
            elif u == "mesero":
                x = 30
                y = 45
            nombre = u

            espacio = QRect(dato[u].x(), dato[u].y(), x, y)
            self.objetos[u] = QRect(dato[u].x(), dato[u].y(), x, y)

        self.senal_enviar_objetos.emit(self.objetos)
        self.ajustar_colision(self.objetos, espacio, nombre)


    def ajustar_colision(self, objetos, espacio, nombre):
        posiciones = objetos.values()
        for posicion in posiciones:
            if self.intersectan(espacio, posicion) == True and espacio != posicion:
                print(f"Se ha cambiado de lugar {nombre}")
                self.senal_ajustar_label.emit({"nombre": nombre,
                                               "x": random.randint(0, 600),
                                               "y": random.randint(0, 330)})

    def intersectan(self, a, b):
        if a.intersects(b) == True:
            return True
        else:
            return False


class Mesero(Objetos):

    def __init__(self, x, y):
        super().__init__()
        self.__x = x
        self.__y = y
        self.__frame = 1
        self.orientacion = "down"
        self.choque_chef = "no"
        self.chef_chocado = ""
        self.choque_mesa = "no"
        self.mesa_chocada = ""
        self.snack = ""

    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, value):
        if 3 < value:
            self.__frame = 1
        else:
            self.__frame = value

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value


    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value


    def move(self, event, objetos):
        self.frame += 1
        self.mesero_qrect = QRect(self.__x, self.__y, 30, 45)
        self.choque_chef = "no"
        self.choque_mesa = "no"

        if event == 'R':
            self.orientacion = "right"
            if self.__x < 680:
                self.x += 10
                self.mesero_qrect = QRect(self.__x, self.__y, 30, 45)

                for y in objetos:
                    if y == "mesero":
                        pass
                    else:
                        if self.intersectan(self.mesero_qrect, objetos[y]) == True:
                            if y[0:4] == "chef":
                                self.choque_chef = "si"
                                self.chef_chocado = str(y)

                            elif y[0:4] == "mesa":
                                self.choque_mesa = "si"
                                self.mesa_chocada = str(y)
                            self.x -= 10

            return ({'x': self.x,
                     'y': self.y,
                     "frame": self.frame,
                     "orientacion": self.orientacion,
                     "choque_chef": self.choque_chef,
                     "chef_chocado": self.chef_chocado,
                     "choque_mesa": self.choque_mesa,
                     "mesa_chocada": self.mesa_chocada,
                     "snack": self.snack,
                     "sprite": "mesero"
                     })

        if event == 'L':
            self.orientacion = "left"
            if self.__x > 0:
                self.x -= 10
                self.mesero_qrect = QRect(self.__x, self.__y, 30, 45)

                for y in objetos:
                    if y == "mesero":
                        pass
                    else:
                        if self.intersectan(self.mesero_qrect, objetos[y]) == True:
                            if y[0:4] == "chef":
                                self.choque_chef = "si"
                                self.chef_chocado = str(y)

                            elif y[0:4] == "mesa":
                                self.choque_mesa = "si"
                                self.mesa_chocada = str(y)
                            self.x += 10

            return ({'x': self.x,
                     'y': self.y,
                     "frame": self.frame,
                     "orientacion": self.orientacion,
                     "choque_chef": self.choque_chef,
                     "chef_chocado": self.chef_chocado,
                     "choque_mesa": self.choque_mesa,
                     "mesa_chocada": self.mesa_chocada,
                     "snack": self.snack,
                     "sprite": "mesero"
                     })

        if event == "U":
            self.orientacion = "up"
            if self.__y > 0:
                self.y -= 10
                self.mesero_qrect = QRect(self.__x, self.__y, 30, 45)

                for y in objetos:
                    if y == "mesero":
                        pass
                    else:
                        if self.intersectan(self.mesero_qrect, objetos[y]) == True:
                            if y[0:4] == "chef":
                                self.choque_chef = "si"
                                self.chef_chocado = str(y)

                            elif y[0:4] == "mesa":
                                self.choque_mesa = "si"
                                self.mesa_chocada = str(y)
                            self.y += 10

            return ({'x': self.x,
                     'y': self.y,
                     "frame": self.frame,
                     "orientacion": self.orientacion,
                     "choque_chef": self.choque_chef,
                     "chef_chocado": self.chef_chocado,
                     "choque_mesa": self.choque_mesa,
                     "mesa_chocada": self.mesa_chocada,
                     "snack": self.snack,
                     "sprite": "mesero"
                     })

        if event == "D":
            self.orientacion = "down"
            if self.__y <= 340:
                self.y += 10
                self.mesero_qrect = QRect(self.__x, self.__y, 30, 45)

                for y in objetos:
                    if y == "mesero":
                        pass
                    else:
                        if self.intersectan(self.mesero_qrect, objetos[y]) == True:
                            if y[0:4] == "chef":
                                self.choque_chef = "si"
                                self.chef_chocado = str(y)

                            elif y[0:4] == "mesa":
                                self.choque_mesa = "si"
                                self.mesa_chocada = str(y)
                            self.y -= 10

            return ({'x': self.x,
                     'y': self.y,
                     "frame": self.frame,
                     "orientacion": self.orientacion,
                     "choque_chef": self.choque_chef,
                     "chef_chocado": self.chef_chocado,
                     "choque_mesa": self.choque_mesa,
                     "mesa_chocada": self.mesa_chocada,
                     "snack": self.snack,
                     "sprite": "mesero"
                     })

class Chefs(QThread):

    senal_actualizar_chef = pyqtSignal(dict)

    def __init__(self, x, y, numero):
        super().__init__()
        self.x = x
        self.y = y
        self.__frame = 1
        self.numero = numero
        self.estado = "espera"
        self.nivel = 1
        self.platos_preparados = 0
        self.reputacion_dccafe = 5

    @property
    def frame(self):
        return self.__frame
    @frame.setter
    def frame(self, value):
        if 16 >= value:
            self.__frame = value
            self.estado = "cocinando"
        else:
            self.estado = "listo"

    def revisar_nivel(self):
        if self.platos_preparados == Parametros.platos_intermedio:
            self.nivel = 2
            print(f"chef{self.numero} subio a nivel 2")
        elif self.platos_preparados == Parametros.platos_experto:
            self.nivel = 3
            print(f"chef{self.numero} subio a nivel 3")

    def run(self):
        self.__frame = 1
        self.revisar_nivel()
        for u in range(1, 17):
            self.senal_actualizar_chef.emit({"frame": self.frame,
                                            "label": f"chef{self.numero}",
                                             "estado": self.estado})
            self.frame += 1
            tiempo_preparacion = max(0, 15 - self.reputacion_dccafe - self.nivel * 2)
            time.sleep(tiempo_preparacion/16)

class Clientes(QObject):
    def __init__(self, x, y, tipo, widged):
        super().__init__()
        self.x = x
        self.y = y
        self.tipo = tipo
        self.tiempo_espera = 0
        self.tiempo_cambio_humor = 0
        self.widget = widged

    def crear_label(self):
        self.label = QLabel(self.widget)
        if self.tipo == "apurado":
            self.label.setPixmap(QPixmap("sprites/clientes/hamster/hamster_02.png"))
            self.tiempo_espera = 30
            self.tiempo_cambio_humor = 20
        elif self.tipo == "tranquilo":
            self.label.setPixmap(QPixmap("sprites/clientes/perro/perro_01.png"))
            self.tiempo_espera = 45
            self.tiempo_cambio_humor = 30
        self.label.move(self.x, self.y - 5)
        self.label.resize(30, 30)
        self.label.setScaledContents(True)
        self.label.show()