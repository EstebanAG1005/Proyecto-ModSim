from festival import Festival
from asistente import Asistente
from seguridad import Seguridad  # Asegúrate de tener este módulo y clase
from cola import Cola
import numpy as np
from time import sleep
import matplotlib.pyplot as plt

TOTAL_ASISTENTES_INICIAL = 500


festival = Festival(100, 100, TOTAL_ASISTENTES_INICIAL)
festival.agregar_escenario(50, 20, 20, 10, 500)
festival.agregar_escenario(15, 60, 10, 10, 250)
festival.agregar_zona_comida(50, 50, 100, 50)
festival.agregar_zona_comercial(95, 5, 10, 10, 100)
festival.agregar_baños(80, 90, 10, 10)
festival.agregar_baños(90, 80, 10, 10)

seguridad = [
    Seguridad(festival, np.random.randint(100), np.random.randint(100))
    for _ in range(5)
]

asistentes = [
    Asistente(festival, np.random.randint(100), np.random.randint(100),
              np.random.uniform(0.01, 1))
    for _ in range(TOTAL_ASISTENTES_INICIAL)
]

metricas = {
    'asistentes_en_escenario':[],
    'asistentes_en_comida':[],
    'asistentes_salidos':[],
    'gasto_total':[],
    'asistentes_en_banos':[],
    'tiempo_en_escenarios':[],
    'tiempo_en_banos':[],
    'tiempo_en_restaurantes':[],
    'tiempo_en_tiendas':[],
    'incidentes_detectados':[],
    'total_asistentes': [],
    'tiempo_transcurrido': []
}

festival.dibujar(asistentes, seguridad, metricas)

# 1. Gráfico de Líneas
plt.figure(figsize=(10, 6))
for key in ['asistentes_en_escenario', 'asistentes_en_comida', 'asistentes_salidos']:
    plt.plot(metricas[key], label=key)
plt.title('Tendencias a lo Largo del Tiempo')
plt.xlabel('Tiempo (Iteraciones)')
plt.ylabel('Valor')
plt.legend()
plt.show()

# 1. Gráfico de Líneas
plt.figure(figsize=(10, 6))
for key in ['gasto_total']:
    plt.plot(metricas[key], label=key)
plt.title('Gasto')
plt.xlabel('Tiempo (Iteraciones)')
plt.ylabel('Valor')
plt.legend()
plt.show()


# 3. Gráficos de Barras
for key in ['tiempo_en_banos', 'tiempo_en_restaurantes', 'tiempo_en_tiendas', 'tiempo_en_escenarios', 'total_asistentes']:
    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    index = range(len(metricas[key]))
    plt.bar(index, metricas[key], bar_width, label=key)
    plt.title(f'Comparación de {key}')
    plt.xlabel('Iteración')
    plt.ylabel('')
    plt.legend()
    plt.show()

# 5. Gráfico de Áreas Apiladas
plt.figure(figsize=(10, 6))
plt.stackplot(range(len(metricas['total_asistentes'])), metricas['asistentes_en_escenario'], metricas['asistentes_en_comida'], metricas['asistentes_en_banos'], labels=['En Escenario', 'En Comida', 'En Baño'])
plt.title('Distribución de Asistentes a lo Largo del Tiempo')
plt.xlabel('Tiempo (Iteraciones)')
plt.ylabel('Número de Asistentes')
plt.legend()
plt.show()

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
