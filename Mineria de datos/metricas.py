import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

# ── 1. Utilidad matemática ────────────────────────────────────────────────────
def raiz_cuadrada(valor):
    if valor <= 0:
        return 0
    x = valor
    for _ in range(20):
        x = 0.5 * (x + valor / x)
    return x


# ── 2. Métricas (retornan (valor, n_comunes)) ─────────────────────────────────
def distancia_manhattan(user1_dict, user2_dict):
    comunes = [item for item in user1_dict if item in user2_dict]
    n = len(comunes)
    if n == 0:
        return float('inf'), 0
    distancia = sum(
        abs(user1_dict[item] - user2_dict[item]) for item in comunes
    )
    return distancia, n


def distancia_euclidiana(user1_dict, user2_dict):
    comunes = [item for item in user1_dict if item in user2_dict]
    n = len(comunes)
    if n == 0:
        return float('inf'), 0
    suma_cuadrados = sum(
        (user1_dict[item] - user2_dict[item]) ** 2 for item in comunes
    )
    return raiz_cuadrada(suma_cuadrados), n


def correlacion_pearson(user1_dict, user2_dict):
    comunes = [item for item in user1_dict if item in user2_dict]
    n = len(comunes)
    if n < 2:
        return 0, n
    x = [user1_dict[item] for item in comunes]
    y = [user2_dict[item] for item in comunes]
    prom_x, prom_y = sum(x) / n, sum(y) / n
    num = sum((x[i] - prom_x) * (y[i] - prom_y) for i in range(n))
    den = (
        raiz_cuadrada(sum((x[i] - prom_x) ** 2 for i in range(n))) *
        raiz_cuadrada(sum((y[i] - prom_y) ** 2 for i in range(n)))
    )
    return (num / den if den != 0 else 0), n


def similitud_coseno(user1_dict, user2_dict):
    comunes = [item for item in user1_dict if item in user2_dict]
    n = len(comunes)
    if n == 0:
        return 0, 0
    num = sum(user1_dict[item] * user2_dict[item] for item in comunes)
    den = (
        raiz_cuadrada(sum(v ** 2 for v in user1_dict.values())) *
        raiz_cuadrada(sum(v ** 2 for v in user2_dict.values()))
    )
    return (num / den if den != 0 else 0), n


# ── 3. Gráfico de barras (matplotlib) ────────────────────────────────────────
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


# ── 4. Gráfico de pastel interactivo (plotly) ─────────────────────────────────
def graficar_recomendaciones_pastel(recomendaciones_lista, usuario_objetivo, mapeo_titulos={}):
    """
    Genera un gráfico de pastel interactivo usando Plotly.
    El tamaño de la rebanada es la nota predicha, el nombre es el título de la película.
    mapeo_titulos es opcional: si no se pasa, usa el ID directamente.
    """
    if not recomendaciones_lista:
        print("No hay recomendaciones suficientes para graficar.")
        return

    df = pd.DataFrame(recomendaciones_lista)

    # Reemplazar IDs por títulos reales (si hay mapeo disponible)
    df['item_nombre'] = df['item'].apply(
        lambda x: mapeo_titulos.get(str(x), str(x))
    )

    fig = px.pie(
        df,
        values='prediccion',
        names='item_nombre',
        title=f"Top {len(recomendaciones_lista)} Recomendaciones para Usuario {usuario_objetivo}",
        hover_data={'prediccion': ':.2f', 'confianza': True},
        labels={
            'item_nombre': 'Película/Canción',
            'prediccion': 'Nota Predicha (★)',
            'confianza': 'Vecinos que recomiendan'
        },
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=True, hovermode='closest')
    fig.show()