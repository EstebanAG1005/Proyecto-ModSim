import numpy as np


class Asistente:

    ESTADOS = [
        "relajado",
        "buscando amigos",
        "moviéndose hacia el escenario",
        "en pánico"
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
        self.aburrimiento = np.random.uniform(0, 100)  # Dinero disponible para gastar
        self.hambre = np.random.uniform(0, 100)  # Hambre de 0 a 100%
        self.necesidad_bano = np.random.uniform(0, 100)  # Ganas de ir al baño de 0 a 100%
        self.causando_problemas = np.random.choice(
            [True, False], p=[0.05, 0.95]
        )  # 5% de probabilidad de causar problemas

    def mover(self):
        if self.aburrimiento >= 80 and self.gasto > 10:
            if len(self.festival.zonas_comerciales) > 0: 
                # Movemos al asistente hacia la zona de comercio
                    escenario_cercano = min(
                        self.festival.zonas_comerciales,
                        key=lambda e: np.hypot(
                            self.x - e["coords"][0], self.y - e["coords"][1]
                        ),
                    )
                    dir_x = escenario_cercano["coords"][0] - self.x
                    dir_y = escenario_cercano["coords"][1] - self.y
                    norm = np.hypot(dir_x, dir_y)
                    if norm > 0:
                        dir_x /= norm
                        dir_y /= norm
                        self.x += dir_x * self.velocidad
                        self.y += dir_y * self.velocidad
        
        elif self.aburrimiento >= 80:
            if 0 <= self.x <= self.festival.width: 
                self.x += np.random.randint(0, 2) -1
            
            if 0 <= self.y <= self.festival.height:
                self.y += np.random.randint(0, 2) -1
            self.aburrimiento -=2
        
        else:
            if len(self.festival.escenarios) > 0:
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
                if norm > 0:
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
                if self.gasto > 0:
                    self.gasto -= np.random.uniform(
                        0, self.gasto
                    )  # Gastará una cantidad aleatoria de su dinero disponible
                self.aburrimiento -= 2

    def mover_hacia_baño(self):
        # Suponemos que si un asistente necesita ir al baño su necesidad es > 90
        if self.necesidad_bano > 90 and len(self.festival.baños) > 0:
            baño_cercano = min(
                self.festival.baños,
                key=lambda b: np.hypot(self.x - b["coords"][0], self.y - b["coords"][1])
            )
            
            # Calculamos la dirección hacia el baño
            dir_x = baño_cercano["coords"][0] - self.x
            dir_y = baño_cercano["coords"][1] - self.y

            if -3 <= dir_x <= 3 and -3 <= dir_y <= 3:
                self.necesidad_bano = 0

            norm = np.hypot(dir_x, dir_y)
            
            # Movemos al asistente hacia el baño
            if norm > 0:
                dir_x /= norm
                dir_y /= norm
                self.x += dir_x * self.velocidad
                self.y += dir_y * self.velocidad
            
            return True
        return False


    def mover_hacia_comida(self):
        if self.hambre < 20 and len(self.festival.zonas_comida) > 0:
            zona_cercana = min(
                self.festival.zonas_comida,
                key=lambda z: np.hypot(
                    self.x - z["coords"][0], self.y - z["coords"][1]
                ),
            )
            dir_x = zona_cercana["coords"][0] - self.x
            dir_y = zona_cercana["coords"][1] - self.y

            if np.abs(dir_x) <= 4 and np.abs(dir_y) <=4:
                self.hambre = 100
                
            norm = np.hypot(dir_x, dir_y)
            if norm > 0:
                dir_x /= norm
                dir_y /= norm
                self.x += dir_x * self.velocidad
                self.y += dir_y * self.velocidad
            return True
        return False

    def mover_hacia_salida(self):
        if self.energia < 10:
            dir_x = self.festival.salida["x"] - self.x
            dir_y = self.festival.salida["y"] - self.y
            norm = np.hypot(dir_x, dir_y)
            if norm > 0:
                dir_x /= norm
                dir_y /= norm
                self.x += dir_x * self.velocidad
                self.y += dir_y * self.velocidad

            if self.festival.salida['x']-3 <= self.x <= self.festival.salida['x']+3 and self.festival.salida['y']-3 <= self.y <= self.festival.salida['y'] +3:
                self.estado = "salió"
            return True
        return False

    def actualizar(self):
        # Actualizamos el estado y comportamiento del asistente

        if not self.mover_hacia_salida():
            if not self.mover_hacia_baño():
                if not self.mover_hacia_comida():
                    self.interactuar_tiendas()
                    self.mover()

        self.energia -= 0.05  # Cada paso consume un poco de energía
        self.hambre -= 0.1  # Los asistentes se vuelven más hambrientos con el tiempo
        self.aburrimiento += 0.5
