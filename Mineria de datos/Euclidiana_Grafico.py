import matplotlib.pyplot as plt
import csv

def cargar_desde_csv(nombre_archivo):
    dataset = {}
    with open(nombre_archivo, mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            usuario = fila.pop('Usuario')
            dataset[usuario] = {k: float(v) for k, v in fila.items() if v.strip()}
    return dataset

def raiz_cuadrada(valor):
    if valor == 0:
        return 0
    x = valor
    for _ in range(20):
        x = 0.5 * (x + valor / x)
    return x

def distancia_euclidiana(idx_a, idx_b, datos):
    suma = 0
    # Iterar sobre las columnas (canciones), no sobre usuarios
    num_canciones = len(datos[idx_a])
    for k in range(num_canciones):
        val_a = datos[idx_a][k] if k < len(datos[idx_a]) else None
        val_b = datos[idx_b][k] if k < len(datos[idx_b]) else None
        if val_a is not None and val_b is not None:
            diferencia = val_a - val_b
            suma += diferencia ** 2
    return raiz_cuadrada(suma)

# Cargar datos
data = cargar_desde_csv('musica.csv')
usuarios = list(data.keys())
datos = [list(data[u].values()) for u in usuarios]

# Calcular distancias desde el usuario base (Angelica = índice 0)
usuario_base = 0
distancias = []
nombres = []

for i in range(len(usuarios)):
    if i != usuario_base:
        d = distancia_euclidiana(usuario_base, i, datos)
        distancias.append(d)
        nombres.append(usuarios[i])

# Graficar
plt.figure(figsize=(10, 5))
plt.bar(nombres, distancias, color='steelblue')
plt.title(f"Distancia Euclidiana desde {usuarios[usuario_base]}")
plt.xlabel("Usuario")
plt.ylabel("Distancia")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

