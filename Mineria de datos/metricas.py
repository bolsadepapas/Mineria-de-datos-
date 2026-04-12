import matplotlib.pyplot as plt


def raiz_cuadrada(valor):
    if valor <= 0: return 0
    x = valor
    for _ in range(20):
        x = 0.5 * (x + valor / x)
    return x


# 2. Algoritmos de similitud/distancia

# Modifica estas funciones en metricas.py para que retornen (valor, n_comunes)

def distancia_manhattan(user1_dict, user2_dict):
    comunes = [item for item in user1_dict if item in user2_dict]
    n = len(comunes)
    if n == 0: return float('inf'), 0
        
    distancia = 0
    for item in comunes:
        diferencia = user1_dict[item] - user2_dict[item]
        distancia += diferencia if diferencia >= 0 else -diferencia
    return distancia, n

def distancia_euclidiana(user1_dict, user2_dict):
    comunes = [item for item in user1_dict if item in user2_dict]
    n = len(comunes)
    if n == 0: return float('inf'), 0
        
    suma_cuadrados = 0
    for item in comunes:
        diferencia = user1_dict[item] - user2_dict[item]
        suma_cuadrados += diferencia ** 2
    return raiz_cuadrada(suma_cuadrados), n

def correlacion_pearson(user1_dict, user2_dict):
    comunes = [item for item in user1_dict if item in user2_dict]
    n = len(comunes)
    if n < 2: return 0, n # Pearson necesita al menos 2 para no dar error

    x = [user1_dict[item] for item in comunes]
    y = [user2_dict[item] for item in comunes]
    prom_x, prom_y = sum(x)/n, sum(y)/n

    num = sum((x[i]-prom_x)*(y[i]-prom_y) for i in range(n))
    sum_x_diff_sq = sum((x[i]-prom_x)**2 for i in range(n))
    sum_y_diff_sq = sum((y[i]-prom_y)**2 for i in range(n))

    den = raiz_cuadrada(sum_x_diff_sq) * raiz_cuadrada(sum_y_diff_sq)
    return (num / den if den != 0 else 0), n

def similitud_coseno(user1_dict, user2_dict):
    comunes = [item for item in user1_dict if item in user2_dict]
    n = len(comunes)
    if n == 0: return 0, 0
    
    num = sum(user1_dict[item] * user2_dict[item] for item in comunes)
    sum_u1 = sum(v**2 for v in user1_dict.values())
    sum_u2 = sum(v**2 for v in user2_dict.values())
    den = raiz_cuadrada(sum_u1) * raiz_cuadrada(sum_u2)
    return (num / den if den != 0 else 0), n 


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