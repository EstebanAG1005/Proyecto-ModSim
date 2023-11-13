# Importamos las bibliotecas necesarias
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation
import numpy as np
import sys
from cola import Cola

#REPORT
REPORT_INTERVAL = 50
INTERVAL_TIME = 5 # MINS
FRAMES_PER_MIN = REPORT_INTERVAL / INTERVAL_TIME

#OTHER
MAX_TIME = 180 #3 HOURS
MAX_FRAMES = MAX_TIME * FRAMES_PER_MIN


class Festival:
    def __init__(self, width, height, total_asistentes_inicial):
        self.width = width
        self.height = height
        #self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.escenarios = []
        self.zonas_comida = []
        self.baños = []
        self.puntos_encuentro = []
        self.salidas = []
        self.zonas_comerciales = []
        self.frame_counter = 0
        self.report_interval = REPORT_INTERVAL
        self.salida = {
            "x": width,
            "y": height / 2,
        }  # Añadimos una salida en la mitad del borde derecho
        self.baños = []
        self.total_asistentes_inicial = total_asistentes_inicial

    def agregar_escenario(self, x, y, width, height, capacidad):
        self.escenarios.append(
            {"coords": (x, y), "dims": (width, height), "capacidad": capacidad}
        )

    def agregar_zona_comida(self, x, y, capacidad, capacidad_cola):
        self.zonas_comida.append({"coords": (x, y), "capacidad": capacidad, "cola": Cola(capacidad_cola)})

    def agregar_baños(self, x, y, radio, capacidad_cola):
        self.baños.append({"coords": (x, y), "radio": radio, "cola": Cola(capacidad_cola)})

    def agregar_punto_encuentro(self, x, y, capacidad):
        self.puntos_encuentro.append({"coords": (x, y),
                                      "capacidad": capacidad})

    def agregar_salida(self, x, y, width, height):
        self.salidas.append({"coords": (x, y), "dims": (width, height)})

    def agregar_zona_comercial(self, x, y, width, height, capacidad):
        self.zonas_comerciales.append(
            {"coords": (x, y), "dims": (width, height), "capacidad": capacidad}
        )

    def dibujar(self, asistentes, seguridad, metricas):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)

        plt.scatter(
            self.salida["x"],
            self.salida["y"],
            color="black",
            marker="s",
            label="Salida",
        )

        # Dibuja los baños
        for baño in self.baños:
            plt.scatter(
                baño["coords"][0],
                baño["coords"][1],
                color="blue",
                label="Baño"
            )

        # Dibujar escenarios
        for escenario in self.escenarios:
            ax.add_patch(
                patches.Rectangle(
                    (
                        # Cambio aquí
                        escenario["coords"][0]\
                        - escenario["dims"][0] / 2,
                        # Y aquí
                        escenario["coords"][1] - escenario["dims"][1] / 2,
                    ),
                    escenario["dims"][0],  # Cambio aquí
                    escenario["dims"][1],  # Y aquí
                    color="blue",
                )
            )

        # Dibujar zonas de comida
        for zona in self.zonas_comida:
            ax.add_patch(patches.Circle(zona["coords"], 5, color="green"))

        # Dibujar zonas comerciales
        for zona in self.zonas_comerciales:
            ax.add_patch(
                patches.Rectangle(
                    (
                        # Corrección aquí
                        zona["coords"][0] - zona["dims"][0] / 2,
                        zona["coords"][1] - zona["dims"][1] / 2,  # Y aquí
                    ),
                    zona["dims"][0],  # Aquí
                    zona["dims"][1],  # Y aquí
                    color="red",
                )
            )

        # asistentes
        (puntos_asistentes,) = ax.plot(
            [a.x for a in asistentes],
            [a.y for a in asistentes],
            "o",
            markersize=3
        )

        # seguridad
        (puntos_seguridad,) = ax.plot(
            [s.x for s in seguridad],
            [s.y for s in seguridad],
            "s",
            markersize=5,
            color="orange"
        )

        def update(num):
            self.frame_counter +=1
            # Actualizar posiciones de los asistentes
            for a in asistentes:
                a.actualizar()
            puntos_asistentes.set_data(
                [a.x for a in asistentes if a.estado != "salió"],
                [a.y for a in asistentes if a.estado != "salió"]
            )

            # Actualización adicional para manejar las colas
            for baño in self.baños:
                cola_baño = baño["cola"].cola
                if cola_baño:
                    cola_baño[0].tiempo_en_baño -= 1
                    if cola_baño[0].tiempo_en_baño <= 0:
                        asistente = baño["cola"].salir_de_cola()
                        if asistente:
                            asistente.necesidad_bano = 0
                            asistente.estado = "relajado"
                            
            for zona_comida in self.zonas_comida:
                if zona_comida["cola"].cola:  # Si hay gente en la cola
                    asistente = zona_comida["cola"].salir_de_cola()
                    if asistente:
                        asistente.hambre = 100  # Asistente ha comido
                        asistente.estado = "relajado"

            # Actualiza posiciones de los miembros de seguridad
            for s in seguridad:
                s.patrullar()
            puntos_seguridad.set_data(
                [a.x for a in seguridad], [a.y for a in seguridad]
            )

            if self.frame_counter % self.report_interval == 0:
                self.generar_reporte(asistentes, seguridad, metricas)

            if self.frame_counter == MAX_FRAMES - 1:
                plt.close()

            return (puntos_asistentes, puntos_seguridad)

        ani = animation.FuncAnimation(fig, update, frames=100,
                                      blit=True, interval=2)

        plt.show()

    def generar_reporte(self, asistentes, seguridad, metricas):

        metricas["asistentes_en_escenario"].append(sum(
            [
                1
                for a in asistentes
                if any(
                    [
                        e["coords"][0] - e["dims"][0] / 2
                        <= a.x
                        <= e["coords"][0] + e["dims"][0] / 2
                        and e["coords"][1] - e["dims"][1] / 2
                        <= a.y
                        <= e["coords"][1] + e["dims"][1] / 2
                        for e in self.escenarios
                    ]
                )
            ]
        ))
        metricas["asistentes_en_comida"].append(sum(
            [
                1
                for a in asistentes
                if np.hypot(
                    a.x - self.zonas_comida[0]["coords"][0],
                    a.y - self.zonas_comida[0]["coords"][1],
                )
                <= 5
            ]
        ))

        metricas["gasto_total"].append(sum([a.gasto for a in asistentes]))

        metricas["asistentes_en_banos"].append(sum(
            [
                1
                for a in asistentes
                if np.hypot(
                    a.x - self.baños[0]["coords"][0],
                    a.y - self.baños[0]["coords"][1],
                )
                <= self.baños[0]["radio"]
            ]
        ))

        metricas["tiempo_en_escenarios"].append(sum(
            [
                a.tiempos['escenarios']/FRAMES_PER_MIN for a in asistentes
            ]
        ) / len(asistentes))
        metricas["tiempo_en_banos"].append(sum(
            [
                a.tiempos['baños']/FRAMES_PER_MIN for a in asistentes
            ]
        ) / len(asistentes))
        metricas["tiempo_en_restaurantes"].append(sum(
            [
                a.tiempos['restaurantes']/FRAMES_PER_MIN for a in asistentes
            ]
        ) / len(asistentes))
        metricas["tiempo_en_tiendas"].append(sum(
            [
                a.tiempos['tiendas']/FRAMES_PER_MIN for a in asistentes
            ]
        ) / len(asistentes))

        metricas["total_asistentes"].append(sum(
            [
                1 for a in asistentes if a.estado != 'salió'
             ]
        ))
        if len(metricas["asistentes_salidos"]) >0 :
            metricas["asistentes_salidos"].append(metricas['total_asistentes'][-2] - metricas['total_asistentes'][-1])
        else:
            metricas["asistentes_salidos"].append(self.total_asistentes_inicial - metricas['total_asistentes'][-1])

        if len(metricas["tiempo_transcurrido"]) >0:
            metricas["tiempo_transcurrido"].append(metricas["tiempo_transcurrido"][-1] + 5)
        else:
            metricas["tiempo_transcurrido"].append(5)


        for guardia in seguridad:
            guardia.patrullar()
            # Asumiendo que devuelve el número de incidentes detectados
            metricas['incidentes_detectados'].append(guardia.detectar_incidentes(asistentes))

        for asistente in asistentes:
            asistente.actualizar()
            asistente.reset_times()

        print(f"Tiempo transcurrido {metricas['tiempo_transcurrido'][-1]} minutos")
        print(f"Total de asistentes {metricas['total_asistentes'][-1]}")
        print(f"Asistentes en escenario: {metricas['asistentes_en_escenario'][-1]}")
        print(f"Asistentes en zonas de comida: {metricas['asistentes_en_comida'][-1]}")
        print(f"Asistentes que han salido: {metricas['asistentes_salidos'][-1]}")
        print(f"Gasto promedio por asistente: {metricas['gasto_total'][-1] / len(asistentes)}")
        print(f"Incidentes detectados: {metricas['incidentes_detectados'][-1]}")
        print(f"Asistentes en baños: {metricas['asistentes_en_banos'][-1]}")
        print(f"Tiempo promedio en escenarios: {metricas['tiempo_en_escenarios'][-1]}")
        print(f"Tiempo promedio en tiendas: {metricas['tiempo_en_tiendas'][-1]}")
        print(f"Tiempo promedio en baños: {metricas['tiempo_en_banos'][-1]}")
        print(f"Tiempo promedio en restaurantes: {metricas['tiempo_en_restaurantes'][-1]}\n")