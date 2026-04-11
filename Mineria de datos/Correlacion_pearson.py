import csv
import matplotlib.pyplot as plt


def cargar_desde_csv(nombre_archivo):
    dataset = {}
    with open(nombre_archivo, mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            usuario = fila.pop('Usuario')
            # Convertimos a float solo si hay valor, si no, None
            dataset[usuario] = {k: float(v) for k, v in fila.items() if v.strip()}
    return dataset


def raiz_cuadrada(valor):
    if valor <= 0: return 0
    x = valor
    for _ in range(20):
        x = 0.5 * (x + valor / x)
    return x

def correlacion_pearson(user1_dict, user2_dict):
    # Encontrar artistas comunes
    comunes = [art for art in user1_dict if art in user2_dict]
    n = len(comunes)
    if n == 0: return 0

    # Extraer valores
    x = [user1_dict[art] for art in comunes]
    y = [user2_dict[art] for art in comunes]

    prom_x = sum(x) / n
    prom_y = sum(y) / n

    num = 0
    sum_x_diff_sq = 0
    sum_y_diff_sq = 0

    for i in range(n):
        dx = x[i] - prom_x
        dy = y[i] - prom_y
        num += dx * dy
        sum_x_diff_sq += dx ** 2
        sum_y_diff_sq += dy ** 2

    den = raiz_cuadrada(sum_x_diff_sq) * raiz_cuadrada(sum_y_diff_sq)
    return num / den if den != 0 else 0

# Funcion para cargar datos y calcular correlación
data = cargar_desde_csv('musica.csv')
usuario_base = "Angelica"
resultados = {}

for usuario, calificaciones in data.items():
    if usuario != usuario_base:
        puntuacion = correlacion_pearson(data[usuario_base], calificaciones)
        resultados[usuario] = puntuacion

# grafico de barras con colores condicionales
plt.figure(figsize=(10, 5))
nombres = list(resultados.keys())
valores = list(resultados.values())

# Color condicional: verde si es buena correlación, rojo si es mala
colores = ['#2ecc71' if v > 0.5 else '#e74c3c' for v in valores]

plt.bar(nombres, valores, color=colores)
plt.axhline(0, color='black', linewidth=0.8) # Línea base
plt.title(f"Similitud con {usuario_base} (Coeficiente de Pearson)")
plt.ylabel("Grado de Correlación (-1 a 1)")
plt.ylim(-1, 1)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()