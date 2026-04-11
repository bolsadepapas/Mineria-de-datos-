import matplotlib.pyplot as plt


def raiz_cuadrada(valor):
    if valor <= 0: return 0
    x = valor
    for _ in range(20):
        x = 0.5 * (x + valor / x)
    return x


# 2. Algoritmos de similitud/distancia

def distancia_manhattan(user1_dict, user2_dict):
    comunes = [item for item in user1_dict if item in user2_dict]
    if len(comunes) == 0:
        return float('inf')
        
    distancia = 0
    for item in comunes:
        diferencia = user1_dict[item] - user2_dict[item]
        distancia += diferencia if diferencia >= 0 else -diferencia
        
    return distancia

def distancia_euclidiana(user1_dict, user2_dict):
    comunes = [item for item in user1_dict if item in user2_dict]
    if len(comunes) == 0:
        return float('inf')
        
    suma_cuadrados = 0
    for item in comunes:
        diferencia = user1_dict[item] - user2_dict[item]
        suma_cuadrados += diferencia ** 2
        
    return raiz_cuadrada(suma_cuadrados)

def correlacion_pearson(user1_dict, user2_dict):
    comunes = [item for item in user1_dict if item in user2_dict]
    n = len(comunes)
    if n == 0: return 0

    x = [user1_dict[item] for item in comunes]
    y = [user2_dict[item] for item in comunes]

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

def similitud_coseno(user1_dict, user2_dict):
    comunes = [item for item in user1_dict if item in user2_dict]
    if len(comunes) == 0:
        return 0
        
    numerador = sum(user1_dict[item] * user2_dict[item] for item in comunes)
    
    suma_user1 = sum(user1_dict[item] ** 2 for item in user1_dict)
    suma_user2 = sum(user2_dict[item] ** 2 for item in user2_dict)
    
    denominador = raiz_cuadrada(suma_user1) * raiz_cuadrada(suma_user2)
    
    if denominador == 0:
        return 0
        
    return numerador / denominador


# 3. Visualización de resultados con plot, es generico, grafico de barras 

def graficar_resultados(usuario_base, resultados_dict, nombre_metrica, es_similitud=True):
    plt.figure(figsize=(10, 5))
    nombres = list(resultados_dict.keys())
    valores = list(resultados_dict.values())

    if es_similitud:
        colores = ['#2ecc71' if v > 0.5 else '#e74c3c' for v in valores]
        plt.ylim(-1, 1)
        plt.ylabel("Grado de Similitud (-1 a 1)")
    else:
        colores = ['#3498db' for _ in valores]
        plt.ylabel("Distancia (Más bajo es más similar)")

    plt.bar(nombres, valores, color=colores)
    plt.axhline(0, color='black', linewidth=0.8)
    plt.title(f"Resultados de {usuario_base} ({nombre_metrica})")
    
    if len(nombres) > 15:
        plt.xticks(rotation=90, fontsize=8)
        
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()