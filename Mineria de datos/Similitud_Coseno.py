import matplotlib.pyplot as plt
import csv

def cargar_desde_csv(nombre_archivo):
    dataset = {}
    with open(nombre_archivo, mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            usuario = fila.pop('Usuario')
            # None para valores vacíos, float para los que tienen dato
            dataset[usuario] = {
                k: (float(v) if v.strip() else None)
                for k, v in fila.items()
            }
    return dataset

data = cargar_desde_csv('musica.csv')
usuarios = list(data.keys())
canciones = list(data[usuarios[0]].keys())  # columnas del CSV

# Matriz alineada: todos los usuarios con todas las canciones (None si falta)
datos = [
    [data[u].get(c, None) for c in canciones]
    for u in usuarios
]

def raiz_cuadrada(valor):
    if valor == 0:
        return 0
    x = valor
    for _ in range(20):
        x = 0.5 * (x + valor / x)
    return x

def producto_punto(idx_a, idx_b, datos):
    suma = 0
    longitud = min(len(datos[idx_a]), len(datos[idx_b]))  # ← fix principal
    for k in range(longitud):
        a = datos[idx_a][k]
        b = datos[idx_b][k]
        if a is not None and b is not None:
            suma += a * b
    return suma

def magnitud(idx, datos):
    suma = 0
    for k in range(len(datos[idx])):
        v = datos[idx][k]
        if v is not None:
            suma += v * v
    return raiz_cuadrada(suma)

def similitud_coseno(idx_a, idx_b, datos):
    pp = producto_punto(idx_a, idx_b, datos)
    mag_a = magnitud(idx_a, datos)
    mag_b = magnitud(idx_b, datos)
    if mag_a == 0 or mag_b == 0:
        return 0
    return pp / (mag_a * mag_b)

# Calcular similitudes respecto a Angelica
usuario_base = "Angelica"
i = usuarios.index(usuario_base)

valores = []
nombres = []
for j in range(len(usuarios)):
    if j != i:
        sim = similitud_coseno(i, j, datos)
        valores.append(sim)
        nombres.append(usuarios[j])

# Graficar
plt.figure(figsize=(10, 5))
plt.bar(nombres, valores, color='steelblue')
plt.title("Similitud de Coseno respecto a Angelica")
plt.xlabel("Usuarios")
plt.ylabel("Similitud (0 a 1)")
plt.xticks(rotation=45, ha='right')
plt.ylim(0, 1)
plt.tight_layout()
plt.show()