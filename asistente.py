import numpy as np


class Asistente:

    ESTADOS = [
        "relajado",
        "buscando amigos",
        "moviéndose hacia el escenario",
        "en pánico"
    ]

    def __init__(self, festival, x, y, clumpsynes=0.05):
        self.festival = festival
        self.x = x
        self.y = y
        self.estado = np.random.choice(Asistente.ESTADOS)
        # Velocidad de 1 a 5 m/s
        self.velocidad = np.random.uniform(1, 5)
        # Energía de 0 a 100%
        self.energia = np.random.uniform(0, 100)
        # Edad de 15 a 60 años
        self.edad = np.random.randint(15, 60)
        # Dinero disponible para gastar
        self.gasto = np.random.uniform(0, 500)
        # Dinero disponible para gastar
        self.aburrimiento = np.random.uniform(0, 100)
        # Hambre de 0 a 100%
        self.hambre = np.random.uniform(0, 100)
        # Ganas de ir al baño de 0 a 100%
        self.necesidad_bano = np.random.uniform(0, 100)
        # % de probabilidad de causar problemas
        self.causando_problemas = np.random.choice(
            [True, False], p=[clumpsynes, 1 - clumpsynes]
        )
        self.tiempos = {
            'tiendas': 0,
            'escenarios': 0,
            'baños': 0,
            'restaurantes': 0,
        }
        self.current_queue = None
    
    def reset_times(self):
        self.tiempos = {
            'tiendas': 0,
            'escenarios': 0,
            'baños': 0,
            'restaurantes': 0,
        }

    def mover(self):
        if self.aburrimiento >= 80 and self.gasto > 10:
            if len(self.festival.zonas_comerciales) > 0:
                # Movemos al asistente hacia la zona de comercio
                zona_comercial_cercana = min(
                    self.festival.zonas_comerciales,
                    key=lambda e: np.hypot(
                        self.x - e["coords"][0], self.y - e["coords"][1]
                    ),
                )
                dir_x = zona_comercial_cercana["coords"][0] - self.x
                dir_y = zona_comercial_cercana["coords"][1] - self.y
                norm = np.hypot(dir_x, dir_y)
                if norm > 0:
                    dir_x /= norm
                    dir_y /= norm
                    self.x += dir_x * self.velocidad
                    self.y += dir_y * self.velocidad
        
        elif self.aburrimiento >= 80:
            if 0 <= self.x <= self.festival.width:
                self.x += np.random.randint(0, 3) - 1
            if 0 <= self.y <= self.festival.height:
                self.y += np.random.randint(0, 3) - 1
            if np.random.randint(0, 100) < 6:
                self.aburrimiento = 10
        
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
                if -3 <= dir_x <= 3 and -3 <= dir_y <= 3:
                    self.tiempos['escenarios'] +=1
                if norm > 0:
                    dir_x /= norm
                    dir_y /= norm
                    self.x += dir_x * self.velocidad
                    self.y += dir_y * self.velocidad
        # Se pueden añadir más comportamientos dependiendo
        # del estado del asistente

    def interactuar_tiendas(self):
        # Si el asistente se encuentra cerca de una tienda,
        # interactuará con ella
        for tienda in self.festival.zonas_comerciales:
            distancia = np.hypot(
                self.x - tienda["coords"][0], self.y - tienda["coords"][1]
            )
            # Asumiendo que 5 metros es una distancia de interacción
            if distancia <= 5:
                if self.gasto > 0:
                    self.gasto -= np.random.uniform(
                        0, self.gasto
                    )/10
                self.aburrimiento -= 2
                self.tiempos['tiendas'] += 1

    def mover_hacia_baño(self):
        if self.necesidad_bano > 90 and len(self.festival.baños) > 0:
            # If already in a queue, continue to the same bathroom
            if self.current_queue:
                baño_cercano = self.current_queue
            else:
                # Choose the bathroom with the shortest queue
                baño_cercano = min(
                    self.festival.baños,
                    key=lambda b: (len(b["queue"]), np.hypot(self.x - b["coords"][0],
                                                            self.y - b["coords"][1]))
                )

            dir_x = baño_cercano["coords"][0] - self.x
            dir_y = baño_cercano["coords"][1] - self.y
            norm = np.hypot(dir_x, dir_y)

            if norm <= 3:  # Near the bathroom
                if self not in baño_cercano["queue"]:
                    baño_cercano["queue"].append(self)
                    self.current_queue = baño_cercano  # Update the current queue
                    self.tiempos['baños'] += 1

                if baño_cercano["queue"][0] == self:  # It's their turn
                    if np.random.randint(0, 100) <= 50:
                        self.necesidad_bano = 0
                        baño_cercano["queue"].pop(0)  # Leave the queue
                        self.current_queue = None  # Clear the current queue
                    self.tiempos['baños'] += 1
            else:
                # Move towards the bathroom
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

            if np.abs(dir_x) <= 4 and np.abs(dir_y) <= 4:
                if np.random.randint(0, 100) <= 20:
                    self.hambre = 100
                    self.necesidad_bano += 30
                self.tiempos['restaurantes'] += 1
                
            norm = np.hypot(dir_x, dir_y)
            if norm > 0:
                dir_x /= norm
                dir_y /= norm
                self.x += dir_x * self.velocidad
                self.y += dir_y * self.velocidad
            return True
        return False
    
    def in_bound(self, x, y):
        inLow_salida_X = self.festival.salida['x'] - 3 <= x
        inHigh_salida_X = x <= self.festival.salida['x'] + 3
        in_salida_X = inLow_salida_X and inHigh_salida_X

        inLow_salida_Y = self.festival.salida['y'] - 3 <= y
        inHigh_salida_Y = y <= self.festival.salida['y'] + 3
        in_salida_Y = inLow_salida_Y and inHigh_salida_Y

        return in_salida_X and in_salida_Y

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

            if self.in_bound(self.x, self.y):
                self.estado = "salió"

            if np.random.randint(0, 100) <= 5:
                self.energia = 50
            
            return True
        return False

    def actualizar(self):
        # Actualizamos el estado y comportamiento del asistente

        if not self.mover_hacia_salida():
            if not self.mover_hacia_baño():
                if not self.mover_hacia_comida():
                    self.interactuar_tiendas()
                    self.mover()


        # Parámetros de la distribución normal
        media = 0.01  # Ejemplo: reduce en promedio un 2% de energía
        desviacion = 0.04  # Varía hasta un 1% alrededor de la media

        # Reducir energía usando una distribución normal
        reduccion_energia = np.random.normal(media, desviacion)
        self.energia -= reduccion_energia

        # Asegurarse de que la energía no caiga por debajo de 0
        self.energia = max(self.energia, 0)
        # Los asistentes se vuelven más hambrientos con el tiempo
        self.hambre -= 0.6
        self.aburrimiento += 0.8
        self.necesidad_bano += 0.5
