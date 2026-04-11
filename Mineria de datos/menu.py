import time
from gestor_datos import cargar_dataset_inteligente
from logica_knn import obtener_k_vecinos
from metricas import (
    distancia_euclidiana, 
    distancia_manhattan, 
    similitud_coseno, 
    correlacion_pearson,
    graficar_resultados 
)

def seleccionar_dataset():
    print("Seleccione un dataset para cargar:")
    print("1. Dataset Pequeño Musica.csv")
    print("2. Dataset Mediano MovieLens")
    print("3. Ingresar ruta manual de otro CSV")
    
    opcion = input("Elija un dataset (1-3): ")
    if opcion == '1':
        return "data/musica.csv"
    elif opcion == '2':
        return "data/ratings.csv"
    elif opcion == '3':
        return input("Ingrese la ruta exacta del archivo .csv: ")
    else:
        print("Opción inválida. Cargando Música por defecto.")
        return "data/musica.csv"

def iniciar_menu():
    ruta = seleccionar_dataset()
    print(f"\nCargando datos desde {ruta}...")
    dataset = cargar_dataset_inteligente(ruta)
    
    if not dataset:
        print("No se pudieron cargar los datos. Saliendo...")
        return
        
    print(f"¡Carga exitosa! {len(dataset)} usuarios encontrados.\n")

    # SOLUCIÓN 1: El while ahora está ADENTRO de la función iniciar_menu()
    while True:
        print("--- SISTEMA DE RECOMENDACIÓN KNN ---")
        usuario = input("Ingrese el ID del usuario de interés (ej. Angelica o 1) o 'q' para salir: ")
        
        if usuario.lower() == 'q':
            print("Saliendo del sistema...")
            break
            
        # SOLUCIÓN 2: Buscamos en "dataset", no en la función
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

        inicio_tiempo = time.perf_counter()
        
        # SOLUCIÓN 2: Pasamos la variable "dataset"
        vecinos = obtener_k_vecinos(dataset, usuario, metrica, k, es_dist)
        
        fin_tiempo = time.perf_counter()
        tiempo_ms = (fin_tiempo - inicio_tiempo) * 1000

        print(f"\nResultados para el Usuario {usuario} usando {nombre_metrica}:")
        print(f"Tiempo de ejecución: {tiempo_ms:.2f} ms")
        print("-" * 40)
        
        for i, (id_vecino, valor) in enumerate(vecinos):
            etiqueta = "Distancia" if es_dist else "Similitud"
            print(f"{i+1}. Usuario {id_vecino} | {etiqueta}: {valor:.4f}")
        print("\n" + "="*40 + "\n")

        # --- INTEGRACIÓN DEL GRÁFICO ---
        # Convertimos la lista de resultados en un diccionario para la función de graficar
        if vecinos:
            dict_resultados = {vecino: valor for vecino, valor in vecinos}
            # es_dist es True si es distancia. Para el gráfico, pasamos 'not es_dist' (es_similitud)
            graficar_resultados(usuario, dict_resultados, nombre_metrica, es_similitud=not es_dist)

if __name__ == "__main__":
    iniciar_menu()
    