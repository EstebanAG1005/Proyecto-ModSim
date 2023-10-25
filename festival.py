# Importamos las bibliotecas necesarias
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation


class Festival:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.escenarios = []
        self.zonas_comida = []
        self.baños = []
        self.puntos_encuentro = []
        self.salidas = []
        self.zonas_comerciales = []
        self.salida = {
            "x": width,
            "y": height / 2,
        }  # Añadimos una salida en la mitad del borde derecho
        self.baños = []

    def agregar_escenario(self, x, y, width, height, capacidad):
        self.escenarios.append(
            {"coords": (x, y), "dims": (width, height), "capacidad": capacidad}
        )

    def agregar_zona_comida(self, x, y, capacidad):
        self.zonas_comida.append({"coords": (x, y), "capacidad": capacidad})

    def agregar_baños(self, x, y, radio):
        self.baños.append({"coords": (x, y), "radio": radio})

    def agregar_punto_encuentro(self, x, y, capacidad):
        self.puntos_encuentro.append({"coords": (x, y), "capacidad": capacidad})

    def agregar_salida(self, x, y, width, height):
        self.salidas.append({"coords": (x, y), "dims": (width, height)})

    def agregar_zona_comercial(self, x, y, width, height, capacidad):
        self.zonas_comerciales.append(
            {"coords": (x, y), "dims": (width, height), "capacidad": capacidad}
        )

    def mostrar_mapa(self):
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)

        for escenario in self.escenarios:
            rect = patches.Rectangle(
                escenario["coords"],
                *escenario["dims"],
                linewidth=1,
                edgecolor="blue",
                facecolor="blue",
                alpha=0.5,
                label="Escenario"
            )
            self.ax.add_patch(rect)

        for zona in self.zonas_comida:
            circ = patches.Circle(zona["coords"], 5, color="red", label="Zona Comida")
            self.ax.add_patch(circ)

        for baño in self.baños:
            rect = patches.Rectangle(
                baño,
                2,
                2,
                linewidth=1,
                edgecolor="green",
                facecolor="green",
                alpha=0.5,
                label="Baño",
            )
            self.ax.add_patch(rect)

        for punto in self.puntos_encuentro:
            circ = patches.Circle(
                punto["coords"], 3, color="yellow", label="Punto de Encuentro"
            )
            self.ax.add_patch(circ)

        for salida in self.salidas:
            rect = patches.Rectangle(
                salida["coords"],
                *salida["dims"],
                linewidth=1,
                edgecolor="black",
                facecolor="black",
                alpha=0.5,
                label="Salida"
            )
            self.ax.add_patch(rect)

        for zona in self.zonas_comerciales:
            rect = patches.Rectangle(
                zona["coords"],
                *zona["dims"],
                linewidth=1,
                edgecolor="purple",
                facecolor="purple",
                alpha=0.5,
                label="Zona Comercial"
            )
            self.ax.add_patch(rect)

        self.ax.set_title("Mapa del Festival")
        handles, labels = self.ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        self.ax.legend(
            by_label.values(), by_label.keys(), loc="upper left", bbox_to_widthr=(1, 1)
        )
        plt.show()

    def dibujar(self, asistentes):
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
                baño["coords"][0], baño["coords"][1], color="blue", label="Baño"
            )

        # Dibujar escenarios
        for escenario in self.escenarios:
            ax.add_patch(
                patches.Rectangle(
                    (
                        escenario["coords"][0]
                        - escenario["dims"][0] / 2,  # Cambio aquí
                        escenario["coords"][1] - escenario["dims"][1] / 2,  # Y aquí
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
                        zona["coords"][0] - zona["dims"][0] / 2,  # Corrección aquí
                        zona["coords"][1] - zona["dims"][1] / 2,  # Y aquí
                    ),
                    zona["dims"][0],  # Aquí
                    zona["dims"][1],  # Y aquí
                    color="red",
                )
            )

        (puntos_asistentes,) = ax.plot(
            [a.x for a in asistentes], [a.y for a in asistentes], "o", markersize=3
        )

        def update(num):
            # Actualizar posiciones de los asistentes
            for a in asistentes:
                a.actualizar()
            puntos_asistentes.set_data(
                [a.x for a in asistentes], [a.y for a in asistentes]
            )
            return (puntos_asistentes,)

        ani = animation.FuncAnimation(fig, update, frames=100, blit=True, interval=100)
        plt.show()
