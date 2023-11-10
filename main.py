from festival import Festival
from asistente import Asistente
from seguridad import Seguridad  # Asegúrate de tener este módulo y clase
import numpy as np
from time import sleep
import matplotlib.pyplot as plt

# Duración total de la simulación en tiempo real (segundos)
DURACION_SIMULACION_REAL = 60  # 3 minutos en este ejemplo

DURACION_CONCIERTO_MINUTOS = 60  # 3 horas
TIEMPO_POR_ITERACION_MINUTOS = 5
ITERACIONES_TOTAL = DURACION_CONCIERTO_MINUTOS // TIEMPO_POR_ITERACION_MINUTOS

# Tiempo que cada iteración debe durar en tiempo real (segundos)
PAUSA_POR_ITERACION = DURACION_SIMULACION_REAL / ITERACIONES_TOTAL


festival = Festival(100, 100)
festival.agregar_escenario(20, 70, 20, 10, 500)
festival.agregar_escenario(40, 90, 10, 10, 250)
festival.agregar_zona_comida(60, 60, 100)
festival.agregar_zona_comercial(80, 20, 10, 5, 100)
festival.agregar_baños(30, 30, 10)

seguridad = [
    Seguridad(festival, np.random.randint(100), np.random.randint(100))
    for _ in range(5)
]

asistentes = [
    Asistente(festival, np.random.randint(100), np.random.randint(100),
              np.random.uniform(0.01, 1))
    for _ in range(100)
]
festival.dibujar(asistentes, seguridad)

# Métricas
asistentes_en_escenario = 0
asistentes_en_comida = 0
asistentes_en_baños = 0  # Nueva métrica
asistentes_salidos = 0
gasto_total = 0
incidentes_detectados = 0  # Nueva métrica

costo_en_escenario = []
costo_en_comida = []
costo_salidos = []
costo_sin_lugar = []

# Realizamos una simulación simple mostrando el movimiento
# de los asistentes en cada paso
for iteracion in range(ITERACIONES_TOTAL):

    festival.dibujar(asistentes, seguridad)

    asistentes_en_escenario = sum(
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
                    for e in festival.escenarios
                ]
            )
        ]
    )
    asistentes_en_comida = sum(
        [
            1
            for a in asistentes
            if np.hypot(
                a.x - festival.zonas_comida[0]["coords"][0],
                a.y - festival.zonas_comida[0]["coords"][1],
            )
            <= 5
        ]
    )
    asistentes_salidos = sum(
        [
            1
            for a in asistentes
            if a.estado == "salió"
        ]
    )

    Locationasistentes_en_escenario = [
        a
        for a in asistentes
        if any(
            e["coords"][0] - e["dims"][0] / 2
            <= a.x
            <= e["coords"][0] + e["dims"][0] / 2
            and e["coords"][1] - e["dims"][1] / 2
            <= a.y
            <= e["coords"][1] + e["dims"][1] / 2
            for e in festival.escenarios
        )
    ]
    Locationasistentes_en_comida = [
        a
        for a in asistentes
        if np.hypot(
            a.x - festival.zonas_comida[0]["coords"][0],
            a.y - festival.zonas_comida[0]["coords"][1],
        ) <= 5
    ]
    Locationasistentes_salidos = [
        a
        for a in asistentes
        if a.estado == "salió"
    ]
    asistentes_faltantes = [
        a for a in asistentes
        if a not in Locationasistentes_en_escenario
        and a not in Locationasistentes_en_comida
        and a not in Locationasistentes_salidos
    ]

    gasto_total = sum([a.gasto for a in asistentes])

    asistentes_en_baños = sum(
        [
            1
            for a in asistentes
            if np.hypot(
                a.x - festival.baños[0]["coords"][0],
                a.y - festival.baños[0]["coords"][1],
            )
            <= festival.baños[0]["radio"]
        ]
    )

    for guardia in seguridad:
        guardia.patrullar()
        # Asumiendo que devuelve el número de incidentes detectados
        incidentes_detectados += guardia.detectar_incidentes(asistentes)

    for asistente in asistentes:
        asistente.actualizar()

    sleep(PAUSA_POR_ITERACION)

    tiempo_transcurrido = (iteracion + 1) * TIEMPO_POR_ITERACION_MINUTOS
    print(f"Tiempo transcurrido: {tiempo_transcurrido} minutos")
    print(f"Asistentes en escenario: {asistentes_en_escenario}")
    print(f"Asistentes en zonas de comida: {asistentes_en_comida}")
    print(f"Asistentes que han salido: {asistentes_salidos}")
    print(f"Gasto promedio por asistente: {gasto_total / len(asistentes)}")
    print(f"Incidentes detectados: {incidentes_detectados}")
    print(f"Asistentes en baños: {asistentes_en_baños}\n")

# TODO: Graficar

# iteraciones = list(range(1, ITERACIONES_TOTAL + 1))

# plt.figure(figsize=(10, 5))  # Ajusta el tamaño de la gráfica según necesites
# plt.plot(iteraciones, costo_en_escenario, label='Escenario',
#          marker='o', color='red')
# plt.plot(iteraciones, costo_en_comida, label='Comida',
#          marker='1', color='green')
# plt.plot(iteraciones, costo_salidos, label='Salidos',
#          marker='2', color='blue')
# plt.plot(iteraciones, costo_sin_lugar, label='Sin lugar',
#          marker='3', color='yellow')

# # Etiquetas y título
# plt.xlabel('Iteración')
# plt.ylabel('Costo')
# plt.title('Costo por Ubicación en el Tiempo')
# plt.legend()  # Para mostrar las leyendas de las líneas

# # Muestra la gráfica
# plt.show()
