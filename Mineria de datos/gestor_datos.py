import csv

def cargar_dataset_inteligente(ruta):
    """
    Carga un CSV de ratings. Detecta automáticamente si es:
    - Formato simple (Usuario, Cancion1, Cancion2...)
    - Formato MovieLens (userId, movieId, rating)
    """
    dataset = {}
    
    try:
        with open(ruta, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            columnas = lector.fieldnames

            # ── Formato MovieLens (userId, movieId, rating) ───────────────
            if 'userId' in columnas and 'movieId' in columnas and 'rating' in columnas:
                for fila in lector:
                    usuario = fila['userId']
                    item = fila['movieId']
                    rating = float(fila['rating'])
                    if usuario not in dataset:
                        dataset[usuario] = {}
                    dataset[usuario][item] = rating

            # ── Formato simple (Usuario, Item1, Item2...) ─────────────────
            else:
                for fila in lector:
                    usuario = fila.get('Usuario') or fila.get('userId') or list(fila.values())[0]
                    dataset[usuario] = {
                        k: float(v)
                        for k, v in fila.items()
                        if k not in ('Usuario', 'userId') and v.strip()
                    }

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en '{ruta}'")
        return {}
    except Exception as e:
        print(f"Error al cargar el dataset: {e}")
        return {}

    return dataset


def cargar_titulos_peliculas(ruta_movies):
    """
    Carga el archivo movies.csv de MovieLens.
    Devuelve un diccionario {movieId: titulo}
    """
    titulos = {}
    try:
        with open(ruta_movies, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                titulos[fila['movieId']] = fila['title']
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de películas en '{ruta_movies}'")
    except Exception as e:
        print(f"Error al cargar títulos: {e}")

    return titulos