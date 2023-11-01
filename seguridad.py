import numpy as np


class Seguridad:
    def __init__(self, festival, x, y):
        self.festival = festival
        self.x = x
        self.y = y
        self.radio_deteccion = 10  # capacidad de detección de incidentes en un radio

    def patrullar(self):
        # Mover al miembro de seguridad aleatoriamente dentro de un radio limitado
        dx = np.random.randint(-3, 4)  # un movimiento aleatorio en x entre -3 y 3
        dy = np.random.randint(-3, 4)  # un movimiento aleatorio en y entre -3 y 3

        # Asegurar que no se sale de los límites del festival
        self.x = max(0, min(self.festival.width, self.x + dx))
        self.y = max(0, min(self.festival.height, self.y + dy))

    def detectar_incidentes(self, asistentes):
        asistentes_problematicos = []

        for asistente in asistentes:
            distancia = np.hypot(self.x - asistente.x, self.y - asistente.y)
            if distancia <= self.radio_deteccion and asistente.causando_problemas:
                asistentes_problematicos.append(asistente)

        # Por ahora, simplemente eliminamos a los asistentes problemáticos
        for asistente in asistentes_problematicos:
            asistentes.remove(asistente)

        return len(asistentes_problematicos)  # devuelve el número de asistentes problemáticos detectados
    
