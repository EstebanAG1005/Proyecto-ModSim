class Cola:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.cola = []

    def entrar_en_cola(self, asistente):
        if len(self.cola) < self.capacidad:
            self.cola.append(asistente)
            return True
        return False

    def salir_de_cola(self):
        if self.cola:
            return self.cola.pop(0)
        return None
