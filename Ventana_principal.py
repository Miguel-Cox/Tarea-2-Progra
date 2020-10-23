from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QThread, QRect, QPoint
from PyQt5.QtGui import QPixmap, QDrag, QPainter, QCursor
import Parametros
from Clases import Mesero, Chefs, Clientes
from Reloj import Crear_reloj
import random
import time

window_name, base_class = uic.loadUiType("ventana_principal.ui")

class Ventana_principal(window_name, base_class):

    senal_moverse = pyqtSignal(str)
    senal_crear_mesa = pyqtSignal(dict)
    senal_crear_chef = pyqtSignal(dict)
    senal_crear_mesero = pyqtSignal(dict)
    senal_limites = pyqtSignal(dict)
    senal_comenzar_juego = pyqtSignal()
    senal_pausar = pyqtSignal()
    senal_abrir_post_ronda = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.x = 0
        self.y = 0
        self.reloj = Crear_reloj()
        self.reloj.senal_clientes.connect(self.clientes)
        self.mesero = Mesero(self.x, self.y)
        self.empezo = "no"
        self.apreto_objeto = "no"
        self.numero_mesa = 1
        self.numero_chef = 1
        self.boton_comenzar = 0
        self.boton_pausar = 0
        self.se_puede_comprar = "si"
        self.setWindowTitle("Main")
        self.dict_clientes = dict()
        self.numero_clientes = 0
        self.valor_posible = 1

        self.button_comenzar.clicked.connect(self.comenzar_juego)
        self.button_pausar.clicked.connect(self.pausar_juego)
        self.button_salir.clicked.connect(self.salir_juego)

        self.chef_venta = QLabel(self)
        self.chef_venta.setPixmap(QPixmap("sprites/chef/meson_01.png"))
        self.chef_venta.resize(82.6, 96.6)
        self.chef_venta.setScaledContents(True)
        self.chef_venta.setStyleSheet("border: 0px; background-color:rgba(0,0,0,0%);")
        self.chef_venta.hide()

        self.mesa_venta = QLabel(self)
        self.mesa_venta.setPixmap(QPixmap("sprites/mapa/accesorios/silla_mesa_amarilla.png"))
        self.mesa_venta.resize(35, 60)
        self.mesa_venta.setScaledContents(True)
        self.mesa_venta.setStyleSheet("border: 0px; background-color:rgba(0,0,0,0%);")
        self.mesa_venta.hide()

        self.dinero = Parametros.dinero_default
        self.reputacion = Parametros.reputacion_default
        self.rondas_terminadas = Parametros.rondas_terminadas_default
        self.atendidos = Parametros.atendidos_default
        self.perdidos = Parametros.perdidos_default
        self.proximos = Parametros.proximos_default
        self.total_por_atender_ronda = self.proximos

        self.label_dinero.setText(str(self.dinero))
        self.label_reputacion.setText(f"{self.reputacion}/5")
        self.label_atendidos.setText(str(self.atendidos))
        self.label_perdidos.setText(str(self.perdidos))
        self.label_proximos.setText(str(self.proximos))

        self.labels = dict()
        self.widgets = dict()
        self.chefs = dict()
        self.lista_trampa = []

        self.datos = {"perdidos": 0,
                              "atendidos": 0,
                              "reputacion": 5,
                      "dinero": 500,
                      "total": self.total_por_atender_ronda}

        widget_mapa = QWidget(self)
        widget_mapa.resize(721, 401)
        widget_mapa.move(40, 320)
        widget_mapa.setStyleSheet("border: 0px; background-color:rgba(0,0,0,0%);")
        # https://stackoverflow.com/questions/56327000/qlabel-removing-border-and-background
        self.widgets["mapa"] = widget_mapa

    def iniciar_juego(self):

        self.senal_crear_mesero.emit({
            "x": Parametros.posicion_mesero_default[0],
            "y": Parametros.posicion_mesero_default[1]
        })
        self.x = Parametros.posicion_mesero_default[0]
        self.y = Parametros.posicion_mesero_default[1]

        self.senal_crear_mesa.emit({
            "x": Parametros.posicion_mesa1_default[0],
            "y": Parametros.posicion_mesa1_default[1]
        })
        self.senal_crear_mesa.emit({
            "x": Parametros.posicion_mesa2_default[0],
            "y": Parametros.posicion_mesa2_default[1]
        })

        self.senal_crear_chef.emit({
            "x": Parametros.posicion_chef_default[0],
            "y": Parametros.posicion_chef_default[1]
        })

        self.mesero = Mesero(self.x, self.y)
        self.show()

    def continuar_partida(self):
        with open("mapa.csv", "r", encoding="UTf-8") as archivo_mapa:
            objetos =  archivo_mapa.readlines()

            for linea in objetos:
                nombre, x, y = linea.split(",")
                if nombre == "mesa":
                    self.senal_crear_mesa.emit({"x": int(x),
                                                "y": int(y)})


                elif nombre == "chef":
                    self.senal_crear_chef.emit({"x": int(x),
                                                "y": int(y)})

                elif nombre == "mesero":
                    self.senal_crear_mesero.emit({"x": int(x),
                                                  "y": int(y)})
                    self.x = int(x)
                    self.y = int(y)

                    self.mesero = Mesero(self.x, self.y)

        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A and self.empezo == "si":
            self.senal_moverse.emit('L')
        elif event.key() == Qt.Key_D and self.empezo == "si":
            self.senal_moverse.emit('R')
        elif event.key() == Qt.Key_W and self.empezo == "si":
            self.senal_moverse.emit("U")
        elif event.key() == Qt.Key_S and self.empezo == "si":
            self.senal_moverse.emit("D")
        elif event.key() == Qt.Key_P:
            self.senal_pausar.emit()

        self.lista_trampa.append(event.key())
        if self.lista_trampa[len(self.lista_trampa)-3::] == [77, 79, 78]:
            print("Codigo dinero activado")
            self.agregar_dinero(5000)
        elif self.lista_trampa[len(self.lista_trampa)-3::] == [70, 73, 78]:
            print("Codigo terminar ronda activado")
        elif self.lista_trampa[len(self.lista_trampa)-3::] == [82, 84, 71]:
            print("Codigo reputacion activado")
            self.actualizar_reputacion(5)

    def mover_mesero(self, event):
        actualizar = self.mesero.move(event, self.objetos)
        self.actualizar_mesero(actualizar)

    def actualizar_mesero(self, event):
        pixmap = QPixmap(f"sprites/{event['sprite']}/{event['orientacion']}{event['snack']}_0{event['frame']}.png")
        if event["snack"] == "_snack" and (event["orientacion"] == "left" or event["orientacion"] == "right"):
            self.labels["mesero"].resize(50, 45)
        else:
            self.labels["mesero"].resize(30, 45)

        if event["choque_chef"] == "si" and self.mesero.snack == "":
            prob_fallar = 0.3/(self.chefs[event["chef_chocado"]].nivel + 1)
            prob_obtenida = random.randint(1, 100)/100
            self.chefs[event["chef_chocado"]].start()
            self.chefs[event["chef_chocado"]].reputacion_dccafe = self.reputacion
            if prob_obtenida > prob_fallar:
                if self.chefs[event["chef_chocado"]].estado == "listo":
                    self.mesero.snack = "_snack"
                    self.chefs[event["chef_chocado"]].platos_preparados += 1
                    self.agregar_dinero(50)
                    self.atendidos += 1
                    self.actualizar_atendidos(self.atendidos)


        elif event["choque_mesa"] == "si" and self.mesero.snack == "_snack" and self.labels[event["mesa_chocada"]].disponible == False:
            self.mesero.snack = ""
            for u in self.dict_clientes:
                if self.dict_clientes[u][1] == self.labels[event["mesa_chocada"]]:
                    self.dict_clientes[u][0].hide()

            self.labels[event["mesa_chocada"]].disponible = True

        self.labels["mesero"].setPixmap(pixmap)

        self.labels["mesero"].move(event['x'], event['y'])

    def actualizar_chef(self, event):
        if self.empezo == "si":
            if event["frame"] < 10:
                pixmap = QPixmap(f"sprites/chef/meson_0{event['frame']}.png")
            else:
                pixmap = QPixmap(f"sprites/chef/meson_{event['frame']}.png")

            self.labels[event['label']].setPixmap(pixmap)

    def crear_mesa(self, data):

        mesa_label = QLabel(self.widgets["mapa"])
        mesa_label.setPixmap(QPixmap("sprites/mapa/accesorios/silla_mesa_amarilla.png"))
        mesa_label.resize(35, 60)
        mesa_label.setScaledContents(True)
        mesa_label.move(data["x"],
                        data["y"])
        self.labels[f"mesa{str(self.numero_mesa)}"] = mesa_label
        self.labels[f"mesa{str(self.numero_mesa)}"].disponible = True
        self.labels[f"mesa{str(self.numero_mesa)}"].posx = data["x"]
        self.labels[f"mesa{str(self.numero_mesa)}"].posy = data["y"]
        self.senal_limites.emit({f"mesa{str(self.numero_mesa)}": mesa_label})

        self.numero_mesa += 1

    def crear_chef(self, data):

        chef_label = QLabel(self.widgets["mapa"])
        chef_label.setPixmap(QPixmap("sprites/chef/meson_01.png"))
        chef_label.resize(82.6, 96.6)
        chef_label.setScaledContents(True)
        chef_label.move(data["x"],
                        data["y"])
        self.labels[f"chef{str(self.numero_chef)}"] = chef_label
        self.chefs[f"chef{str(self.numero_chef)}"] = Chefs(data["x"], data["y"], str(self.numero_chef))
        self.chefs[f"chef{str(self.numero_chef)}"].senal_actualizar_chef.connect(self.actualizar_chef)

        self.senal_limites.emit({f"chef{str(self.numero_chef)}": chef_label})
        self.numero_chef += 1

    def crear_mesero(self, data):

        mesero_label = QLabel(self.widgets["mapa"])
        mesero_label.setPixmap(QPixmap("sprites/mesero/down_02.png"))
        mesero_label.resize(30, 45)
        mesero_label.setScaledContents(True)
        mesero_label.move(data["x"],
                          data["y"])

        self.labels["mesero"] = mesero_label
        self.senal_limites.emit({"mesero": mesero_label})

    def mover_label(self, data):
        self.labels[data["nombre"]].move(data["x"], data["y"])
        self.labels[data["nombre"]].posx = data["x"]
        self.labels[data["nombre"]].posy = data["y"]
        self.senal_limites.emit(self.labels)

    def recibir_objetos(self, event):
        self.objetos = event

    def comenzar_juego(self):
        if self.boton_comenzar == 0:
            self.reloj.ejecutar_timer()
            self.boton_comenzar = 1
            self.empezo = "si"
            self.se_puede_comprar = "no"

    def pausar_juego(self):
        if self.boton_pausar == 0:
            if self.empezo == "si":
                self.reloj.parar()
                self.boton_pausar = 1
                self.empezo = "no"
        elif self.boton_pausar == 1:
            self.reloj.reanudar()
            self.boton_pausar = 0
            self.empezo = "si"

    def salir_juego(self):
        self.senal_abrir_post_ronda.emit(self.datos)
        self.hide()

    def agregar_dinero(self, value):
        self.dinero += value
        self.label_dinero.setText(str(self.dinero))

    def actualizar_reputacion(self, value):
        self.reputacion = value
        self.label_reputacion.setText(f"{self.reputacion}/5")

    def actualizar_atendidos(self, value):
        self.atendidos = value
        self.label_atendidos.setText(str(self.atendidos))

    def actualizar_perdidos(self, value):
        self.perdidos = value
        self.label_perdidos.setText(str(self.perdidos))

    def actualizar_proximos(self, value):
        self.proximos = value
        self.label_proximos.setText(str(self.proximos))

    def mousePressEvent(self, event):
        qrec_chef = QRect(830, 320, 101, 101)
        qrec_mesa = QRect(860, 490, 41, 81)
        x = event.x() - 40
        y = event.y() - 320
        pos = QPoint(x, y)
        self.apreto_objeto = "no"

        for u in self.objetos:
            if pos in self.objetos[u] and event.buttons() == Qt.LeftButton and self.empezo == "no":
                if u == "mesero":
                    pass
                else:
                    self.borrar_label(u)

        if event.buttons() == Qt.LeftButton and (event.pos() in qrec_chef or event.pos() in qrec_mesa) and self.empezo == "no" and self.se_puede_comprar == "si":
            self.apreto_objeto = "si"

            if event.pos() in qrec_chef:
                self.apreto_cual = "chef"
            elif event.pos() in qrec_mesa:
                self.apreto_cual = "mesa"

    def mouseMoveEvent(self, event):
        self.posicion_actual = event.pos()
        if event.buttons() == Qt.LeftButton and self.apreto_objeto == "si" and self.apreto_cual == "chef":
            self.chef_venta.move(self.posicion_actual)
            self.chef_venta.show()
        elif event.buttons() == Qt.LeftButton and self.apreto_objeto == "si" and self.apreto_cual == "mesa":
            self.mesa_venta.move(self.posicion_actual)
            self.mesa_venta.show()

    def mouseReleaseEvent(self, event):
        qrec_window = QRect(40, 320, 721, 401)
        x = event.x() - 40
        y = event.y() - 320
        if event.pos() in qrec_window and self.apreto_objeto == "si":
            if self.apreto_cual == "chef" and self.dinero >= 300:
                self.crear_chef({"x": x,
                                 "y": y})
                self.labels[f"chef{str(self.numero_chef - 1)}"].show()
                self.agregar_dinero(-300)
                self.chef_venta.hide()

            elif self.apreto_cual == "mesa" and self.dinero >= 100:

                self.crear_mesa({"x": x,
                                 "y": y})
                self.labels[f"mesa{str(self.numero_mesa - 1)}"].show()
                self.agregar_dinero(-100)
                self.mesa_venta.hide()

            elif self.apreto_cual == "chef" and self.dinero < 300:
                print("No tienes suficiente dinero")
                self.chef_venta.hide()

            elif self.apreto_cual == "mesa" and self.dinero < 100:
                print("No tienes suficiente dinero")
                self.mesa_venta.hide()
        else:
            self.mesa_venta.hide()
            self.chef_venta.hide()

    def borrar_label(self, w):
        chefs = []
        mesas = []
        for u in self.labels:
            if u[0:4] == "chef":
                chefs.append(u)
            elif u[0:4] == "mesa":
                mesas.append(u)

        if w[0:4] == "mesa" and len(mesas) > 1:
            self.labels[w].hide()
            self.labels[w].move(600, 600)
            self.senal_limites.emit(self.labels)
            self.labels.pop(w)

        elif w[0:4] == "chef" and len(chefs) > 1:
            self.labels[w].hide()
            self.labels[w].move(600, 600)
            self.senal_limites.emit(self.labels)
            self.labels.pop(w)

    def clientes(self):
        for u in self.labels:
            if u[0:4] == "mesa" and self.labels[u].disponible == True and self.proximos > 0:
                b = random.randint(0, 1)
                if b == 1:
                    self.numero_clientes += 1
                    cliente = Clientes(self.labels[u].posx, self.labels[u].posy, "apurado", self.widgets["mapa"])
                    cliente.crear_label()
                    self.labels[u].disponible = False
                    tiempo_llegada = self.reloj.segundos_totales
                    self.dict_clientes[f"cliente{self.numero_clientes}"] = cliente.label, self.labels[u], tiempo_llegada, cliente.tiempo_espera, cliente.tiempo_cambio_humor, cliente.tipo
                    self.actualizar_proximos(self.proximos-1)
                    self.valor_posible = 1



                else:
                    self.numero_clientes += 1
                    cliente = Clientes(self.labels[u].posx, self.labels[u].posy, "tranquilo", self.widgets["mapa"])
                    cliente.crear_label()
                    self.labels[u].disponible = False
                    tiempo_llegada = self.reloj.segundos_totales
                    self.dict_clientes[f"cliente{self.numero_clientes}"] = cliente.label, self.labels[u], tiempo_llegada, cliente.tiempo_espera, cliente.tiempo_cambio_humor, cliente.tipo
                    self.actualizar_proximos(self.proximos - 1)
                    self.valor_posible = 1

        if len(self.dict_clientes) > 0:
            for u in self.dict_clientes:
                if self.dict_clientes[u][3] < (self.reloj.segundos_totales - self.dict_clientes[u][2]):
                    self.dict_clientes[u][0].hide()
                    self.dict_clientes[u][1].disponible = True

                    # ERROR AQUI
                    if self.valor_posible == 1:
                        self.perdidos += 1
                        self.actualizar_perdidos(self.perdidos)
                        self.valor_posible = 0

                elif self.dict_clientes[u][4] < (self.reloj.segundos_totales - self.dict_clientes[u][2]):

                    if self.dict_clientes[u][5] == "apurado":
                        self.dict_clientes[u][0].setPixmap(QPixmap("sprites/clientes/hamster/hamster_21.png"))
                        self.dict_clientes[u][0].show()


                    elif self.dict_clientes[u][5] == "tranquilo":
                        self.dict_clientes[u][0].setPixmap(QPixmap("sprites/clientes/perro/perro_15.png"))
                        self.dict_clientes[u][0].resize(45, 45)
                        self.dict_clientes[u][0].show()

        if self.perdidos + self.atendidos == self.total_por_atender_ronda:
            self.datos = {"perdidos": self.perdidos,
                              "atendidos": self.atendidos,
                              "reputacion": self.reputacion,
                          "dinero": self.dinero}
            self.salir_juego()