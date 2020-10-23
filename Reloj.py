from PyQt5.QtCore import QObject, pyqtSignal, QTimer


class MiTimers(QObject):
    senal_actualizar_tiempo = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.segundos = 0
        self.minutos = 0
        self.horas = 0
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.enviar_dato)


    def enviar_dato(self):
        self.segundos += 1
        if self.segundos < 60:
            self.senal_actualizar_tiempo.emit({"seg": self.segundos,
                                               "min": self.minutos,
                                               "hora": self.horas})

        elif self.segundos >= 60:
            self.minutos += 1
            self.segundos = 0
            self.senal_actualizar_tiempo.emit({"seg": self.segundos,
                                               "min": self.minutos,
                                               "hora": self.horas})

        elif self.minutos >= 60:
            self.minutos = 0
            self.segundos = 0
            self.horas += 1
            self.senal_actualizar_tiempo.emit({"seg": self.segundos,
                                               "min": self.minutos,
                                               "hora": self.horas})

    def comenzar(self):
        self.timer.start()

    def parar(self):
        self.timer.stop()

    def reiniciar(self):
        self.segundos = 0
        self.minutos = 0
        self.horas = 0

    def isActive(self):
        if self.timer.isActive() == True:
            return True
        else:
            return False


class Crear_reloj(QObject):

    senal_clientes = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.segundos = 0
        self.minutos = 0
        self.horas = 0
        self.segundos_totales = 0

    def ejecutar_timer(self):
        self.timer = MiTimers()
        self.timer.senal_actualizar_tiempo.connect(self.actualizador_datos)
        self.timer.comenzar()

    def actualizador_datos(self, datos):
        self.segundos = datos["seg"]
        self.minutos = datos["min"]
        self.horas = datos["hora"]

        self.senal_clientes.emit()
        self.segundos_totales = self.segundos + self.minutos * 60 + self.horas * 60 * 60

    def reanudar(self):
        self.timer.comenzar()

    def parar(self):
        self.timer.parar()

    def reiniciar(self):
        self.timer.reiniciar()

    def isAlive(self):
        if self.timer.isActive() == True:
            return True
        else:
            return False