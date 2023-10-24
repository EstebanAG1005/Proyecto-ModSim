from festival import Festival
from asistente import Asistente

# Suponemos que el festival ya está definido como en el código anterior
festival = Festival(100, 100)
festival.agregar_escenario(20, 70, 20, 10, 500)
festival.agregar_zona_comida(60, 60, 100)
festival.agregar_zona_comercial(80, 20, 10, 5, 100)

# Creamos un asistente en el punto (10, 10)
asistente = Asistente(festival, 10, 10)

# Actualizamos al asistente varias veces para ver su comportamiento
for _ in range(10):
    asistente.actualizar()
    print(asistente.x, asistente.y, asistente.estado, asistente.gasto)
