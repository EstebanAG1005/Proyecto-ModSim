import numpy as np


class Asistente:

    ESTADOS = [
        "relajado",
        "buscando amigos",
        "moviéndose hacia el escenario",
        "en pánico",
    ]

    def __init__(self, festival, x, y):
        self.festival = festival
        self.x = x
        self.y = y
        self.estado = np.random.choice(Asistente.ESTADOS)
        self.velocidad = np.random.uniform(1, 5)  # Velocidad de 1 a 5 m/s
        self.energia = np.random.uniform(0, 100)  # Energía de 0 a 100%
        self.edad = np.random.randint(15, 60)  # Edad de 15 a 60 años
        self.gasto = np.random.uniform(0, 500)  # Dinero disponible para gastar

    def mover(self):
        if (
            self.estado == "moviéndose hacia el escenario"
            and len(self.festival.escenarios) > 0
        ):
            # Movemos al asistente hacia el escenario más cercano
            escenario_cercano = min(
                self.festival.escenarios,
                key=lambda e: np.hypot(
                    self.x - e["coords"][0], self.y - e["coords"][1]
                ),
            )
            dir_x = escenario_cercano["coords"][0] - self.x
            dir_y = escenario_cercano["coords"][1] - self.y
            norm = np.hypot(dir_x, dir_y)
            dir_x /= norm
            dir_y /= norm
            self.x += dir_x * self.velocidad
            self.y += dir_y * self.velocidad

        # Se pueden añadir más comportamientos dependiendo del estado del asistente

    def interactuar_tiendas(self):
        # Si el asistente se encuentra cerca de una tienda, interactuará con ella
        for tienda in self.festival.zonas_comerciales:
            distancia = np.hypot(
                self.x - tienda["coords"][0], self.y - tienda["coords"][1]
            )
            if distancia <= 5:  # Asumiendo que 5 metros es una distancia de interacción
                self.gasto -= np.random.uniform(
                    0, self.gasto
                )  # Gastará una cantidad aleatoria de su dinero disponible

    def actualizar(self):
        # Actualizamos el estado y comportamiento del asistente
        self.mover()
        self.interactuar_tiendas()
        self.energia -= 0.1  # Cada paso consume un poco de energía
