import os
import time
from gestor_datos import cargar_dataset_inteligente, cargar_titulos_peliculas
from logica_knn import obtener_k_vecinos, generar_recomendaciones
from metricas import (
    distancia_euclidiana,
    distancia_manhattan,
    similitud_coseno,
    correlacion_pearson,
    graficar_resultados,
    graficar_recomendaciones_pastel
)

def seleccionar_dataset():
    print("Seleccione un dataset para cargar:")
    print("1. Dataset Pequeño Musica.csv")
    print("2. Dataset Mediano MovieLens")
    print("3. Ingresar ruta manual de otro CSV")
    opcion = input("Elija un dataset (1-3): ")

    base_path = os.path.dirname(os.path.abspath(__file__))

    if opcion == '1':
        ruta = os.path.join(base_path, "data", "musica.csv")
        if not os.path.exists(ruta):
            print(f"⚠️ Alerta: No se encontró el archivo en {ruta}")
            ruta = input("Por favor, introducí la ruta correcta del archivo musica.csv: ")
        return ruta, None

    elif opcion == '2':
        ruta_ratings = os.path.join(base_path, "data", "ratings.csv")
        ruta_movies  = os.path.join(base_path, "data", "movies.csv")

        if not os.path.exists(ruta_ratings):
            print(f"⚠️ Alerta: No se encontró el archivo en {ruta_ratings}")
            ruta_ratings = input("Por favor, introducí la ruta correcta del archivo ratings.csv: ")

        if not os.path.exists(ruta_movies):
            print(f"⚠️ Alerta: No se encontró el archivo en {ruta_movies}")
            ruta_movies = input("Por favor, introducí la ruta correcta del archivo movies.csv: ")

        return ruta_ratings, ruta_movies

    elif opcion == '3':
        ruta = input("Ingrese la ruta exacta del archivo .csv: ")
        return ruta, None

    else:
        print("Opción inválida. Cargando Música por defecto.")
        return os.path.join(base_path, "data", "musica.csv"), None


def iniciar_menu():
    ruta, ruta_movies = seleccionar_dataset()

    print(f"\nCargando datos desde {ruta}...")
    dataset = cargar_dataset_inteligente(ruta)

    if not dataset:
        print("No se pudieron cargar los datos. Saliendo...")
        return

    # ── Cargar títulos si es MovieLens ────────────────────────────────────
    titulos = {}
    if ruta_movies:
        titulos = cargar_titulos_peliculas(ruta_movies)
        print(f"¡Carga exitosa! {len(dataset)} usuarios y {len(titulos)} películas.\n")
    else:
        print(f"¡Carga exitosa! {len(dataset)} usuarios encontrados.\n")

    while True:
        print("--- SISTEMA DE RECOMENDACIÓN KNN ---")
        usuario = input("Ingrese el ID del usuario (ej. Angelica o 1) o 'q' para salir: ")

        if usuario.lower() == 'q':
            print("Saliendo del sistema...")
            break

        if usuario not in dataset:
            print("Error: El usuario no existe en la base de datos.\n")
            continue

        print("\nSeleccione el algoritmo a utilizar:")
        print("1. Distancia de Manhattan")
        print("2. Distancia Euclidiana")
        print("3. Similitud del Coseno")
        print("4. Correlación de Pearson")
        opcion = input("Opción (1-4): ")

        if opcion == '1':
            metrica, es_dist = distancia_manhattan, True
            nombre_metrica = "Manhattan"
        elif opcion == '2':
            metrica, es_dist = distancia_euclidiana, True
            nombre_metrica = "Euclidiana"
        elif opcion == '3':
            metrica, es_dist = similitud_coseno, False
            nombre_metrica = "Coseno"
        elif opcion == '4':
            metrica, es_dist = correlacion_pearson, False
            nombre_metrica = "Pearson"
        else:
            print("Opción inválida.\n")
            continue

        k_str = input("¿Cuántos vecinos desea calcular (K)? (ej. 5): ")
        k = int(k_str) if k_str.isdigit() else 5

        min_str = input("¿Mínimo de ítems en común requeridos? (Enter = 3): ")
        min_coincidencias = int(min_str) if min_str.isdigit() else 3

        inicio_tiempo = time.perf_counter()
        vecinos = obtener_k_vecinos(
            dataset, usuario, metrica, k, es_dist,
            min_coincidencias=min_coincidencias
        )
        fin_tiempo = time.perf_counter()
        tiempo_ms = (fin_tiempo - inicio_tiempo) * 1000

        print(f"\nVecinos más confiables para {usuario} usando {nombre_metrica}:")
        print(f"Tiempo de ejecución: {tiempo_ms:.2f} ms")
        print(f"Filtro aplicado: mínimo {min_coincidencias} ítems en común")
        print("-" * 40)

        if not vecinos:
            print("No se encontraron vecinos con ese mínimo de coincidencias.")
            print("Intentá bajar el valor de mínimo de ítems en común.\n")
            continue

        for i, v in enumerate(vecinos):
            tipo = "Distancia" if es_dist else "Similitud"
            print(f"{i+1}. {v['usuario']} | {tipo}: {v['valor']:.4f} | "
                  f"Basado en: {v['n_comunes']} ítems comunes")

        # ── Gráfico de barras de vecinos ──────────────────────────────────
        dict_resultados = {v['usuario']: v['valor'] for v in vecinos}
        graficar_resultados(
            usuario, dict_resultados, nombre_metrica,
            es_similitud=not es_dist
        )

        # ── Fase 5: Recomendaciones ───────────────────────────────────────
        print("\n" + "=" * 40)
        print("¿Desea generar recomendaciones para este usuario basado en sus vecinos?")
        respuesta = input("Presione 's' para Sí, cualquier otra tecla para omitir: ")

        if respuesta.lower() == 's':

            # 1. Umbral
            umbral_str = input("Ingrese el umbral mínimo de predicción (ej. 3.5): ")
            try:
                umbral = float(umbral_str)
            except ValueError:
                umbral = 3.5
                print("Valor inválido. Se usará umbral por defecto: 3.5")

            # 2. Tope
            tope_str = input("¿Cuántas recomendaciones desea ver en el top? (ej. 10): ")
            tope = int(tope_str) if tope_str.isdigit() else 10

            # 3. Mínimo de vecinos de soporte
            min_vec_str = input("Mínimo de vecinos que deben respaldar la película (ej. 3): ")
            min_vecinos = int(min_vec_str) if min_vec_str.isdigit() else 3

            recos = generar_recomendaciones(
                dataset, usuario, vecinos,
                umbral=umbral, tope=tope, min_vecinos=min_vecinos, es_distancia=es_dist 
            )

            print(f"\n--- TOP {tope} RECOMENDACIONES "
                  f"(Umbral >= {umbral} | Soporte >= {min_vecinos} vecinos) ---")

            if not recos:
                print("Ningún ítem superó el umbral/soporte o ya vio todo lo de sus vecinos.")
            else:
                for i, r in enumerate(recos):
                    nombre_item = titulos.get(str(r['item']), f"ID {r['item']}") if titulos else r['item']
                    print(f"{i+1}. {nombre_item}")
                    print(f"   ↳ Predicción: {r['prediccion']:.2f} ★ | "
                          f"Apoyado por {r['confianza']} vecino(s)")

                graficar_recomendaciones_pastel(recos, usuario, titulos)

        print("\n" + "=" * 40 + "\n")

if __name__ == "__main__":
    iniciar_menu()