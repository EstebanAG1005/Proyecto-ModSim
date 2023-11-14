# Importamos las bibliotecas necesarias
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from matplotlib import animation
from matplotlib.widgets import TextBox
import numpy as np
import sys
from tqdm import tqdm
from queue import Queue


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
        self.total_asistentes_inicial = total_asistentes_inicial
        self.baños_queue = {i: Queue() for i in range(len(self.baños))}
        self.tiendas_queue = {i: Queue() for i in range(len(self.zonas_comerciales))}
        self.comida_queue = {i: Queue() for i in range(len(self.zonas_comida))}

    def procesar_colas(self):
        for i, baño in enumerate(self.baños):
            if not self.baños_queue[i].empty():
                asistente = self.baños_queue[i].get()
                # Allow the assistant to use the bathroom
                asistente.usar_baño()

    def agregar_escenario(self, x, y, width, height, capacidad):
        self.escenarios.append(
            {"coords": (x, y), "dims": (width, height), "capacidad": capacidad}
        )

    def agregar_zona_comida(self, x, y, capacidad):
        self.zonas_comida.append({"coords": (x, y), "capacidad": capacidad})

    def agregar_baños(self, x, y, radio):
        self.baños.append({"coords": (x, y), "radio": radio})

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

        img_bano = mpimg.imread('./imgs/toilet.png')
        img_esce = mpimg.imread('./imgs/stage.png')
        img_truck = mpimg.imread('./imgs/truck.png')
        img_store = mpimg.imread('./imgs/store.png')
        img_pasto = mpimg.imread('./imgs/grass.png')

        #ax.imshow(img_pasto, extent=[0, self.width, 0, self.height], aspect='auto')
        ax.set_facecolor('#73BE73')
        # Dibuja los baños
        for baño in self.baños:
            # plt.scatter(
            #     baño["coords"][0],
            #     baño["coords"][1],
            #     color="blue",
            #     label="Baño"
            # )
            # Ajusta el tamaño con el parámetro 'zoom'
            imagebox = OffsetImage(img_bano, zoom=0.2)
            ab = AnnotationBbox(imagebox, (baño["coords"][0],
                                           baño["coords"][1]),
                                frameon=False)
            ax.add_artist(ab)

        # Dibujar escenarios
        for escenario in self.escenarios:
            # ax.add_patch(
            #     patches.Rectangle(
            #         (
            #             # Cambio aquí
            #             escenario["coords"][0]\
            #             - escenario["dims"][0] / 2,
            #             # Y aquí
            #             escenario["coords"][1] - escenario["dims"][1] / 2,
            #         ),
            #         escenario["dims"][0],  # Cambio aquí
            #         escenario["dims"][1],  # Y aquí
            #         color="blue",
            #     )
            # )
            imagebox = OffsetImage(img_esce, zoom=0.1)  # Ajusta el tamaño con el parámetro 'zoom'
            ab = AnnotationBbox(imagebox, (escenario["coords"][0], escenario["coords"][1]), frameon=False)
            ax.add_artist(ab)

        # Dibujar zonas de comida
        for zona in self.zonas_comida:
            #ax.add_patch(patches.Circle(zona["coords"], 5, color="green"))
            imagebox = OffsetImage(img_truck, zoom=0.1)  # Ajusta el tamaño con el parámetro 'zoom'
            ab = AnnotationBbox(imagebox, (zona["coords"][0], zona["coords"][1]), frameon=False)
            ax.add_artist(ab)

        # Dibujar zonas comerciales
        for zona in self.zonas_comerciales:
            # ax.add_patch(
            #     patches.Rectangle(
            #         (
            #             # Corrección aquí
            #             zona["coords"][0] - zona["dims"][0] / 2,
            #             zona["coords"][1] - zona["dims"][1] / 2,  # Y aquí
            #         ),
            #         zona["dims"][0],  # Aquí
            #         zona["dims"][1],  # Y aquí
            #         color="red",
            #     )
            # )
            imagebox = OffsetImage(img_store, zoom=0.1)  # Ajusta el tamaño con el parámetro 'zoom'
            ab = AnnotationBbox(imagebox, (zona["coords"][0], zona["coords"][1]), frameon=False)
            ax.add_artist(ab)

        # asistentes
        (puntos_asistentes,) = ax.plot(
            [a.x for a in asistentes],
            [a.y for a in asistentes],
            "o",
            markersize=3,
            color="black"
        )

        # seguridad
        (puntos_seguridad,) = ax.plot(
            [s.x for s in seguridad],
            [s.y for s in seguridad],
            "s",
            markersize=5,
            color="red"
        )

        # Inicializa la barra de progreso y cuadros de texto
        progress_bar = tqdm(total=MAX_FRAMES, desc="Simulación")

        # Coordenadas y dimensiones del TextBox (ajusta según sea necesario)
        text_box_x = 0.125
        text_box_y = 0.88
        text_box_width = 0.30
        text_box_height = 0.1

        text_box = TextBox(
            fig.add_axes([text_box_x, text_box_y, text_box_width, text_box_height]),
            "",
            initial=""
        )

        def update_text_box():
            text_box.set_val(
                f"Asistentes en escenario: {metricas['asistentes_en_escenario'][-1]}\n"
                f"Asistentes en comida: {metricas['asistentes_en_comida'][-1]}\n"
                f"Asistentes en baños: {metricas['asistentes_en_banos'][-1]}\n"
                f"Incidentes Detectados: {metricas['incidentes_detectados'][-1]}\n"
                f"Gasto total: {metricas['gasto_total'][-1]}"
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

            # Actualiza posiciones de los miembros de seguridad
            for s in seguridad:
                s.patrullar()
            puntos_seguridad.set_data(
                [a.x for a in seguridad], [a.y for a in seguridad]
            )

            if self.frame_counter % self.report_interval == 0:
                self.generar_reporte(asistentes, seguridad, metricas)

                # Actualiza las métricas en tiempo real
                progress_bar.set_postfix({
                    'Asistentes en escenario': metricas['asistentes_en_escenario'][-1],
                    'Asistentes en comida': metricas['asistentes_en_comida'][-1],
                    'Asistentes en baños': metricas['asistentes_en_banos'][-1],
                    'Incidentes detectados': metricas['incidentes_detectados'][-1],
                    'Gasto total': metricas['gasto_total'][-1]
                })

                update_text_box()

                progress_bar.update(self.report_interval)

            if self.frame_counter == MAX_FRAMES - 1:
                plt.close()
                progress_bar.close()

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