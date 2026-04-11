import csv
import matplotlib.pyplot as plt


def cargar_desde_csv(nombre_archivo):
    dataset = {}
    with open(nombre_archivo, mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            usuario = fila.pop('Usuario')
            dataset[usuario] = {k: float(v) for k, v in fila.items() if v.strip()}
    return dataset

def distancia_manhattan_normalizada(idx_a, idx_b, datos):
    distancia = 0
    contador = 0

    num_canciones = len(datos[idx_a])
    for k in range(num_canciones):
        val_a = datos[idx_a][k] if k < len(datos[idx_a]) else None
        val_b = datos[idx_b][k] if k < len(datos[idx_b]) else None
        if val_a is not None and val_b is not None:
            diferencia = abs(val_a - val_b)
            contador += 1

            distancia += diferencia

    return distancia

data = cargar_desde_csv('musica.csv')
usuarios = list(data.keys())
datos = [list(data[u].values()) for u in usuarios]

usuario_base = 0  # Angelica
distancias = []
nombres = []

for i in range(len(usuarios)):
    if i != usuario_base:
        d = distancia_manhattan_normalizada(usuario_base, i, datos)
        distancias.append(d)
        nombres.append(usuarios[i])

plt.bar(nombres, distancias)
plt.title("Distancia Manhattan desde Angelica")
plt.xticks(rotation=45)
plt.show()

matriz = []

for i in range(len(datos)):
    fila = []
    for j in range(len(datos)):
        d = distancia_manhattan_normalizada(i, j, datos)
        fila.append(d if d is not None else 0)
    matriz.append(fila)