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
        self.puntos_encuentro.append({"coords": (x, y),
                                      "capacidad": capacidad})

    def agregar_salida(self, x, y, width, height):
        self.salidas.append({"coords": (x, y), "dims": (width, height)})

    def agregar_zona_comercial(self, x, y, width, height, capacidad):
        self.zonas_comerciales.append(
            {"coords": (x, y), "dims": (width, height), "capacidad": capacidad}
        )

    def dibujar(self, asistentes, seguridad):
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

            return (puntos_asistentes, puntos_seguridad)

        ani = animation.FuncAnimation(fig, update, frames=100,
                                      blit=True, interval=100)

        plt.show()
